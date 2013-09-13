# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView
from matem.solicitudes.interfaces import ISolicitudFolder
from matem.solicitudes.config import DICCIONARIO_AREAS
from matem.solicitudes.browser.queries import Queries

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from DateTime.DateTime import DateTime

from operator import itemgetter

import datetime
import sys

class ImportView(BrowserView):
    """An import view of an application"""

    template = ViewPageTemplateFile('import_form.pt')
    template_global = ViewPageTemplateFile('import_form_global.pt')
    pendientes = ViewPageTemplateFile('folderpendientes.pt')
#    pendientes = ViewPageTemplateFile('solicitudfolder.pt')

    def __call__(self):
            form = self.request.form
            req = self.request
            container = self.context
            file=req.get('file', '')
            tipo=req.get('tiposolicitud', '')
            import_but = form.get('form.button.Import', None) is not None
            importador=False
            usuarioAutenticado=self.context.portal_membership.getAuthenticatedMember()
    
            if "Importador de Solicitudes" in list(usuarioAutenticado.getRoles()):
                importador=True
    
            if not import_but or not container.aceptando():
                   if importador:
                       return self.template_global()
                   else:
                       return self.template()
            else:
                if file is None:
                    if importador:
                       return self.template_global()
                    return self.template()
                elif file.filename.find("txt")==-1:
                    if importador:
                        return self.template_global()
                    return self.template()

                if tipo is None:
                    if importador:
                        return self.template_global()
                    return self.template()
                elif tipo == "":
                    if importador:
                        return self.template_global()
                    return self.template()

                fullname=self.context.portal_membership.getAuthenticatedMember().getProperty('fullname')
                username=str(self.context.portal_membership.getAuthenticatedMember().getId())
                now = datetime.datetime.now()

                rolesInicial=['Importador de Solicitudes','Member']

                if importador:
                    if 'Authenticated user' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Authenticated user')
                    if 'Investigador' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Investigador')
                    if 'Tecnico Academico' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Tecnico Academico')
                    if 'Postdoc' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Postdoc')
                    if 'Becario' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Becario')
                    if 'Consejero' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Consejero')
                    if 'Comisionado' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Comisionado')
                    if 'Responsable del Consejo' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Responsable del Consejo')
                    if 'Responsable de la Comision' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Responsable de la Comision')
                    if 'Tecnico Academico' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Tecnico Academico')
                    if 'Programador de Presupuesto' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Programador de Presupuestp')
                    if 'Manager' in list(usuarioAutenticado.getRoles()):
                        rolesInicial.append('Manager')
    
                    container.manage_delLocalRoles(username)
                    container.manage_setLocalRoles(username, ['Importador de Solicitudes','Authenticated user','Investigador','Postdoc','Tecnico Academico','Becario','Comisionado','Consejero','Responsable del Consejo','Responsable de la Comision']) 

                noInsertadas=""
                errorInsercion=""
                numeracionError=0

                Duenio=""
                Pais=""
                Grado=""
                Visitante=""
                Ciudad=""
                Institucion=""
                Desde=""
                Hasta=""
                Objetivo=""
                Area=""
                Titulo=""
                Trabajo="No"
                Comentarios=""
                Transporte="No"
                Medio=[]
                Viaticos="No"
                Inscripcion="No"
                Objetivo=""
                CantidadTransporte="0.0"
                CantidadViaticos="0.0"
                CantidadInscripcion="0.0"
                fechaRevision=""
                actaci="0"
                Estado=""
                comentariosConsejo=""
                addable = True
                debugline=""

