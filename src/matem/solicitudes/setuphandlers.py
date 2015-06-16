from Products.CMFCore.utils import getToolByName
from matem.solicitudes.browser.queries import Queries

def install_dependencies(portal):
    """Install required products that does not have a profiles"""
    qi = getToolByName(portal, 'portal_quickinstaller')
    for product in ['FacultyStaffDirectory', 'ATCountryWidget']:
        if not qi.isProductInstalled(product):
            if qi.isProductInstallable(product):
                qi.installProduct(product)
            else:
                raise "Product %s not installable" % product


def setupVarious(context):
    portal = context.getSite()
#    catalog = getToolByName(portal, 'portal_catalog')
#    results = catalog(portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario'))
#    for brain in results:
#            start=brain.start
#            url=brain.getURL()
#            obj=brain.getObject()
#            try:
#                fsdperson = Queries(obj,None).getPersonWrapper(obj.getIdOwner())
#                obj.setSede(fsdperson.getSede())
#            except:
#                pass;

    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('importsteps-unam-solicitudes.txt') is None:
        return
    # install_dependencies(portal)
