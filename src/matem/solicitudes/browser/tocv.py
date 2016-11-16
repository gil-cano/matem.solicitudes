# -*- coding: utf-8 -*-

from matem.solicitudes.content.solicitud import Solicitud
from matem.solicitudes.content.solicitudvisitante import SolicitudVisitante
from plone import api
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import ObjectEditedEvent
from unidecode import unidecode
from z3c.form import button
from z3c.form import form
from zope import event

import logging


class ApplicationstoCVForm(form.Form):
    """docstring for ApplicationstoCVForm"""

    @button.buttonAndHandler(u'Dump applications to cv')
    def dump_to_cv(self, action):
        """Create cv items form applications"""
        logging.info('Dumpping applications')
        folder = api.content.get(
            path='/servicios/servicios-internos/solicitudes/2016')
        catalog = api.portal.get_tool('portal_catalog')
        # 'Solicitud', 'SolicitudInstitucional', 'SolicitudVisitante'
        brains = catalog(
            path={'query': '/'.join(folder.getPhysicalPath()), 'depth': 1},
            review_state='aprobada',
            portal_type=('Solicitud'),
            sort_on='created')
        for brain in brains:
            # test for applications in old format
            aux_folder = api.content.get(
                path='/servicios/servicios-internos/solicitudes/2006')
            application = brain.getObject()
            userid = application.getIdOwner()
            if brain.id in aux_folder:
                application = aux_folder[brain.id]
            # prides = ['rajsbaum', 'folchgab', 'dolivero', 'flopez', 'geronimo', 'adolfo', 'acano', 'omendoza']
            # # prides = ['rajsbaum', ]
            # if userid not in prides:
            #     continue
            if isinstance(application, Solicitud):
                self.app2cv(application, userid)
            # if isinstance(application, SolicitudVisitante):
            #     self.app2cv_guest(application, userid)

        logging.info('Done')

    def get_folder(self, userid, content_type, metacv=True):
        """Get cvitem folder inside the metacv or the user CVFolder"""
        ctype = content_type.lower()
        path = '/catalogos/meta-cv/{ctype}folder'.format(ctype=ctype)
        if not metacv:
            path = '/fsd/{id}/cv/{ctype}folder'.format(id=userid, ctype=ctype)
        return api.content.get(path=path)

    def app2cv(self, application, userid):
        """Splits an application in cvitems."""
        # assistance
        if application.assistance:
            self.app2cv_assistance(application, userid)
        # conferences
        if application.conferences:
            self.app2cv_conference(application, userid)
        # courses
        if application.courses:
            self.app2cv_courses(application, userid)
        # sresearch
        if application.sresearch:
            self.app2cv_research(application, userid)
        # organization
        if application.organization:
            self.app2cv_organization(application, userid)

    def app2cv_assistance(self, application, userid):
        logging.info('Asistencia: {0} - {1}'.format(application.id, userid))
        content_type = 'CVEvent'
        folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.assistance):
            pre = 'se-{0}'.format(i)
            id = application.id.replace('solicitud', pre)
            date = item['assistancedate'].split('/')
            begin_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            institution =  self.lookupInstitution(item['institution'])
            otherinstitution = ''
            if institution is None:
                otherinstitution = item['institution']
            fields = {
                'event_date': begin_date,
                'numberOfDays': application.getCantidadDeDias(),
                'audienceType': u'assistant',
                'where': u'institution',
                'institutionCountry': application.pais[0],
                'institution': institution,
                'otherinstitution': otherinstitution,
                'creators': ([userid, 'admin'])}
            obj = api.content.create(
                type=content_type,
                id=id,
                title=item['eventName'],
                container=folder,
                **fields)
            # {'othereventtype': '',
            # 'eventtype': 'seminary',
            # 'eventName': 'Seminario Iterino del grupo de Representaciones de Algebras',
            # 'assistancedate': '25/02/2016',
            # 'place': 'Guanajuato, M\xc3\xa9xico',
            # 'institution': 'Centro de Investigaci\xc3\xb3n en Matem\xc3\xa1ticas (CIMAT)'}

    def app2cv_conference(self, application, userid):
        logging.info('Conferencia: {0} - {1}'.format(application.id, userid))
        content_type = 'CVConference'
        folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.conferences):
            pre = 'sconf-{0}'.format(i)
            id = application.id.replace('solicitud', pre)
            fields = {
                'creators': ([userid, 'admin'])}
            # obj = api.content.create(
            #     type=content_type,
            #     id=id,
            #     title=item[''],
            #     container=folder,
            #     **fields)
            # ({'conferencedate': '10/01/2016',
            # 'conferencetype': ['research'],
            # 'title': 'Algebraic differential equations with single-valued solutions',
            # 'eventtype': 'congress',
            # 'participationtype': 'invitation',
            # 'eventName': 'Geometric Aspects of Modern Dynamics',
            # 'place': 'Oporto, Portugal',
            # 'isplenary': 'no',
            # 'institution': 'Universidad de Porto'},)

    def app2cv_courses(self, application, userid):
        logging.info('Curso: {0} - {1}'.format(application.id, userid))
        content_type = 'CVCourse'
        folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.courses):
            pre = 'sc-{0}'.format(i)
            id = application.id.replace('solicitud', pre)

            fields = {
                'creators': ([userid, 'admin'])}
            # obj = api.content.create(
            #     type=content_type,
            #     id=id,
            #     title=item[''],
            #     container=folder,
            #     **fields)
            # ({'objective': 'Trabajar en nuestro proyecto de investigacion acerca de Distributed Fault-tolerant Checkability apoyado por CONACYT-ECOS-NORD',
            # 'hostresearcher': '',
            # 'sresearchinitdate': '20/02/2016',
            # 'institution': 'Universit\xc3\xa9 Paris Diderot - Paris 7',
            # 'sresearchenddate': '29/02/2016'},)

    def app2cv_research(self, application, userid):
        logging.info('Estancias de Inv: {0} - {1}'.format(application.id, userid))
        content_type = 'CVVisit'
        folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.sresearch):
            pre = 'sv-{0}'.format(i)
            id = application.id.replace('solicitud', pre)

            fields = {
                'creators': ([userid, 'admin'])}
            # obj = api.content.create(
            #     type=content_type,
            #     id=id,
            #     title=item[''],
            #     container=folder,
            #     **fields)
            # ({'objective': 'Trabajar en nuestro proyecto de investigacion acerca de Distributed Fault-tolerant Checkability apoyado por CONACYT-ECOS-NORD',
            # 'hostresearcher': '',
            # 'sresearchinitdate': '20/02/2016',
            # 'institution': 'Universit\xc3\xa9 Paris Diderot - Paris 7',
            # 'sresearchenddate': '29/02/2016'},)

    def app2cv_organization(self, application, userid):
        logging.info('Organizador: {0} - {1}'.format(application.id, userid))
        content_type = 'CVEventOrg'
        folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.organization):
            pre = 'se-{0}'.format(i)
            id = application.id.replace('solicitud', pre)
            fields = {
                'creators': ([userid, 'admin'])}
            # obj = api.content.create(
            #     type=content_type,
            #     id=id,
            #     title=item[''],
            #     container=folder,
            #     **fields)
            # ({'otherimposition': '',
            # 'imposition': [],
            # 'level': ['phd', 'master', 'bachelor'],
            # 'otherresearcherposition': '',
            # 'activitytype': ['research'],
            # 'eventName': 'Bertinoro Seminar on Distributed Runtime Verification 2016',
            # 'organizationdate': '15/05/2016',
            # 'sessionName': '',
            # 'assistants': 'stage2',
            # 'researcherposition': ['co-organizer'],
            # 'otherlevel': '',
            # 'speakersnac': 'stage1',
            # 'speakersint': 'stage1'},)

    def app2cv_guest(self, application, userid):
        logging.info('{0} - {1}'.format(application.id, userid))
        content_type = 'CVGuest'
        folder = self.get_folder(userid, content_type)
        id = application.id.replace('solicitudvisitante', 'sv')
        date = application.fecha_desde
        begin_date = {
            'Year': str(date.year()), 'Month': str(date.month()), 'Day': str(date.day())}
        date = application.fecha_hasta
        end_date = {
            'Year': str(date.year()), 'Month': str(date.month()), 'Day': str(date.day())}
        institution =  self.lookupInstitution(
            application.getInstitucion_procedencia())
        otherinstitution = ''
        if institution is None:
            otherinstitution = application.getInstitucion_procedencia()
        fields = {
            'institutionCountry': application.getPais_procedencia()[0],
            'institution': institution,
            'otherinstitution': otherinstitution,
            'goalGuest': application.ObjetoViaje(),
            'begin_date': begin_date,
            'end_date': end_date,
            'interchangeProgram': (application.getExchangeProgram() == 'yes') and 'si' or '',
            'creators': ([userid, 'admin'])}
        obj = api.content.create(
            type=content_type,
            id=id,
            title=application.invitado,
            container=folder,
            **fields)

    def lookupInstitution(self, institution):
        if not institution:
            return None
        institution = self.normalize(institution)
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            portal_type='CVInstitution',
            Title=institution,
            sort_on='sortable_title')
        if brains:
            return brains[0].UID
        logging.warning('Institution: "{0}" not in catalog'.format(institution))
        return None

    def normalize(self, title):
        return filter(lambda ch: ch not in "\(\)-\n\\'", title)
