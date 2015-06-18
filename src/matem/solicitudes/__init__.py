# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory  # noqa
solicitudesMessageFactory = MessageFactory('matem.solicitudes')  # noqa

from Products.validation import validation  # noqa
from matem.solicitudes.content.validators import StartBeforeEnd  # noqa
validation.register(StartBeforeEnd('isGreaterthanStart'))  # noqa


from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore import utils

from matem.solicitudes.content.solicitud import Solicitud  # noqa
from matem.solicitudes.content.solicitudbecario import SolicitudBecario  # noqa
from matem.solicitudes.content.solicitudfolder import SolicitudFolder  # noqa
from matem.solicitudes.content.solicitudinstitucional import SolicitudInstitucional  # noqa
from matem.solicitudes.content.solicitudvisitante import SolicitudVisitante  # noqa

import config


def initialize(context):

    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit(
            '%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype, ),
            permission=config.ADD_CONTENT_PERMISSION[atype.portal_type],
            extra_constructors=(constructor, ),
        ).initialize(context)
