# -*- coding: utf-8 -*-

from DateTime.DateTime import DateTime
from matem.solicitudes.browser.queries import Queries
from matem.solicitudes.browser.requests import Requests
from matem.solicitudes.config import DICCIONARIO_AREAS
from matem.solicitudes.config import getCountriesVocabulary
from matem.solicitudes.interfaces import ISolicitudFolder
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SearchView(BrowserView):

    globaltemplate = ViewPageTemplateFile('global_request_search_form.pt')
    localtemplate = ViewPageTemplateFile('search_form.pt')

    queryObj = None
    reqObj = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.queryObj = Queries(self.context, self.request)
        self.reqObj = Requests(self.context, self.request)

    def __call__(self):
        self.queryObj = Queries(self.context, self.request)
        self.reqObj = Requests(self.context, self.request)
        if ISolicitudFolder.providedBy(self.context):
            return self.localtemplate()
        return self.globaltemplate()

    def search(self):
        form = self.request.form
        req = self.request

        queryObj=self.queryObj

        applications=[]

        try:
            searchStr=[ self.request.form['Creator'], #0
                        self.request.form['Pais'],    #1
                        self.request.form['Ciudad'].lower(),#2
                        self.request.form['Institucion'].lower(),#3
                        self.request.form['Desde'],#4
                        self.request.form['Hasta'],#5
                        self.request.form['Objeto'].lower(),#6
                        self.request.form['Area'],#7
                        self.request.form['TTrabajo'].lower(),#8
                        self.request.form['Becario'],#9
                        self.request.form['Asesor'],#10
                        self.request.form['Cantidad'],#11
                        self.request.form['CantidadLarger'],#12
                        self.request.form['CantidadLower']]#13

            Creator = self.request.form['Creator'] #0

            unTipo=self.request.form['Type']
            unEstado=self.request.form['State']

            if 'revision' in unEstado:
                unEstado=('preeliminar','revisioncomision','revisionconsejo')

        except:
            return applications

        zeroDate=DateTime(1920,1,1)

        try:
            fechaDesde=DateTime(int(self.request.form['Desde_year']),int(self.request.form['Desde_month']),int(self.request.form['Desde_day']))
        except:
            fechaDesde=zeroDate

        encontradas=[]

        if 'any' in unEstado:
            if 'todos' in Creator:
                encontradas = queryObj.getCurrentFolderApplications()
            else:
                encontradas = queryObj.getUserApplications(Creator)
        else:
            if 'todos' in Creator:
                encontradas = queryObj.getFolderApplicationsByState(unEstado)
            else:
                encontradas = queryObj.getFolderApplicationsByStateAndUser(unEstado,Creator)


        for obj in encontradas:
            append=False

            try:

                if obj['owner_id'].find(searchStr[0])!=-1 and searchStr[0] is not "":
                    append=True
                elif searchStr[0]=='todos':
                    append=True
                elif obj['country_code'][0].find(searchStr[1])!=-1 and searchStr[1] is not "":
                    append=True
                elif obj['country'].lower().find(searchStr[2])!=-1 and searchStr[2] is not "":
                    append=True
                elif obj['institution'].lower().find(searchStr[3])!=-1 and searchStr[3] is not "":
                    append=True
                elif obj['from'] >= fechaDesde and fechaDesde != zeroDate:
                    if fechaHasta == zeroDate :
                        append=True
                    else:
                        if obj['to'] <= fechaHasta:
                            append=True
                elif obj['to'] <= fechaHasta and fechaHasta != zeroDate:
                    if fechaDesde == zeroDate :
                        append=True
                    else:
                        if obj['from'] >= fechaDesde:
                            append=True
                elif obj['objective'].lower().find(searchStr[6])!=-1 and searchStr[6] is not "":
                    append=True
                elif obj['special_fields']['work_title'].lower().find(searchStr[8])!=-1 and searchStr[8] is not "":
                    append=True
            except:
                append=False

            for area in obj['research_areas']:
                if area.find(searchStr[7])!=-1 and searchStr[7] is not "":
                    append=True

            if obj['meta_type'] == 'SolicitudBecario':

                if obj['owner_id'].find(searchStr[9])!=-1 and searchStr[9] is not "":
                    append=True
                if obj['special_fields']['researcher_id'].find(searchStr[10])!=-1 and searchStr[10] is not "":
                    append=True

            try:
                equal=float(searchStr[11])
                larger=float(searchStr[12])
                lower=float(searchStr[13])
            except:
                equal=larger=lower=0.0

            if obj['workflow_state']=="aprobada":
                referencia=obj['total_approved_quantity']
            else:
                referencia=obj['total_quantity']

            if equal == referencia and equal > 0:
                append=True
            elif referencia > larger and larger > 0:
                append=True
            elif referencia < lower and lower > 0:
                append=True

            if append and unTipo is not None:
                if unTipo == "becario":
                    if not obj['meta_type'] == "SolicitudBecario":
                        append=False
                elif unTipo == "visitante":
                    if not obj['meta_type'] == "SolicitudVisitante":
                        append=False
                elif unTipo == "licencia":
                    if not obj['meta_type'] == "Solicitud":
                        append=False

            if append and unEstado is not None:
                if unEstado == "aprobada" and not obj['workflow_state']=="aprobada":
                        append=False
                elif unEstado == "rechazada" and not obj['workflow_state']=="rechazada":
                        append=False
                elif unEstado == "revision" and obj['workflow_state']=="aprobada":
                        append=False
                elif unEstado == "revision" and obj['workflow_state']=="rechazada":
                        append=False

            if append:
                applications.append(obj)

            append=False
        sorted_list = [(a['revision_ci_date'], a) for a in applications] 
        sorted_list.sort(key=lambda  x: x[0])
        return [dic for name, dic in sorted_list] 

    def searchSlow(self):
        form = self.request.form
        req = self.request

        applications=[]

        queryObj=self.queryObj

        try:
            searchStr=[ self.request.form['Creator'], #0
                        self.request.form['Pais'],    #1
                        self.request.form['Ciudad'].lower(),#2
                        self.request.form['Institucion'].lower(),#3
                        self.request.form['Desde'],#4
                        self.request.form['Hasta'],#5
                        self.request.form['Objeto'].lower(),#6
                        self.request.form['Area'],#7
                        self.request.form['TTrabajo'].lower(),#8
                        self.request.form['Becario'],#9
                        self.request.form['Asesor'],#10
                        self.request.form['Cantidad'],#11
                        self.request.form['CantidadLarger'],#12
                        self.request.form['CantidadLower']]#13

            unTipo=self.request.form['Type']
            unEstado=self.request.form['State']

        except:
            return applications

        zeroDate=DateTime(1920,1,1)

        try:
            fechaDesde=DateTime(int(self.request.form['Desde_year']),int(self.request.form['Desde_month']),int(self.request.form['Desde_day']))
        except:
            fechaDesde=zeroDate

        try:
            fechaHasta=DateTime(int(self.request.form['Hasta_year']),int(self.request.form['Hasta_month']),int(self.request.form['Hasta_day']))
        except:
            fechaHasta=zeroDate

        for obj in queryObj.getAllApplications():
            append=False

            try:

                if obj['owner_id'].find(searchStr[0])!=-1 and searchStr[0] is not "":
                    append=True
                elif searchStr[0]=='todos':
                    append=True
                elif obj['country_code'][0].find(searchStr[1])!=-1 and searchStr[1] is not "":
                    append=True
                elif obj['country'].lower().find(searchStr[2])!=-1 and searchStr[2] is not "":
                    append=True
                elif obj['institution'].lower().find(searchStr[3])!=-1 and searchStr[3] is not "":
                    append=True
                elif obj['from'] >= fechaDesde and fechaDesde != zeroDate:
                    if fechaHasta == zeroDate :
                        append=True
                    else:
                        if obj['to'] <= fechaHasta:
                            append=True
                elif obj['to'] <= fechaHasta and fechaHasta != zeroDate:
                    if fechaDesde == zeroDate :
                        append=True
                    else:
                        if obj['from'] >= fechaDesde:
                            append=True
                elif obj['objective'].lower().find(searchStr[6])!=-1 and searchStr[6] is not "":
                    append=True
                elif obj['special_fields']['work_title'].lower().find(searchStr[8])!=-1 and searchStr[8] is not "":
                    append=True
            except:
                append=False

            for area in obj['research_areas']:
                if area.find(searchStr[7])!=-1 and searchStr[7] is not "":
                    append=True

            if obj['meta_type'] == 'SolicitudBecario':
            
                if obj['owner_id'].find(searchStr[9])!=-1 and searchStr[9] is not "":
                    append=True
                if obj['special_fields']['researcher_id'].find(searchStr[10])!=-1 and searchStr[10] is not "":
                    append=True

            try:
                equal=float(searchStr[11])
                larger=float(searchStr[12])
                lower=float(searchStr[13])
            except:
                equal=larger=lower=0.0

            if obj['workflow_state']=="aprobada":
                referencia=obj['total_approved_quantity']
            else:
                referencia=obj['total_quantity']

            if equal == referencia and equal > 0:
                append=True
            elif referencia > larger and larger > 0:
                append=True
            elif referencia < lower and lower > 0:
                append=True

            if append and unTipo is not None:
                if unTipo == "becario":
                    if not obj['meta_type'] == "SolicitudBecario":
                        append=False
                elif unTipo == "visitante":
                    if not obj['meta_type'] == "SolicitudVisitante":
                        append=False
                elif unTipo == "licencia":
                    if not obj['meta_type'] == "Solicitud":
                        append=False

            if append and unEstado is not None:
                if unEstado == "aprobada" and not obj['workflow_state']=="aprobada":
                        append=False
                elif unEstado == "rechazada" and not obj['workflow_state']=="rechazada":
                        append=False
                elif unEstado == "revision" and obj['workflow_state']=="aprobada":
                        append=False
                elif unEstado == "revision" and obj['workflow_state']=="rechazada":
                        append=False

            if append:
                applications.append(obj)
            append=False
        return applications

    def hasPendingReviews(self,usuarioActual):
        mt = self.context.portal_membership
        member=mt.getMemberById(usuarioActual)

        for obj in self.context.objectValues():
            if obj.getWFState()=="borrador":
                if usuarioActual == obj.getIdOwner():
                    return True
            elif obj.getWFState()=="preeliminar":
                if usuarioActual == obj.getIdAsesor():
                    return True
            elif obj.getWFState()=="revisioncomision":
                if 'Comisionado' in list(member.getRoles()):
                    return True
                elif 'Responsable de la Comision' in list(member.getRoles()):
                    return True
            elif obj.getWFState()=="revisionconsejo":
                if 'Consejero' in list(member.getRoles()):
                    return True
                elif 'Responsable del Consejo' in list(member.getRoles()):
                    return True
        return False

    def getCreatorsBecario(self):
        folder=self.context
        solicitantes=folder.getSolicitantes()[0]
        users = []

        for solicitante in solicitantes.keys():
            if 'Becario' in solicitantes[solicitante][3]:
                users.append([solicitantes[solicitante][0]+", "+solicitantes[solicitante][1]+" "+solicitantes[solicitante][2],
                          solicitante])
        users.sort()

        return users

    def getCreatorsInvestigador(self):
        folder=self.context
        solicitantes=folder.getSolicitantes()[0]
        users = []

        for solicitante in solicitantes.keys():
            if 'Investigador' in solicitantes[solicitante][3]:
                users.append([solicitantes[solicitante][0]+", "+solicitantes[solicitante][1]+" "+solicitantes[solicitante][2],
                          solicitante])
        users.sort()

        return users

    def getCreatorsPostdoc(self):
        folder=self.context
        solicitantes=folder.getSolicitantes()[0]
        users = []

        for solicitante in solicitantes.keys():
            if 'Postdoc' in solicitantes[solicitante][3]:
                users.append([solicitantes[solicitante][0]+", "+solicitantes[solicitante][1]+" "+solicitantes[solicitante][2],
                          solicitante])
        users.sort()
        
        return users

    def getCreatorsTecnicoAcademico(self):
        folder=self.context
        solicitantes=folder.getSolicitantes()[0]
        users = []

        for solicitante in solicitantes.keys():
            if 'Tecnico Academico' in solicitantes[solicitante][3]:
                users.append([solicitantes[solicitante][0]+", "+solicitantes[solicitante][1]+" "+solicitantes[solicitante][2],
                          solicitante])
        users.sort()
        
        return users

    def getCreatorsAll(self):
        folder=self.context
        solicitantes=folder.getSolicitantes()[0]
        users = []

        for solicitante in solicitantes.keys():
            users.append([solicitantes[solicitante][0]+", "+solicitantes[solicitante][1]+" "+solicitantes[solicitante][2],
                          solicitante])
        users.sort()

        return users

    def getCreatorsBecarioInvestigador(self):
        folder=self.context
        solicitantes=folder.getSolicitantes()[0]
        users = []
        insertar = False

        for solicitante in solicitantes.keys():
            if 'Investigador' in solicitantes[solicitante][3]:
                insertar = True
            elif 'Becario' in solicitantes[solicitante][3]:
                insertar = True

            if insertar:
                users.append([solicitantes[solicitante][0]+", "+solicitantes[solicitante][1]+" "+solicitantes[solicitante][2],
                          solicitante])
                insertar = False

        users.sort()

        return users

    def getAreasInv(self):
        options=[]
        llaves= DICCIONARIO_AREAS.keys()
        llaves.sort()

        for llave in llaves:
            options.append([llave,DICCIONARIO_AREAS[llave]])
        return options

    def getRequest(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, '')
            f = tipo
            if tipo is None:
                return ""
            else:
                return f
        except:
            return ""

    def hasReqDataStr(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, '')
            f = tipo
            if tipo is None:
                return False
            else:
                if tipo == "":
                    return False
                else:
                    return True
        except:
            return False


    def getCountriesVocabulary(self):
        #This function is defined in config.py
        return getCountriesVocabulary(self).items()[1:]


