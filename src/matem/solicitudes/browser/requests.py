# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView


class Requests(BrowserView):
    """A class for querying the site for applications"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def hasReqData(self,tipodato):
        try:
            req = self.request
            tipo=req.get(tipodato, None)
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