#            try:
                if tipo.find("bloque")!= -1:
                    bloque=[]

                    for line in file:
                        line=line.replace("\t","")
                        debugline=line
                        Duenio=""
                        Asesor=""
                        Pais=""
                        Ciudad=""
                        Grado=""
                        Visitante=""
                        Institucion=""
                        listaDesde=""
                        listaHasta=""
                        Desde=""
                        Hasta=""
                        Objetivo=""
                        Medio=[]
                        Area="00-xx"
                        Viaticos="No"
                        Titulo=""
                        Trabajo="No"
                        Transporte="No"
                        Inscripcion="No"
                        Comentarios=""
                        CantidadViaticos="0.0"
                        CantidadTransporte="0.0"
                        CantidadInscripcion="0.0"
                        fechaRevision=""
                        listaRevision=""
                        comentariosConsejo=""
                        actaci="0"
                        Estado=""
                        addable = True

                        if importador:
                            fullname=""

                        if not line.find(";")==-1:
                            tempList=line.split(";")
                             
                            if tempList[0].find("Visitante")!= -1:
                                if len(tempList)==15:
                                    if importador:
                                        Duenio=self.context.portal_membership.getMemberById(tempList[1].replace(" ",""))
                                        if Duenio is None:
                                            Duenio=self.findDuenio(tempList[1])
                                            if Duenio is None:
                                                addable=False
                                            else:
                                                fullname=Duenio.getProperty('fullname')
                                                username=str(Duenio.getId())
                                        else:
                                            fullname=Duenio.getProperty('fullname')
                                            username=str(Duenio.getId())
                                    Pais=tempList[4]
                                    Visitante=tempList[2]
                                    Ciudad=tempList[5]
                                    Institucion=tempList[3]
                                    listaDesde=tempList[7].split("/")
                                    listaHasta=tempList[8].split("/")
                                    Objetivo=tempList[6]
                                    if tempList[9].find(",")==-1:
                                        Area=tempList[9].split("xx")[0]+"xx"
                                        Area=Area.replace(" ","")
                                    else:
                                        Area=tempList[9].split(",")
                                        for area in Area:
                                            area=area.split("xx")[0]+"xx"
                                            area=area.replace(" ","")
                                        Area=tuple(Area)
                                    if not tempList[10].lower().find("carro")==-1:
                                        Medio.append("auto")
                                    elif not tempList[10].lower().replace("autobus","").find("auto")==-1:
                                        Medio.append("auto")
                                    if not tempList[10].lower().find("bus")==-1:
                                        Medio.append("autobus")
                                    elif not tempList[10].lower().find("terrestre")==-1:
                                        Medio.append("autobus")
                                    elif not tempList[10].lower().replace("ó","o").find("camion")==-1:
                                        Medio.append("autobus")
                                    if not tempList[10].lower().replace("ó","o").find("avion")==-1:
                                        Medio.append("avion")
                                    elif not tempList[10].lower().replace("é","e").find("aereo")==-1:
                                        Medio.append("avion")
                                    Medio=tuple(Medio)
                                    if len(Medio)>0:
                                        Transporte="Si"
                                    CantidadViaticos=tempList[11]
                                    CantidadTransporte=tempList[12]
                                    Comentarios=tempList[13]
                                    if tempList[14].find("&") == -1:
                                        Estado=tempList[14].replace(" ","")
                                    else:
                                        temporal=tempList[14].split("&")
                                        if len(temporal) > 3:
                                            listaRevision=temporal[0].split("/")
                                            fechaRevision=DateTime(int(listaRevision[0]), int(listaRevision[1]), int(listaRevision[2]))
                                            actaci=temporal[1]
                                            comentariosConsejo=temporal[2]
                                            Estado=temporal[len(temporal)-1]
                                        else: 
                                            Estado="aprobada"

                                try: 
                                    total=float(CantidadTransporte)+float(CantidadViaticos)
                                    id="solicitud-visitante-de-"+fullname.replace(" ","-")+"-para-"+str(Visitante)+"-por-"+str(total)+"-con-origen-"+Ciudad+"-"+Institucion+"-el-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-desde-"+str(listaDesde[0])+"-"+str(listaDesde[1])+"-"+str(listaDesde[2])+"-hasta-"+str(listaHasta[0])+"-"+str(listaHasta[1])+"-"+str(listaHasta[2])
                                    id=id.replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()
                                    fechadesde=DateTime(int(listaDesde[0]), int(listaDesde[1]), int(listaDesde[2]))
                                    fechahasta=DateTime(int(listaHasta[0]), int(listaHasta[1]), int(listaHasta[2]))
                                except:
                                    numeracionError+=1
                                    noInsertadas+=str(numeracionError)+".  "+line
                                    errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                    continue

                                if id not in container.objectIds() and addable:
                                  try: 
                                    container.invokeFactory(type_name="SolicitudVisitante", id=id, invitado=Visitante, pais_procedencia=Pais, procedencia=Ciudad, institucion_procedencia=Institucion, objeto_viaje=Objetivo, investigacionarea=Area, trabajo=Trabajo, titulo_trabajo=Titulo, pasaje=Transporte, tipo_pasaje=Medio, cantidad_pasaje=float(CantidadTransporte), viaticos=Viaticos, cantidad_viaticos=float(CantidadViaticos), fecha_solicitud=now,comentario_owner=Comentarios)
                                  except:
                                      numeracionError+=1
                                      noInsertadas+=str(numeracionError)+".  "+line
                                      errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                      continue
                                      

                                if addable:
                                  try:
                                    obj=container[id]
                                    obj.setFecha_desde(fechadesde)
                                    obj.setFecha_hasta(fechahasta)
                                    if importador:
                                        obj.toState(Estado)
                                        self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))
                                        obj.setFecha_sesionci(fechaRevision)
                                        obj.setActaci(actaci)
                                        obj.setComentario_ci(comentariosConsejo)
                                  except:
                                      numeracionError+=1
                                      noInsertadas+=str(numeracionError)+".  "+line
                                      errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                      continue
                                else:
                                  numeracionError+=1
                                  noInsertadas+=str(numeracionError)+".  "+line
                                  errorInsercion+=str(numeracionError)+". User not found"+"\n\n"
                                  continue

                            elif tempList[0].find("Becario")!= -1:
                                if len(tempList)==17:
                                    if importador:
                                        if not tempList[1].find(",") == -1:
                                            Duenio=self.context.portal_membership.getMemberById(tempList[1].split(",")[0].replace(" ",""))
                                            Asesor=self.context.portal_membership.getMemberById(tempList[1].split(",")[1].replace(" ",""))
                                        else: 
                                            addable=False
                                        if Duenio is None:
                                            Duenio=self.findDuenio(tempList[1].split(",")[0])
                                            if Duenio is None:
                                                addable=False
                                            else:
                                                fullname=Duenio.getProperty('fullname')
                                                username=str(Duenio.getId())
                                        else:
                                            fullname=Duenio.getProperty('fullname')
                                            username=str(Duenio.getId())
                                        if Asesor is None:
                                            Asesor=self.findDuenio(tempList[1].split(",")[1])
                                            if Asesor is None:
                                                addable=False
                                    Pais=tempList[4]
                                    if not tempList[2].lower().find("ph")==-1:
                                        Grado="Doctorado"
                                    elif not tempList[2].lower().find("oct")==-1:
                                        Grado="Doctorado"
                                    elif not tempList[2].lower().find("m")==-1:
                                        Grado="Maestria"
                                    elif not tempList[2].lower().find("l")==-1:
                                        Grado="Licenciatura"
                                    else:
                                        Grado="Licenciatura"
                                    Ciudad=tempList[5]
                                    Institucion=tempList[3]
                                    listaDesde=tempList[7].split("/")
                                    listaHasta=tempList[8].split("/")
                                    Objetivo=tempList[6]
                                    if tempList[9].find(",")==-1:
                                        Area=tempList[9].split("xx")[0]+"xx"
                                        Area=Area.replace(" ","")
                                    else:
                                        Area=tempList[9].split(",")
                                        for area in Area:
                                            area=area.split("xx")[0]+"xx"
                                            area=area.replace(" ","")
                                        Area=tuple(Area)
                                    if len(tempList[10])>2:
                                        Titulo=tempList[10].replace("\n","")
                                        Trabajo="Si"
                                    if not tempList[11].lower().find("carro")==-1:
                                        Medio.append("auto")
                                    elif not tempList[11].lower().replace("autobus","").find("auto")==-1:
                                        Medio.append("auto")
                                    if not tempList[11].lower().find("bus")==-1:
                                        Medio.append("autobus")
                                    elif not tempList[11].lower().find("terrestre")==-1:
                                        Medio.append("autobus")
                                    elif not tempList[11].lower().replace("ó","o").find("camion")==-1:
                                        Medio.append("autobus")
                                    if not tempList[11].lower().replace("ó","o").find("avion")==-1:
                                        Medio.append("avion")
                                    elif not tempList[11].lower().replace("é","e").find("aereo")==-1:
                                        Medio.append("avion")
                                    Medio=tuple(Medio)
                                    if len(Medio)>0:
                                        Transporte="Si"
                                    CantidadInscripcion=tempList[12]
                                    if len(CantidadInscripcion)>1:
                                        Inscripcion="Si"
                                    CantidadViaticos=tempList[13]
                                    CantidadTransporte=tempList[14]
                                    Comentarios=tempList[15]
                                    if tempList[16].find("&") == -1:
                                        Estado=tempList[16].replace(" ","")
                                    else:
                                        temporal=tempList[16].split("&")
                                        if len(temporal) > 3:
                                            listaRevision=temporal[0].split("/")
                                            fechaRevision=DateTime(int(listaRevision[0]), int(listaRevision[1]), int(listaRevision[2]))
                                            actaci=temporal[1]
                                            comentariosConsejo=temporal[2]
                                            Estado=temporal[len(temporal)-1]
                                        else: 
                                            Estado="aprobada"

                                if not importador:
                                    Asesor=req.get('Creator', '')

                                if Asesor is not None:
                                    if importador:
                                      try:
                                        Asesor=str(Asesor.getId())
                                      except:
                                        numeracionError+=1
                                        noInsertadas+=str(numeracionError)+".  "+line
                                        errorInsercion+=str(numeracionError)+".  "+"Asesor no encontrado"+"\n\n"
                                        continue
                                    if Asesor is not "":
                                        try:
                                            total=float(CantidadTransporte)+float(CantidadViaticos)+float(CantidadInscripcion)
                                            id="solicitud-becario-de-"+fullname.replace(" ","-")+"-por-"+str(total)+"-"+Ciudad+"-"+Institucion+"-el-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-desde-"+str(listaDesde[0])+"-"+str(listaDesde[1])+"-"+str(listaDesde[2])+"-hasta-"+str(listaHasta[0])+"-"+str(listaHasta[1])+"-"+str(listaHasta[2])
                                            id=id.replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()
                                            fechadesde=DateTime(int(listaDesde[0]), int(listaDesde[1]), int(listaDesde[2]))
                                            fechahasta=DateTime(int(listaHasta[0]), int(listaHasta[1]), int(listaHasta[2]))
                                        except:
                                            numeracionError+=1
                                            noInsertadas+=str(numeracionError)+".  "+line
                                            errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                            continue
                                        
                                        if id not in container.objectIds() and addable:
                                          print "3"
                                          try: 
                                            container.invokeFactory(type_name="SolicitudBecario", id=id, grado=Grado, asesor=Asesor, pais=Pais, ciudad_pais=Ciudad, institucion=Institucion, objeto_viaje=Objetivo, investigacionarea=Area, trabajo=Trabajo, titulo_trabajo=Titulo, pasaje=Transporte, tipo_pasaje=Medio, cantidad_pasaje=float(CantidadTransporte), viaticos=Viaticos, cantidad_viaticos=float(CantidadViaticos), inscripcion=Inscripcion, cantidad_inscripcion=float(CantidadInscripcion),fecha_solicitud=now,comentario_owner=Comentarios)
                                          except:
                                              numeracionError+=1
                                              noInsertadas+=str(numeracionError)+".  "+line
                                              errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                              continue

                                        if addable:
                                          try:
                                            obj=container[id]
                                            obj.setFecha_desde(fechadesde)
                                            obj.setFecha_hasta(fechahasta)
                                            if importador:
                                                obj.toState(Estado)
                                                self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))
                                                obj.setFecha_sesionci(fechaRevision)
                                                obj.setActaci(actaci)
                                                obj.setComentario_ci(comentariosConsejo)
                                          except:
                                              numeracionError+=1
                                              noInsertadas+=str(numeracionError)+".  "+line
                                              errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                              continue
                                        else:
                                            numeracionError+=1
                                            noInsertadas+=str(numeracionError)+".  "+line
                                            errorInsercion+=str(numeracionError)+". User not found"+"\n\n"
                                            continue

                            elif tempList[0].find("Licencia")!= -1:
                                if len(tempList)==16:
                                    if importador:
                                        Duenio=self.context.portal_membership.getMemberById(tempList[1].replace(" ",""))
                                        if Duenio is None:
                                            Duenio=self.findDuenio(tempList[1].split(",")[0])
                                            if Duenio is None:
                                                addable=False
                                            else:
                                                fullname=Duenio.getProperty('fullname')
                                                username=str(Duenio.getId())
                                        else:
                                            fullname=Duenio.getProperty('fullname')
                                            username=str(Duenio.getId())
                                    Pais=tempList[3]
                                    Ciudad=tempList[4]
                                    Institucion=tempList[2]
                                    listaDesde=tempList[6].split("/")
                                    listaHasta=tempList[7].split("/")
                                    Objetivo=tempList[5]
                                    if tempList[8].find(",")==-1:
                                        Area=tempList[8].split("xx")[0]+"xx"
                                        Area=Area.replace(" ","")
                                    else:
                                        Area=tempList[8].split(",")
                                        for area in Area:
                                            area=area.split("xx")[0]+"xx"
                                            area=area.replace(" ","")
                                        Area=tuple(Area)
                                    if len(tempList[9])>2:
                                        Titulo=tempList[9].replace("\n","")
                                        Trabajo="Si"
                                    if not tempList[10].lower().find("carro")==-1:
                                        Medio.append("auto")
                                    elif not tempList[10].lower().replace("autobus","").find("auto")==-1:
                                        Medio.append("auto")
                                    if not tempList[10].lower().find("bus")==-1:
                                        Medio.append("autobus")
                                    elif not tempList[10].lower().find("terrestre")==-1:
                                        Medio.append("autobus")
                                    elif not tempList[10].lower().replace("ó","o").find("camion")==-1:
                                        Medio.append("autobus")
                                    if not tempList[10].lower().replace("ó","o").find("avion")==-1:
                                        Medio.append("avion")
                                    elif not tempList[10].lower().replace("é","e").find("aereo")==-1:
                                        Medio.append("avion")
                                    Medio=tuple(Medio)
                                    if len(Medio)>0:
                                        Transporte="Si"
                                    CantidadInscripcion=tempList[11]
                                    if int(CantidadInscripcion)>0:
                                        Inscripcion="Si"
                                    CantidadViaticos=tempList[12]
                                    if int(CantidadViaticos)>0:
                                        Viaticos="Si"                                    
                                    CantidadTransporte=tempList[13]
                                    Comentarios=tempList[14]
                                    if tempList[15].find("&") == -1:
                                        Estado=tempList[15].replace(" ","")
                                    else:
                                        temporal=tempList[15].split("&")
                                        if len(temporal) > 3:
                                            listaRevision=temporal[0].split("/")
                                            fechaRevision=DateTime(int(listaRevision[0]), int(listaRevision[1]), int(listaRevision[2]))
                                            actaci=temporal[1]
                                            comentariosConsejo=temporal[2]
                                            Estado=temporal[len(temporal)-1]
                                        else: 
                                            Estado="aprobada"

                                try:
                                    total=float(CantidadTransporte)+float(CantidadViaticos)+float(CantidadInscripcion)
                                    id="solicitud-licencia-de-"+fullname.replace(" ","-")+"-por-"+str(total)+"-"+Ciudad+"-"+Institucion+"-el-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-desde-"+str(listaDesde[0])+"-"+str(listaDesde[1])+"-"+str(listaDesde[2])+"-hasta-"+str(listaHasta[0])+"-"+str(listaHasta[1])+"-"+str(listaHasta[2])
                                    id=id.replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()
                                    fechadesde=DateTime(int(listaDesde[0]), int(listaDesde[1]), int(listaDesde[2]))
                                    fechahasta=DateTime(int(listaHasta[0]), int(listaHasta[1]), int(listaHasta[2]))
                                except:
                                    numeracionError+=1
                                    noInsertadas+=str(numeracionError)+".  "+line
                                    errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                    continue

                                if id not in container.objectIds() and addable:
                                  try: 
                                    container.invokeFactory(type_name="Solicitud", id=id, pais=Pais, ciudad_pais=Ciudad, institucion=Institucion, objeto_viaje=Objetivo, investigacionarea=Area, trabajo=Trabajo, titulo_trabajo=Titulo, pasaje=Transporte, tipo_pasaje=Medio, cantidad_pasaje=float(CantidadTransporte), viaticos=Viaticos, cantidad_viaticos=float(CantidadViaticos), inscripcion=Inscripcion, cantidad_inscripcion=float(CantidadInscripcion),fecha_solicitud=now,comentario_owner=Comentarios)
                                  except:
                                      numeracionError+=1
                                      noInsertadas+=str(numeracionError)+".  "+line
                                      errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                      continue

                                if addable:
                                  try:
                                    obj=container[id]
                                    obj.setFecha_desde(fechadesde)
                                    obj.setFecha_hasta(fechahasta)
                                    if importador:
                                        obj.toState(Estado)
                                        self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))
                                        obj.setFecha_sesionci(fechaRevision)
                                        obj.setActaci(actaci)
                                        obj.setComentario_ci(comentariosConsejo)
                                  except:
                                      numeracionError+=1
                                      noInsertadas+=str(numeracionError)+".  "+line
                                      errorInsercion+=str(numeracionError)+".  "+str(sys.exc_info()[0])+"\n\n"
                                      continue
                                else:
                                  numeracionError+=1
                                  noInsertadas+=str(numeracionError)+".  "+line
                                  errorInsercion+=str(numeracionError)+". User not found"+"\n\n"
                                  continue

                    if importador:
                        username=str(self.context.portal_membership.getAuthenticatedMember().getId())
                        container.manage_delLocalRoles(username)
