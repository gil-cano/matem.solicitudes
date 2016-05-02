# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


def install_dependencies(portal):
    """Install required products that does not have a profiles."""
    qi = getToolByName(portal, 'portal_quickinstaller')
    for product in ['FacultyStaffDirectory', 'ATCountryWidget']:
        if not qi.isProductInstalled(product):
            if qi.isProductInstallable(product):
                qi.installProduct(product)
            else:
                raise 'Product {0} not installable'.format(product)


def setupVarious(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('importsteps-unam-solicitudes.txt') is None:
        return
    # install_dependencies(portal)
