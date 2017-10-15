# -*- coding: utf-8 -*-

from matem.solicitudes.browser.queries import Queries
from Products.CMFCore.utils import getToolByName


def modificationHandler(obj, event):  # noqa
    mt = getToolByName(obj, 'portal_membership')
    catalog = getToolByName(obj, 'portal_catalog')
    userid = mt.getAuthenticatedMember().getId()
    try:
        if 'tuple' in str(type(obj.getSolicitante())):
            userid = obj.getSolicitante()[0]
        else:
            userid = obj.getSolicitante()

        fsdperson = Queries(obj, None).getPersonWrapper(userid)
        obj.setSede(fsdperson.getSede())

        if 'Solicitante Auxiliar' in list(mt.getAuthenticatedMember().getRoles()):
            solicitante = mt.getMemberById(userid)
            obj.setCreators(userid)
            obj.changeOwnership(solicitante.getUser())
            obj.manage_setLocalRoles(userid, ['Owner'])
    except Exception:
        pass
    try:
        if obj.getPasaje() == 'No':
            obj.setCantidad_pasaje(0.0)
            obj.setTipo_pasaje(())
    except Exception:
        pass
    try:
        if obj.getViaticos() == 'No':
            obj.setCantidad_viaticos(0.0)
    except Exception:
        pass
    try:
        if obj.getInscripcion() == 'No':
            obj.setCantidad_inscripcion(0.0)
    except Exception:
        pass
    try:
        obj.setNombre_owner(obj.getNombreOwner())
    except Exception:
        pass
    try:
        obj.setNombre_asesor(obj.getNombreAsesor())
    except Exception:
        pass

    try:
        if obj.getViaticos_becario() == 'No':
            obj.setCantidad_viaticos(0.0)
    except Exception:
        pass

    catalog.reindexObject(obj)


def movetofolder(obj, event):
    """ When a application is created it must be moved
    to a folder that correspond to the year of the activity.
    """
    event_year = str(obj.getFechaDesde().year())
    content_folder = obj.aq_parent
    # content_id = obj.getId()
    getattr(content_folder.aq_parent, event_year, content_folder)
