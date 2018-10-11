from AccessControl.unauthorized import Unauthorized
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFPlone.utils import _createObjectByType
from matem.solicitudes.tests.base import TestCase
from zope.event import notify

import unittest

class TestsDeCreacion(TestCase):
    """
      Test de creacion de solicitudes y contenedores de solicitudes
    """

    portal_type = 'FSDPerson'

    def afterSetUp(self):
        self.setRoles(['Manager', 'Member'])

        self.portal.invokeFactory(type_name='FSDFacultyStaffDirectory', id='FSDFolder')
        FSDFolder = self.portal.FSDFolder
        FSDFolder.reindexObject()

        self.portal.invokeFactory(type_name='SolicitudFolder', id='folderSolicitudes', fecha_desde='', fecha_hasta='')
        folderSolicitudes = self.portal.folderSolicitudes
        folderSolicitudes.reindexObject()

        self.portal.portal_workflow.doActionFor(FSDFolder, 'publish')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')

        FSDFolder.invokeFactory(type_name=self.portal_type, id='manager')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='solicitante')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='investigador')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='becario')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='comisionado')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='tecnico')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='postdoc')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='consejero')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='responsablecomision')
        FSDFolder.invokeFactory(type_name=self.portal_type, id='responsableconsejo')

        self.portal.manage_setLocalRoles('manager', ['Manager', 'Member'])
        folderSolicitudes.manage_setLocalRoles('manager', ['Manager', 'Member'])
        folderSolicitudes.manage_setLocalRoles('solicitante', ['Solicitante Auxiliar', 'Member'])
        folderSolicitudes.manage_setLocalRoles('investigador', ['Investigador', 'Member'])
        folderSolicitudes.manage_setLocalRoles('becario', ['Becario', 'Member'])
        folderSolicitudes.manage_setLocalRoles('tecnico', ['Tecnico Academico', 'Member'])
        folderSolicitudes.manage_setLocalRoles('postdoc', ['Postdoc', 'Member'])
        folderSolicitudes.manage_setLocalRoles('comisionado', ['Comisionado', 'Member'])
        folderSolicitudes.manage_setLocalRoles('consejero', ['Consejero', 'Member'])
        folderSolicitudes.manage_setLocalRoles('responsablecomision', ['Responsable de la Comision', 'Member'])
        folderSolicitudes.manage_setLocalRoles('responsableconsejo', ['Responsable del Consejo', 'Member'])

    def testCrearFolderDeSolicitudes(self):
        self.changeUser('solicitante')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('investigador')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('tecnico')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('becario')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('comisionado')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('consejero')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('responsablecomision')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('responsableconsejo')
        self.failUnlessRaises(Unauthorized,
            self.portal.invokeFactory,
            type_name='SolicitudFolder',
            id='TestSolicitudFolder',
            fecha_desde='',
            fecha_hasta='',
        )

        self.changeUser('manager')
        folderAdded = self.portal.invokeFactory(type_name='SolicitudFolder',
                id='TestSolicitudFolder',
                fecha_desde='',
                fecha_hasta='')

        folderSolicitudes = self.portal.TestSolicitudFolder

        self.assertEquals('TestSolicitudFolder', folderAdded)

        self.assertEquals('noaceptando', folderSolicitudes.getWFState())

        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'archivar')
        self.assertEquals('historico', folderSolicitudes.getWFState())

        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')
        self.assertEquals('aceptando', folderSolicitudes.getWFState())

        total = folderSolicitudes.getPresupuesto_inicial()
        total += folderSolicitudes.getPresupuesto_asignado()
        total += folderSolicitudes.getPresupuesto_maximo_investigadores()
        total += folderSolicitudes.getPresupuesto_maximo_becarios()
        total += folderSolicitudes.getPresupuesto_maximo_tecnicos()
        total += folderSolicitudes.getPresupuesto_maximo_postdocs()

        self.assertEquals(0.0, total)

        self.assertEquals([{}], folderSolicitudes.getPresupuesto_asignado_solicitantes())
        self.assertEquals([{}], folderSolicitudes.getDias_licencia_utilizados_solicitantes())
        self.assertEquals([{}], folderSolicitudes.getDias_comision_utilizados_solicitantes())

        self.assertTrue(folderSolicitudes.actualizarPeriodo())

        self.assertEquals([{}], folderSolicitudes.getPresupuesto_asignado_solicitantes())
        self.assertEquals([{}], folderSolicitudes.getDias_licencia_utilizados_solicitantes())
        self.assertEquals([{}], folderSolicitudes.getDias_comision_utilizados_solicitantes())

    def testSolicitanteCreaSolicitudes(self):
        """ Revisa que la solicitud de licencia se cree correctamente"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'noaceptar')

        self.changeUser('solicitante')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudBecario',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'archivar')

        self.changeUser('solicitante')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudBecario',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')

        self.changeUser('solicitante')

        createdId = folderSolicitudes.invokeFactory(type_name='Solicitud', id='TestSolicitudLicencia', solicitante='investigador')
        self.assertEquals('TestSolicitudLicencia', createdId)

        notify(ObjectInitializedEvent(folderSolicitudes.TestSolicitudLicencia))
        self.assertEquals('investigador', folderSolicitudes.TestSolicitudLicencia.getIdOwner())
        self.failUnless(self.hasPermission('Delete objects', folderSolicitudes.TestSolicitudLicencia))

        createdId = folderSolicitudes.invokeFactory(type_name='SolicitudVisitante', id='TestSolicitudVisitante', solicitante='investigador')
        self.assertEquals('TestSolicitudVisitante', createdId)

        notify(ObjectInitializedEvent(folderSolicitudes.TestSolicitudVisitante))
        self.assertEquals('investigador', folderSolicitudes.TestSolicitudVisitante.getIdOwner())
        self.failUnless(self.hasPermission('Delete objects', folderSolicitudes.TestSolicitudVisitante))

        createdId = folderSolicitudes.invokeFactory(type_name='SolicitudBecario', id='TestSolicitudBecario', solicitante='becario')
        self.assertEquals('TestSolicitudBecario', createdId)

        notify(ObjectInitializedEvent(folderSolicitudes.TestSolicitudBecario))
        self.assertEquals('becario', folderSolicitudes.TestSolicitudBecario.getIdOwner())
        self.failUnless(self.hasPermission('Delete objects', folderSolicitudes.TestSolicitudBecario))

    def testInvestigadorCreaSolicitudes(self):
        """ Revisa que la solicitud de licencia se cree correctamente"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'noaceptar')

        self.changeUser('investigador')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'archivar')

        self.changeUser('investigador')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')

        self.changeUser('investigador')

        createdId = folderSolicitudes.invokeFactory(type_name='Solicitud', id='TestSolicitudLicencia')
        self.assertEquals('TestSolicitudLicencia', createdId)

        createdId = folderSolicitudes.invokeFactory(type_name='SolicitudVisitante', id='TestSolicitudVisitante')
        self.assertEquals('TestSolicitudVisitante', createdId)

    def testTecnicoAcademicoCreaSolicitudes(self):
        """ Revisa que la solicitud de licencia se cree correctamente"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'noaceptar')

        self.changeUser('tecnico')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'archivar')

        self.changeUser('tecnico')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')

        self.changeUser('tecnico')

        createdId = folderSolicitudes.invokeFactory(type_name='Solicitud', id='TestSolicitudLicencia')
        self.assertEquals('TestSolicitudLicencia', createdId)

        createdId = folderSolicitudes.invokeFactory(type_name='SolicitudVisitante', id='TestSolicitudVisitante')
        self.assertEquals('TestSolicitudVisitante', createdId)

    def testPostdocCreaSolicitudes(self):
        """ Revisa que la solicitud de licencia se cree correctamente"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'noaceptar')

        self.changeUser('postdoc')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'archivar')

        self.changeUser('postdoc')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')

        self.changeUser('postdoc')

        createdId = folderSolicitudes.invokeFactory(type_name='Solicitud', id='TestSolicitudLicencia')
        self.assertEquals('TestSolicitudLicencia', createdId)

        createdId = folderSolicitudes.invokeFactory(type_name='SolicitudVisitante', id='TestSolicitudVisitante')
        self.assertEquals('TestSolicitudVisitante', createdId)

    def testBecarioCreaSolicitudes(self):
        """ Revisa que un becario pueda crear solicitudes de becario"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'noaceptar')

        self.changeUser('becario')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudBecario',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'archivar')

        self.changeUser('becario')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudBecario',
        )

        self.changeUser('manager')
        self.portal.portal_workflow.doActionFor(folderSolicitudes, 'aceptar')

        self.changeUser('becario')

        createdId = folderSolicitudes.invokeFactory(type_name='SolicitudBecario', id='TestSolicitudBecario')
        self.assertEquals('TestSolicitudBecario', createdId)

    def testSoloCrearTiposAutorizados(self):
        """ Revisa que la solicitud de licencia se cree correctamente"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('becario')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.changeUser('investigador')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )
        self.changeUser('postdoc')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )

        self.changeUser('tecnico')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )

    def testRevisoresNoCreanSolicitudes(self):
        """ Revisa que la solicitud de licencia se cree correctamente"""
        folderSolicitudes = self.portal.folderSolicitudes

        self.changeUser('comisionado')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )

        self.changeUser('responsablecomision')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )

        self.changeUser('consejero')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )

        self.changeUser('responsableconsejo')
        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='Solicitud',
            id='TestSolicitudLicencia',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudVisitante',
            id='TestSolicitudVisitante',
        )

        self.failUnlessRaises(Unauthorized,
            folderSolicitudes.invokeFactory,
            type_name='SolicitudBecario',
            id='TestSolicitudLicencia',
        )

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestsDeCreacion))
    return suite
