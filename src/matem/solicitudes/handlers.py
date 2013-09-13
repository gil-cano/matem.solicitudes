from Products.CMFCore.utils import getToolByName
from matem.solicitudes.browser.queries import Queries


def modificationHandler(obj, event):
    mt = getToolByName(obj, "portal_membership")
    catalog = getToolByName(obj, "portal_catalog")
    userid = mt.getAuthenticatedMember().getId()
    try:
        if 'tuple' in str(type(obj.getSolicitante())):
            userid = obj.getSolicitante()[0]
        else:
            userid = obj.getSolicitante()

        fsdperson = Queries(obj, None).getPersonWrapper(userid)
        obj.setSede(fsdperson.getSede())

        if "Solicitante Auxiliar" in list(mt.getAuthenticatedMember().getRoles()):
            solicitante = mt.getMemberById(userid)
            obj.setCreators(userid)
            obj.changeOwnership(solicitante.getUser())
            obj.manage_setLocalRoles(userid, ["Owner"])
    except:
        pass
    try:
        if obj.getPasaje()=="No":
            obj.setCantidad_pasaje(0.0)
            obj.setTipo_pasaje(())
    except:
        pass
    try:
        if obj.getViaticos()=="No":
            obj.setCantidad_viaticos(0.0)
    except:
        pass
    try:
        if obj.getInscripcion()=="No":
            obj.setCantidad_inscripcion(0.0)
    except:
        pass
    try:
        obj.setNombre_owner(obj.getNombreOwner())
    except:
        pass
    try:
        obj.setNombre_asesor(obj.getNombreAsesor())
    except:
        pass
    catalog.reindexObject(obj)


def movetofolder(obj, event):
    """ When a application is created it must be moved
    to a folder that correspond to the year of the activity.
    """
    event_year = str(obj.getFechaDesde().year())
    content_folder = obj.aq_parent
    content_id = obj.getId()
    dest_folder = getattr(content_folder.aq_parent, event_year, content_folder)
    # mt = getToolByName(obj, "portal_membership")
    # idActual=mt.getAuthenticatedMember().getId()
    # obj.manage_setLocalRoles(idActual, ['Owner', 'Manager'])
    # if dest_folder != content_folder:
    #     sm = getSecurityManager()
    #     try:
    #         try:
    #             tmp_user = UnrestrictedUser(
    #                 sm.getUser().getId(),
    #                 '', ["Manager"],
    #                 ''
    #             )
    #             # Act as user of the portal
    #             portal = getToolByName(obj, 'portal_url').getPortalObject()
    #             tmp_user = tmp_user.__of__(portal.acl_users)
    #             newSecurityManager(None, tmp_user)
    #             # Call the function
    #             dest_folder.manage_pasteObjects(content_folder.manage_cutObjects([content_id]))
    #         except:
    #             raise
    #     finally:
    #         # Restore the old security manager
    #         setSecurityManager(sm)
