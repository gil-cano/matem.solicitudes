import unittest

import zope.event
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from matem.solicitudes.content.solicitud import Solicitud
from matem.solicitudes.tests.base import TestCase


class TestSolicitud(TestCase):
    """
      Test de creacion de solicitudes y contenedores de solicitudes
    """
    klass = Solicitud
    portal_type = 'Solicitud'
    title = 'solicitud-oaxaca'
    meta_type = 'Solicitud'

    def afterSetUp(self):
        # self.loginAsPortalOwner()
        self.setRoles(['Manager', 'Member', 'Investigador'])
        self.folder2011 = self._createType(self.folder, 'SolicitudFolder', '2011')
        self.folder.portal_workflow.doActionFor(self.folder2011, 'aceptar')
        self.application = self._createType(self.folder2011, self.portal_type, self.title)

    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog

        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        zope.event.notify(ObjectInitializedEvent(obj))
        return obj

    def test_handler_movetofolder(self):
        """ test the initialized handler """
        folder2012 = self._createType(self.folder, 'SolicitudFolder', '2012')
        self.folder.portal_workflow.doActionFor(folder2012, 'aceptar')
        
        # test content should not be moved
        content2011 = 'solicitud-2011'
        application = self._createType(self.folder2011, self.portal_type, content2011, fecha_desde='2011/10/10')
        self.failUnless(content2011 in self.folder2011)

        # test content should be moved
        content2012 = 'solicitud-2012'
        application = self._createType(self.folder2011, self.portal_type, content2012, fecha_desde='2012/10/10')
        self.failUnless(content2012 in self.folder2012)
        self.failIf(content2012 in self.folder2011)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSolicitud))
    return suite
