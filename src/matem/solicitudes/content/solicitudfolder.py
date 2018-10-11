# -*- coding: utf-8 -*-

from matem.solicitudes.config import PROJECTNAME
from matem.solicitudes.extender import PersonWrapper
from matem.solicitudes.interfaces import ISolicitudFolder
from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import registerType
from Products.ATExtensions.field.records import RecordsField
from Products.ATExtensions.widget.records import RecordsWidget
from Products.CMFCore.utils import getToolByName
from zope.interface import implements


from matem.solicitudes import solicitudesMessageFactory as _
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.SelectColumn import SelectColumn
from collective.datagridcolumns.MultiSelectColumn import MultiSelectColumn
from matem.solicitudes.widgets.vocabularies import SolResponsibleVocabulary


import logging

logger = logging.getLogger("Plone")

schema = ATFolder.schema.copy() + Schema((

    DateTimeField(
        'fecha_desde',
        searchable=1,
        required=1,
        widget=CalendarWidget(
            label='Start date',
            label_msgid='label_fecha_desde_folder',
            i18n_domain='plone',
            description='Date on which this period starts',
            description_msgid='help_fecha_desde_folder',
            show_hm=False
        ),
    ),

    DateTimeField(
        'fecha_hasta',
        searchable=1,
        required=1,
        widget=CalendarWidget(
            label='End date',
            label_msgid='label_fecha_hasta_folder',
            i18n_domain='plone',
            description='Date on which this period ends',
            description_msgid='help_fecha_hasta_folder',
            show_hm=False
        ),
    ),

    DataGridField(
        name='useresponsible',
        columns=('nameresponsable', 'sede'),
        widget=DataGridWidget(
            label=_(u"label_widget_useresponsible", default=u"Responsibles for view"),
            # helper_js=('datagridwidget.js', 'datagriddatepicker.js', 'datagrid_course.js'),
            helper_js=('datagridwidget.js', 'datagridwidget_patches.js', 'datagridmultiselect.js',),
            columns={
                'nameresponsable': SelectColumn(
                    _(u"useresponsible_nameresponsable_label", default="Responsable name"),
                    vocabulary=SolResponsibleVocabulary(),
                ),
                'sede': MultiSelectColumn(
                    _(u"useresponsible_sede_label", default="Campus"),
                    vocabulary_factory='matem.solicitudes.vocabularies.IMCampus',
                ),
            },
        ),
    ),

    FloatField(
        'presupuesto_inicial',
        searchable=1,
        required=0,
        default=0.0,
        widget=StringWidget(
            label='Total Budget',
            label_msgid='label_presupuesto_total',
            i18n_domain='plone',
            description='Total amount of assignable budget',
            description_msgid='help_presupuesto_total',
            visible=False
        ),
    ),

    FloatField(
        'presupuesto_asignado',
        searchable=1,
        required=0,
        default=0.0,
        widget=StringWidget(
            label='Assigned Budget',
            label_msgid='label_presupuesto_asignado',
            i18n_domain='plone',
            description='Total amount of already assigned budget',
            description_msgid='help_presupuesto_asignado',
            visible=False
        ),
    ),

    FloatField(
        'presupuesto_maximo_investigadores',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    FloatField(
        'presupuesto_maximo_becarios',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    FloatField(
        'presupuesto_maximo_tecnicos',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    FloatField(
        'presupuesto_maximo_postdocs',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    RecordsField(
        'solicitantes',
        default=[{}],
        widget=RecordsWidget(visible=False),
    ),

    RecordsField(
        'presupuesto_asignado_solicitantes',
        default=[{}],
        widget=RecordsWidget(visible=False),
    ),

    RecordsField(
        'dias_licencia_utilizados_solicitantes',
        default=[{}],
        widget=RecordsWidget(visible=False),
    ),

    RecordsField(
        'dias_comision_utilizados_solicitantes',
        default=[{}],
        widget=RecordsWidget(visible=False),
    ),

    FloatField(
        'apoyoinst_maximo_investigadores',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    FloatField(
        'apoyoinst_maximo_becarios',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    FloatField(
        'apoyoinst_maximo_tecnicos',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    FloatField(
        'apoyoinst_maximo_postdocs',
        searchable=0,
        required=0,
        default=0.0,
        widget=StringWidget(visible=False),
    ),

    RecordsField(
        'apoyoinst_asignado_solicitantes',
        default=[{}],
        widget=RecordsWidget(visible=False),
    ),
))


class SolicitudFolder(ATFolder):
    "A simple folder content type."

    implements(ISolicitudFolder)

    schema = schema

    _at_rename_after_creation = True

    def canSetDefaultPage(self):
        return False

    def getWFState(self):
        workflowTool = getToolByName(self, "portal_workflow")
        current_state = workflowTool.getInfoFor(self, 'review_state', None)
        return current_state

    def getWFStateName(self):
        workflowTool = getToolByName(self, "portal_workflow")
        current_state = workflowTool.getInfoFor(self, 'review_state', None)
        statename = workflowTool.getTitleForStateOnType(current_state, self.meta_type)
        return statename

    def getLegalTransitions(self):
        workflowTool = getToolByName(self, "portal_workflow")
        transitions = workflowTool.getTransitionsFor(self)
        return transitions

    def aceptando(self):
        wf_state = self.getWFState()
        if (wf_state == 'aceptando'):
            return True
        else:
            return False

    def historico(self):
        wf_state = self.getWFState()
        if (wf_state == 'historico'):
            return True
        else:
            return False

    def restante(self):
        return (self.getPresupuesto_inicial() - self.getPresupuesto_asignado())

    def sumarACantidadAutorizada(self, esComision, cantidad, dias, idCreador, cargo):
        try:
            cantidad = float(cantidad)
            dias = int(dias)
            if cargo.find('institucional') != -1:
                dictcargo = self.getApoyoinst_asignado_solicitantes()[0]
            else:
                dictcargo = self.getPresupuesto_asignado_solicitantes()[0]
                self.setPresupuesto_asignado(cantidad + self.getPresupuesto_asignado())
            try:
                dictcargo[idCreador] += cantidad
            except:
                dictcargo[idCreador] = cantidad

            if esComision is not None:

                if not esComision:
                    try:
                        dictDiasLicencia = self.getDias_licencia_utilizados_solicitantes()[0]
                        dictDiasLicencia[idCreador] += dias
                    except:
                        dictDiasLicencia[idCreador] = dias
                    self.setDias_licencia_utilizados_solicitantes(dictDiasLicencia)
                else:
                    try:
                        dictDiasComision = self.getDias_comision_utilizados_solicitantes()[0]
                        dictDiasComision[idCreador] += dias
                    except:
                        dictDiasComision[idCreador] = dias
                    self.setDias_comision_utilizados_solicitantes(dictDiasComision)

            return True
        except:
            return False

    def restarACantidadAutorizada(self, esComision, cantidad, dias, idCreador):
        try:
            cantidad = float(cantidad)
            dias = int(dias)

            try:
                dictPresupuesto = self.getPresupuesto_asignado_solicitantes()[0]
                dictPresupuesto[idCreador] -= cantidad
            except:
                dictPresupuesto[idCreador] = 0.0

            if esComision is not None:

                if not esComision:
                    try:
                        dictDiasLicencia = self.getDias_licencia_utilizados_solicitantes()[0]
                        dictDiasLicencia[idCreador] -= dias
                    except:
                        dictDiasLicencia[idCreador] = 0
                    self.setDias_licencia_utilizados_solicitantes(dictDiasLicencia)
                else:
                    try:
                        dictDiasComision = self.getDias_comision_utilizados_solicitantes()[0]
                        dictDiasComision[idCreador] -= dias
                    except:
                        dictDiasComision[idCreador] = 0.0
                    self.setDias_comision_utilizados_solicitantes(dictDiasComision)

            cantidad = self.getPresupuesto_asignado() - cantidad
            self.setPresupuesto_asignado(cantidad)
            self.setPresupuesto_asignado_solicitantes(dictPresupuesto)
            return True
        except:
            return False

    def actualizarPeriodo(self):
        """ Recalculate users and expenses
        """
        cantidadAutorizada = 0.0
        # dictionaries of current expenses
        dictPresupuesto = self.encontrarSolicitantes()
        dictApoyoInst = dict(dictPresupuesto)
        dictDiasLicencia = dict(dictPresupuesto)
        dictDiasComision = dict(dictPresupuesto)

        self.setPresupuesto_asignado(cantidadAutorizada)
        self.setPresupuesto_asignado_solicitantes(dictPresupuesto)
        self.setApoyoinst_asignado_solicitantes(dictApoyoInst)
        self.setDias_licencia_utilizados_solicitantes(dictDiasLicencia)
        self.setDias_comision_utilizados_solicitantes(dictDiasComision)

        for obj in self.objectValues(['Solicitud', 'SolicitudInstitucional', 'SolicitudVisitante', 'SolicitudBecario']):
            if obj.aprobada():
                cantidadAutorizadaSolicitud = obj.getCantidadAutorizadaTotal()
                cantidadDiasAprobados = obj.getCantidadDeDias()

                # TODO: verificar a donde se deve cargar esta solicitud
                # se esta cargando presupuesto anual y apoyo institucional
                cantidadAutorizada += cantidadAutorizadaSolicitud

                if obj.getCargo_presupuesto().find('institucional') != -1:
                    presupuesto = obj.getCantidadAutorizadaPasaje() + obj.getCantidadAutorizadaViaticos() + obj.getCantidadAutorizadaInscripcion()
                    dictPresupuesto.setdefault(obj.getIdOwner(), 0)
                    dictPresupuesto[obj.getIdOwner()] += presupuesto

                    apoyo = obj.getCantidad_autorizada_pasaje_apoyo() + obj.getCantidad_autorizada_viaticos_apoyo() + obj.getCantidad_autorizada_inscripcion_apoyo()
                    dictApoyoInst.setdefault(obj.getIdOwner(), 0)
                    dictApoyoInst[obj.getIdOwner()] += apoyo
                else:
                    dictPresupuesto.setdefault(obj.getIdOwner(), 0)
                    dictPresupuesto[obj.getIdOwner()] += cantidadAutorizadaSolicitud

                if obj.meta_type in ['Solicitud', 'SolicitudInstitucional']:
                    if obj.getLicenciacomision() == "Comision":
                        dictDiasComision.setdefault(obj.getIdOwner(), 0)
                        dictDiasComision[obj.getIdOwner()] += cantidadDiasAprobados
                    else:
                        dictDiasLicencia.setdefault(obj.getIdOwner(), 0)
                        dictDiasLicencia[obj.getIdOwner()] += cantidadDiasAprobados
                elif obj.meta_type == "SolicitudBecario":
                    dictDiasLicencia.setdefault(obj.getIdOwner(), 0)
                    dictDiasLicencia[obj.getIdOwner()] += cantidadDiasAprobados
        try:
            self.setPresupuesto_asignado(cantidadAutorizada)
            self.setPresupuesto_asignado_solicitantes(dictPresupuesto)
            self.setApoyoinst_asignado_solicitantes(dictApoyoInst)
            self.setDias_licencia_utilizados_solicitantes(dictDiasLicencia)
            self.setDias_comision_utilizados_solicitantes(dictDiasComision)
        except:
            return False

        return True

    def encontrarSolicitantes(self):
        fsd_tool = getToolByName(self, "facultystaffdirectory_tool")
        mt = getToolByName(self, "portal_membership")
        member = mt.getAuthenticatedMember()
        dictSolicitantes = {}
        dictVacio = {}
        append = False
        presupuestoMaximo = 0
        apoyoinstMaximo = 0

        if 'Programador de Presupuesto' not in list(member.getRoles()):
            return {}

        solicitantes = list(fsd_tool.getDirectoryRoot().getSortedPeople())

        for person in solicitantes:
            try:
                fsdperson = PersonWrapper(person)
                user = mt.getMemberById(person.getId())
            except:
                logger.info("Error encontrando solicitantes")
                continue

            if 'Postdoc' in list(user.getRoles()):
                rol = "Postdoc"
                presupuestoMaximo = self.getPresupuesto_maximo_postdocs()
                apoyoinstMaximo = self.getApoyoinst_maximo_postdocs()
                append = True
            elif 'Investigador' in list(user.getRoles()):
                rol = "Investigador"
                presupuestoMaximo = self.getPresupuesto_maximo_investigadores()
                apoyoinstMaximo = self.getApoyoinst_maximo_investigadores()
                append = True
            elif 'Tecnico Academico' in list(user.getRoles()):
                rol = "Tecnico Academico"
                presupuestoMaximo = self.getPresupuesto_maximo_tecnicos()
                apoyoinstMaximo = self.getApoyoinst_maximo_tecnicos()
                append = True
            elif 'Becario' in list(user.getRoles()):
                rol = "Becario"
                presupuestoMaximo = self.getPresupuesto_maximo_becarios()
                apoyoinstMaximo = self.getApoyoinst_maximo_becarios()
                append = True

            if append:
                dictVacio[person.getId()] = 0
                dictSolicitantes[person.getId()] = [
                    fsdperson.getLastName(),
                    fsdperson.getFirstName(),
                    fsdperson.getMiddleName(),
                    rol,
                    presupuestoMaximo,
                    apoyoinstMaximo
                ]
            append = False
        self.setSolicitantes(dictSolicitantes)

        return dictVacio

    def getBalance(self, userid):
        """ Return details of userid
        """
        # solicitantes is a list of one dict!!!
        # every value in the dict is of the form
        # ['app', 'name', '', 'classification', 20000.0, 10000.0]
        userdata = self.getSolicitantes()[0].get(userid, None)
        if not userdata:
            return {}

        balance = {}
        balance['yearly'] = userdata[4]
        balance['yearly_spent'] = self.getPresupuesto_asignado_solicitantes()[0][userid]
        balance['institutional'] = userdata[5]
        balance['institutional_spent'] = self.getApoyoinst_asignado_solicitantes()[0][userid]
        balance['licence_days'] = self.getDias_licencia_utilizados_solicitantes()[0][userid]
        balance['comission_days'] = self.getDias_comision_utilizados_solicitantes()[0][userid]
        return balance


registerType(SolicitudFolder, PROJECTNAME)
