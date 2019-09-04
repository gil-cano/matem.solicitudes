#-*- coding: utf-8 -*-
from DateTime import DateTime
from operator import itemgetter
from plone import api
from plone.i18n.normalizer import idnormalizer as idn
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class EtyView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        if self.context.id == 'licencias-y-comisiones':
            userid = api.user.get_current().id

            pm = getToolByName(self.context, 'portal_membership')
            roles_in_context = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if 'Reader' in self.context.get_local_roles_for_userid(userid) or 'Manager' in roles_in_context:
                return self.index()

        myportal = self.context.portal_url.getPortalObject()
        return myportal.restrictedTraverse('insufficient_privileges')()

    def staff_on_leave_or_commission_days(self):

        researchers = []

        ftoday = DateTime()
        today = DateTime('/'.join([str(ftoday.year()), str(ftoday.month()), str(ftoday.day())]))
        start_date = today
        # end_date = today + 9.9999
        end_date = today + 1

        with api.env.adopt_user(username='admin'):

            brains = api.content.find(
                Type='Solicitud de Licencia/Comision',
                review_state='aprobada',
                fecha_hasta={'query': [start_date, ], 'range': 'min'},
                fecha_desde={'query': [end_date, ], 'range': 'max'},
                sort_on='sortable_title',
            )
            for b in brains:
                obj = b.getObject()
                researchers.append((obj.nombre_owner, b.fecha_hasta.strftime('%d/%m/%Y')))

        aux = [(r, idn.normalize(r[0]), ) for r in researchers]
        aux_sorted = sorted(aux, key=itemgetter(1))
        sortresearchers = [t[0] for t in aux_sorted]

        return sortresearchers

    def staff_on_sabbatical(self):

        return []
