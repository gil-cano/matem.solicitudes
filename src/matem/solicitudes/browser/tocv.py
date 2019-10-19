# -*- coding: utf-8 -*-

from matem.solicitudes.content.solicitud import Solicitud
from matem.solicitudes.content.solicitudinstitucional import SolicitudInstitucional
from matem.solicitudes.content.solicitudvisitante import SolicitudVisitante
from plone import api
from plone.i18n.normalizer import idnormalizer as idn
from Products.ATCountryWidget.config import COUNTRIES
from z3c.form import button
from z3c.form import form
from zope.component.hooks import getSite

import logging


class ApplicationstoCVForm(form.Form):
    """docstring for ApplicationstoCVForm"""

    @button.buttonAndHandler(u'Dump applications to cv')
    def dump_to_cv(self, action):
        """Create cv items form applications"""
        logging.info('Dumpping applications')
        folder = api.content.get(
            path='/servicios/servicios-internos/solicitudes/2019')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            path={'query': '/'.join(folder.getPhysicalPath()), 'depth': 1},
            review_state='aprobada',
            portal_type=('Solicitud', 'SolicitudInstitucional', 'SolicitudVisitante'),
            sort_on='created')
        for brain in brains:
            application = brain.getObject()
            userid = application.getIdOwner()
            # if brain.id in aux_folder:
            #     application = aux_folder[brain.id]
            # prides = []
            # if userid not in prides:
            #     continue
            if userid in ['mclapp']:
                continue
            if isinstance(application, Solicitud):
                self.app2cv(application, userid)
            elif isinstance(application, SolicitudVisitante):
                self.app2cv_guest(application, userid)
            elif isinstance(application, SolicitudInstitucional):
                self.app2cv_inst(application, userid)
        logging.info('Done')

    def get_folder(self, userid, content_type, metacv=False):
        """Get cvitem folder inside the metacv or the user CVFolder"""
        ctype = content_type.lower()
        path = '/catalogos/copy_of_meta-cv/{ctype}folder'.format(ctype=ctype)
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
            pre = 'sea-{0}'.format(i)
            id = application.id.replace('solicitud', pre)
            try:
                date = item['assistancedate'].split('/')
                begin_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            except IndexError as e:
                continue
            institution = None
            otherinstitution = item['institution']
            # if institution is None:
            #     otherinstitution = item['institution']
            fields = {
                'event_date': begin_date,
                'numberOfDays': application.getCantidadDeDias(),
                'audienceType': u'assistant',
                'where': u'institution',
                'institutionCountry': application.pais[0],
                'institution': institution,
                'otherinstitution': otherinstitution,
                'creators': ([userid, 'admin'])}
            api.content.create(
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

    def app2cv_inst(self, application, userid):
        if not application.titulo_trabajo:
            return
        logging.info('Conferencia: {0} - {1}'.format(application.id, userid))
        id = application.id.replace('solicitudinstitucional', 'siconf-')
        fields = {}
        fields['creators'] = ([userid, 'admin'])

        content_type = 'CVConference'
        fields['modality'] = u'conference'
        fields['conftype'] = u'research'
        # En solicitudes: congress, seminary, coloquio, school, workshop, other
        fields['eventtype'] = u'congress'
        fields['meetingName'] = application.event_title

        date = application.fecha_desde
        event_date = {'Year': str(date.year()), 'Month': date.mm(), 'Day': date.dd()}
        fields['event_date'] = event_date

        fields['assist'] = u'application'
        folder = self.get_folder(userid, content_type)

        fields['city'] = application.ciudad_pais
        fields['where'] = application.ciudad_pais
        fields['speakto'] = u'Investigadores'

        # En conferencias: u'metting', u'institution', u'other'
        # institution = self.lookupInstitution(application.institucion)
        fields['institution'] = None
        fields['otherinstitution'] = application.institucion
        # if institution is None:
        #     fields['otherinstitution'] = application.institucion
        #     fields['institution'] = None

        fields['institutionCountry'] = application.pais[0]
        countries = self.getCountriesVocabulary()
        iscountry = countries.get(application.pais[0], '')
        if iscountry:
            fields['institutionCountry'] = iscountry
        if id not in folder:
            api.content.create(
                type=content_type,
                id=id,
                title=application.titulo_trabajo,
                container=folder,
                **fields)
        # reportamos asistencias
        content_type = 'CVEvent'
        folder = self.get_folder(userid, content_type)
        fields = {
            'event_date': event_date,
            'numberOfDays': application.getCantidadDeDias(),
            'audienceType': u'assistant',
            'where': u'institution',
            'institutionCountry': application.pais[0],
            'institution': None,
            'otherinstitution': application.institucion,
            'creators': ([userid, 'admin'])}

        if id not in folder:
            api.content.create(
                type=content_type,
                id=id,
                title=application.event_title,
                container=folder,
                **fields)


    def getCountriesVocabulary(self):
        translation_service = getSite().translation_service
        sorted_list = [x for x in COUNTRIES.iteritems()]
        # sorted_list.append(('', ''))
        spanish_list = [(x[0], translation_service.translate(x[1], domain="plone", target_language="es")) for x in sorted_list]
        spanish_list.sort(key=lambda x: idn.normalize(x[1]))

        foo = {}
        for ctry in spanish_list:
            foo[idn.normalize(ctry[1])] = ctry[0]
        # return DisplayList(spanish_list)
        return foo

    def app2cv_conference(self, application, userid):
        logging.info('Conferencia: {0} - {1}'.format(application.id, userid))
        # content_type = 'CVConference'
        # folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.conferences):
            pre = 'sconf-{0}'.format(i)
            id = application.id.replace('solicitud', pre)
            fields = {}
            fields['creators'] = ([userid, 'admin'])

            if item['isplenary'] == 'yes':
                content_type = 'CVConferencePlus'
            else:
                content_type = 'CVConference'
                # #### Campos que sólo los tiene conference ###

                # En conference: u'conference', u'discussion_metting'
                fields['modality'] = u'conference'

                # En solicitudes: 'invitation', 'application'
                # En conference: u'invitation', u'application'
                fields['assist'] = unicode(item['participationtype'])

            folder = self.get_folder(userid, content_type)

            if item['conferencedate']:
                date = item['conferencedate'].split('/')
                event_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            else:
                date = application.fecha_desde
                event_date = {'Year': str(date.year()), 'Month': date.mm(), 'Day': date.dd()}
            fields['event_date'] = event_date

            # Puedes elegir varios tipos en la solicitud y en el contenido
            # sólo uno: u'research', u'divulgation', u'human_resources'
            # en solicitud son str y en contenidos son unicode
            conferencetypes = item['conferencetype']
            conftype = u'divulgation'
            speakto = u'Público en general'
            if 'research' in conferencetypes:
                conftype = u'research'
                speakto = u'Investigadores'
            else:
                if 'human_resources' in conferencetypes:
                    conftype = u'human_resources'
                    speakto = u'Estudiantes'
            fields['conftype'] = conftype
            fields['speakto'] = speakto

            # En solicitudes: congress, seminary, coloquio, school, workshop, other
            fields['eventtype'] = unicode(item['eventtype'])

            meetingName = item['eventName']
            fields['meetingName'] = meetingName

            # En conferencias: u'metting', u'institution', u'other'
            if item['institution']:
                where = u'institution'
                fields['otherinstitution'] = item['institution']
                # newinst = self.lookupInstitution(item['institution'])
                # if newinst is None:
                #     fields['otherinstitution'] = item['institution']
                # else:
                #     fields['institution'] = newinst
            else:
                where = u'other'
                fields['other'] = item['place']

            fields['where'] = where

            fields['institutionCountry'] = application.pais[0]
            countries = self.getCountriesVocabulary()
            for country in item['place'].split(' '):
                ncountry = country.replace(',', '').replace('.', '')
                iscountry = countries.get(idn.normalize(ncountry), '')
                if iscountry:
                    fields['institutionCountry'] = iscountry
            api.content.create(
                type=content_type,
                id=id,
                title=item['title'],
                container=folder,
                **fields)
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
            date = item['coursedate'].split('/')
            begin_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            hours = ''
            if unicode(item['duration']).isnumeric():
                hours = item['duration']
            institution = None
            otherinstitution = item['institution']
            if institution is None:
                otherinstitution = item['institution']
            coursetype = {
                'research': u'researcher',
                'divulgation': u'divulgation',
                'human_resources': u'rhuman'}
            fields = {
                'courseName': item['title'],
                'level': item['level'],
                'otherLevel': item['otherlevel'],
                'speaktype': [coursetype[i] for i in item['coursetype']],
                'coursetype': u'other',
                'duration': u'otro',
                'numberOfHours': hours,
                'hourType': u'in-total',
                'institutionCountry': application.pais[0],
                'institution': institution,
                'otherinstitution': otherinstitution,
                'eventNotes': item['eventName'],
                'begin_date': begin_date,
                'creators': ([userid, 'admin'])}
            api.content.create(
                type=content_type,
                id=id,
                container=folder,
                **fields)
            # ({'coursetype': ['human_resources'],
            # 'level': 'bachelor',
            # 'title': 'Formas cuadr\xc3\xa1ticas (Minicurso)',
            # 'eventName': 'X jornadas de f\xc3\xadsica y matem\xc3\xa1ticas de la UACJ',
            # 'place': 'Chihuahua, M\xc3\xa9xico',
            # 'duration': '',
            # 'coursedate': '18/04/2016',
            # 'otherlevel': '',
            # 'institution': 'Universidad Aut\xc3\xb3noma de Ciudad Ju\xc3\xa1rez (UACJ)'},)

    def app2cv_research(self, application, userid):
        logging.info('Estancias de Inv: {0} - {1}'.format(application.id, userid))
        content_type = 'CVVisit'
        folder = self.get_folder(userid, content_type)
        for i, item in enumerate(application.sresearch):
            pre = 'sv-{0}'.format(i)
            id = application.id.replace('solicitud', pre)
            date = item['sresearchinitdate'].split('/')
            begin_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            date = item['sresearchenddate'].split('/')
            end_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            institution = None
            otherinstitution = item['institution']
            # if institution is None:
            #     otherinstitution = item['institution']
            fields = {
                'institutionCountry': application.pais[0],
                'institution': institution,
                'otherinstitution': otherinstitution,
                'begin_date': begin_date,
                'end_date': end_date,
                'goalVisit': item['objective'],
                'researchVisit': True,
                'creators': ([userid, 'admin'])}
            api.content.create(
                type=content_type,
                id=id,
                container=folder,
                **fields)
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

            # 'activitytype',
            # En solicitudes: 'research', 'divulgation', 'human_resources'
            # En eventorg: u'researcher', u'rhuman', u'divulgation'
            newactivitiestype = []
            activitiestype = item['activitytype']
            if 'research' in activitiestype:
                newactivitiestype.append(u'researcher')
            if 'divulgation' in activitiestype:
                newactivitiestype.append(u'divulgation')
            if 'human_resources' in activitiestype:
                newactivitiestype.append(u'rhuman')
            fields['speakto'] = newactivitiestype

            # 'eventName'
            # En eventorg es 'meetingName'
            # fields['title'] = item['eventName']

            # 'level',
            # En solicitudes: 'phd', 'master', 'bachelor', 'highschool', 'other'
            # En eventorg: u'phd', u'master', u'bachelor', u'highschool', 'other'
            newlevels = []
            for level in item['level']:
                newlevels.append(unicode(level))
            fields['level'] = newlevels

            # 'otherlevel',
            fields['otherlevel'] = item['otherlevel']

            # 'researcherposition',
            # En solicitudes: 'organizer', 'co-organizer', 'responsible', 'scientific', 'localc', 'directivec', 'other'
            fields['researcherposition'] = item['researcherposition']

            # 'otherresearcherposition',
            fields['otherresearcherposition'] = item['otherresearcherposition']

            # 'sessionName',
            fields['sessionName'] = item['sessionName']

            # 'imposition',
            # En solicitudes: 'sponsor', 'campus', 'support' (Support for the diffusion), 'other'
            # En eventorg: u'sponsor', u'campus', u'organizer', u'co-organizer', u'support', u'other'
            # En solicitudes es multiselection y en eventorg no
            impositions = item['imposition']
            instituteParticipation = u'other'
            if 'campus' in impositions:
                instituteParticipation = u'campus'
            else:
                if 'sponsor' in impositions:
                    instituteParticipation = u'sponsor'
                else:
                    if 'support' in impositions:
                        instituteParticipation = u'support'

            fields['instituteParticipation'] = instituteParticipation

            # 'otherimposition',
            fields['otherimposition'] = item['otherimposition']

            # 'speakersint',
            # Values of ExpectedNumbersVocabulary:
            nassistants = {
                'stage1': '1 - 20',
                'stage2': '21 - 40',
                'stage3': '41 - 60',
                'stage4': '61 - 80',
                'stage5': '80 - 100',
                'stage6': 'More than 100',
            }

            fields['foreignSpeakers'] = nassistants.get(item['speakersint'], '0')

            # 'speakersnac',
            fields['nationalSpeakers'] = nassistants.get(item['speakersnac'], '0')

            # 'assistants',
            fields['assistants'] = nassistants.get(item['assistants'], '0')

            # 'organizationdate',
            if item['organizationdate']:
                date = item['organizationdate'].split('/')
                event_date = {'Year': date[2], 'Month': date[1], 'Day': date[0]}
            else:
                date = application.fecha_desde
                event_date = {'Year': str(date.year()), 'Month': date.mm(), 'Day': date.dd()}
            fields['event_date'] = event_date

            # En eventorg: u'national', u'international', u'international-mx'
            if application.pais[0] == 'MX':
                fields['eventType'] = u'international-mx'
            else:
                fields['eventType'] = u'international'

            fields['country'] = application.pais[0]
            fields['city'] = application.ciudad_pais

            api.content.create(
                type=content_type,
                id=id,
                title=item['eventName'],
                container=folder,
                **fields)
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
            'Year': str(date.year()),
            'Month': str(date.month()),
            'Day': str(date.day())}
        date = application.fecha_hasta
        end_date = {
            'Year': str(date.year()),
            'Month': str(date.month()),
            'Day': str(date.day())}
        institution = self.lookupInstitution(
            application.getInstitucion_procedencia())
        otherinstitution = ''
        if institution is None:
            otherinstitution = application.getInstitucion_procedencia()
        fields = {
            'institutionCountry': application.getPais_procedencia()[0],
            'institution': None,
            'otherinstitution': application.getInstitucion_procedencia(),
            'goalGuest': application.ObjetoViaje(),
            'begin_date': begin_date,
            'end_date': end_date,
            'interchangeProgram': (application.getExchangeProgram() == 'yes') and 'si' or '',
            'creators': ([userid, 'admin'])}
        if id not in folder:
            api.content.create(
                type=content_type,
                id=id,
                title=application.invitado,
                container=folder,
                **fields)

    def lookupInstitution(self, institution):
        institution = self.normalize(institution)
        if not institution:
            return None
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            portal_type='CVInstitution',
            Title=institution,
            sort_on='sortable_title')
        if brains:
            return brains[0].UID
        logging.warning('Institution: not in catalog')
        return None

    def normalize(self, title):
        return filter(lambda ch: ch not in "\(\)-\n\\'", title)
