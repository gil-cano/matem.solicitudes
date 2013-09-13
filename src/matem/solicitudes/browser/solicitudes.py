# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from matem.solicitudes.browser.queries import Queries
from matem.solicitudes.interfaces import ISolicitud
from matem.solicitudes.extender import PersonWrapper
from matem.solicitudes.config import DICCIONARIO_AREAS,DICCIONARIO_TIPO_TRANSPORTE_EN,DICCIONARIO_TIPO_TRANSPORTE

class SolicitudView(BrowserView):
    """A view of an application"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def esEditor(self,usuarioActual):
        if 'Owner' in self.context.get_local_roles_for_userid(self.context.getIdOwner()):
            return True
        return False

    def esPropietario(self,usuarioActual):
        if self.context.getIdOwner()==usuarioActual:
            return True
        return False

    def esComisionado(self,usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Comisionado' in list(member.getRoles()):
            return True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            return True
        return False

    def esConsejero(self,usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Consejero' in list(member.getRoles()):
            return True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            return True
        return False

    def esResponsableConsejo(self,usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Responsable del Consejo' in list(member.getRoles()):
            return True
        return False

    def esInvestigadorACargo(self,usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Investigador' in list(member.getRoles()):
            return True
        return False

    def esBorrador(self):
        if self.context.getWFState()=="borrador":
            return True
        return False

    def esRevisionComision(self):
        if self.context.getWFState()=="revisioncomision":
            return True
        return False

    def esRevisionConsejo(self):
        if self.context.getWFState()=="revisionconsejo":
            return True
        return False

    def esAprobada(self):
        if self.context.getWFState()=="aprobada":
            return True
        return False

    def esRechazada(self):
        if self.context.getWFState()=="rechazada":
            return True
        return False

    def esPreeliminar(self):
        if self.context.getWFState()=="preeliminar":
            return True
        return False

    def getPresupuestoOwner(self):
        folder=self.context.aq_inner.aq_parent
        usuarioActual=self.context.getIdOwner()
        queryObj = Queries(self.context,self.request)
        member=queryObj.getPersonWrapper(usuarioActual)
        user=[]
 
        cantidadAsignada=folder.getPresupuesto_asignado_solicitantes()[0].get(usuarioActual,0.0)
        cantidadInicial=folder.getSolicitantes()[0].get(usuarioActual,[0,0,0,0,0.0])[4]
        cantidadInicialApoyos=folder.getSolicitantes()[0].get(usuarioActual,[0,0,0,0,0.0])[5]        
        user.append([member.getLastName()+', '+member.getFirstName() + " " + member.getMiddleName(),
                     cantidadAsignada,
                     cantidadInicial-cantidadAsignada,
                     folder.getDias_comision_utilizados_solicitantes()[0].get(usuarioActual,0.0),
                     folder.getDias_licencia_utilizados_solicitantes()[0].get(usuarioActual,0.0),
                     folder.getApoyoinst_asignado_solicitantes()[0].get(usuarioActual,0.0),
                     cantidadInicialApoyos-folder.getApoyoinst_asignado_solicitantes()[0].get(usuarioActual,0.0)
                     ])

        return user

    def getArea(self,codigoArea):
        areas=[]
        for area in codigoArea:
            try:
                areas.append(DICCIONARIO_AREAS[area])
            except:
                areas.append("")
        return areas

    def getTipoTransporte(self,codigoTrans):
        temp="";

        for codigo in codigoTrans:
            try:
                temp+=DICCIONARIO_TIPO_TRANSPORTE[codigo]
                temp+=","
            except:
                temp=temp

        return temp

    def getPresupuestoAprobadoSolicitud(self):
        return self.context.getCantidadAutorizadaTotal()

    def getNombreAsesor(self,asesor):
        queryObj = Queries(self.context,self.request)
        member = queryObj.getPersonWrapper(asesor)
        return member.getLastName()+', '+member.getFirstName() + " " + member.getMiddleName()

class ExportView(BrowserView):
    """An export view of an application"""

    def __call__(self):
        usuarioActual=self.context.getIdOwner()
        queryObj = Queries(self.context,self.request)
        fsdperson=queryObj.getPersonWrapper(usuarioActual)
        mt = self.context.portal_membership
        member=mt.getMemberById(usuarioActual)
        user=[]

        cantidadAsignada=fsdperson.getPresupuesto_asignado()
        cantidadInicial=fsdperson.getPresupuesto_inicial()
        user.append([fsdperson.getLastName()+', '+fsdperson.getFirstName(),cantidadAsignada,cantidadInicial-cantidadAsignada])

        # Hide the editable-object border
        self.request.set('disable_border', True)
        self.request.response.setHeader('Content-Type','application/octet-stream')
        self.request.response.setHeader('Content-Disposition','attachment; filename=solicitud.txt')

        obj=self.context

        uline1="                         \n"
        lline1="                         \n\n"
        seccion1=uline1+":: Datos del Solicitante ::\n"+lline1

	nombre="      Id de Solicitante: "
        nombreValor=obj.getIdOwner()+"\n"

	estado="    Estado de Solicitud: "
        estadoValor=obj.getWFState()+"\n"

        presupuestoA="   Presupuesto Asignado: "
        presupuestoAValor=str(user[0][1])+"\n"

        presupuestoD=" Presupuesto Disponible: "
        presupuestoDValor=str(user[0][2])+"\n"

        if obj.meta_type == "SolicitudBecario":

            nombreValor=obj.getIdOwner()+","+obj.getIdAsesor()+"\n"

            grado="      Grado de Estudios: "
            gradoValor=obj.getGrado()+"\n"

            asesor="                 Asesor: "
            asesorValor=self.getNombreAsesor(obj.getAsesor())+"\n"

            uline2="\n                     \n"
            lline2="                     \n\n"
            seccion2=uline2+":: Datos del Destino ::\n"+lline2

            presupuestoDValor+=grado+gradoValor+asesor+asesorValor

        elif obj.meta_type == "Solicitud":

            uline2="\n                     \n"
            lline2="                     \n\n"
            seccion2=uline2+":: Datos del Destino ::\n"+lline2

        elif obj.meta_type == "SolicitudVisitante":

            uline2="\n                       \n"
            lline2="                       \n\n"
    	    seccion2=uline2+":: Datos del Visitante ::\n"+lline2

            invitado="      Nombre: "
            invitadoValor= obj.getInvitado()+"\n"

            seccion2+=invitado+invitadoValor

        pais="        Pais: "
        paisValor= obj.getPaisCodigo()[0]+"\n"

        ciudad="      Ciudad: " 
        ciudadValor=obj.getCiudadPais()+"\n"

        institucion=" Institucion: "
        institucionValor=obj.getInstitucion()+"\n"

        fechaDesde="       Desde: "
        fechaDesdeValor=str(obj.getFechaDesde())+"\n"

        fechaHasta="       Hasta: "
        fechaHastaValor=str(obj.getFechaHasta())+"\n"

        uline3="\n                     \n"
        lline3="                     \n\n"
        seccion3=uline3+":: Datos Adicionales ::\n"+lline3

        objetoViaje="          Objetivo de la visita: "
        objetoViajeValor=obj.getObjetoViaje()+"\n"

        invArea="          Area de Investigacion: "
        invAreaValor=""
        for area in obj.getInvestigacionArea():
            invAreaValor+=area+","
        invAreaValor=invAreaValor.rstrip(',')
        invAreaValor+="\n"

        tituloTrabajo=" Titulo del trabajo a presentar: "
        tituloTrabajoValor=obj.getTituloTrabajo()+"\n"

        if obj.meta_type == "SolicitudBecario":

            comentariosAsesor="             Comentarios Asesor: "
            comentariosAsesorValor= obj.getComentario_asesor()+"\n"

            tituloTrabajoValor+=comentariosAsesor+comentariosAsesorValor

        comentarios="        Comentarios Adicionales: "
        comentariosValor=obj.getComentario_owner()+"\n"

        if obj.meta_type == "SolicitudBecario":
            apoyo="                    Apoyo Extra: "
            apoyoValor= obj.getApoyo_texto()+"\n"

            comentariosValor+=apoyo+apoyoValor

        pasaje="                     Transporte: "
        pasajeValor=obj.getPasaje()+"\n"

        tipoPasaje="            Medio de Transporte: "
        tipoPasajeValor=""
        for trans in obj.getTipo_pasaje():
            tipoPasajeValor+=trans+","
        tipoPasajeValor=tipoPasajeValor.rstrip(',')
        tipoPasajeValor+="\n"

        if obj.meta_type == "SolicitudBecario":
            viaticos="                       Viaticos: "
            viaticosValor=obj.getViaticos_becario()+"\n"
        else:
            viaticos="                       Viaticos: "
            viaticosValor=obj.getViaticos()+"\n"

        if not obj.meta_type == "SolicitudVisitante":
            inscripcion="                    Inscripcion: "
            inscripcionValor=obj.getInscripcion()+"\n"

        uline41="\n              \n"
        lline41="              \n\n"
        seccion41=uline41+":: Cantidades ::\n"+lline41

        back1=""
        while len(str(obj.getCantidad_pasaje()))+len(back1) < 20:
            back1+=" "
        back2=""
        while len(str(obj.getCantidad_recomendada_pasaje()))+len(back2) < 43:
            back2+=" "
        back3=""
        while len(str(obj.getCantidad_autorizada_pasaje()))+len(back3) < 43:
            back3+=" "

        back4=""
        while len(str(obj.getCantidad_viaticos()))+len(back4) < 20:
            back4+=" "
        back5=""
        while len(str(obj.getCantidad_recomendada_viaticos()))+len(back5) < 43:
            back5+=" "
        back6=""
        while len(str(obj.getCantidad_autorizada_viaticos()))+len(back6) < 43:
            back6+=" "

        if not obj.meta_type == "SolicitudVisitante":

            back7=""
            while len(str(obj.getCantidad_inscripcion()))+len(back7) < 20:
                back7+=" "
            back8=""
            while len(str(obj.getCantidad_recomendada_inscripcion()))+len(back8) < 43:
                back8+=" "
            back9=""
            while len(str(obj.getCantidad_autorizada_inscripcion()))+len(back9) < 43:
                back9+=" "

        uline42="                                                                                                                             \n"
        lline42="                                                                                                                             \n"
        seccion42=uline42+"              Cantidad Solicitada   Cantidad Recomendada por Comision Especial   Cantidad Autorizada por el Consejo Interno  \n"+lline42
        seccion43=      "  Transporte:"+back1+str(obj.getCantidad_pasaje())+" ,"+back2+str(obj.getCantidad_recomendada_pasaje())+" ,"+back3+str(obj.getCantidad_autorizada_pasaje())+"  \n"+lline42
        seccion44="    Viaticos:"+back4+str(obj.getCantidad_viaticos())+" ,"+back5+str(obj.getCantidad_recomendada_viaticos())+" ,"+back6+str(obj.getCantidad_autorizada_viaticos())+"  \n"+lline42

        if not obj.meta_type == "SolicitudVisitante":
            seccion45=" Inscripcion:"+back7+str(obj.getCantidad_inscripcion())+" ,"+back8+str(obj.getCantidad_recomendada_inscripcion())+" ,"+back9+str(obj.getCantidad_autorizada_inscripcion())+"  \n"+lline42

        raw=seccion1
        raw+=nombre+nombreValor
        raw+=estado+estadoValor
        raw+=presupuestoA+presupuestoAValor
        raw+=presupuestoD+presupuestoDValor

        raw+=seccion2
        raw+=pais+paisValor
        raw+=ciudad+ciudadValor
        raw+=institucion+institucionValor
        raw+=fechaDesde+fechaDesdeValor
        raw+=fechaHasta+fechaHastaValor

        raw+=seccion3
        raw+=objetoViaje+objetoViajeValor
        raw+=invArea+invAreaValor
        if not obj.meta_type == "SolicitudVisitante":
            raw+=tituloTrabajo+tituloTrabajoValor
        raw+=comentarios+comentariosValor
        raw+=pasaje+pasajeValor
        raw+=tipoPasaje+tipoPasajeValor
        raw+=viaticos+viaticosValor

        if not obj.meta_type == "SolicitudVisitante":
            raw+=inscripcion+inscripcionValor

        raw+=seccion41+seccion42+seccion43+seccion44

        if not obj.meta_type == "SolicitudVisitante":
            raw+=seccion45

        comisionado=self.esComisionado()
        consejero=self.esConsejero()

        if comisionado or consejero:

            uline5="\n                       \n"
            lline5="                       \n\n"
            seccion5=uline5+":: Informacion Interna ::\n"+lline5

            comentarioce="Recomendacion de la Comision Especial:"
            comentarioceValor=obj.getComentario_ce()+"\n"

            if consejero:

                fechasesion=" Fecha de Revision por Consejo Interno:"
                fechasesionValor=str(obj.getFecha_sesionci())+"\n"

                actaci="                 Numero de expediente:"
                actaciValor=obj.getActaci()+"\n"

                comentarioci="      Comentarios del Consejo Interno:"
                comentariociValor=obj.getComentario_ci()+"\n"

                comentarioceValor+=fechasesion+fechasesionValor
                comentarioceValor+=actaci+actaciValor
                comentarioceValor+=comentarioci+comentariociValor

            raw+=seccion5
            raw+=comentarioce+comentarioceValor

        return raw

    def getArea(self,codigoArea):
        areas=[]
        for area in codigoArea:
            try:
                areas.append(DICCIONARIO_AREAS[area])
            except:
                areas.append("")
        return areas

    def getTipoTransporte(self,codigoTrans):
        temp="";

        for codigo in codigoTrans:
            try:
                temp+=DICCIONARIO_TIPO_TRANSPORTE[codigo]
                temp+=","
            except:
                temp=temp

        return temp

    def getNombreAsesor(self,asesor):
        return self.context.portal_membership.getMemberById(asesor).getProperty('fullname')

    def esComisionado(self):
        try:
            member=self.context.portal_membership.getAuthenticatedMember()
            if 'Comisionado' in list(member.getRoles()):
                return True
            elif 'Responsable de la Comision' in list(member.getRoles()):
                return True
        except:
            return False
        return False

    def esConsejero(self):
        try:
            member=self.context.portal_membership.getAuthenticatedMember() 
            if 'Consejero' in list(member.getRoles()):
                return True
            elif 'Responsable del Consejo' in list(member.getRoles()):
                return True
        except:
            return False
        return False
