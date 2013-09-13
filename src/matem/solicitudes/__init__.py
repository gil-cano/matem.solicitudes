from Products.Archetypes.atapi import process_types
from Products.Archetypes.atapi import listTypes

from Products.CMFCore import utils
from zope.i18nmessageid import MessageFactory

solicitudesMessageFactory = MessageFactory('matem.solicitudes')

from content.solicitud import Solicitud
from content.solicitudbecario import SolicitudBecario
from content.solicitudvisitante import SolicitudVisitante
from content.solicitudfolder import SolicitudFolder
from content.solicitudinstitucional import SolicitudInstitucional

import config


def initialize(context):

    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types      = (atype, ),
            permission         = config.ADD_CONTENT_PERMISSION[atype.portal_type],
            extra_constructors = (constructor, ),
            ).initialize(context)
