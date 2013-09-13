from Products.CMFCore.utils import getToolByName

def upgrade_to_308(portal_setup):
    # recalculate travel expenses in solicitud folders
    portal_catalog = getToolByName(portal_setup, 'portal_catalog')
    for brain in portal_catalog(portal_type = 'SolicitudFolder'):
        brain.getObject().actualizarPeriodo()
