# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class ISolicitud(Interface):
    """Marker interface
    """


class ISolicitudTabular(Interface):
    """Marker interface
    """


class ISolicitudBecario(Interface):
    """Marker interface
    """


class ISolicitudVisitante(Interface):
    """Marker interface
    """


class ISolicitudFolder(Interface):
    """Marker interface
    """


class ISolicitudSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer
       for this product.
    """


class ISolicitudInstitucional(Interface):
    """Description of the Example Type"""
