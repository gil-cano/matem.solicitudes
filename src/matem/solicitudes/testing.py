# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2

import unittest2 as unittest


class ApplicationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load missing dependencies for Products.FacultyStaffDirectory
        import Products.membrane
        self.loadZCML(package=Products.membrane)
        import Products.Relations
        self.loadZCML(package=Products.Relations)
        # Load ZCML
        import matem.solicitudes
        self.loadZCML(package=matem.solicitudes)
        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'Products.membrane')
        z2.installProduct(app, 'Products.Relations')
        z2.installProduct(app, 'Products.ATCountryWidget')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'matem.solicitudes:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'matem.solicitudes')


FIXTURE = ApplicationLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="matem.solicitudes:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="matem.solicitudes:Functional")


class IntegrationTestCase(unittest.TestCase):
    """docstring for IntegrationTestCase"""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """docstring for FunctionalTestCase"""

    layer = FUNCTIONAL_TESTING
