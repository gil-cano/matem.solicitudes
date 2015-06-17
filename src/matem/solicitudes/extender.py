# -*- coding: utf-8 -*-

from Products.Archetypes.public import FloatField
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import StringWidget
from Products.FacultyStaffDirectory.interfaces.person import IPerson

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from matem.solicitudes.interfaces import ISolicitudSpecific
from zope.component import adapts
from zope.interface import implements


class PersonWrapper:

    fsdperson = None

    def __init__(self, fsdperson):
        self.fsdperson = fsdperson

    def getFsdperson(self):
        return self.fsdperson

    def getLastName(self):
        fsdperson = self.fsdperson
        apellidos = fsdperson.getLastName() + " " + fsdperson.getField('apellidoMaterno').get(fsdperson)
        return apellidos

    def getSede(self):
        fsdperson = self.fsdperson
        return fsdperson.getField('sede').get(fsdperson)

    def getFirstName(self):
        fsdperson = self.fsdperson
        return fsdperson.getFirstName()

    def getMiddleName(self):
        fsdperson = self.fsdperson
        return fsdperson.getMiddleName()

    def getId(self):
        fsdperson = self.fsdperson
        return fsdperson.getId()

    def getSuffix(self):
        fsdperson = self.fsdperson
        return fsdperson.getSuffix()

    def getNumeroDeCuenta(self):
        fsdperson = self.fsdperson
        return fsdperson.getField('ncuenta').get(fsdperson)
