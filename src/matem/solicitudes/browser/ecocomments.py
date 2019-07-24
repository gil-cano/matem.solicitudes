# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
# from UNAM.imateCVct import _
# from UNAM.imateCVct.vocabularies import CURSOSEMUNAM
# from collections import OrderedDict
# from operator import itemgetter
# from plone.i18n.normalizer import idnormalizer as idn
# from zope.component import getUtility
from zope.component.hooks import getSite
# from zope.i18n import translate
# from zope.schema.interfaces import IVocabularyFactory
# import collections
# from DateTime import DateTime


class SolComments(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def catalog(self):
        return getToolByName(getSite(), 'portal_catalog')

    def foo(self):

        # if ptype == 'all':
        #     ptype = (
        #         'Solicitud',
        #         'SolicitudVisitante',
        #         'SolicitudBecario',
        #         'SolicitudInstitucional'
        #     )
        path = '/'.join(self.context.getPhysicalPath())
        # query = {'path': {'query': path, 'depth': 1}, 'portal_type': ptype}

        # import pdb; pdb.set_trace()

        query = {
            'path': {'query': path, 'depth': 1},
            'portal_type': ['Solicitud', 'SolicitudVisitante', 'SolicitudBecario', 'SolicitudInstitucional'],
            'review_state': 'aprobada'
        }

        brains = self.catalog(query)


        attlist = [
            'absolute_url',
            'Type',
            'getNombreOwner',
            'getPais',
            'getFechaDesde',
            'getFechaHasta',
            'getObjetoViaje',
            'getCantidadDeDias',
            'getCantidadAutorizadaTotal',
            'getFecha_sesionci',
            'getActaci',
            'getCargo_presupuesto',
            'getWFStateName',
        ]
        items = []
        for b in brains:
            o = b.getObject()
            comentario = o.comentario_ci
            if comentario and ('AGOTA' not in comentario.upper()):
                adic = {a: getattr(o, a)() for a in attlist}
                ffrom = adic['getFechaDesde']
                if ffrom is not None:
                    adic['getFechaDesde'] = ffrom.strftime('%d/%m/%Y')
                tto = adic['getFechaHasta']
                if tto is not None:
                    adic['getFechaHasta'] = tto.strftime('%d/%m/%Y')
                cidate = adic['getFecha_sesionci']
                if cidate is not None:
                    adic['getFecha_sesionci'] = cidate.strftime('%d/%m/%Y')
                adic['commentsci'] = o.comentario_ci
                items.append(adic)
                # improve type
                if '/' in adic['Type']:
                    adic['Type'] = 'Solicitud de {0}'.format(o.getLicenciacomision())
                if 'Visitante' in adic['Type']:
                    adic['Type'] = '{0} ({1})'.format(adic['Type'], o.getNombreInvitado())
        return items


        # for b in brains:
        #     obj = b.getObject()
        #     if obj.comentario_ci:


        # import pdb; pdb.set_trace()