#                        container.manage_setLocalRoles(username, ['Importador de Solicitudes']) 
                        container.manage_setLocalRoles(username, rolesInicial)

                        if numeracionError>0:
                            self.request.set('disable_border', True)
                            self.request.response.setHeader('Content-Type','application/octet-stream')
                            self.request.response.setHeader('Content-Disposition','attachment; filename=errorLog.txt')
                            return noInsertadas+"\n\nErrores\n\n"+errorInsercion
                        else:
                            return self.template_global()

                    if numeracionError>0:
                        self.request.set('disable_border', True)
                        self.request.response.setHeader('Content-Type','application/octet-stream')
                        self.request.response.setHeader('Content-Disposition','attachment; filename=errorLog.txt')
                        return noInsertadas+"\n\nErrores\n\n"+errorInsercion
                    else:
                        return self.pendientes()

                elif not tipo == "bloque":

                    for line in file:
                         if not line.find(":")==-1 and line.find("::")==-1:
                             tempList=line.split(":",1)
                             tempList[0]=tempList[0].lower()

                             if not tempList[0].find("pais")==-1:
                                 Pais=tempList[1].replace("\n","")
                             elif not tempList[0].find("grado")==-1:
                                 if not tempList[1].lower().find("ph")==-1:
                                     Grado="Doctorado"
                                 elif not tempList[1].lower().find("oct")==-1:
                                     Grado="Doctorado"
                                 elif not tempList[1].lower().find("m")==-1:
                                     Grado="Maestria"
                                 elif not tempList[1].lower().find("l")==-1:
                                     Grado="Licenciatura"
                                 elif not tempList[1].lower().find("un")==-1:
                                     Grado="Licenciatura"
                             elif not tempList[0].find("solicitante")==-1:
                                 if not tempList[1].find(",") == -1:
                                     Duenio=self.context.portal_membership.getMemberById(tempList[1].split(",")[0].replace(" ","").replace("\n",""))
                                     Asesor=self.context.portal_membership.getMemberById(tempList[1].split(",")[1].replace(" ","").replace("\n",""))
                                 else: 
                                     Duenio=self.context.portal_membership.getMemberById(tempList[1].replace(" ","").replace("\n",""))
                                 if Duenio is None:
                                     addable=False
                                 else:
                                     fullname=Duenio.getProperty('fullname')
                                     username=str(Duenio.getId())
                             elif not tempList[0].find("visitante")==-1:
                                 Visitante=tempList[1].replace("\n","")
                             elif not tempList[0].find("nombre")==-1:
                                 Visitante=tempList[1].replace("\n","")
                             elif not tempList[0].find("ciudad")==-1:
                                 Ciudad=tempList[1].replace("\n","")
                             elif not tempList[0].find("institucion")==-1:
                                 Institucion=tempList[1].replace("\n","")
                             elif not tempList[0].find("desde")==-1:
                                 Desde=tempList[1].replace("\n","")
                                 listaDesde=Desde.split("/")
                             elif not tempList[0].find("hasta")==-1:
                                 Hasta=tempList[1].replace("\n","")
                                 listaHasta=Hasta.split("/")
                             elif not tempList[0].find("objetivo")==-1:
                                 Objetivo=tempList[1].replace("\n","")
                             elif not tempList[0].find("area")==-1:
                                 if tempList[1].find(",")==-1:
                                     Area=tempList[1].split("xx")[0]+"xx"
                                     Area=Area.replace(" ","")
                                 else:
                                     Area=tempList[1].split(",")
                                     for area in Area:
                                         area=area.split("xx")[0]+"xx"
                                         area=area.replace(" ","")
                                     Area=tuple(Area)
                             elif not tempList[0].find("titulo")==-1:
                                 Titulo=tempList[1].replace("\n","")
                                 Trabajo="Si"
                             elif not tempList[0].find("comentarios")==-1:
                                 Comentarios=tempList[1].replace("\n","")
                             elif not tempList[0].find("transporte")==-1 and tempList[0].find("medio")==-1:
                                 CantidadTransporte=tempList[1].replace("\n","")
                                 if not CantidadTransporte.find(",")==-1:
                                     CantidadTransporte=CantidadTransporte.split(",")[0]
                                 Transporte="Si"
                             elif not tempList[0].find("medio")==-1:
                                 if not tempList[1].lower().find("carro")==-1:
                                     Medio.append("auto")
                                 elif not tempList[1].lower().replace("autobus","").find("auto")==-1:
                                     Medio.append("auto")
                                 if not tempList[1].lower().find("bus")==-1:
                                     Medio.append("autobus")
                                 elif not tempList[1].lower().find("terrestre")==-1:
                                     Medio.append("autobus")
                                 elif not tempList[1].lower().replace("ó","o").find("camion")==-1:
                                     Medio.append("autobus")
                                 if not tempList[1].lower().replace("ó","o").find("avion")==-1:
                                     Medio.append("avion")
                                 elif not tempList[1].lower().replace("é","e").find("aereo")==-1:
                                     Medio.append("avion")
                                 Medio=tuple(Medio)
