# -*- coding: utf-8 -*-


class PersonWrapper:

    fsdperson = None

    def __init__(self, fsdperson):
        self.fsdperson = fsdperson

    def getFsdperson(self):
        return self.fsdperson

    def getLastName(self):
        fsdperson = self.fsdperson
        apellidos = fsdperson.getLastName() + ' ' + fsdperson.getField('apellidoMaterno').get(fsdperson)
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
