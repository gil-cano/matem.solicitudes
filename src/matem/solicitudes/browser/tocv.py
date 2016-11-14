# -*- coding: utf-8 -*-

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
            portal_type=('Solicitud', 'SolicitudInstitucional'),
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
            prides = ['rajsbaum', ]
            if userid not in prides:
                continue

            if isinstance(application, SolicitudVisitante):
                self.app2cv_guest(application, userid)
        logging.info('Done')

    def get_folder(self, userid, content_type):
        """Get cvitem folder inside user CVFolder"""
        path = '/fsd/{id}/cv/{ctype}folder'.format(id=userid, ctype=content_type)
        return api.content.get(path=path)

    def get_metacv(self, userid, content_type):
        """Get cvitem folder inside meta-cv."""
        path = '/catalogos/meta-cv/{ctype}folder'.format(ctype=content_type)
        return api.content.get(path=path)

    def app2cv_guest(self, application, userid, metacv=True):
        logging.info('{0} - {1}'.format(application.id, userid))
        content_type = 'CVGuest'

        folder = self.get_metacv(userid, content_type.lower())
        if not metacv:
            folder = self.get_folder(userid, content_type.lower())
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
