#-*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
# from UNAM.imateCVct import _
# from UNAM.imateCVct.vocabularies import CURSOSEMUNAM
# from collections import OrderedDict
# from operator import itemgetter
# from plone.i18n.normalizer import idnormalizer as idn
# from zope.component import getUtility
# from zope.component.hooks import getSite
# from zope.i18n import translate
# from zope.schema.interfaces import IVocabularyFactory
# import collections
from DateTime import DateTime
from plone.i18n.normalizer import idnormalizer as idn
from operator import itemgetter

from plone import api


class EtyView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
    #     self.atype = self.context.portal_type.replace('Folder', '')


    def staff_on_leave_or_commission_days(self):

        researchers = []

        ftoday = DateTime()
        today = DateTime('/'.join([str(ftoday.year()), str(ftoday.month()), str(ftoday.day())]))
        start_date = today
        # end_date = today + 9.9999
        end_date = today + 10

        brains = api.content.find(
            Type='Solicitud de Licencia/Comision',
            review_state='aprobada',
            fecha_hasta={'query': [start_date, ], 'range': 'min'},
            fecha_desde={'query': [end_date, ], 'range': 'max'},
            sort_on='sortable_title',
        )
        for b in brains:
            obj = b.getObject()
            # researchers.append((b.Title, b.fecha_desde.strftime('%d/%m/%Y'), b.fecha_hasta.strftime('%d/%m/%Y')))
            researchers.append((obj.nombre_owner, b.fecha_desde.strftime('%d/%m/%Y'), b.fecha_hasta.strftime('%d/%m/%Y')))

        aux = [(r, idn.normalize(r[0]), ) for r in researchers]
        aux_sorted = sorted(aux, key=itemgetter(1))
        sortresearchers = [t[0] for t in aux_sorted]

        # return researchers
        return sortresearchers

    def staff_on_sabbatical(self):

        return []
