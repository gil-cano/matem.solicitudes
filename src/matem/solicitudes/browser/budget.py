# -*- coding: utf-8 -*-

from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from matem.solicitudes.browser.folder import SolicitudFolderView
from matem.solicitudes.browser.queries import Queries
from matem.solicitudes.config import DICCIONARIO_AREAS
from matem.solicitudes.extender import PersonWrapper
from matem.solicitudes.interfaces import ISolicitudFolder
from operator import itemgetter

import datetime
import sys


class BudgetView(BrowserView):
    """The budget view"""

    template = ViewPageTemplateFile('presupuesto.pt')
    solicitantes = None
    queryObj = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.queryObj = Queries(self.context, self.request)

    def __call__(self):
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()

        self.queryObj = Queries(self.context, self.request)

        if 'Programador de Presupuesto' in list(member.getRoles()):
            return self.template()
        else:
            return self.context()

    def programaPresupuesto(self):
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()
        users = []

        if 'Programador de Presupuesto' in list(member.getRoles()):
            return True
        else:
            return False

    def esSolicitanteAuxiliar(self):
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()
        users = []

        if 'Solicitante Auxiliar' in list(member.getRoles()):
            return True
        else:
            return False

    def hasReqData(self, tipodato):
        try:
            req = self.request
            tipo = req.get(tipodato, None)
            f = float(tipo)
            if tipo is None:
                return False
            else:
                return True
        except:
            return False

    def hasReqDataStr(self, tipodato):
        try:
            req = self.request
            tipo = req.get(tipodato, '')
            if tipo is None:
                return False
            else:
                return True
        except:
            return False

    def getPage(self, tipodato):
        try:
            req = self.request
            tipo = req.get(tipodato, '')
            f = int(tipo)
            if tipo is None:
                return 0
            else:
                return f
        except:
            return 0

    def getReqDataStr(self, tipodato):
        try:
            req = self.request
            tipo = req.get(tipodato, '')
            if tipo is None:
                return None
            else:
                return tipo
        except:
            return None

    def getCantidadAsignadaTotal(self, usuarioActual):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        users = []
        suma = 0.0
        inicial = 0.0

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    suma = suma + folder.getPresupuesto_asignado()
                    inicial = inicial + folder.getPresupuesto_inicial()

            users.append(["Presupuesto maximo total (todos los periodos)", inicial])
            users.append(["Presupuesto ejercido en todos los periodos", suma])
            users.append(["Presupuesto restante", inicial - suma])

            return users
        except:
            return []

    def getFolders(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders = []

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    folders.append([folder.getId(), str(folder.getFecha_desde()), str(folder.getFecha_hasta()), folder.getPresupuesto_inicial(), folder.getPresupuesto_asignado(), folder.absolute_url()])
            return folders
        except:
            return []

    def getTotalBudget(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        cantidadTotal = 0.0

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    cantidadTotal += folder.getPresupuesto_inicial()
        except:
            return -1.0

        return cantidadTotal

    def recalcular(self):
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    folder.actualizarPeriodo()
        except:
            return False

        return True

    def actualizar(self, userID, newBudget):
        user = self.queryObj.getPersonWrapper(userID)
        nuevo = float(newBudget)
        user.setPresupuesto_inicial(nuevo)
        return True

    def getIndividualBudgetsPerson(self):
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()
        append = False
        rol = ""
        fsd_tool = self.context.facultystaffdirectory_tool
        users = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

        if 'Programador de Presupuesto' in list(member.getRoles()):
            for person in list(fsd_tool.getDirectoryRoot().getSortedPeople()):
                fsdperson = PersonWrapper(person)
                letter = unicode(fsdperson.getLastName())[0].upper()
                letter = letter.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('Ñ', 'N').replace('Ö', 'O')
                user = mt.getMemberById(fsdperson.getId())

                if 'Investigador' in list(user.getRoles()):
                    rol = "Investigador"
                    append = True
                elif 'Postdoc' in list(user.getRoles()):
                    rol = "Postdoc"
                    append = True
                elif 'Tecnico Academico' in list(user.getRoles()):
                    rol = "Tecnico Academico"
                    append = True
                elif 'Becario' in list(user.getRoles()):
                    rol = "Becario"
                    append = True

                if append :
                    users[letter].append([fsdperson.getId(), fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName(), fsdperson.getPresupuesto_inicial()])

                    append = False
        return users

    def getIndividualBudgets(self):
        mt = self.context.portal_membership
        member = mt.getAuthenticatedMember()
        rol = ""
        users = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

        if 'Programador de Presupuesto' in list(member.getRoles()):
            llaves = self.solicitantes.keys()
            for person in llaves:
                personinfo = self.solicitantes[person]
                letter = unicode(personinfo[0])[0].upper()
                letter = letter.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('Ñ', 'N').replace('Ö', 'O')
                users[letter].append([personinfo[0] + ", " + personinfo[1] + " " + personinfo[2],
                          personinfo[3],
                          person])

            for letter in users.keys():
                users[letter].sort()

        return users

    def getAlphabetLetters(self):
        users = {'A': {}, 'B': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}, 'G': {}, 'H': {}, 'I': {}, 'J': {}, 'K': {}, 'L': {}, 'M': {}, 'N': {}, 'O': {}, 'P': {}, 'Q': {}, 'R': {}, 'S': {}, 'T': {}, 'U': {}, 'V': {}, 'W': {}, 'X': {}, 'Y': {}, 'Z': {}}
        result = users.keys()
        result.sort()
        return result

    def getPageAlphabetic(self, tipodato):
        try:
            req = self.request
            tipo = req.get(tipodato, '')
            if str(tipo) != '':
                return str(tipo)
            else:
                return 'A'
        except:
            return 'A'

    def getPageAlphabeticNumber(self, tipodato):
        try:
            alphabet = self.getAlphabetLetters()
            req = self.request
            tipo = req.get(tipodato, '')
            for x in range(0, len(alphabet)):
                if alphabet[x] is str(tipo):
                    return x
                else:
                    return 0
        except:
            return 0

    def getBudgetInvestigador(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders = []

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    return folder.getPresupuesto_maximo_investigadores()
        except:
            return 0.0

    def getBudgetBecario(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders = []

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    return folder.getPresupuesto_maximo_becarios()
        except:
            return 0.0

    def getBudgetTecnico(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders = []

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    return folder.getPresupuesto_maximo_tecnicos()
        except:
            return 0.0

    def getBudgetPostdoc(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders = []

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    return folder.getPresupuesto_maximo_postdocs()
        except:
            return 0.0

    def setBudget(self, tipodato):
        mt = self.context.portal_membership
        fsd_tool = self.context.facultystaffdirectory_tool
        member = mt.getAuthenticatedMember()
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders = []

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()
                if not folder.historico():
                    folders.append(folder)
        except:
            pass

        f = 0.0

        try:
            if tipodato.find('investigador') != -1:
                viejo = float(folders[0].getPresupuesto_maximo_investigadores())
            elif tipodato.find('becario') != -1:
                viejo = float(folders[0].getPresupuesto_maximo_becarios())
            elif tipodato.find('tecnico') != -1:
                viejo = float(folders[0].getPresupuesto_maximo_tecnicos())
            elif tipodato.find('postdoc') != -1:
                viejo = float(folders[0].getPresupuesto_maximo_postdocs())
            else:
                viejo = 0.0
            req = self.request
            tipo = req.get(tipodato, '')
            if tipo is None:
                return viejo
            else:
                f = float(tipo)
                if f < 0:
                    return viejo
        except:
            return -1

        if 'Programador de Presupuesto' in list(member.getRoles()):
            if tipodato.find('investigador') != -1:
                for folder in folders:
                    folder.setPresupuesto_maximo_investigadores(f)
            elif tipodato.find('becario') != -1:
                for folder in folders:
                    folder.setPresupuesto_maximo_becarios(f)
            elif tipodato.find('tecnico') != -1:
                for folder in folders:
                    folder.setPresupuesto_maximo_tecnicos(f)
            elif tipodato.find('postdoc') != -1:
                for folder in folders:
                    folder.setPresupuesto_maximo_postdocs(f)

            for fsdperson in list(fsd_tool.getDirectoryRoot().getSortedPeople()):
                user = mt.getMemberById(fsdperson.getId())

                if "Investigador" in list(user.getRoles()) and tipodato.find('investigador') != -1:
                    PersonWrapper(fsdperson).setPresupuesto_inicial(f)
                elif "Becario" in list(user.getRoles()) and tipodato.find('becario') != -1:
                    PersonWrapper(fsdperson).setPresupuesto_inicial(f)
                elif "Tecnico Academico" in list(user.getRoles()) and tipodato.find('tecnico') != -1:
                    PersonWrapper(fsdperson).setPresupuesto_inicial(f)
                elif "Postdoc" in list(user.getRoles()) and tipodato.find('postdoc') != -1:
                    PersonWrapper(fsdperson).setPresupuesto_inicial(f)

        return f

    def registrarSolicitudesEnPersonas(self):
        mt = self.context.portal_membership
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        personas = {}

        try:
            for brain in results:
                start = brain.start
                url = brain.getURL()
                folder = brain.getObject()

                prefix = str(folder.getId())
                for solicitud in folder.objectValues():

                    if personas.get(solicitud.getIdOwner(), None) is None:
                        personas[solicitud.getIdOwner()] = []

                    reference = prefix + ";" + str(solicitud.getId())

                    personas[solicitud.getIdOwner].append(reference)

            for personId in personas.keys():
                persona = self.queryObj(personId)
                persona.setSolicitudes_creadas(tuple(personas[personId]))

        except:
            print "Error al registrar solicitudes en personas"
            return False

        return True

    def getSolicitantes(self):
        fsd_tool = getToolByName(self, "facultystaffdirectory_tool")
        mt = getToolByName(self, "portal_membership")
        member = mt.getAuthenticatedMember()
        dictSolicitantes = {}
        append = False

        if 'Programador de Presupuesto' in list(member.getRoles()):
            print "Cargando lista de solicitantes en presupuesto global..."
            try:
                solicitantes = list(fsd_tool.getDirectoryRoot().getSortedPeople())

                for person in solicitantes:
                    fsdperson = PersonWrapper(person)
                    user = mt.getMemberById(person.getId())

                    if 'Investigador' in list(user.getRoles()):
                        rol = "Investigador"
                        append = True
                    elif 'Postdoc' in list(user.getRoles()):
                        rol = "Postdoc"
                        append = True
                    elif 'Tecnico Academico' in list(user.getRoles()):
                        rol = "Tecnico Academico"
                        append = True
                    elif 'Becario' in list(user.getRoles()):
                        rol = "Becario"
                        append = True

                    if append:
                        dictSolicitantes[person.getId()] = [
                                fsdperson.getLastName(),
                                fsdperson.getFirstName(),
                                fsdperson.getMiddleName(),
                                fsdperson.getPresupuesto_inicial()]
                    append = False
            except:
                print "Error encontrando solicitantes en vista de presupuesto global."
                return {}
        print str(len(dictSolicitantes)) + " cargados."
        return dictSolicitantes