#                                 Medio=Medio.replace(" ","")
                             elif not tempList[0].find("viaticos")==-1:
                                 CantidadViaticos=tempList[1].replace("\n","")
                                 if not CantidadViaticos.find(",")==-1:
                                     CantidadViaticos=CantidadViaticos.split(",")[0]
                                 Viaticos="Si"
                             elif not tempList[0].find("inscripcion")==-1:
                                 CantidadInscripcion=tempList[1].replace("\n","")
                                 if not CantidadInscripcion.find(",")==-1:
                                     CantidadInscripcion=CantidadInscripcion.split(",")[0]
                                 Inscripcion="Si"
                             elif not tempList[0].find("objetivo")==-1:
                                 Objetivo=tempList[1].replace("\n","")
                             elif not tempList[0].find("estado")==-1:
                                 Estado=tempList[1].replace("\n","")


                    if tipo == "licencia":
                        total=float(CantidadTransporte)+float(CantidadViaticos)+float(CantidadInscripcion)
                        id="solicitud-licencia-de-"+fullname.replace(" ","-")+"-por-"+str(total)+"-"+Ciudad+"-"+Institucion+"-el-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-desde-"+str(listaDesde[0])+"-"+str(listaDesde[1])+"-"+str(listaDesde[2])+"-hasta-"+str(listaHasta[0])+"-"+str(listaHasta[1])+"-"+str(listaHasta[2])
                        id=id.replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()
                        fechadesde=DateTime(int(listaDesde[0]), int(listaDesde[1]), int(listaDesde[2]))
                        fechahasta=DateTime(int(listaHasta[0]), int(listaHasta[1]), int(listaHasta[2]))

                        if id not in container.objectIds() and addable: 
                            container.invokeFactory(type_name="Solicitud", id=id, pais=Pais, ciudad_pais=Ciudad, institucion=Institucion, objeto_viaje=Objetivo, investigacionarea=Area, trabajo=Trabajo, titulo_trabajo=Titulo, pasaje=Transporte, tipo_pasaje=Medio, cantidad_pasaje=float(CantidadTransporte), viaticos=Viaticos, cantidad_viaticos=float(CantidadViaticos), inscripcion=Inscripcion, cantidad_inscripcion=float(CantidadInscripcion),fecha_solicitud=now,comentario_owner=Comentarios)
                        obj=container[id]
                        obj.setFecha_desde(fechadesde)
                        obj.setFecha_hasta(fechahasta)
                        if importador:
                            obj.toState(Estado)
                            self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))

                    elif tipo=="becario":
                        if not importador:
                            Asesor=req.get('Creator', '')
                        else:
                            Asesor=str(Asesor.getId())

                        if Asesor is None:
                            return "sin Asesor"
                        elif Asesor is "":
                            return "sin Asesor"

                        total=float(CantidadTransporte)+float(CantidadViaticos)+float(CantidadInscripcion)
                        id="solicitud-becario-de-"+fullname.replace(" ","-")+"-por-"+str(total)+"-"+Ciudad+"-"+Institucion+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-desde-"+str(listaDesde[0])+"-"+str(listaDesde[1])+"-"+str(listaDesde[2])+"-hasta-"+str(listaHasta[0])+"-"+str(listaHasta[1])+"-"+str(listaHasta[2])
                        id=id.replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()
                        fechadesde=DateTime(int(listaDesde[0]), int(listaDesde[1]), int(listaDesde[2]))
                        fechahasta=DateTime(int(listaHasta[0]), int(listaHasta[1]), int(listaHasta[2]))

                        if id not in container.objectIds() and addable: 
                            container.invokeFactory(type_name="SolicitudBecario", id=id, grado=Grado, asesor=Asesor, pais=Pais, ciudad_pais=Ciudad, institucion=Institucion, objeto_viaje=Objetivo, investigacionarea=Area, trabajo=Trabajo, titulo_trabajo=Titulo, pasaje=Transporte, tipo_pasaje=Medio, cantidad_pasaje=float(CantidadTransporte), viaticos=Viaticos, cantidad_viaticos=float(CantidadViaticos), inscripcion=Inscripcion, cantidad_inscripcion=float(CantidadInscripcion),fecha_solicitud=now,comentario_owner=Comentarios)
                        obj=container[id]
                        obj.setFecha_desde(fechadesde)
                        obj.setFecha_hasta(fechahasta)
                        if importador:
                            self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))
                            obj.toState(Estado)
                            self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))

                    elif tipo=="visitante":
                        total=float(CantidadTransporte)+float(CantidadViaticos)
                        id="solicitud-visitante-de-"+fullname.replace(" ","-")+"-por-"+str(total)+"-"+Ciudad+"-"+Institucion+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-desde-"+str(listaDesde[0])+"-"+str(listaDesde[1])+"-"+str(listaDesde[2])+"-hasta-"+str(listaHasta[0])+"-"+str(listaHasta[1])+"-"+str(listaHasta[2])
                        id=id.replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()
                        fechadesde=DateTime(int(listaDesde[0]), int(listaDesde[1]), int(listaDesde[2]))
                        fechahasta=DateTime(int(listaHasta[0]), int(listaHasta[1]), int(listaHasta[2]))

                        if id not in container.objectIds() and addable: 
                            container.invokeFactory(type_name="SolicitudVisitante", id=id, invitado=Visitante, pais_procedencia=Pais, procedencia=Ciudad, institucion_procedencia=Institucion, objeto_viaje=Objetivo, investigacionarea=Area, trabajo=Trabajo, titulo_trabajo=Titulo, pasaje=Transporte, tipo_pasaje=Medio, cantidad_pasaje=float(CantidadTransporte), viaticos=Viaticos, cantidad_viaticos=float(CantidadViaticos), fecha_solicitud=now,comentario_owner=Comentarios)
                        obj=container[id]
                        obj.setFecha_desde(fechadesde)
                        obj.setFecha_hasta(fechahasta)
                        if importador:
                            obj.toState(Estado)
                            self.context.plone_utils.changeOwnershipOf(obj,str(Duenio.getId()))

                    if importador:
                        username=str(self.context.portal_membership.getAuthenticatedMember().getId())
                        container.manage_delLocalRoles(username)
