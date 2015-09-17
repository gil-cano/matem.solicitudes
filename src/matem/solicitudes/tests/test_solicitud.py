# -*- coding: utf-8 -*-
"""Test Solicitud content type."""

from matem.solicitudes.content.solicitud import Solicitud
from matem.solicitudes.testing import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import unittest2 as unittest


class TestsSolicitud(IntegrationTestCase):
    """Test Solicitud type."""

    portal_type = 'Solicitud'
    klass = Solicitud

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('SolicitudFolder', '2015')
        self.folder = self.portal['2015']
        self.portal.portal_workflow.doActionFor(self.folder, 'aceptar')

    def test_adding(self):
        """Test that we can add a Solicitud."""
        setRoles(self.portal, TEST_USER_ID, ['Investigador'])
        self.folder.invokeFactory(self.portal_type, 'solicitud-oaxaca-2015')
        self.assertTrue('solicitud-oaxaca-2015' in self.folder)


def test_suite():
    """This """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
