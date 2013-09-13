from Products.Archetypes.public import IntegerField, FloatField, StringWidget, LinesField, LinesWidget
from Products.FacultyStaffDirectory.interfaces.person import IPerson
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from interfaces import ISolicitudSpecific
from zope.component import adapts
from zope.interface import implements

#class _ExtensionFloatField(ExtensionField, FloatField): pass
#class _ExtensionIntegerField(ExtensionField, IntegerField): pass
#class _ExtensionLinesField(ExtensionField, LinesField): pass


#class PersonExtender(object):
#    adapts(IPerson)
#    implements(ISchemaExtender, IBrowserLayerAwareExtender)
#
#    layer = ISolicitudSpecific
#
#    fields = [
#        _ExtensionLinesField(
#            "solicitudes_creadas",
#            default=(),
#            widget = LinesWidget(visible={'view':'invisible','edit':'invisible'}),
#        ),
#        _ExtensionFloatField(
#            "presupuesto_inicial",
#            default=0.0,
#            widget = StringWidget(visible={'view':'invisible','edit':'invisible'}),
#        ),
#        _ExtensionFloatField(
#            "presupuesto_asignado",
#            default=0.0,
#            widget = StringWidget(visible={'view':'invisible','edit':'invisible'}),
#        ),
#        _ExtensionFloatField(
#            "presupuesto_ejercido",
#            default=0.0,
#            widget = StringWidget(visible={'view':'invisible','edit':'invisible'}),
#        ),
#        _ExtensionIntegerField(
#            "dias_comision_utilizados",
#            default=0,
#            widget = StringWidget(visible={'view':'invisible','edit':'invisible'}),
#        ),
#        _ExtensionIntegerField(
#            "dias_licencia_utilizados",
#            default=0,
#            widget = StringWidget(visible={'view':'invisible','edit':'invisible'}),
#        ),
#    ]
#
#    def __init__(self, context):
#        self.context = context
#
#    def getFields(self):
#        return self.fields

class PersonWrapper:

    fsdperson=None

    def __init__(self,fsdperson):
        self.fsdperson=fsdperson

    def getFsdperson(self):
        return self.fsdperson

#    def getSolicitudes_creadas(self):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('solicitudes_creadas').get(fsdperson)
#
#    def setSolicitudes_creadas(self,solicitudes):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('solicitudes_creadas').set(fsdperson,solicitudes)
#
#    def getPresupuesto_inicial(self):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('presupuesto_inicial').get(fsdperson)
#
#    def setPresupuesto_inicial(self,cantidad):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('presupuesto_inicial').set(fsdperson,cantidad)
#
#    def getPresupuesto_asignado(self):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('presupuesto_asignado').get(fsdperson)
#
#    def setPresupuesto_asignado(self,cantidad):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('presupuesto_asignado').set(fsdperson,cantidad)
#
#    def getPresupuesto_ejercido(self):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('presupuesto_ejercido').get(fsdperson)
#
#    def setPresupuesto_ejercido(self,cantidad):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('presupuesto_ejercido').set(fsdperson,cantidad)
#
#    def getDias_comision_utilizados(self):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('dias_comision_utilizados').get(fsdperson)
#
#    def setDias_comision_utilizados(self,cantidad):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('dias_comision_utilizados').set(fsdperson,cantidad)
#
#    def getDias_licencia_utilizados(self):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('dias_licencia_utilizados').get(fsdperson)
#
#    def setDias_licencia_utilizados(self,cantidad):
#        fsdperson=self.fsdperson
#        return fsdperson.getField('dias_licencia_utilizados').set(fsdperson,cantidad)

    def getLastName(self):
        fsdperson=self.fsdperson
        apellidos= fsdperson.getLastName() + " " + fsdperson.getField('apellidoMaterno').get(fsdperson)
        return apellidos

    def getSede(self):
        fsdperson=self.fsdperson
        return fsdperson.getField('sede').get(fsdperson)

    def getFirstName(self):
        fsdperson=self.fsdperson
        return fsdperson.getFirstName()

    def getMiddleName(self):
        fsdperson=self.fsdperson
        return fsdperson.getMiddleName()

    def getId(self):
        fsdperson=self.fsdperson
        return fsdperson.getId()
    
    def getSuffix(self):
        fsdperson=self.fsdperson
        return fsdperson.getSuffix()

    def getNumeroDeCuenta(self):
        fsdperson=self.fsdperson
        return fsdperson.getField('ncuenta').get(fsdperson)
