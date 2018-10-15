# -*- coding: utf-8 -*-

from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from matem.solicitudes.browser.queries import Queries
from matem.solicitudes.config import DICCIONARIO_AREAS
from matem.solicitudes.interfaces import ISolicitudFolder
from operator import itemgetter

import datetime
import sys


class AuxiliaresView(BrowserView):
    """Clase para importar solicitudes auxiliares"""

    queryObj = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.queryObj = Queries(context, request)

    def __call__(self):
        self.queryObj = Queries(context, request)
        form = self.request.form
        req = self.request
        container = self.context
        realowner = req.get('Creator', None)
        tipo = req.get('tiposolicitud', None)
        auxiliar_but = form.get('form.button.Create', None) is not None
        usuarioAutenticado = self.context.portal_membership.getAuthenticatedMember()

        if (tipo is not None) and (realowner is not None):
            usuarioDestino = self.context.portal_membership.getMemberById(realowner)
        else:
            usuarioDestino = usuarioAutenticado

        if "Solicitante Auxiliar" in list(usuarioAutenticado.getRoles()):
            if tipo == "becario":
                if "Becario" in list(usuarioDestino.getRoles()):
                    return ViewPageTemplateFile('solicitudfolder.pt')()
            else:
                return ViewPageTemplateFile('solicitudfolder.pt')()

    def getProductCreators(self):
        return self.queryObj.getProductCreators()
