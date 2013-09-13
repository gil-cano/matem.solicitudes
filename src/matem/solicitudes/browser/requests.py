# -*- coding: utf-8 -*-
import sys
from Products.Five.browser import BrowserView

from plone.memoize import forever

class Requests(BrowserView):
    """A class for querying the site for applications"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

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

    def hasReqDataStr(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, '')
            if tipo is None:
                return False
            elif tipo is '':
                return False
            else:
                return True
        except:
            return False

    def programaPresupuesto(self):
        mt = self.context.portal_membership
        member=mt.getAuthenticatedMember()
        users = []

        if 'Programador de Presupuesto' in list(member.getRoles()):
            return True
        else:
            return False

    def esSolicitanteAuxiliar(self):
        mt = self.context.portal_membership
        member=mt.getAuthenticatedMember()
        users = []

        if 'Solicitante Auxiliar' in list(member.getRoles()):
            return True
        else:
            return False
