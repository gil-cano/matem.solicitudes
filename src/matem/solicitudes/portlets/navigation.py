from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets.navigation import Renderer


class MyRenderer(Renderer):
    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')

    def getMetaTypesNotToList(self):
        context = self.context
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        nueva = list(navtree_properties.metaTypesNotToList)
        nueva.append("Solicitud")
        nueva.append("SolicitudVisitante")
        nueva.append("SolicitudBecario")
        return nueva

    def getIdsNotToList(self):
        context = self.context
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        return list(navtree_properties.idsNotToList)