#                        container.manage_setLocalRoles(username, ['Importador de Solicitudes']) 
                        container.manage_setLocalRoles(username, rolesInicial)
                        return self.template_global()

                    return self.pendientes()
                else:
                    if importador:
                        username=str(self.context.portal_membership.getAuthenticatedMember().getId())
                        container.manage_delLocalRoles(username)
#                        container.manage_setLocalRoles(username, ['Importador de Solicitudes']) 
                        container.manage_setLocalRoles(username, rolesInicial)
                        return self.template_global()

                    return self.template()
#            except:
#                if importador:
#                    username=str(self.context.portal_membership.getAuthenticatedMember().getId())
#                    container.manage_delLocalRoles(username)
#                    container.manage_setLocalRoles(username, ['Importador de Solicitudes']) 
#                    container.manage_setLocalRoles(username, rolesInicial)

#                print debugline+"\n"

#                return self.request.response.redirect('@@import?unerror=1')

    def findDuenio(self,nombreCompleto):
        mt=self.context.portal_membership
        lista=[]
        counter=0

        if nombreCompleto.find(" ") != -1:
            temp=nombreCompleto.split(" ")
            for user in mt.listMembers():
                nombre=user.getProperty('fullname')
                for t in temp:
                    if nombre.find(t) != -1:
                        counter=counter+1
                if counter > 1:
                    lista.append(user)
                counter=0

        if len(lista) == 1:
            return lista[0]
        else:
            return None

    def hasPendingReviews(self,usuarioActual):
        view = SolicitudFolderView(self.context,self.request)
        return view.hasPendingReviews(usuarioActual)

    def getSolicitudesPendientes(self,usuarioActual):
        view = SolicitudFolderView(self.context,self.request)
        return view.getSolicitudesPendientes(usuarioActual)

    def getSolicitudesPendientesEnvio(self,usuarioActual):
        view = SolicitudFolderView(self.context,self.request)
        return view.getSolicitudesPendientesEnvio(usuarioActual)

    def getSolicitudesPendientesRevisionPreeliminar(self,usuarioActual):
        view = SolicitudFolderView(self.context,self.request)
        return view.getSolicitudesPendientesRevisionPreeliminar(usuarioActual)

    def getSolicitudesPendientesRevisionComision(self,usuarioActual):
        view = SolicitudFolderView(self.context,self.request)
        return view.getSolicitudesPendientesRevisionComision(usuarioActual)

    def getSolicitudesPendientesRevisionConsejo(self,usuarioActual):
        view = SolicitudFolderView(self.context,self.request)
        return view.getSolicitudesPendientesRevisionConsejo(usuarioActual)

    def esPostdoc(self):
        member=self.context.portal_membership.getAuthenticatedMember()

        if 'Postdoc' in list(member.getRoles()):
            return True
        else:
            return False

    def esInvestigador(self):
        member=self.context.portal_membership.getAuthenticatedMember()

        if 'Investigador' in list(member.getRoles()):
            return True
        else:
            return False

    def esTecnicoAcademico(self):
        member=self.context.portal_membership.getAuthenticatedMember()

        if 'Tecnico Academico' in list(member.getRoles()):
            return True
        else:
            return False

    def esBecario(self):
        member=self.context.portal_membership.getAuthenticatedMember()

        if 'Becario' in list(member.getRoles()):
            if not 'Investigador' in list(member.getRoles()) and not 'Postdoc' in list(member.getRoles()):
                return True
            else:
                return False
        else:
            return False

    def hasReqData(self):
    
        try:
            req = self.request
            tipo=req.get('tiposolicitud', '')
            if tipo is None:
                if "Becario" in list(self.context.portal_membership.getAuthenticatedMember().getRoles()):
                    return True
                return False
            elif tipo == "becario":
                return True

            return False
        except:
            return False

    def hasError(self):
        req = self.request
        tipo=req.get('unerror', '')
        if not tipo is None:
            if tipo=="1":
                return True
        else:
            return False

    def getCreators(self):
        mt = self.context.portal_membership
        member=mt.getAuthenticatedMember()
        users = []
        esPermitido=False

        if 'Becario' in list(member.getRoles()):
            esPermitido=True
        elif 'Investigador' in list(member.getRoles()):
            esPermitido=True
        elif 'Postdoc' in list(member.getRoles()):
            esPermitido=True
        elif 'Tecnico Academico' in list(member.getRoles()):
            esPermitido=True
        elif 'Manager' in list(member.getRoles()):
            esPermitido=True
        elif 'Comisionado' in list(member.getRoles()):
            esPermitido=True
        elif 'Consejero' in list(member.getRoles()):
            esPermitido=True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            esPermitido=True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            esPermitido=True

        if esPermitido:
            for user in mt.listMembers():
                if 'Investigador' in list(user.getRoles()):
                    users.append([user.getId(),user.getProperty('fullname')])
                elif 'Postdoc' in list(user.getRoles()):
                    users.append([user.getId(),user.getProperty('fullname')])
                elif 'Tecnico Academico' in list(user.getRoles()):
                    users.append([user.getId(),user.getProperty('fullname')])

        return users
