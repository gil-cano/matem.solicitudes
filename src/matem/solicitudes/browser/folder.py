# -*- coding: utf-8 -*-
from matem.solicitudes.browser.queries import Queries
from matem.solicitudes.browser.requests import Requests
from matem.solicitudes.extender import PersonWrapper
from matem.solicitudes.PyRTF import *
from operator import itemgetter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import re


class SolicitudFolderView(BrowserView):
    """A view of the application folder."""

    menu = ViewPageTemplateFile('solicitudfolder.pt')
    misaprobadas = ViewPageTemplateFile('misaprobadas.pt')
    misrechazadas = ViewPageTemplateFile('misrechazadas.pt')
    misenviadas = ViewPageTemplateFile('misenviadas.pt')
    generaractas = ViewPageTemplateFile('generaractas.pt')
    folderpendientes = ViewPageTemplateFile('folderpendientes.pt')
    folderaprobadas = ViewPageTemplateFile('folderaprobadas.pt')
    folderrechazadas = ViewPageTemplateFile('folderrechazadas.pt')
    presupuestolocal = ViewPageTemplateFile('presupuesto_folder.pt')
    solicitudesauxiliares = ViewPageTemplateFile('solicitudes_auxiliares.pt')
    micuenta = ViewPageTemplateFile('micuenta.pt')

    queryObj = None
    reqObj = None

    def __call__(self):
        # fisrt time in folder
        if not self.request.form:
            return self.menu()

        self.queryObj = Queries(self.context, self.request)
        self.reqObj = Requests(self.context, self.request)
        form = self.request.form
        req = self.request
        container = self.context

        tipo = req.get('vistafolder')
        letra = req.get('pagina', '')
        memberid = req.get('memberID', None)
        user = req.get('user', '')
        adder = False
        reviewer = False
        usuarioAutenticado = self.context.portal_membership.getAuthenticatedMember()

        if "Investigador" in list(usuarioAutenticado.getRoles()):
            adder = True
        elif "Postdoc" in list(usuarioAutenticado.getRoles()):
            adder = True
        elif "Tecnico Academico" in list(usuarioAutenticado.getRoles()):
            adder = True
        elif "Becario" in list(usuarioAutenticado.getRoles()):
            adder = True

        if "Comisionado" in list(usuarioAutenticado.getRoles()):
            reviewer = True
        elif "Consejero" in list(usuarioAutenticado.getRoles()):
            reviewer = True
        elif "Responsable de la Comision" in list(usuarioAutenticado.getRoles()):
            reviewer = True
        elif "Responsable del Consejo" in list(usuarioAutenticado.getRoles()):
            reviewer = True

        if tipo is None:
            if req.form.get('-C') is None:
                return self.changeBlockState(req.form)
            else:
                return self.menu()
        else:
            if tipo == "misaprobadas":
                return self.misaprobadas()
            elif tipo == "misrechazadas":
                return self.misrechazadas()
            elif tipo == "misenviadas":
                return self.misenviadas()
            elif tipo == "generaractas":
                return self.generaractas()
            elif tipo == "folderpendientes":
                return self.folderpendientes()
            elif tipo == "folderaprobadas":
                return self.folderaprobadas()
            elif tipo == "folderrechazadas":
                return self.folderrechazadas()
            elif tipo == "presupuestolocal":
                if letra is not None:
                    self.request.set('pagina', letra)
                if memberid is not None:
                    solicitantes = self.context.getSolicitantes()
                    try:
                        solicitantes[0][memberid][4] = float(req.get('newBudget', solicitantes[0][memberid][4]))
                        self.context.setSolicitantes(solicitantes)
                    except:
                        print req.get('newBudget', '')
                return self.presupuestolocal()
            elif tipo == "solicitudesauxiliares":
                return self.solicitudesauxiliares()
            elif tipo == "micuenta":
                if user is not None:
                    self.micuenta.pt_getContext().get('request', '').set('user', user)
                return self.micuenta()
            else:
                return self.menu()

    def esManager(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Manager' in list(member.getRoles()):
            return True
        return False

    def esComisionado(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Comisionado' in list(member.getRoles()):
            return True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            return True
        return False

    def esResponsableDeLaComision(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Responsable de la Comision' in list(member.getRoles()):
            return True
        return False

    def esConsejero(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Consejero' in list(member.getRoles()):
            return True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            return True
        return False

    def esResponsableDelConsejo(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Responsable del Consejo' in list(member.getRoles()):
            return True
        return False

    def esTecnicoAcademico(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Tecnico Academico' in list(member.getRoles()):
            return True
        return False

    def esPostdoc(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Postdoc' in list(member.getRoles()):
            return True
        return False

    def esInvestigador(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Investigador' in list(member.getRoles()):
            return True
        return False

    def esBecario(self, usuario):
        member = self.context.portal_membership.getMemberById(usuario)
        if 'Becario' in list(member.getRoles()):
            return True
        return False

    def esSolicitanteNormal(self, usuario):
        return self.esTecnicoAcademico(usuario) or self.esInvestigador(usuario) or self.esBecario(usuario) or self.esPostdoc(usuario)

    def getSolicitudesPosibles(self, investigador):
        solicitudes = []
        mt = self.context.portal_membership
        member = mt.getMemberById(investigador)
        vertodo = False
        queryObj = self.queryObj

        if 'Manager' in list(member.getRoles()):
            vertodo = True
        elif 'Comisionado' in list(member.getRoles()):
            vertodo = True
        elif 'Consejero' in list(member.getRoles()):
            vertodo = True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            vertodo = True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            vertodo = True

        if vertodo is True:
            return queryObj.getCurrentFolderApplications()
        else:
            return queryObj.getMyApplications()

    def getSolicitudesAprobadasIndividuales(self, usuario):
        queryObj = self.queryObj
        applications = queryObj.getFolderApplicationsByStateAndUser('aprobada', usuario)
        return applications

    def getSolicitudesRechazadasIndividuales(self, usuario):
        queryObj = self.queryObj
        applications = queryObj.getFolderApplicationsByStateAndUser('rechazada', usuario)
        return applications

    def getSolicitudesEnviadasIndividuales(self, usuario):
        applications = []
        queryObj = self.queryObj
        applications += queryObj.getFolderApplicationsByStateAndUser('revisioncomision', usuario)
        applications += queryObj.getFolderApplicationsByStateAndUser('revisionconsejo', usuario)
        return applications

    def getInvestigadores(self, usuario):
        folder = self.context
        mt = self.context.portal_membership
        member = mt.getMemberById(usuario)
        fsdperson = self.queryObj.getPersonWrapper(usuario)
        users = []
        rol = ""
        append = False

        if 'Becario' in list(member.getRoles()):
            rol = "Becario"
            append = True
        elif 'Investigador' in list(member.getRoles()):
            rol = "Investigador"
            append = True
        elif 'Postdoc' in list(member.getRoles()):
            rol = "Postdoc"
            append = True
        elif 'Tecnico Academico' in list(member.getRoles()):
            rol = "Tecnico Academico"
            append = True

        if append:
            users[letter].append([fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),
                       folder.getPresupuesto_asignado_solicitantes()[0].get(fsdperson.getId(),0.0),
                       rol,
                       fsdperson.getId(),
                       folder.getSolicitantes()[0].get(fsdperson.getId(),[0,0,0,0,0.0])[4]-folder.getPresupuesto_asignado_solicitantes()[0].get(fsdperson.getId(),0.0),
                       folder.getDias_comision_utilizados_solicitantes()[0].get(fsdperson.getId(),0),
                       folder.getDias_licencia_utilizados_solicitantes()[0].get(fsdperson.getId(),0)])
        return users

    def getPresupuestoIndividual(self, usuario):
        folder = self.context
        mt = self.context.portal_membership
        member = mt.getMemberById(usuario)

        fsdperson = self.queryObj.getPersonWrapper(usuario)
        users = []
        rol = ""

        if 'Becario' in list(member.getRoles()):
            rol = "Becario"
        elif 'Investigador' in list(member.getRoles()):
            rol = "Investigador"
        elif 'Postdoc' in list(member.getRoles()):
            rol = "Postdoc"
        elif 'Tecnico Academico' in list(member.getRoles()):
            rol = "Tecnico Academico"
        else:
            rol = "No puede solicitar recursos"

#        users.append([fsdperson.getLastName()+', '+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),fsdperson.getPresupuesto_asignado(),fsdperson.getDias_licencia_utilizados(),fsdperson.getDias_comision_utilizados(),rol,str(fsdperson.getId())])
        users.append([fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),
                  folder.getPresupuesto_asignado_solicitantes()[0].get(fsdperson.getId(),0.0),
                  rol,
                  fsdperson.getId(),
                  folder.getSolicitantes()[0].get(fsdperson.getId(),[0,0,0,0,0.0])[4]-folder.getPresupuesto_asignado_solicitantes()[0].get(fsdperson.getId(),0.0),
                  folder.getDias_comision_utilizados_solicitantes()[0].get(fsdperson.getId(),0),
                  folder.getDias_licencia_utilizados_solicitantes()[0].get(fsdperson.getId(),0)])

        return users

    def getInvestigadoresLocalAlfabeticamentePerson(self,usuario):
        folder=self.context
        mt = self.context.portal_membership
        member=mt.getMemberById(usuario)
        append=False
        rol=""
        fsd_tool = self.context.facultystaffdirectory_tool
        users = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[],'I':[],'J':[],'K':[],'L':[],'M':[],'N':[],'O':[],'P':[],'Q':[],'R':[],'S':[],'T':[],'U':[],'V':[],'W':[],'X':[],'Y':[],'Z':[]}

        if 'Programador de Presupuesto' in list(member.getRoles()):
            for person in list(fsd_tool.getDirectoryRoot().getSortedPeople()):
                fsdperson = PersonWrapper(person)
                letter=unicode(fsdperson.getLastName())[0].upper();
                letter=letter.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U').replace('Ñ','N').replace('Ö','O');
                user=mt.getMemberById(fsdperson.getId());

                if 'Investigador' in list(user.getRoles()):
                    rol="Investigador"
                    append=True
                elif 'Postdoc' in list(user.getRoles()):
                    rol="Postdoc"
                    append=True
                elif 'Tecnico Academico' in list(user.getRoles()):
                    rol="Tecnico Academico"
                    append=True
                elif 'Becario' in list(user.getRoles()):
                    rol="Becario"
                    append=True

                try:
                    if append :
#                        users[letter].append([fsdperson.getLastName()+","+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),fsdperson.getPresupuesto_asignado(),rol,fsdperson.getId(),fsdperson.getPresupuesto_inicial()-fsdperson.getPresupuesto_asignado(),fsdperson.getDias_comision_utilizados(),fsdperson.getDias_licencia_utilizados()])
                        append=False
                except:
                    pass;
        return users

    def getInvestigadoresLocalAlfabeticamente(self,usuario):
        folder=self.context
        mt = self.context.portal_membership
        member=mt.getMemberById(usuario)
        users = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[],'I':[],'J':[],'K':[],'L':[],'M':[],'N':[],'O':[],'P':[],'Q':[],'R':[],'S':[],'T':[],'U':[],'V':[],'W':[],'X':[],'Y':[],'Z':[]}

        if 'Programador de Presupuesto' in list(member.getRoles()):
            llaves=folder.getSolicitantes()[0].keys()
            for person in llaves:
                personinfo=folder.getSolicitantes()[0][person]
                letter = unicode(personinfo[0], "utf-8")[0].upper()
                letter = letter.replace(u'Á','A').replace(u'É','E').replace(u'Í','I').replace(u'Ó','O').replace(u'Ú','U').replace(u'Ñ','N').replace(u'Ö','O');
                users[letter].append([personinfo[0]+", "+personinfo[1]+" "+personinfo[2],
                          folder.getPresupuesto_asignado_solicitantes()[0].get(person,0.0),
                          personinfo[3],
                          person,
                          personinfo[4]-folder.getPresupuesto_asignado_solicitantes()[0].get(person,0.0),
                          folder.getDias_comision_utilizados_solicitantes()[0].get(person,0),
                          folder.getDias_licencia_utilizados_solicitantes()[0].get(person,0),
                          folder.getApoyoinst_asignado_solicitantes()[0].get(person,0.0),
                          personinfo[5]-folder.getApoyoinst_asignado_solicitantes()[0].get(person,0.0)],
                          )

            for letter in users.keys():
                users[letter].sort()
        return users

    def getIndividualBudgets(self):
        solicitantes = self.context.getSolicitantes()
        mt = self.context.portal_membership
        member=mt.getAuthenticatedMember()
        users = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[],'I':[],'J':[],'K':[],'L':[],'M':[],'N':[],'O':[],'P':[],'Q':[],'R':[],'S':[],'T':[],'U':[],'V':[],'W':[],'X':[],'Y':[],'Z':[]}

        if 'Programador de Presupuesto' in list(member.getRoles()):
            for key, value in solicitantes[0].iteritems():
                letter = unicode(value[0], "utf-8")[0].upper()
                letter = letter.replace(u'Á','A').replace(u'É','E').replace(u'Í','I').replace(u'Ó','O').replace(u'Ú','U').replace(u'Ñ','N').replace(u'Ö','O');
                users[letter].append(["%s, %s %s" % (value[0], value[1], value[2]),
                                      value[4], key])

            for letter in users.keys():
                users[letter].sort()

        return users

    def getAlphabetLetters(self):
        users = {'A':{},'B':{},'C':{},'D':{},'E':{},'F':{},'G':{},'H':{},'I':{},'J':{},'K':{},'L':{},'M':{},'N':{},'O':{},'P':{},'Q':{},'R':{},'S':{},'T':{},'U':{},'V':{},'W':{},'X':{},'Y':{},'Z':{}}
        result=users.keys()
        result.sort()
        return result

    def getPageAlphabetic(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, '')
            if str(tipo) != '':
                return str(tipo)
            else:
                return 'A'
        except:
            return 'A'

    def getPageAlphabeticNumber(self,tipodato):
        try:
            alphabet=self.getAlphabetLetters()
            req = self.request
            tipo=req.get(tipodato, '')
            for x in range(0,len(alphabet)):
                if alphabet[x] is str(tipo):
                    return x
                else:
                    return 0
        except:
            return 0

    def getSortedKeys(self,keyList):
        keyList.sort()
        return keyList
    def getPage(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, '')
            f = int(tipo)
            if tipo is None:
                return 0
            else:
                return f
        except:
            return 0

    def getRequestValue(self,campo):
        try:
            req = self.request
            return req.get(campo, None)
        except:
            return None

    def getReqDataStr(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, '')
            if tipo is None:
                return None
            else:
                return tipo
        except:
            return None

    def getIndexedList(self,data,qty_of_results):
        i=0
        page=[]
        temp=[]

        try:
            qty_of_results=int(qty_of_results)-1
            if qty_of_results < 1 :
                qty_of_results=9
        except:
            qty_of_results=9

        for result in data:
            page.append(result)
            i+=1
            if i > qty_of_results:
                temp.append(page[:])
                i=0
                page=[]

        if i>0:
            temp.append(page)

        return temp

    def getCantidadAsignadaTotal(self,usuario):
        mt = self.context.portal_membership
        member=mt.getMemberById(usuario)
        users = []
        vertodo=False
        cantidadTotal=0.0
        presupuestoInicial=0.0

        if 'Manager' in list(member.getRoles()):
            vertodo=True
        elif 'Comisionado' in list(member.getRoles()):
            vertodo=True
        elif 'Consejero' in list(member.getRoles()):
            vertodo=True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            vertodo=True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            vertodo=True
        elif 'Programador de Presupuesto' in list(member.getRoles()):
            vertodo=True

        if vertodo is True:
            for user in mt.listMembers():
                if 'Becario' in list(user.getRoles()) or 'Investigador' in list(user.getRoles()) or 'Tecnico Academico' in list(user.getRoles()) or 'Postdoc' in list(user.getRoles()):
                    cantidadTotal+=user.getProperty('presupuesto_asignado')
                    presupuestoInicial+=user.getProperty('presupuesto_inicial')
        else:
            cantidadTotal=member.getProperty('presupuesto_asignado')
            presupuestoInicial=member.getProperty('presupuesto_inicial')

        users.append(["Presupuesto Maximo",presupuestoInicial])
        users.append(["Total Ejercido",cantidadTotal])
        users.append(["Restante",presupuestoInicial-cantidadTotal])

        return users

    def calcularTotal(self,items):
        itemtotal=0.0
        for item in items:
            itemtotal+=item['total_approved_quantity']
        return itemtotal

    def calcularTotalInvDict(self,investigadores):
        itemtotal=0.0
        for key in list(investigadores):
            for investigador in investigadores[key]:
                itemtotal+=investigador[1]
        return itemtotal

    def calcularTotalInv(self,investigadores):
        itemtotal=0.0
        for page in investigadores:
            for investigador in page:
                itemtotal+=investigador[1]
        return itemtotal

    def compararValores(self,cantidadAsignada,cantidadCalculada):
        mt = self.context.portal_membership
        investigador = mt.getAuthenticatedMember()
        if cantidadAsignada != cantidadCalculada:
            investigador.setMemberProperties({'presupuesto_asignado': cantidadCalculada})
            return False
        return True

    def getCantidadAsignadaLocal(self,usuario):
        folder=self.context
        mt = self.context.portal_membership
        member=mt.getMemberById(usuario)
        fsdperson = self.queryObj.getPersonWrapper(usuario)
        users = []
        vertodo=False
        cantidadTotal=0.0
        presupuestoInicial=0.0

        if vertodo is True:
            for user in mt.listMembers():
                if 'Becario' in list(user.getRoles()) or 'Investigador' in list(user.getRoles()) or 'Tecnico Academico' in list(user.getRoles()) or 'Postdoc' in list(user.getRoles()):
                    cantidadTotal+=user.getProperty('presupuesto_asignado')
                    presupuestoInicial+=user.getProperty('presupuesto_inicial')
        else:
            cantidadTotal=folder.getPresupuesto_asignado_solicitantes()[0].get(fsdperson.getId(),0.0)
            presupuestoInicial=folder.getSolicitantes()[0].get(fsdperson.getId(),[0,0,0,0,0.0])[4]

        users.append(["Presupuesto Maximo",presupuestoInicial])
        users.append(["Total Ejercido",cantidadTotal])
        users.append(["Restante",presupuestoInicial-cantidadTotal])

        return users


    def isTotal(self,usuario):
        mt = self.context.portal_membership
        member=mt.getMemberById(usuario)
        vertodo=False

        if 'Manager' in list(member.getRoles()):
            vertodo=True
        elif 'Comisionado' in list(member.getRoles()):
            vertodo=True
        elif 'Consejero' in list(member.getRoles()):
            vertodo=True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            vertodo=True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            vertodo=True

        return vertodo

    def hasPendingReviews(self, usuarioActual):
        """ This fuction return True if the are drafts or
        students pending reviews
        """
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        drafts = catalog(
            path={'query': folder_path, 'depth': 1},
            portal_type=(
                'Solicitud',
                'SolicitudVisitante',
                'SolicitudBecario',
                'SolicitudInstitucional',
            ),
            review_state='borrador',
            Creator=usuarioActual,
        )
        students = catalog(
            path={'query': folder_path, 'depth': 1},
            portal_type='SolicitudBecario',
            review_state='preeliminar',
            asesor=usuarioActual,
        )
        return drafts or students

    def getTodasSolicitudesProcesadas(self): #Aprobadas y Rechazadas como Dictionario
        queryObj = self.queryObj
        applications = self.getTodasSolicitudesAprobadas()+self.getTodasSolicitudesRechazadas()
        applicationDict={}
        for application in applications:
            if applicationDict.get(application['acta_ci'],None) is None:
                applicationDict[application['acta_ci']]=[]
            applicationDict[application['acta_ci']].append(application)
        return applicationDict

    def getTodasSolicitudesAprobadas(self): #getSolicitudesAprobadas
        queryObj=self.queryObj
        applications=queryObj.getFolderApplicationsByState('aprobada')
        # sort by acta
        sorted_list = [('%s-%s' % (a['acta_ci'], a['owner_name']), a) for a in applications]
        sorted_list.sort(key=lambda  x: x[0])
        return [dic for name, dic in sorted_list]

    def getTodasSolicitudesRechazadas(self): #getSolicitudesRechazadas
        queryObj=self.queryObj
        applications=queryObj.getFolderApplicationsByState('rechazada')
        return applications

    def getSolicitudesPendientes(self,usuario):
        applications=[]
        mt = self.context.portal_membership
        memberdataObj = mt.getMemberById(usuario)

        applications+=self.getSolicitudesPendientesEnvio(usuario)
        applications+=self.getSolicitudesPendientesRevisionPreeliminar(usuario)
        applications+=self.getSolicitudesPendientesRevisionComision()
        applications+=self.getSolicitudesPendientesRevisionConsejo()

        return applications

    def getSolicitudesPendientesEnvio(self,usuario):
        queryObj=self.queryObj
        applications=queryObj.getFolderApplicationsByStateAndUser('borrador',usuario)
        return applications

    def getSolicitudesPendientesRevisionPreeliminar(self,usuario):
        queryObj=self.queryObj
        temp=queryObj.getFolderApplicationsByState('preeliminar')
        applications=[]
        for form in temp:
            try:
                if form['special_fields']['researcher_id']==usuario:
                    applications.append(form)
            except:
                print "No es solicitud de becario."
        return applications

    def getSolicitudesPendientesRevisionComision(self):
        queryObj = self.queryObj
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()
        hasPermission = False

        if 'Comisionado' in list(member.getRoles()):
            hasPermission = True
        elif 'Responsable de la Comision' in list(member.getRoles()):
            hasPermission = True

        if hasPermission:
            applications = queryObj.getFolderApplicationsByState('revisioncomision')
            # regresamos lista ordenada por sede y luego por solicitante
            applications.sort(key=itemgetter('owner_name'))
            applications.sort(key=itemgetter('sede'))
            return applications
        else:
            return []

    def getSolicitudesPendientesRevisionConsejo(self):
        queryObj = self.queryObj
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()
        hasPermission = False

        if 'Consejero' in list(member.getRoles()):
            hasPermission = True
        elif 'Responsable del Consejo' in list(member.getRoles()):
            hasPermission = True

        if hasPermission:
            applications = queryObj.getFolderApplicationsByState('revisionconsejo')
            # regresamos lista ordenada por sede y luego por solicitante
            applications.sort(key=itemgetter('owner_name'))
            applications.sort(key=itemgetter('sede'))
            return applications
        else:
            return []

    def getBudget(self):
        mt = self.context.portal_membership
        member= mt.getAuthenticatedMember()
        return member.getProperty('presupuesto_inicial')

    def getBudgetBecario(self):
        mt = self.context.portal_membership
        member= mt.getAuthenticatedMember()
        return member.getProperty('presupuesto_inicial_becario')

    def setBudget(self,tipodato):
        mt = self.context.portal_membership
        member= mt.getAuthenticatedMember()

        f= 0.0


        viejo = self.context.getSolicitantes()[0].get(member.getId(),[0,0,0,0,0.0])[4]
        req = self.request
        tipo=req.get(tipodato, '')
        if tipo is None:
            return viejo
        else:
            f=float(tipo)
            if f < 0:
                return viejo

        if 'Programador de Presupuesto' in list(member.getRoles()):
            solicitantes=getSolicitantes()[0]
            solicitantes.get(fsdperson.getId(),[0,0,0,0,0.0])[4]=f
            self.context.setSolicitantes(solicitantes)

        return f

    def setBudgets(self,tipodato):
        mt = self.context.portal_membership
        member= mt.getAuthenticatedMember()
        folder=self.context

        f= 0.0
        try:
            if tipodato.find('budgetvalueinvestigador') != -1:
                viejo = float(folder.getPresupuesto_maximo_investigadores())
            elif tipodato.find('budgetvaluebecario') != -1:
                viejo = float(folder.getPresupuesto_maximo_becarios())
            elif tipodato.find('budgetvaluetecnico') != -1:
                viejo = float(folder.getPresupuesto_maximo_tecnicos())
            elif tipodato.find('budgetvaluepostdoc') != -1:
                viejo = float(folder.getPresupuesto_maximo_postdocs())
            elif tipodato.find('apoyovalueinvestigador') != -1:
                viejo = float(folder.getApoyoinst_maximo_investigadores())
            elif tipodato.find('apoyovaluebecario') != -1:
                viejo = float(folder.getApoyoinst_maximo_becarios())
            elif tipodato.find('apoyovaluetecnico') != -1:
                viejo = float(folder.getApoyoinst_maximo_tecnicos())
            elif tipodato.find('apoyovaluepostdoc') != -1:
                viejo = float(folder.getApoyoinst_maximo_postdocs())
            else:
                viejo = 0.0
            req = self.request
            tipo=req.get(tipodato, None)
            if tipo is None:
                return viejo
            else:
                f=float(tipo)
                if f < 0:
                    return viejo
        except:
            return -1

        if 'Programador de Presupuesto' in list(member.getRoles()):
            if tipodato.find('budgetvalueinvestigador') != -1:
                folder.setPresupuesto_maximo_investigadores(f);
            elif tipodato.find('budgetvaluebecario') != -1:
                folder.setPresupuesto_maximo_becarios(f);
            elif tipodato.find('budgetvaluetecnico') != -1:
                folder.setPresupuesto_maximo_tecnicos(f);
            elif tipodato.find('budgetvaluepostdoc') != -1:
                folder.setPresupuesto_maximo_postdocs(f);
            elif tipodato.find('apoyovalueinvestigador') != -1:
                folder.setApoyoinst_maximo_investigadores(f);
            elif tipodato.find('apoyovaluebecario') != -1:
                folder.setApoyoinst_maximo_becarios(f);
            elif tipodato.find('apoyovaluetecnico') != -1:
                folder.setApoyoinst_maximo_tecnicos(f);
            elif tipodato.find('apoyovaluepostdoc') != -1:
                folder.setApoyoinst_maximo_postdocs(f);

            solicitantes=folder.getSolicitantes()
            for person in solicitantes[0]:
                if "Investigador" in solicitantes[0][person][3] and tipodato.find('budgetvalueinvestigador') != -1:
                    solicitantes[0][person][4]=f;
                elif "Becario" in solicitantes[0][person][3] and tipodato.find('budgetvaluebecario') != -1:
                    solicitantes[0][person][4]=f;
                elif "Tecnico Academico" in solicitantes[0][person][3] and tipodato.find('budgetvaluetecnico') != -1:
                    solicitantes[0][person][4]=f;
                elif "Postdoc" in solicitantes[0][person][3] and tipodato.find('budgetvaluepostdoc') != -1:
                    solicitantes[0][person][4]=f;
                elif "Investigador" in solicitantes[0][person][3] and tipodato.find('apoyovalueinvestigador') != -1:
                    solicitantes[0][person][5]=f;
                elif "Becario" in solicitantes[0][person][3] and tipodato.find('apoyovaluebecario') != -1:
                    solicitantes[0][person][5]=f;
                elif "Tecnico Academico" in solicitantes[0][person][3] and tipodato.find('apoyovaluetecnico') != -1:
                    solicitantes[0][person][5]=f;
                elif "Postdoc" in solicitantes[0][person][3] and tipodato.find('apoyovaluepostdoc') != -1:
                    solicitantes[0][person][5]=f;

            folder.setSolicitantes(solicitantes)
        return f

    def hasReqData(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, None)
            f = float(tipo)
            if tipo is None:
                return False
            else:
                return True
        except:
            return False

    def search(self):
        form = self.request.form
        req = self.request

        applications=[]

        mt = self.context.portal_membership
        member=mt.getAuthenticatedMember()

        queryObj=self.queryObj

        try:
            searchStr=self.request.form['Creator']
            unEstado=self.request.form['State']
        except:
            return applications

        if self.context.meta_type == "SolicitudFolder":
            folder=self.context
            for dictionary in queryObj.getCurrentFolderApplications():
                append=False

                meta = dictionary['meta_type']

                #¿Que hice aqui?
                if dictionary['owner_id'].find(searchStr)!=-1 and searchStr is not "":
                    append=True
                    if append and unEstado is not None:
                        if unEstado == "aprobada" and not dictionary['workflow_state']=="aprobada":
                                append=False
                        elif unEstado == "rechazada" and not dictionary['workflow_state']=="rechazada":
                                append=False
                        elif unEstado == "revision" and dictionary['workflow_state']=="aprobada":
                                append=False
                        elif unEstado == "revision" and dictionary['workflow_state']=="rechazada":
                                append=False

                    if append:
                        applications.append(dictionary)

        return applications

    def getProductCreatorsList(self):
        return self.queryObj.getProductCreatorsList()

    def hasReqDataStr(self,tipodato):
        return self.reqObj.hasReqDataStr(tipodato)

    def programaPresupuesto(self):
        """ return true if user has 'Programador de Presupuesto' rol
        """
        mt = getToolByName(self.context, 'portal_membership')
        member=mt.getAuthenticatedMember()
        if 'Programador de Presupuesto' in list(member.getRoles()):
            return True
        return False

    def esSolicitanteAuxiliar(self):
        """ return true if user has 'Solicitante Auxiliar' rol
        """
        mt = getToolByName(self.context, 'portal_membership')
        member=mt.getAuthenticatedMember()
        if 'Solicitante Auxiliar' in list(member.getRoles()):
            return True
        return False

    def getUserApplications(self,user):
        return self.queryObj.getUserApplications(user)

    def getProductUsers(self):
        return self.queryObj.getProductUsers()

    def getUserApplicationsInState(self,user,state):
        applications=[]
        for dictionary in queryObj.getUserApplications(user):
           if dictionary['workflow_state'] == state:
               applications.append(dictionary)
        return applications

    def changeBlockState(self,dictionary):
        folder_path = [i for i in self.context.getPhysicalPath()]
        folder_path.pop()
        folder_path = "/".join(folder_path)
        if dictionary.get('borrador.Enviar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    try:
                        self.context.portal_workflow.doActionFor(solicitud,'enviar')
                    except:
                        self.context.portal_workflow.doActionFor(solicitud,'enviarainvestigador')
                except:
                    pass;
        elif dictionary.get('revision.preeliminar.Enviar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    self.context.portal_workflow.doActionFor(solicitud,'enviar')
                except:
                    pass;
        elif dictionary.get('revision.preeliminar.Regresar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    self.context.portal_workflow.doActionFor(solicitud,'rechazarabecario')
                except:
                    pass;
        elif dictionary.get('revision.comision.PonerFechaComision','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionce(dictionary.get('fechaderevisionCE',''))
                    fdaterev = dictionary.get('fechaderevisionCE','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionce(fdaterev)
                except:
                    pass;
        elif dictionary.get('revision.comision.PonerNumeroActa','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    solicitud.setActace(dictionary.get('numeroDeActaCE',''))
                except:
                    pass;
        elif dictionary.get('revision.comision.PonerActaYFecha','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionce(dictionary.get('fechaderevisionCE',''))
                    fdaterev = dictionary.get('fechaderevisionCE','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionce(fdaterev)
                    solicitud.setActace(dictionary.get('numeroDeActaCE',''))
                except:
                    pass;
        elif dictionary.get('revision.comision.Enviar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    self.context.portal_workflow.doActionFor(solicitud,'enviaraconsejo')
                except:
                    pass;
        elif dictionary.get('revision.comision.PonerFechaComisionYEnviar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionce(dictionary.get('fechaderevisionCE',''))
                    fdaterev = dictionary.get('fechaderevisionCE','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionce(fdaterev)
                    self.context.portal_workflow.doActionFor(solicitud,'enviaraconsejo')
                except:
                    pass;
        elif dictionary.get('revision.consejo.GenerarActa','') is not '':

            boldText = TextPropertySet(bold='bold')
            boldUnderlineText = TextPropertySet(bold='bold',underline='underline')
            smallText = TextPropertySet(size=18)
            alignRight = ParagraphPropertySet(alignment=ParagraphPropertySet.RIGHT)
            alignCenter = ParagraphPropertySet(alignment=ParagraphPropertySet.CENTER)

            DR = Renderer()
            doc = Document()
            ss = doc.StyleSheet
            header = Section()
            licencia = Section()
            licencia.append(Paragraph(ss.ParagraphStyles.Heading2,
                                      Text(self.rtf_repr(u"Licencias"), boldUnderlineText)))
            comision = Section()
            comision.append(Paragraph(ss.ParagraphStyles.Heading2,
                                      Text(self.rtf_repr(u"Comisión"), boldUnderlineText)))
            visitante = Section()
            visitante.append(Paragraph(ss.ParagraphStyles.Heading2,
                                      Text(self.rtf_repr(u"Visitante"), boldUnderlineText)))
            estudiante = Section()
            estudiante.append(Paragraph(ss.ParagraphStyles.Heading2,
                                      Text(self.rtf_repr(u"Estudiante"), boldUnderlineText)))
            signers = Section()

            doc.Sections.append(header)
            doc.Sections.append(licencia)
            doc.Sections.append(comision)
            doc.Sections.append(visitante)
            doc.Sections.append(estudiante)
            doc.Sections.append(signers)

            l=0
            c=0
            v=0
            e=0

            fecha = None

            # Sort applications by submitter name
            parent_id = [k.split('/') for k in dictionary.keys()
                        if 'solicitud' in k]
            sorted_list = [(self.context.aq_inner.aq_parent[parent][id], self.context.aq_inner.aq_parent[parent][id].getNombreOwner()) for parent, id in parent_id]
            sorted_list.sort(key=lambda  x: x[1])
            for solicitud, name in sorted_list:
                tempText= ''
                extraInfo=""
                try:
                    person=self.queryObj.getPersonWrapper(solicitud.getIdOwner())
                    author = unicode(' '.join((person.getSuffix(), person.getFirstName(), person.getMiddleName(), person.getLastName())), 'utf-8')
                    t_objeto = unicode(' '.join(solicitud.getObjetoViaje().splitlines()), 'utf-8')
                    institution_u = unicode(solicitud.getInstitucion(), 'utf-8')
                    city_u = unicode(solicitud.getCiudadPais(), 'utf-8')
                    text_objective = '%s. A realizarse en %s, %s, %s.' % (t_objeto, institution_u, city_u, solicitud.translate(solicitud.getPais()))
                            #t_objeto.encode('utf-8'), solicitud.getInstitucion().encode('utf-8'), solicitud.getCiudadPais().encode('utf-8'), solicitud.translate(solicitud.getPais()).encode('utf-8'))

                    # text_dates = 'Duración %s días, del %s al %s.' % (
                    #         solicitud.getCantidadDeDias(),
                    #         solicitud.getFechaDesde().strftime('%d/%m/%Y'),
                    #         solicitud.getFechaHasta().strftime('%d/%m/%Y'))
                    text_dates = unicode('Duración %s días, del %s al %s.' % (solicitud.getCantidadDeDias(), solicitud.getFechaDesde().strftime('%d/%m/%Y'), solicitud.getFechaHasta().strftime('%d/%m/%Y')), 'utf-8')

                    if solicitud.getTotal() > 0:
                        exp_viaticos = unicode('%s para viáticos' % solicitud.getCantidad_viaticos(), 'utf-8')
                        exp_pasaje = unicode('%s para pasaje' % solicitud.getCantidad_pasaje(), 'utf-8')
                        exp_inscripcion = unicode('%s para inscripción' % solicitud.getCantidad_inscripcion(), 'utf-8')
                        exp_total = unicode('Total: %s' % solicitud.getTotal(), 'utf-8')
                        expenses = 'Solicita %s, %s y %s. %s.' % (exp_viaticos, exp_pasaje, exp_inscripcion, exp_total)
                        if solicitud.getPasaje() == 'si':
                            tipopasaje = unicode(' '.join(solicitud.getTipo_pasaje()), 'utf-8')
                            expenses = 'Solicita %s, %s. Tipo de pasaje %s y %s. %s.' % (exp_viaticos, exp_pasaje, tipopasaje, exp_inscripcion, exp_total)
                        rec_expenses = unicode('Cantidad recomendada: %s.' % solicitud.getCantidadRecomendadaTotal(), 'utf-8')
                        text_expenses = ' '.join((expenses, rec_expenses))

                        ##########################################################################################
                        ##VERSION ORIGINAL
                        # exp_viaticos = u'%s para viáticos' % solicitud.getCantidad_viaticos()
                        # exp_pasaje = u'%s para pasaje' % solicitud.getCantidad_pasaje()
                        # exp_inscripcion = u'%s para inscripción' % solicitud.getCantidad_inscripcion()
                        # exp_total = u'Total: %s' % solicitud.getTotal()
                        # expenses = u'Solicita %s, %s y %s. %s.' % (exp_viaticos, exp_pasaje, exp_inscripcion, exp_total)
                        # if solicitud.getPasaje() == 'si':
                        #     tipopasaje = ' '.join(solicitud.getTipo_pasaje())
                        #     expenses = u'Solicita %s, %s. Tipo de pasaje %s y %s. %s.' % (exp_viaticos, exp_pasaje, tipopasaje, exp_inscripcion, exp_total)
                        # rec_expenses = u'Cantidad recomendada: %s.' % solicitud.getCantidadRecomendadaTotal()
                        # text_expenses = ' '.join((expenses, rec_expenses))
                        ##########################################################################################
                    else:
                        text_expenses = ''
                        # text_expenses = unicode('Erogación: Ninguna.', 'utf-8')

                    text_comments = unicode('Comentario del solicitante: %s.' % solicitud.getComentario_owner(), 'utf-8')
                    text_ccomments = unicode('Comentario de la comisión: %s' % solicitud.getComentario_ce(), 'utf-8')

                    if solicitud.recomiendaAprobar():
                        recomendacion =unicode("RECOMENDACIÓN: APROBAR.", 'utf-8')
                    else:
                        recomendacion =unicode("RECOMENDACIÓN: RECHAZAR.", 'utf-8')

                    if solicitud.meta_type == "Solicitud":
                        if solicitud.getTrabajo() == 'Si':
                            t_titulo = ' '.join(solicitud.getTituloTrabajo().splitlines())
                            #text_talk = 'El trabajo que presentará se titula "%s".' % t_titulo
                            text_talk = unicode('El trabajo que presentará se titula "%s".' % t_titulo, 'utf-8')
                        else:
                            text_talk = unicode('', 'utf-8')
                        tempText = ' '.join([text_objective, text_talk, text_dates, text_expenses])

                        p = Paragraph(ss.ParagraphStyles.Normal)
                        p.append(Text(self.rtf_repr(author),boldText), ' ', self.rtf_repr(tempText))
                        if solicitud.getComentario_owner():
                            p.append(LINE, self.rtf_repr(text_comments))
                        if solicitud.getComentario_ce():
                            p.append(LINE, self.rtf_repr(text_ccomments))
                        if not text_expenses:
                            p.append(LINE, self.rtf_repr(unicode('Erogación: Ninguna.', 'utf-8')))
                        p.append(LINE, Text(self.rtf_repr(recomendacion),boldText))


                        ##########################################################################################
                        ##VERSION ORIGINAL
                        # # p.append(Text(self.rtf_repr(author.decode('utf-8')),boldText), ' ',
                        # #          self.rtf_repr(tempText.decode('utf-8')))
                        # p.append(Text(self.rtf_repr(author.decode('utf-8')),boldText), ' ', self.rtf_repr(tempText.encode('utf-8')))

                        # if solicitud.getComentario_owner():
                        #     #p.append(LINE, self.rtf_repr(text_comments.decode('utf-8')))
                        #     p.append(LINE, self.rtf_repr(text_comments.encode('utf-8')))
                        # if solicitud.getComentario_ce():
                        #     #p.append(LINE, self.rtf_repr(text_ccomments.decode('utf-8')))
                        #     p.append(LINE, self.rtf_repr(text_ccomments.encode('utf-8')))
                        # #p.append(LINE, Text(self.rtf_repr(recomendacion.decode('utf-8')),boldText))
                        # p.append(LINE, Text(self.rtf_repr(recomendacion.encode('utf-8')),boldText))
                        ##########################################################################################

                        if solicitud.getLicenciacomision()=="Licencia":
                            l+=1
                            numeracion = "L%d." % l
                            p.insert(0, numeracion)
                            licencia.append(p)
                        else:
                            c+=1
                            numeracion = "C%d." % c
                            p.insert(0, numeracion)
                            comision.append(p)
                    elif solicitud.meta_type == "SolicitudInstitucional":
                        if solicitud.getTrabajo() == 'Si':
                            t_titulo = ' '.join(solicitud.getTituloTrabajo().splitlines())
                            #text_talk = 'El trabajo que presentara se titula "%s".' % t_titulo
                            text_talk = unicode('El trabajo que presentará se titula "%s".' % t_titulo, 'utf-8')
                        else:
                            text_talk = unicode('', 'utf-8')

                        # Solicitudes institucionales deben desplegar los dos presupuestos.
                        if solicitud.getTotal() > 0:
                            exp_viaticos = unicode('%s para viáticos' % solicitud.getCantidad_viaticos(), 'utf-8')
                            exp_pasaje = unicode('%s para pasaje' % solicitud.getCantidad_pasaje(), 'utf-8')
                            exp_inscripcion = unicode('%s para inscripción' % solicitud.getCantidad_inscripcion(), 'utf-8')
                            expenses = 'Solicita %s, %s y %s.' % (exp_viaticos, exp_pasaje, exp_inscripcion)
                            if solicitud.getPasaje() == 'si':
                                tipopasaje = unicode(' '.join(solicitud.getTipo_pasaje()), 'utf-8')
                                expenses = 'Solicita %s, %s. Tipo de pasaje %s y %s.' % (exp_viaticos, exp_pasaje, tipopasaje, exp_inscripcion)

                            apoyo_viaticos = unicode('%s para viáticos' % solicitud.getCantidad_viaticos_apoyo(), 'utf-8')
                            apoyo_pasaje = unicode('%s para pasaje' % solicitud.getCantidad_pasaje_apoyo(), 'utf-8')
                            apoyo_inscripcion = unicode('%s para inscripción' % solicitud.getCantidad_inscripcion_apoyo(), 'utf-8')
                            exp_total = unicode('Total: %s' % solicitud.getTotal(), 'utf-8')
                            apoyo_expenses = 'Solicita de apoyo institucional %s, %s y %s. %s.' % (apoyo_viaticos, apoyo_pasaje, apoyo_inscripcion, exp_total)
                            if solicitud.getPasaje() == 'si':
                                tipopasaje = unicode(' '.join(solicitud.getTipo_pasaje()), 'utf-8')
                                apoyo_expenses = 'Solicita de apoyo institucional %s, %s. Tipo de pasaje %s y %s. %s.' % (apoyo_viaticos, apoyo_pasaje, tipopasaje, apoyo_inscripcion, exp_total)
                            rec_expenses = unicode('Cantidad recomendada: %s.' % solicitud.getCantidadRecomendadaTotal(), 'utf-8')
                            text_expenses = ' '.join((expenses, apoyo_expenses, rec_expenses))

                        tempText = ' '.join([text_objective, text_talk, text_dates, text_expenses])
                        p = Paragraph( ss.ParagraphStyles.Normal)
                        p.append(Text(self.rtf_repr(author),boldText), ' ', self.rtf_repr(tempText))
                        if solicitud.getComentario_owner():
                            p.append(LINE, self.rtf_repr(text_comments))
                        if solicitud.getComentario_ce():
                            p.append(LINE, self.rtf_repr(text_ccomments))
                        if not text_expenses:
                            p.append(LINE, self.rtf_repr(unicode('Erogación: Ninguna.', 'utf-8')))
                        p.append(LINE, Text(self.rtf_repr(recomendacion),boldText))

                        ##########################################################################################
                        ##VERSION ORIGINAL
                        # # Solicitudes institucionales deben desplegar los dos presupuestos.
                        # if solicitud.getTotal() > 0:
                        #     exp_viaticos = u'%s para viáticos' % solicitud.getCantidad_viaticos()
                        #     exp_pasaje = u'%s para pasaje' % solicitud.getCantidad_pasaje()
                        #     exp_inscripcion = u'%s para inscripción' % solicitud.getCantidad_inscripcion()
                        #     expenses = u'Solicita %s, %s y %s.' % (exp_viaticos, exp_pasaje, exp_inscripcion)
                        #     if solicitud.getPasaje() == 'si':
                        #         tipopasaje = ' '.join(solicitud.getTipo_pasaje())
                        #         expenses = u'Solicita %s, %s. Tipo de pasaje %s y %s.' % (exp_viaticos, exp_pasaje, tipopasaje, exp_inscripcion)

                        #     apoyo_viaticos = u'%s para viáticos' % solicitud.getCantidad_viaticos_apoyo()
                        #     apoyo_pasaje = u'%s para pasaje' % solicitud.getCantidad_pasaje_apoyo()
                        #     apoyo_inscripcion = u'%s para inscripción' % solicitud.getCantidad_inscripcion_apoyo()
                        #     exp_total = u'Total: %s' % solicitud.getTotal()
                        #     apoyo_expenses = u'Solicita de apoyo institucional %s, %s y %s. %s.' % (apoyo_viaticos, apoyo_pasaje, apoyo_inscripcion, exp_total)
                        #     if solicitud.getPasaje() == 'si':
                        #         tipopasaje = ' '.join(solicitud.getTipo_pasaje())
                        #         apoyo_expenses = u'Solicita de apoyo institucional %s, %s. Tipo de pasaje %s y %s. %s.' % (apoyo_viaticos, apoyo_pasaje, tipopasaje, apoyo_inscripcion, exp_total)
                        #     rec_expenses = u'Cantidad recomendada: %s.' % solicitud.getCantidadRecomendadaTotal()
                        #     text_expenses = ' '.join((expenses, apoyo_expenses, rec_expenses))

                        # tempText = ' '.join([text_objective, text_talk, text_dates, text_expenses])
                        # p = Paragraph( ss.ParagraphStyles.Normal)
                        # p.append(Text(self.rtf_repr(author.decode('utf-8')),boldText), ' ',
                        #          self.rtf_repr(tempText.decode('utf-8')))
                        # if solicitud.getComentario_owner():
                        #     p.append(LINE, self.rtf_repr(text_comments.decode('utf-8')))
                        # if solicitud.getComentario_ce():
                        #     p.append(LINE, self.rtf_repr(text_ccomments.decode('utf-8')))
                        # p.append(LINE, Text(self.rtf_repr(recomendacion.decode('utf-8')),boldText))
                        ##########################################################################################

                        if solicitud.getLicenciacomision()=="Licencia":
                            l+=1
                            numeracion = "L%d." % l
                            p.insert(0, numeracion)
                            licencia.append(p)
                        else:
                            c+=1
                            numeracion = "C%d." % c
                            p.insert(0, numeracion)
                            comision.append(p)
                    elif solicitud.meta_type == "SolicitudVisitante":
                        v+=1
                        numeracion = unicode("V%d. " % v, 'utf-8')
                        guest = unicode(solicitud.getNombreInvitado(), 'utf-8')
                        semblanza = unicode(solicitud.getSemblanza(), 'utf-8')
                        #text_place = unicode('de la %s, %s.' % (solicitud.getInstitucion(), solicitud.getPais()), 'utf-8')
                        text_place = 'de la %s, %s.' % (
                            unicode(solicitud.getInstitucion(), 'utf-8'),
                            solicitud.translate(solicitud.getPais())
                        )

                        travel_obj_u = unicode(solicitud.getObjetoViaje(), 'utf-8')
                        tempText = ' '.join([' para', travel_obj_u, text_dates, text_expenses])
                        p = Paragraph( ss.ParagraphStyles.Normal)

                        p.append(self.rtf_repr(numeracion),
                                 Text(self.rtf_repr(guest), boldText), ' ',
                                 self.rtf_repr(text_place), ' Invitado de: ',
                                 Text(self.rtf_repr(author), boldText),
                                 self.rtf_repr(tempText))
                        p.append(LINE, self.rtf_repr(semblanza))
                        if solicitud.getComentario_owner():
                            p.append(LINE, self.rtf_repr(text_comments))
                        if solicitud.getComentario_ce():
                            p.append(LINE, self.rtf_repr(text_ccomments))
                        if not text_expenses:
                            p.append(LINE, self.rtf_repr(unicode('Erogación: Ninguna.', 'utf-8')))
                        p.append(LINE, Text(self.rtf_repr(recomendacion),boldText))
                        visitante.append(p)

                        ##########################################################################################
                        ##VERSION ORIGINAL
                        # v+=1
                        # numeracion = "V%d. " % v
                        # guest = solicitud.getNombreInvitado()
                        # semblanza = solicitud.getSemblanza()
                        # text_place = 'de la %s, %s.' % (solicitud.getInstitucion(), solicitud.getPais())
                        # tempText = ' '.join([' para', solicitud.getObjetoViaje(), text_dates, text_expenses])
                        # p = Paragraph( ss.ParagraphStyles.Normal)
                        # p.append(self.rtf_repr(numeracion.decode('utf-8')),
                        #          Text(self.rtf_repr(guest.decode('utf-8')), boldText), ' ',
                        #          self.rtf_repr(text_place.decode('utf-8')), ' Invitado de: ',
                        #          Text(self.rtf_repr(author.decode('utf-8')), boldText),
                        #          self.rtf_repr(tempText.decode('utf-8')))
                        # p.append(LINE, self.rtf_repr(semblanza.decode('utf-8')))
                        # if solicitud.getComentario_owner():
                        #     p.append(LINE, self.rtf_repr(text_comments.decode('utf-8')))
                        # if solicitud.getComentario_ce():
                        #     p.append(LINE, self.rtf_repr(text_ccomments.decode('utf-8')))
                        # p.append(LINE, Text(self.rtf_repr(recomendacion.decode('utf-8')),boldText))
                        # visitante.append(p)
                        ##########################################################################################
                    else:
                        e+=1
                        if solicitud.getTrabajo() == 'Si':
                            text_talk = unicode('El trabajo que presentará se titula "%s".' % solicitud.getTituloTrabajo(), 'utf-8')
                        else:
                            text_talk = unicode('', 'utf-8')
                        numeracion = unicode('E%d. ' % e, 'utf-8')
                        tempText = ' '.join([text_objective, text_talk, text_dates, text_expenses])
                        p = Paragraph( ss.ParagraphStyles.Normal)
                        p.append(self.rtf_repr(numeracion),
                                 Text(self.rtf_repr(author),boldText), ' Asesor: ',
                                 Text(self.rtf_repr(solicitud.getNombreAsesor()),boldText),
                                 self.rtf_repr(tempText))
                        if solicitud.getComentario_owner():
                            p.append(LINE, self.rtf_repr(text_comments))
                        if solicitud.getComentario_ce():
                            p.append(LINE, self.rtf_repr(text_ccomments))
                        apoyo_comments = unicode('Comentario de apoyo extra: %s' % solicitud.getApoyo_texto(), 'utf-8')
                        p.append(LINE, self.rtf_repr(apoyo_comments))
                        if not text_expenses:
                            p.append(LINE, self.rtf_repr(unicode('Erogación: Ninguna.', 'utf-8')))
                        p.append(LINE, Text(self.rtf_repr(recomendacion),boldText))
                        estudiante.append(p)

                        ##########################################################################################
                        ##VERSION ORIGINAL
                        # e+=1
                        # if solicitud.getTrabajo() == 'Si':
                        #     text_talk = 'El trabajo que presentara se titula "%s".' % solicitud.getTituloTrabajo()
                        # else:
                        #     text_talk = ''
                        # numeracion = 'E%d. ' % e
                        # tempText = ' '.join([text_objective, text_talk, text_dates, text_expenses])
                        # p = Paragraph( ss.ParagraphStyles.Normal)
                        # p.append(self.rtf_repr(numeracion.decode('utf-8')),
                        #          Text(self.rtf_repr(author.decode('utf-8')),boldText), ' Asesor: ',
                        #          Text(self.rtf_repr(solicitud.getNombreAsesor().decode('utf-8')),boldText),
                        #          self.rtf_repr(tempText.decode('utf-8')))
                        # apoyo_comments = u'Comentario de apoyo extra: %s' % solicitud.getApoyo_texto()
                        # p.append(LINE, self.rtf_repr(apoyo_comments.decode('utf-8')))
                        # if solicitud.getComentario_owner():
                        #     p.append(LINE, self.rtf_repr(text_comments.decode('utf-8')))
                        # if solicitud.getComentario_ce():
                        #     p.append(LINE, self.rtf_repr(text_ccomments.decode('utf-8')))
                        # p.append(LINE, Text(self.rtf_repr(recomendacion.decode('utf-8')),boldText))
                        # estudiante.append(p)
                        ##########################################################################################

                    if fecha is None:
                        fecha=solicitud.getFecha_sesionce().strftime('%d/%m/%Y')
                        #fecha='25/11/2013'
                except Exception, excep:
                    print excep
                    pass;

            reunionDate="REUNION xx-xx"
            mainHeader="RECOMENDACIONES DE LA COMISION ESPECIAL DEL CONSEJO INTERNO ENCARGADA DE LAS SOLICITUDES DE VIATICOS Y PASAJES QUE SERAN PRESENTADAS AL CONSEJO INTERNO EN SU SESION DEL "
            mainHeader+=str(fecha)
            subHeader="Fueron estudiadas las siguientes solicitudes:"

            p = Paragraph( ss.ParagraphStyles.Heading2, alignRight)
            p.append(self.rtf_repr(reunionDate))
            header.append(p)

            p = Paragraph( ss.ParagraphStyles.Heading2)
            p.append(self.rtf_repr(mainHeader))
            header.append(p)

            p = Paragraph( ss.ParagraphStyles.Heading2)
            p.append(self.rtf_repr(subHeader))
            header.append(p)

            generationDate="Cd. Universitaria, a _ de _ de 2016"
            #This source insert/delete the comisations
            # signersTitle="LA COMISION ESPECIAL"
            # signersNames=""

            # p = Paragraph( ss.ParagraphStyles.Heading2,alignCenter)
            # p.append(self.rtf_repr(generationDate))
            # signers.append(p)

            # p = Paragraph( ss.ParagraphStyles.Heading2,alignCenter)
            # p.append(self.rtf_repr(signersNames))
            # signers.append(p)

            # comisionados=self.queryObj.getMiembrosComision()

            # for comisionado in comisionados.keys():
            #     p = Paragraph( ss.ParagraphStyles.Normal)
            #     p.append(Text(self.rtf_repr(unicode(comisionados[comisionado][0], 'utf-8')),boldText))
            #     signers.append(p)

            p = Paragraph( ss.ParagraphStyles.Normal)
            p.append(Text(self.rtf_repr("SRG/gcv*"),smallText))
            signers.append(p)

            acta = 'attachment; filename=%s.rtf' % (self.context.id)
            self.request.response.setHeader('Content-Type','application/rtf;charset=utf-8')
            self.request.response.setHeader("Content-Transfer-Encoding", "8bit")
            self.request.response.setHeader('Content-Disposition',acta)

            DR.Write(doc,self.request.response)

        elif dictionary.get('revision.consejo.PonerFechaConsejo','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                except:
                    pass;
        elif dictionary.get('revision.consejo.PonerNumeroActa','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                except:
                    pass;
        elif dictionary.get('revision.consejo.PonerActaYFecha','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                except:
                    pass;
        elif dictionary.get('revision.consejo.PonerActaYFechaYAprobar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                    self.context.portal_workflow.doActionFor(solicitud,'aprobar')
                except:
                    pass;
        elif dictionary.get('revision.consejo.PonerActaYFechaYRechazar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                    self.context.portal_workflow.doActionFor(solicitud,'rechazar')
                except:
                    pass;
        elif dictionary.get('aprobadas.consejo.PonerFechaConsejo','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                except:
                    pass;
            return self.folderaprobadas()
        elif dictionary.get('aprobadas.consejo.PonerNumeroActa','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                except:
                    pass;
            return self.folderaprobadas()
        elif dictionary.get('aprobadas.consejo.PonerActaYFecha','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                except:
                    pass;
            return self.folderaprobadas()
        elif dictionary.get('rechazadas.consejo.PonerFechaConsejo','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                except:
                    pass;
            return self.folderrechazadas()
        elif dictionary.get('rechazadas.consejo.PonerNumeroActa','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                except:
                    pass;
            return self.folderrechazadas()
        elif dictionary.get('rechazadas.consejo.PonerActaYFecha','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    # solicitud.setFecha_sesionci(dictionary.get('fechaderevisionCI',''))
                    fdaterev = dictionary.get('fechaderevisionCI','')
                    if fdaterev:
                        val_fdaterev = fdaterev.split('/')
                        fdaterev = '/'.join([val_fdaterev[2], val_fdaterev[1], val_fdaterev[0]])
                    solicitud.setFecha_sesionci(fdaterev)
                    solicitud.setActaci(dictionary.get('numeroDeActaCI',''))
                except:
                    pass;
            return self.folderrechazadas()
        elif dictionary.get('revision.consejo.Aprobar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    self.context.portal_workflow.doActionFor(solicitud,'aprobar')
                except:
                    pass;
        elif dictionary.get('revision.consejo.Rechazar','') is not '':
            for key in dictionary:
                object_path=folder_path+"/"+key
                try:
                    solicitud=self.context.portal_catalog(path=object_path)[0].getObject()
                    self.context.portal_workflow.doActionFor(solicitud,'rechazar')
                except:
                    pass;
        else:
            return self.menu()

        return self.folderpendientes()

    # ver http://www.zopatista.com/python/2012/06/06/rtf-and-unicode/
    def rtf_repr(self, s):
        """ escape certain classes of characters to RTF command codes """
        _charescape = re.compile(u'([\x00-\x1f\\\\{}\x80-\uffff])')
        return _charescape.sub(self._encode_unicode, s).encode('ascii')

    def _encode_unicode(self, match):
        codepoint = ord(match.group(1))
        return '\\u%s?' % (codepoint < 32768 and codepoint or codepoint - 65536)

    def getStyles(self, items):

        extra_data = {}
        folder = self.context
        catalog = folder.portal_catalog
        for item in items:
            solicitud = {}
            folder = item['parent_folder']
            usuarioActual = item['owner_id']
            cantidadAsignada = folder.getPresupuesto_asignado_solicitantes()[0].get(usuarioActual, 0.0)
            cantidadInicial = folder.getSolicitantes()[0].get(usuarioActual, [0, 0, 0, 0, 0.0])[4]
            cantidadInicialApoyos = folder.getSolicitantes()[0].get(usuarioActual, [0, 0, 0, 0, 0.0])[5]
            resto = cantidadInicial - cantidadAsignada
            solicitud['resto'] = resto
            solicitud['dcomision'] = folder.getDias_comision_utilizados_solicitantes()[0].get(usuarioActual, 0.0)
            solicitud['dlicencia'] = folder.getDias_licencia_utilizados_solicitantes()[0].get(usuarioActual, 0.0)
            solicitud['apoyo'] = cantidadInicialApoyos-folder.getApoyoinst_asignado_solicitantes()[0].get(usuarioActual, 0.0)
            solicitud['style-days'] = ""
            solicitud['style-days-text'] = item['quantity_of_days']
            solicitud['style-quantity'] = ""
            solicitud['style-quantity-text'] = []
            solicitud['style-country'] = ""
            solicitud['style-country-text'] = ""
            solicitud['style-overlap'] = ""
            solicitud['style-overlap-text'] = ""

            if item['meta_type'] in ['Solicitud', 'SolicitudInstitucional']:
                if item['special_fields']['type'] == 'Licencia':
                    if item['quantity_of_days'] > 45 - solicitud['dlicencia']:
                        solicitud['style-days'] = "background:#FFCC00;"
                        text = 'Solicita %s  días de Licencia y dispone de %s \n'%(item['quantity_of_days'], 45 - solicitud['dlicencia'])
                        solicitud['style-days-text'] = text

                # # comission type
                # else:
                #     if item['quantity_of_days'] > 45 - solicitud['dcomision']:
                #         solicitud['style-days'] = "background:#FFCC00;"
                #         text = 'Solicita %s días de Comisión y dispone de %s \n'%(item['quantity_of_days'], 45 - solicitud['dcomision'])
                #         solicitud['style-days-text'] = text

            institutional_budget = item['institutional_budget']['transport_expenses'] + item['institutional_budget']['registration_expenses'] + item['institutional_budget']['food_expenses']
            if item['meta_type'] != 'SolicitudBecario':
                if institutional_budget > solicitud['apoyo'] and institutional_budget > 0.0:
                    solicitud['style-quantity'] = "color: #FFFFFF; background:#FF0000;"
                    text = 'Solicita de apoyo institucional %.2f y dispone de %.2f \n'%(institutional_budget, solicitud['apoyo'])
                    solicitud['style-quantity-text'].append(text)

                annual_budget = item['annual_budget']['transport_expenses'] + item['annual_budget']['registration_expenses'] + item['annual_budget']['food_expenses']
                if annual_budget > solicitud['resto'] and annual_budget > 0.0:
                    solicitud['style-quantity'] = "color: #FFFFFF; background:#FF0000;"
                    text = 'Solicita de asignación anual %.2f y dispone de %.2f \n'%(annual_budget, solicitud['resto'])
                    solicitud['style-quantity-text'].append(text)

            # if item['meta_type'] == 'SolicitudBecario':
            else:
                if item['country_code'][0] != 'MX':
                    user_level = catalog(portal_type='FSDPerson', id=usuarioActual)[0].getObject().student_education_level
                    if user_level == 'bachelor':
                        # if item['country_code'][0] != 'MX':
                        text = "No puede solicitar salida al extranjero"
                        solicitud['style-country'] = "color: #FFFFFF; background:#006600;"
                        solicitud['style-country-text'] = text

                    else:
                        user_aprobadas = catalog(portal_type="SolicitudBecario", Creator=usuarioActual, review_state='aprobada')
                        country_bylevel = {'Doctorado': [], 'Maestria': []}
                        solicitudesbylevel = {'Doctorado': [], 'Maestria': []}
                        for sol in user_aprobadas:
                            obj = sol.getObject()
                            if obj.getPais() != 'Mexico':
                                country_bylevel[obj.getGrado()].append(obj.getPais())
                                solicitudesbylevel[obj.getGrado()].append(sol)

                        unique_countries = {}
                        for k, v in country_bylevel.iteritems():
                            unique_countries[k] = list(set(v))

                        if user_level == 'phd' and len(unique_countries['Doctorado']) > 0:
                            text = "Ya solicitó salida al extranjero"
                            solicitud['style-country'] = "color: #FFFFFF; background:#006600;"
                            solicitud['style-country-text'] = "%s <a style=\"color: #000000\" href=%s> ver solicitud </a>"%(text,solicitudesbylevel['Doctorado'][0].getURL())
                        if user_level == 'master' and len(unique_countries['Maestria']) > 0:
                            text = "Ya solicitó salida al extranjero"
                            solicitud['style-country'] = "color: #FFFFFF; background:#006600;"
                            solicitud['style-country-text'] = "%s <a style=\"color: #000000\" href=%s> ver solicitud </a>"%(text,solicitudesbylevel['Maestria'][0].getURL())

            if item['meta_type'] != 'SolicitudVisitante':
                sol = catalog(id=item['id'])
                date1 = sol[0].fecha_desde
                date2 = sol[0].fecha_hasta
                overlap_sol = catalog(
                    portal_type=('Solicitud','SolicitudBecario', 'SolicitudInstitucional'),
                    Creator=usuarioActual,
                    review_state=['aprobada', 'revisioncomision', 'revisionconsejo'],
                    fecha_desde={'query': date2, 'range': 'max'},
                    fecha_hasta={'query': date1, 'range': 'min'}
                )
                effective_sol = []
                for sol in overlap_sol:
                    if sol.id != item['id']:
                        effective_sol.append(sol)
                # if len(overlap_sol) > 0:
                if len(effective_sol) > 0:
                    text = 'Tiene otra salida para esas fechas'
                    solicitud['style-overlap'] = "color: #FFFFFF; background:#0066FF;"
                    solicitud['style-overlap-text'] = "%s <a style=\"color: #000000\" href=%s> ver solicitud </a>"%(text,effective_sol[0].getURL())

            extra_data[item['id']] = solicitud

        return extra_data

    def getCampus(self):
        return ['C.U.', 'Cuernavaca', 'Juriquilla', 'Oaxaca', 'Morelia']
