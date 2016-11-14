# -*- coding: utf-8 -*-

from matem.solicitudes.content.solicitudvisitante import SolicitudVisitante
from plone import api
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import ObjectEditedEvent
from z3c.form import button
from z3c.form import form
from zope import event

import logging


# from Acquisition import aq_base
# from UNAM.imateCVct.vocabularies import RESEARCH
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import IIDNormalizer
# import re

class ApplicationstoCVForm(form.Form):
    """docstring for ApplicationstoCVForm"""

    @button.buttonAndHandler(u'Dump applications to cv')
    def dump_to_cv(self, action):
        """Create cv items form applications"""
        logging.info('Dumpping applications')
        folder = api.content.get(
            path='/servicios/servicios-internos/solicitudes/2016')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            path={'query': '/'.join(folder.getPhysicalPath()), 'depth': 1},
            review_state='aprobada',
            portal_type=('Solicitud', 'SolicitudInstitucional', 'SolicitudVisitante'),
            sort_on='created'
        )
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

    def get_folder(self, userid, content_type):
        path = '/fsd/{id}/cv/{ctype}folder'.format(id=userid, ctype=content_type)
        return api.content.get(path=path)

    def app2cv_guest(self, application, userid):
        logging.info('{0} - {1}'.format(application.id, userid))
        content_type = 'CVGuest'
        folder = self.get_folder(userid, content_type.lower())
        id = application.id.replace('solicitudvisitante', 'sv')
        date = application.fecha_desde
        begin_date = {
            'Year': date.year(), 'Month': date.month(), 'Day': date.day()}
        date = application.fecha_hasta
        end_date = {
            'Year': date.year(), 'Month': date.month(), 'Day': date.day()}
        fields = {
            'institutionCountry': application.getPais_procedencia()[0],
            'otherinstitution': application.getInstitucion_procedencia(),
            'goalGuest': application.ObjetoViaje(),
            'begin_date': begin_date,
            'end_date': end_date,
            'interchangeProgram': (application.getExchangeProgram() == 'yes') and 'si' or '',
            'creators': (userid, ),
        }
        obj = api.content.create(
            type=content_type,
            id=id,
            title=application.invitado,
            container=folder,
            **fields)
        # is_new_object = obj.checkCreationFlag()
        # obj.unmarkCreationFlag()

        # if is_new_object:
        #     event.notify(ObjectInitializedEvent(obj))
        #     obj.at_post_create_script()
        # else:
        #     event.notify(ObjectEditedEvent(obj))
        #     obj.at_post_edit_script()
        # obj.reindexObject()
        # event.notify(ObjectInitializedEvent(obj))
        # event.notify(ObjectEditedEvent(obj))
        # obj.reindexObject()
