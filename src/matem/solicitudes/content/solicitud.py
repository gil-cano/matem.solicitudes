# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent
from archetypes.multifile.MultiFileField import MultiFileField
from archetypes.multifile.MultiFileWidget import MultiFileWidget
from datetime import datetime
from DateTime.DateTime import DateTime
from matem.solicitudes import solicitudesMessageFactory as _
from matem.solicitudes.config import AREAS_INVESTIGACION
from matem.solicitudes.config import getCountriesVocabulary
from matem.solicitudes.config import LICENCEDAYS
from matem.solicitudes.config import PROJECTNAME
from matem.solicitudes.config import SEDE
from matem.solicitudes.extender import PersonWrapper
from matem.solicitudes.interfaces import ISolicitud
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import BaseContent
from Products.Archetypes.atapi import BaseSchema
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import ComputedField
from Products.Archetypes.atapi import ComputedWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import LabelWidget
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.atapi import PicklistWidget
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.ATCountryWidget.config import COUNTRIES
from Products.CMFCore.utils import getToolByName
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL
from zope.interface import implements


from Products.DataGridField.Column import Column
from matem.solicitudes.widgets.conference import DataGridConferenceField
from matem.solicitudes.widgets.conference import ConferenceWidget
from matem.solicitudes.widgets.course import DataGridCourseField
from matem.solicitudes.widgets.course import CourseWidget
from matem.solicitudes.widgets.sresearch import DataGridSResearchField
from matem.solicitudes.widgets.sresearch import SResearchWidget
from matem.solicitudes.widgets.assistance import DataGridAssistanceField
from matem.solicitudes.widgets.assistance import AssistanceWidget
from matem.solicitudes.widgets.organization import DataGridOrganizationField
from matem.solicitudes.widgets.organization import OrganizationWidget

from matem.solicitudes.widgets.other import DataGridOtherField
from matem.solicitudes.widgets.other import OtherWidget

from Products.DataGridField.SelectColumn import SelectColumn
# from Products.DataGridField.LinesColumn import LinesColumn
# from Products.DataGridField.DateColumn import DateColumn
# from Products.DataGridField.DatetimeLocalColumn import DatetimeLocalColumn
from collective.datagridcolumns.DateColumn import DateColumn
from collective.datagridcolumns.MultiSelectColumn import MultiSelectColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn


# from Products.DataGridField.CheckboxColumn import CheckboxColumn

from matem.solicitudes.widgets.vocabularies import ConferenceTypeVocabulary
from matem.solicitudes.widgets.vocabularies import ConferenceAssistantVocabulary

from matem.solicitudes.widgets.vocabularies import CourselevelVocabulary
# from matem.solicitudes.widgets.vocabularies import CoursetypeVocabulary

# from matem.solicitudes.widgets.vocabularies import ResearchPositionVocabulary

from matem.solicitudes.widgets.vocabularies import EventTypeVocabulary
from matem.solicitudes.widgets.vocabularies import BooleanTypeVocabulary


import sys


schema = BaseSchema + Schema((
    ComputedField(
        name='title',
        required=1,
        searchable=1,
        expression="((here.getOwner() and 'Solicitud (%s) de %s por %s (%s, %s, %s)' % (here.getLicenciacomision(),here.getNombreOwner(), here.getTotal(), here.getCiudadPais(), here.getInstitucion(), here.getFechaDesde() )) or 'Nueva solicitud')",
        accessor='Title',
        widget=ComputedWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    ComputedField(
        name='text',
        required=0,
        searchable=1,
        expression="""(here.getOwner() and '%s %s %s %s %s' %
                    (here.esSolcitudBorrador(), here.esSolcitudPendiente(),
                    here.setFechaSolicitud(), here.esAcuseRecibo(),
                    here.setFechaSesionCI() ))""",
        widget=ComputedWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    ComputedField(
        name='description',
        required=0,
        searchable=1,
        expression="(here.getOwner() and ' %s, %s ' % (here.getWFTitle(), here.getWFTString() ))",
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    StringField(
        name='id',
        required=0,
        searchable=1,
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    StringField(
        name='sede',
        required=0,
        searchable=1,
        vocabulary=SEDE,
        widget=SelectionWidget(
            label='Sede',
            label_msgid='label_sede',
            i18n_domain='matem.solicitudes',
            description='Especifica de donde es el investigador que pide la licencia',
            description_msgid='help_sede',
            visible={'view': 'invisible', 'edit': 'invisible'},
        ),
    ),

    StringField(
        name='solicitante',
        searchable=0,
        required=1,
        vocabulary='getCreators',
        default_method='getSolicitanteDefault',
        widget=SelectionWidget(
            label="Solicitante",
            label_msgid="label_solicitante",
            i18n_domain='matem.solicitudes',
            description=_(u'help_sol_solicitante', default=u'Researcher Name'),
            # description="Nombre del investigador a nombre del cual es esta solicitud.",
            # description_msgid="help_solicitante",
        ),
        write_permission="Solicitud: Cambiar Solicitante",
    ),

    StringField(
        name='nombre_owner',
        searchable=0,
        required=0,
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    StringField(
        name='mensaje_licencias',
        widget=LabelWidget(
            label=u'Recuerde que el número máximo de días de Licencia es 45. Si los rebasa consulte con la Secretaría Académica.',
            label_msgid='label_mensaje_licencias',
            i18n_domain='matem.solicitudes',
            visible={'view': 'invisible', 'edit': 'visible'}
        ),
    ),

    StringField(
        name='licenciacomision',
        searchable=1,
        required=1,
        default='Licencia',
        # vocabulary=DisplayList((
        #     ('Licencia', 'Licencia'), ('Comision', 'Comision')
        # )),
        vocabulary=DisplayList((
            ('Licencia', _(u'Licencia')), ('Comision', _(u'Comision'))
        )),
        widget=SelectionWidget(
            label='Tipo de solicitud',
            label_msgid='label_licenciacomision',
            i18n_domain='matem.solicitudes',
            description=_(u'help_sol_licenciacomision', default=u'Licencia/Comision'),
            # description='Especifica si esta es una solicitud de comisión o de licencia',
            # description_msgid='help_licenciacomision',
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    LinesField(
        name='pais',
        required=True,
        default=('MX'),
        widget=SelectionWidget(
            label='Country',
            label_msgid='label_pais',
            description='Country to visit',
            description_msgid='help_pais',
            i18n_domain='matem.solicitudes',
        ),
        vocabulary="getCountriesVocabulary",
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='ciudad_pais',
        searchable=1,
        required=1,
        widget=StringWidget(
            label='City',
            label_msgid='label_ciudad_pais',
            i18n_domain='matem.solicitudes',
            description='City to visit',
            description_msgid='help_ciudad_pais',
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='institucion',
        searchable=1,
        required=1,
        widget=StringWidget(
            label='Institution',
            label_msgid='label_institucion',
            i18n_domain='matem.solicitudes',
            description='Institution to visit',
            description_msgid='help_institucion'
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    DateTimeField(
        name='fecha_desde',
        searchable=1,
        required=1,
        default_method='getDefaultDate',
        widget=CalendarWidget(
            label='Start date',
            label_msgid='label_fecha_desde',
            i18n_domain='matem.solicitudes',
            description=_(u'help_sol_fecha_desde', default=u'Date on wich the visit will start (it can be approximate)'),
            # description='Date on wich the visit will start (it can be approximate)',
            # description_msgid='help_fecha_desde',
            starting_year=2011,
            future_years=1,
            show_hm=False,
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    DateTimeField(
        name='fecha_hasta',
        searchable=1,
        required=1,
        default_method='getDefaultDate',
        widget=CalendarWidget(
            label='End date',
            label_msgid='label_fecha_hasta',
            i18n_domain='matem.solicitudes',
            description=_(u'help_sol_fecha_hasta', default=u'Date on wich the visit will end (it can be approximate)'),
            # description='Date on wich the visit will end (it can be approximate)',
            # description_msgid='help_fecha_hasta',
            starting_year=2011,
            future_years=1,
            show_hm=False,
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    LinesField(
        name='investigacionarea',
        required=1,
        default=(),
        widget=PicklistWidget(
            label='Research areas',
            label_msgid='label_investigacionarea',
            description=_(u'help_sol_investigacionarea', default=u'Doubts about the classification and how to find an area, go to the official website of the <a href=\"http://www.ams.org/msc\">ams</a>'),
            # description="Doubts about the classification and how to find an area, go to the official website of the <a href=\"http://www.ams.org/msc\">ams</a>",
            # description_msgid='help_investigacionarea',
            i18n_domain='matem.solicitudes',
        ),
        multiValued=1,
        vocabulary=AREAS_INVESTIGACION,
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='trabajo',
        searchable=1,
        required=0,
        default='No',
        # vocabulary=DisplayList((
        #     ('No', 'No'), ('Si', 'Si')
        # )),
        vocabulary=DisplayList((
            ('No', _(u'No')), ('Si', _(u'Si'))
        )),
        widget=MasterSelectWidget(
            label='Paper',
            label_msgid='label_trabajo',
            i18n_domain='matem.solicitudes',
            description='Specify if a paper will be presented',
            description_msgid='help_trabajo',
            slave_fields=({
                'name': 'titulo_trabajo',
                'action': 'hide',
                'hide_values': ('No',),
            },),
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='titulo_trabajo',
        searchable=1,
        required=0,
        default='',
        widget=TextAreaWidget(
            label='Title of the work to be presented',
            label_msgid='label_titulo_trabajo',
            i18n_domain='matem.solicitudes',
            description='Enter the title of the paper to present',
            description_msgid='help_titulo_trabajo',
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='warning',
        widget=LabelWidget(
            label=u'Especifique las cantidades que desea se carguen a su asignación anual (cantidades que usará de otras fuentes como proyectos CONACYT/PAPIIT no se deben especificar aquí)',
            visible={'view': 'invisible', 'edit': 'visible'},
        ),
    ),

    StringField(
        name='cargo_presupuesto',
        required=1,
        # vocabulary=DisplayList((
        #     ('Asignación anual', 'Asignación anual'),
        #     ('Apoyo institucional', 'Apoyo institucional')
        # )),
        vocabulary=DisplayList((
            ('Asignación anual', _(u'Asignación anual')),
            ('Apoyo institucional', _(u'Apoyo institucional'))
        )),
        default='Asignación anual',
        widget=SelectionWidget(
            label='Con cargo a',
            label_msgid='label_cargo_a',
            i18n_domain='matem.solicitudes',
            description="Seleccione el presupuesto de donde se descontara el total de está solicitud",
            description_msgid='help_cargo_a',
            visible={'view': 'invisible', 'edit': 'invisible'},
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='pasaje',
        searchable=1,
        required=0,
        default='',
        # vocabulary=DisplayList((
        #     ('No', _(u'No')), ('si', _(u'Si'))
        # )),
        vocabulary=DisplayList((
            ('No', _(u'No')), ('si', _(u'Si'))
        )),
        widget=MasterSelectWidget(
            label='Transportation expenses',
            label_msgid='label_pasaje',
            i18n_domain='matem.solicitudes',
            description='Specify if the airfare or other travel expenses are requested',
            description_msgid='help_pasaje',
            slave_fields=({
                'name': 'tipo_pasaje',
                'action': 'hide',
                'hide_values': ('No',),
            }, {
                'name': 'cantidad_pasaje',
                'action': 'hide',
                'hide_values': ('No',),
            },),
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    LinesField(
        name='tipo_pasaje',
        required=0,
        default=(),
        widget=MultiSelectionWidget(
            label='Transportation means',
            i18n_domain='matem.solicitudes',
            label_msgid='label_tipo_pasaje',
            description="Specify the type of travel mean to be used'",
            description_msgid='help_tipo_pasaje',
            format='checkbox',
        ),
        multiValued=1,
        vocabulary=DisplayList((
            ('auto', _(u'Car')),
            ('autobus', _(u'Bus')),
            ('avion', _(u'Airplane'))
        )),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    FloatField(
        name='cantidad_pasaje',
        searchable=1,
        required=1,
        default='0',
        relationship="c_pasaje",
        widget=StringWidget(
            label='Transportation cost',
            label_msgid='label_cantidad_pasaje',
            i18n_domain='matem.solicitudes',
            description="Amount requested for travel expenses in mexican pesos",
            description_msgid='help_cantidad_pasaje',
            tarifas=False,
            size=12,
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='viaticos',
        searchable=1,
        required=0,
        default='No',
        vocabulary=DisplayList((
            ('No', _(u'No')), ('Si', _(u'Si'))
        )),
        widget=MasterSelectWidget(
            label='Travel allowances',
            label_msgid='label_viaticos',
            i18n_domain='matem.solicitudes',
            description='Specify if daily expenses are requested. 900 daily pesos (Mexico) and 1200 daily pesos (other countries), it is necessary to deliver receipts for the total',
            description_msgid='help_viaticos',
            slave_fields=({
                'name': 'cantidad_viaticos',
                'action': 'hide',
                'hide_values': ('No',),
            }, {
                'name': 'schoolPractices',
                'action': 'hide',
                'hide_values': ('No',),
            },)
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    BooleanField(
        name='schoolPractices',
        default=False,
        widget=BooleanWidget(
            label=_(u'label_school_practices', default=u"School practices"),
            description=_(u'help_school_practices', default=u"Only Students and Posdoc from Cuernavaca"),
            i18n_domain='matem.solicitudes',),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    FloatField(
        name='cantidad_viaticos',
        searchable=1,
        required=1,
        default='0',
        relationship="viaticos",
        widget=StringWidget(
            label='Travel allowances',
            label_msgid='label_cantidad_viaticos',
            i18n_domain='matem.solicitudes',
            description="Amount requested for travel allowances, in mexican pesos",
            description_msgid='help_cantidad_viaticos',
            tarifas=False,
            size=12
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='inscripcion',
        searchable=1,
        required=0,
        default='No',
        vocabulary=DisplayList((
            ('No', _(u'No')), ('Si', _(u'Si'))
        )),
        widget=MasterSelectWidget(
            label='Registration',
            label_msgid='label_inscripcion',
            i18n_domain='matem.solicitudes',
            description='Specify if the registration cost is requested',
            description_msgid='help_inscripcion',
            slave_fields=({
                'name': 'cantidad_inscripcion',
                'action': 'hide',
                'hide_values': ('No',),
            },)
        ),
        # read_permission="Solicitud: Modificar Solicitud",
        write_permission="Solicitud: Modificar Solicitud",
    ),

    FloatField(
        name='cantidad_inscripcion',
        searchable=1,
        required=1,
        default='0',
        relationship="inscripcion",
        widget=StringWidget(
            label='Registration amount',
            label_msgid='label_cantidad_inscripcion',
            i18n_domain='matem.solicitudes',
            description="Amount requested for registration in mexican pesos",
            description_msgid='help_cantidad_inscripcion',
            tarifas=False,
            size=12),
        # read_permission="Solicitud: Modificar Solicitud",
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='fecha_solicitud',
        searchable=1,
        required=0,
        default='',
        widget=StringWidget(
            label='Date of application',
            label_msgid='label_fecha_solicitud',
            i18n_domain='matem.solicitudes',
            description='Date on which the request is sent',
            description_msgid='help_fecha_solicitud',
            visible={'view': 'invisible', 'edit': 'hidden'},
        ),
        # read_permission="Solicitud: Modificar Solicitud",
        write_permission="Solicitud: Modificar Solicitud",
    ),

    MultiFileField(
        name='displayAttachments',
        primary=True,
        languageIndependent=True,
        storage=AnnotationStorage(migrate=True),
        widget=MultiFileWidget(
            label="Attachments",
            label_msgid='label_adjuntos',
            description="Please attach invitation letter or any other related documents",
            description_msgid='help_adjuntos',
            show_content_type=False,
            i18n_domain='matem.solicitudes',
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='comentario_owner',
        searchable=1,
        required=0,
        default='',
        widget=TextAreaWidget(
            label='Additional comments',
            label_msgid='label_comentario_owner',
            i18n_domain='matem.solicitudes',
            description="Add any comment that you consider important for your request",
            description_msgid='help_comentario_owner',
            tarifas=False,
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    DateTimeField(
        name='fecha_sesionce',
        searchable=1,
        required=1,
        default_method='',
        widget=CalendarWidget(
            label='Fecha de Revisión por la Comisión Especial',
            label_msgid='label_fecha_sesionce',
            i18n_domain='matem.solicitudes',
            description='Fecha en que la comisión revisó la solicitud.',
            description_msgid='help_fecha_sesionce',
            starting_year=2010,
            future_years=1,
            show_hm=False
        ),
        read_permission="Solicitud: Comision Revisa Solicitud",
        write_permission="Solicitud: Comision Revisa Solicitud",
    ),

    # Campos CE
    StringField(
        name='comentario_ce',
        searchable=1,
        required=0,
        default='',
        widget=TextAreaWidget(
            label='Recommendation by Special Commission',
            label_msgid='label_comentario_ce',
            i18n_domain='matem.solicitudes',
            description="Add any comment related to your recommendation for this request",
            description_msgid='help_comentario_ce',
            tarifas=False,
        ),
        read_permission="Solicitud: Comision Revisa Solicitud",
        write_permission="Solicitud: Comision Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_recomendada_pasaje',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_recomendada_pasaje', default=u'Recommended amount for transportation expenses'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Comision Revisa Solicitud",
        write_permission="Solicitud: Comision Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_recomendada_viaticos',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_recomendada_viaticos', default=u'Recommended amount for travel allowences'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Comision Revisa Solicitud",
        write_permission="Solicitud: Comision Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_recomendada_inscripcion',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_recomendada_inscripcion', default=u'Recommended amount for registration'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Comision Revisa Solicitud",
        write_permission="Solicitud: Comision Revisa Solicitud",
    ),

    StringField(
        name='recomienda_aprobar',
        searchable=0,
        required=1,
        vocabulary=DisplayList((
            ('No', _(u'No')), ('Si', _(u'Si'))
        )),
        default='Si',
        widget=SelectionWidget(
            label='Recomiendo Aprobar',
            label_msgid='label_recomienda_aprobar',
            i18n_domain='matem.solicitudes',
        ),
        read_permission="Solicitud: Comision Revisa Solicitud",
        write_permission="Solicitud: Comision Revisa Solicitud",
    ),

    # Campos CI
    StringField(
        name='comentario_ci',
        searchable=1,
        required=0,
        default='',
        widget=TextAreaWidget(
            label='Comments by Consejo Interno',
            label_msgid='label_comentario_ci',
            i18n_domain='matem.solicitudes',
            description="Add any comment related to the resolution taken for this request",
            description_msgid='help_comentario_ci',
            tarifas=False,
        ),
        read_permission="Solicitud: Consejo Revisa Solicitud",
        write_permission="Solicitud: Consejo Revisa Solicitud",
    ),

    DateTimeField(
        name='fecha_sesionci',
        searchable=1,
        required=1,
        default_method='',
        widget=CalendarWidget(
            label='Date of revision by the CI',
            label_msgid='label_fecha_sesionci',
            i18n_domain='matem.solicitudes',
            description='Date on which the request was revised',
            description_msgid='help_fecha_sesionci',
            starting_year=2010,
            future_years=1,
            show_hm=False,
        ),
        read_permission="Solicitud: Consejo Revisa Solicitud",
        write_permission="Solicitud: Consejo Revisa Solicitud",
    ),

    StringField(
        name='actaci',
        searchable=1,
        required=0,
        default='',
        widget=StringWidget(
            label='Numero de acta de CI',
            label_msgid='acta_number',
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Revisa Solicitud",
        write_permission="Solicitud: Consejo Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_consejo_pasaje',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_consejo_pasaje', default=u'Approved amount for transportation expenses'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Revisa Solicitud",
        write_permission="Solicitud: Consejo Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_consejo_viaticos',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_consejo_viaticos', default=u'Approved amount for travel allowences'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Revisa Solicitud",
        write_permission="Solicitud: Consejo Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_consejo_inscripcion',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_consejo_inscripcion', default=u'Approved amount for registration'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Revisa Solicitud",
        write_permission="Solicitud: Consejo Revisa Solicitud",
    ),

    FloatField(
        name='cantidad_autorizada_pasaje',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_autorizada_pasaje', default=u'Approved amount for transportation expenses'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Cambia Solicitud",
        write_permission="Solicitud: Consejo Cambia Solicitud",
    ),

    FloatField(
        name='cantidad_autorizada_viaticos',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_autorizada_viaticos', default=u'Approved amount for travel allowences'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Cambia Solicitud",
        write_permission="Solicitud: Consejo Cambia Solicitud",
    ),

    FloatField(
        name='cantidad_autorizada_inscripcion',
        searchable=1,
        required=1,
        default='0.0',
        widget=StringWidget(
            label=_(u'label_cantidad_autorizada_inscripcion', default=u'Approved amount for registration'),
            i18n_domain='matem.solicitudes',
            tarifas=False,
            size=12,
        ),
        read_permission="Solicitud: Consejo Cambia Solicitud",
        write_permission="Solicitud: Consejo Cambia Solicitud",
    ),

    BooleanField(
        name='estadoBorrador',
        label="Review data, if it is correct, you should send it to revision, by selecting 'state: solicitud no enviada' then 'enviar solicitud' inside the transitions menu in the top right corner",
        label_msgid='label_estado_borrador',
        default=False,
        widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
    ),

    BooleanField(
        name='estadoPendiente',
        label="Review data, if it is correct, you should send it to revision, by selecting 'state: pendiente' then 'reenviar solicitud' inside the transitions menu in the top right corner",
        label_msgid='label_estado_pendiente',
        default=False,
        widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
    ),

    BooleanField(
        name='acuseRecibo',
        label="Your request has been received successfully, you can print this page as acknowledgement of receipt",
        label_msgid='label_acuse_recibo',
        default=False,
        widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
    ),

    DataGridAssistanceField(
        name='assistance',
        columns=(
            'eventtype',
            'eventName',
            'place',
            'institution',
            'assistancedate'
        ),
        widget=AssistanceWidget(
            label=_(u"label_widgetassistance", default=u"Only Assists"),
            # description=_(u'help_widgetassistance', default=u'Use this option in only assistance'),
            helper_js=('datagridwidget.js', 'datagriddatepicker.js'),
            columns={
                'eventtype': SelectColumn(
                    _(u"weventtype_label", default="Event Type"),
                    vocabulary=EventTypeVocabulary(),
                ),
                'eventName': Column(
                    _(u"weventname_label", default=u"Event Name"),
                ),
                'place': Column(
                    _(u"wplace_label", default=u"Place"),
                ),
                'institution': Column(
                    _(u"winstitution_label", default=u"Institution"),
                ),
                'assistancedate': DateColumn(
                    _(u"wassistancedate_label", default=u"Date"),
                    date_format="dd/mm/yy",
                ),
            },
        ),
    ),

    DataGridConferenceField(
        name='conferences',
        columns=(
            'eventtype',
            'title',
            'eventName',
            'institution',
            'isplenary',
            'participationtype',
            'conferencetype',
            'place',
            'conferencedate',
            'assistallevent',
        ),
        widget=ConferenceWidget(
            label=_(u"label_widgetconferences", default=u"Conferences"),
            # description=_(u'help_widgetconferences', default=u'Use this option if you give a talk'),
            helper_js=(
                'datagridwidget.js',
                'datagridwidget_patches.js',
                'datagridmultiselect.js',
                'datagriddatepicker.js'
            ),
            columns={
                'eventtype': SelectColumn(
                    _(u"weventtype_label", default="Event Type"),
                    vocabulary=EventTypeVocabulary(),
                ),
                'title': Column(
                    _(u"wtitle_conference_label", default=u"Title"),
                ),
                'eventName': Column(
                    _(u"weventname_label", default=u"Event Name"),
                ),
                'institution': Column(
                    _(u"winstitution_label", default=u"Institution"),
                ),
                'isplenary': SelectColumn(
                    _(u"wisplenary_label", default="Is your conference plenary or masterly?"),
                    vocabulary=BooleanTypeVocabulary(),
                ),
                'participationtype': SelectColumn(
                    _(u"wcparticipationtype_label", default="Participation type"),
                    vocabulary=ConferenceAssistantVocabulary(),
                ),
                'conferencetype': MultiSelectColumn(
                    _(u"wconferencetype_label", default="Conference type"),
                    vocabulary_factory='matem.solicitudes.vocabularies.ConferenceType',
                ),
                'place': Column(
                    _(u"wplace_label", default=u"Place"),
                ),
                'conferencedate': DateColumn(
                    _(u"wconferencedate_label", default=u"Date"),
                    date_format="dd/mm/yy",
                ),
                'assistallevent': SelectColumn(
                    _(u"wassistallevent_label", default="Are you going to all congress?"),
                    vocabulary=BooleanTypeVocabulary(),
                ),
            },
        ),
    ),

    DataGridCourseField(
        name='courses',
        columns=(
            'title',
            'duration',
            'eventName',
            'institution',
            'level',
            'otherlevel',
            'place',
            'coursetype',
            'coursedate'
        ),
        widget=CourseWidget(
            label=_(u"label_widgetcourses", default=u"Courses"),
            helper_js=('datagridwidget.js', 'datagriddatepicker.js'),
            columns={
                'title': Column(
                    _(u"wtitle_course_label", default=u"Title"),
                ),
                'duration': Column(
                    _(u"wduration_course_label", default=u"Duration in hours"),
                ),
                'eventName': Column(
                    _(u"weventname_label", default=u"Event Name"),
                ),
                'institution': Column(
                    _(u"winstitution_label", default=u"Institution"),
                ),
                'level': SelectColumn(
                    _(u"wlevel_label", default="Level"),
                    vocabulary=CourselevelVocabulary(),
                ),
                'otherlevel': Column(
                    _(u"wotherlevel_label", default=u"If you select \"Other\" in Level, please indicate it"),
                ),

                'place': Column(
                    _(u"wplace_label", default=u"Place"),
                ),
                'coursetype': MultiSelectColumn(
                    _(u"wcoursetype_label", default="Coursetype"),
                    vocabulary_factory='matem.solicitudes.vocabularies.ConferenceType',
                ),
                'coursedate': DateColumn(
                    _(u"wcoursedate_label", default=u"Date"),
                    date_format="dd/mm/yy",
                ),
            },
        ),
    ),

    DataGridSResearchField(
        name='sresearch',
        columns=(
            'hostresearcher',
            'objective',
            'institution',
            'sresearchdate'
        ),
        widget=SResearchWidget(
            label=_(u"label_widgetsresearch", default=u"Research Stay"),
            helper_js=('datagridwidget.js', 'datagriddatepicker.js'),
            columns={
                'hostresearcher': Column(
                    _(u"whostresearcher_label", default=u"Host"),
                ),
                'objective': TextAreaColumn(
                    _(u"wobjective_label", default=u"Objective"),
                ),
                'institution': Column(
                    _(u"winstitution_label", default=u"Institution"),
                ),
                'sresearchdate': DateColumn(
                    _(u"sresearchdate_label", default=u"Date"),
                    date_format="dd/mm/yy",
                ),
            },
        ),
    ),

    DataGridOrganizationField(
        name='organization',
        columns=(
            'eventName',
            'imposition',
            'researcherposition',
            'sessionName',
            'activitytype',
            'level',
            'speakersint',
            'speakersnac',
            'assistants',
            'organizationdate',
        ),
        widget=OrganizationWidget(
            label=_(u"label_widgetorganization", default=u"Organized Activities"),
            helper_js=('datagridwidget.js', 'datagriddatepicker.js'),
            columns={
                'eventName': Column(
                    _(u"weventname_label", default=u"Event Name"),
                ),
                # 'imposition': Column(
                #     _(u"wimposition_label", default=u"IM Position"),
                # ),
                'imposition': MultiSelectColumn(
                    _(u"wimposition_label", default="IM Position"),
                    vocabulary_factory='matem.solicitudes.vocabularies.IMPosition',
                ),
                'researcherposition': MultiSelectColumn(
                    _(u"wresearchposition_label", default="Researcher Position"),
                    vocabulary_factory='matem.solicitudes.vocabularies.ResearcherPosition',
                ),
                'sessionName': Column(
                    _(u"wsessionName_label", default=u"If you are Responsible of session, please indicate the session name"),
                ),
                'activitytype': MultiSelectColumn(
                    _(u"wactivitytype_label", default="Activity Type"),
                    vocabulary_factory='matem.solicitudes.vocabularies.ConferenceType',
                ),
                'level': MultiSelectColumn(
                    _(u"wlevel_label", default="Level"),
                    vocabulary_factory='matem.solicitudes.vocabularies.Courselevel',
                    # vocabulary=CourselevelVocabulary(),
                ),
                'speakersint': Column(
                    _(u"wspeakersint_label", default=u"Expected number of International Speakers"),
                ),
                'speakersnac': Column(
                    _(u"wspeakersnac_label", default=u"Expected number of National Speakers"),
                ),
                'assistants': Column(
                    _(u"wassistants_label", default=u"Expected number of Assistants"),
                ),
                'organizationdate': DateColumn(
                    _(u"worganizationdate_label", default=u"Date"),
                    date_format="dd/mm/yy",
                ),

            },
        ),
    ),

    # For the new version this field is for other activity
    StringField(
        name='objeto_viaje',
        searchable=1,
        # required=1,
        accessor='ObjetoViaje',
        widget=TextAreaWidget(
            label=_(u"label_sol_otheractivity", default=u"Other Activities"),
            # label='Objective',
            # label_msgid='label_objeto_viaje',
            i18n_domain='matem.solicitudes',
            description=_(u'help_sol_otheractivity', default=u'Enter the other activities'),
            # description='Enter the other activities',
            # description_msgid='help_sol_otheractivity',
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

))

for f in schema.filterFields(isMetadata=True):
    f.widget.visible = {"edit": "invisible"}


class Solicitud(BaseContent):
    """Request License Commission"""

    implements(ISolicitud)

    security = ClassSecurityInfo()
    schema = schema

    _at_rename_after_creation = False

    # This method is only called once after object creation.
    security.declarePrivate('at_post_create_script')

    def at_post_create_script(self):
        if self.getLicenciacomision() == 'Licencia':
            folder = self.aq_parent
            balance = folder.getBalance(self.getIdOwner())
            remainig_days = LICENCEDAYS - balance['licence_days']
            if self.getCantidadDeDias() > remainig_days:
                self.setLicenciacomision('Comision')

    def canSetDefaultPage(self):
        return False

    def post_validate(self, REQUEST=None, errors=None):
        """Validates start and end date
        End date must be after start date.
        If There is more than 15 days image is required.
        """
        if 'fecha_desde' not in REQUEST or 'fecha_hasta' not in REQUEST:
            # No point in validating bad input
            return

        rstartDate = REQUEST.get('fecha_desde', None)
        rendDate = REQUEST.get('fecha_hasta', None)

        try:
            end = DateTime(rendDate)
        except Exception:
            errors['fecha_hasta'] = u'La fecha de término no es valida'

        try:
            start = DateTime(rstartDate)
        except Exception:
            errors['fecha_desde'] = u'La fecha de inicio no es valida'

        if 'fecha_desde' in errors or 'fecha_hasta' in errors:
            # No point in validating bad input
            return

        if start > end:
            errors['fecha_hasta'] = u'La fecha de término debe ser posterior a la de inicio'

        lassistance = REQUEST.get('assistance', [])
        lconferences = REQUEST.get('conferences', [])
        lcourses = REQUEST.get('courses', [])
        lsresearch = REQUEST.get('sresearch', [])
        lorganization = REQUEST.get('organization', [])

        atleasterror = self.atleastwidget(
            REQUEST.get('objeto_viaje', ''),
            lassistance,
            lconferences,
            lcourses,
            lsresearch,
            lorganization,
        )
        if atleasterror:
            k = atleasterror.keys()[0]
            errors[k] = atleasterror[k]

        # Add validators for widgtes date in range
        widgetserrors = self.validateDateInRange(
            'assistance',
            'assistancedate',
            lassistance,
            start,
            end
        )

        widgetserrors.update(
            self.validateDateInRange(
                'conferences',
                'conferencedate',
                lconferences,
                start,
                end
            )
        )

        widgetserrors.update(
            self.validateDateInRange(
                'courses',
                'coursedate',
                lcourses,
                start,
                end
            )
        )

        widgetserrors.update(
            self.validateDateInRange(
                'sresearch',
                'sresearchdate',
                lsresearch,
                start,
                end
            )
        )

        widgetserrors.update(
            self.validateIntNumbers(
                'organization',
                ['speakersint', 'speakersnac', 'assistants'],
                lorganization,
            )
        )

        widgetserrors.update(
            self.validateDateInRange(
                'organization',
                'organizationdate',
                lorganization,
                start,
                end
            )
        )

        for k, v in widgetserrors.iteritems():
            errors[k] = v

    def atleastwidget(self, otheractivity, lassistance, lconferences, lcourses, lsresearch, lorganization):

        atleasterror = {}
        if (len(lassistance) >= 2) or (len(lconferences) >= 2) or (len(lcourses) >= 2) or (len(lsresearch) >= 2) or (len(lorganization) >= 2):
            return atleasterror

        if otheractivity:
            return atleasterror

        atleasterror['objeto_viaje'] = u'La solicitud debe tener al menos una actividad'
        return atleasterror

    def validateIntNumbers(self, fieldName, columnsnumber, rows):
        columnerrors = {}
        for row in rows:
            if row['orderindex_'] != 'template_row_marker':
                for columnN in columnsnumber:
                    if row[columnN] == '':
                        continue
                    try:
                        rowvalue = int(row[columnN])
                    except Exception:
                        columnerrors[fieldName] = u'El valor del número esperado debe ser un número entero positivo'
                        return columnerrors
                    if rowvalue < 0:
                        columnerrors[fieldName] = u'El valor del número esperado debe ser un número entero positivo'
        return columnerrors

    def validateDateInRange(self, fieldName, columndate, rows, dstart, dend):
        fielderrors = {}
        for row in rows:
            if row['orderindex_'] != 'template_row_marker':
                try:
                    # is necesarily change the order for the widget format
                    rowitem = row[columndate].split('/')
                    rowdate = DateTime(rowitem[2] + rowitem[1] + rowitem[0])
                except Exception:
                    fielderrors[fieldName] = u'La fecha no es válida'
                    return fielderrors
                if (rowdate < dstart) or (rowdate > dend):
                    fielderrors[fieldName] = u'La fecha no está en el rango de fechas de la solicitud'
                #     return translate(
                #         "Validation failed: The year, sponsor and amount are required, please correct.",
                #         domain='UNAM.imateCVct',
                #         context=kwargs['REQUEST'],
                #         default=_("Validation failed: The year, sponsor and amount are required, please correct.")
        return fielderrors

    def addTranslation(self, language, **kwargs):
        # call orginal addTranslation
        BaseContent.addTranslation(self, language, **kwargs)
        o = self.getTranslation()

        # copy images to new object
        for obj in self.objectValues():
            id = obj.getId()
            o.manage_pasteObjects(self.manage_copyObjects(id))
            copied_object = getattr(o, id)
            copied_object.setLanguage(language)

    def getCreationDate(self):
        dt = self.CreationDate().split()
        return dt[0]

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

    def toState(self, State):
        workflowTool = getToolByName(self, "portal_workflow")
        mt = getToolByName(self, "portal_membership")
        member = mt.getAuthenticatedMember()
        nivel = 0

        if not State.lower().find("com") == -1:
            nivel = 1
        elif not State.lower().find("con") == -1 or not State.lower().find("cou") == -1:
            nivel = 2
        elif not State.lower().find("ap") == -1:
            nivel = 3

        if "Importador de Solicitudes" in list(member.getRoles()):
            if nivel > 0:
                workflowTool.doActionFor(self, 'enviar', comment='')
            if nivel > 1:
                workflowTool.doActionFor(self, 'enviaraconsejo', comment='')
            if nivel > 2:
                workflowTool.doActionFor(self, 'aprobar', comment='')
        return

    def getWFTransitionDate(self):
        workflowTool = getToolByName(self, "portal_workflow")
        current_date = workflowTool.getInfoFor(self, 'time', None)
        return current_date

    def getWFTString(self):
        wf_date = "%s" % self.getWFTransitionDate()
        return wf_date[0:10]

    def setFechaSolicitud(self):
        f = self.getField('fecha_solicitud')
        if (f.get(self) == ''):
            wf_state = self.getWFState()
            wfts = self.getWFTString()
            if (wf_state == 'RevisaAdminCE'):
                f.set(self, wfts)
        return

    def setFechaSesionCI(self):
        f = self.getField('fecha_sesionci')
        wf_state = self.getWFState()
        rolesAct = self.getActualRoles()
        if (wf_state == 'RevisionCI'):
            for role in rolesAct:
                if (role == 'Manager' or role == 'admin'):
                    f.set(self, DateTime())
        return

    def getActualRoles(self):
        user = self.getIdActual()
        return user.getRolesInContext(aq_parent(self))

    def getWFTitle(self):
        wf_state = self.getWFState()
        if (wf_state == 'SolicitudBecario'):
            wf_title = 'Solicitud no enviada al tutor'
        elif (wf_state == 'SolicitudBorrador'):
            wf_title = 'Solicitud no enviada'
        elif (wf_state == 'RevisaAdminCE'):
            wf_title = 'Solicitud enviada sin revisar'
        elif (wf_state == 'RevisionCI'):
            wf_title = 'Solicitud Turnada al CI'
        elif (wf_state == 'Aprobada'):
            wf_title = 'Solicitud Aprobada'
        elif (wf_state == 'Pendiente'):
            wf_title = 'Solicitud Pendiente'
        elif (wf_state == 'Retirada'):
            wf_title = 'Solicitud retirada'
        else:
            wf_title = ''
        return wf_title

    def esSolcitudBecario(self):
        f = self.getField('estadoBecario')
        if (self.getWFState() == 'SolicitudBecario'):
            if (('%s' % self.getIdOwner()) == ('%s' % self.getIdActual())):
                f.set(self, True)
        else:
            f.set(self, False)
        return f.get(self)

    def esSolcitudBorrador(self):
        f = self.getField('estadoBorrador')
        if (self.getWFState() == 'SolicitudBorrador'):
            if (('%s' % self.getIdOwner()) == ('%s' % self.getIdActual())):
                f.set(self, True)
        else:
            f.set(self, False)
        return f.get(self)

    def esSolcitudPendiente(self):
        f = self.getField('estadoPendiente')
        if (self.getWFState() == 'Pendiente'):
            if (('%s' % self.getIdOwner()) == ('%s' % self.getIdActual())):
                f.set(self, True)
        else:
            f.set(self, False)
        return f.get(self)

    def esAcuseRecibo(self):
        f = self.getField('acuseRecibo')
        if (self.getWFState() != 'SolicitudBorrador' and self.getWFState() != 'SolicitudBecario'):
            if (('%s' % self.getIdOwner()) == ('%s' % self.getIdActual())):
                f.set(self, True)
        else:
            f.set(self, False)
        return f.get(self)

    def setWFState(self):
        workflowTool = getToolByName(self, "portal_workflow")
        workflowTool.doActionFor(self, "EnviarSolicitud", comment='')
        return

    def getIdActual(self):
        mt = getToolByName(self, 'portal_membership')
        return mt.getAuthenticatedMember()

    def getNombreActual(self):
        fsdperson = self.getPersonWrapper(self.getIdActual())
        return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()

    def getIdCreator(self):
        return self.getOwner().getId()

    def getIdOwner(self):
        return self.getOwner().getId()

    def getNombreOwner(self):
        creator = self.getIdOwner()
        try:
            fsdperson = self.getPersonWrapper(creator)
            return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()
        except Exception:
            # print "Error Solicitud no encontrada persona " + creator + ", " + self.getId()
            return creator

    def getFechaSolicitud(self):
        return self.getField('fecha_solicitud').get(self)

    def getCiudadPais(self):
        return self.getField('ciudad_pais').get(self)

    def getPaisCodigo(self):
        return self.getField('pais').get(self)

    def getPais(self):
        pais = self.getField('pais').get(self)
        try:
            pais = COUNTRIES[pais[0]]
            return pais
        except Exception:
            pais = ""
            return pais

    def getInvestigacionArea(self):
        return self.getField('investigacionarea').get(self)

    def getTituloTrabajo(self):
        return self.getField('titulo_trabajo').get(self)

    def getInstitucion(self):
        return self.getField('institucion').get(self)

    # Estos metodos de fecha fueron cambiados
    def getFechaDesde(self):
        return DateTime(self.getField('fecha_desde').get(self))

    def getFechaHasta(self):
        return DateTime(self.getField('fecha_hasta').get(self))

    def getObjetoViaje(self):
        act1 = self.getField('assistance').getAccessor(self)()
        act2 = self.getField('conferences').getAccessor(self)()
        act3 = self.getField('courses').getAccessor(self)()
        act4 = self.getField('sresearch').getAccessor(self)()
        act5 = self.getField('organization').getAccessor(self)()
        resumen = []
        if len(act1) > 0:
            resumen.append('Sólo asistencias ' + str(len(act1)))
        if len(act2) > 0:
            resumen.append('Conferencias a impartir' + str(len(act2)))
        if len(act3) > 0:
            resumen.append('Cursos a impartir' + str(len(act3)))
        if len(act4) > 0:
            resumen.append('Estancias de Investigación ' + str(len(act4)))
        if len(act5) > 0:
            resumen.append('Organización de Actividades ' + str(len(act5)))

        return self.getField('objeto_viaje').get(self) + ' ' + ', '.join(resumen)

    def getComentarioCI(self):
        return self.getField('comentario_ci').get(self)

    def getSolicitanteDefault(self):
        mt = getToolByName(self, 'portal_membership')
        member = mt.getAuthenticatedMember()
        tupla = (member.getId(),)

        return tupla

    def getCreators(self):
        ''' return list of Researchers
        '''
        portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog(
            portal_type='FSDPerson',
            person_classification=['investigadores', 'tecnicos-academicos', 'posdoc'],
            sort_on='getSortableName',
            review_state='active',
        )
        users = []
        for brain in brains:
            person = brain.getObject()
            tupla = (
                person.getId(),
                person.getLastName() + ", " + person.getFirstName() + " " + person.getMiddleName()
            )
            users.append(tupla)
        return DisplayList(users)

    def setCantidadPasaje(self):
        f = self.getField('cantidad_pasaje')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadPasaje(self):
        try:
            f = self.setCantidadPasaje()
            return self.getCantidad(f)
        except Exception:
                a = sys.exc_info()
                raise a[0], a[1], a[2]

    def setCantidadViaticos(self):
        f = self.getField('cantidad_viaticos')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadViaticos(self):
        try:
            f = self.setCantidadViaticos()
            return self.getCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadInscripcion(self):
        f = self.getField('cantidad_inscripcion')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadInscripcion(self):
        try:
            f = self.setCantidadInscripcion()
            return self.getCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizadaPasaje(self):
        f = self.getField('cantidad_autorizada_pasaje')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaPasaje(self):
        try:
            f = self.setCantidadAutorizadaPasaje()
            return self.getCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizadaViaticos(self):
        f = self.getField('cantidad_autorizada_viaticos')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaViaticos(self):
        try:
            f = self.setCantidadAutorizadaViaticos()
            return self.getCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizadaInscripcion(self):
        f = self.getField('cantidad_autorizada_inscripcion')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaInscripcion(self):
        try:
            f = self.setCantidadAutorizadaInscripcion()
            return self.getCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizada(self):
        f = self.getField('cantidad_autorizada')
        try:
            return self.setCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizada(self):
        try:
            f = self.setCantidadAutorizada()
            return self.getCantidad(f)
        except Exception:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidad(self, field):
        f = field
        if (f.get(self) == ''):
            return ''
        else:
            f1 = '%s' % f.get(self)
            f2 = "".join(f1.split(','))
            try:
                f.set(self, ('%s' % float(f2)))
                return f.get(self)
            except Exception:
                a = sys.exc_info()
                raise a[0], a[1], a[2]

    def getCantidad(self, field):
        try:
            f = field
            if (f == ''):
                return 0.0
            else:
                return float(f)
        except Exception:
                a = sys.exc_info()
                raise a[0], a[1], a[2]

    def getTotal(self):
        pasaje = self.getCantidadPasaje()
        viaticos = self.getCantidadViaticos()
        inscripcion = self.getCantidadInscripcion()
        return (pasaje + viaticos + inscripcion)

    def getCantidadAutorizadaTotal(self):
        pasaje = self.getCantidadAutorizadaPasaje()
        viaticos = self.getCantidadAutorizadaViaticos()
        inscripcion = self.getCantidadAutorizadaInscripcion()
        return (pasaje + viaticos + inscripcion)

    def getCantidadConsejoTotal(self):
        pasaje = self.getCantidad_consejo_pasaje()
        viaticos = self.getCantidad_consejo_viaticos()
        inscripcion = self.getCantidad_consejo_inscripcion()
        return (pasaje + viaticos + inscripcion)

    def getCantidadRecomendadaTotal(self):
        pasaje = self.getCantidad_recomendada_pasaje()
        viaticos = self.getCantidad_recomendada_viaticos()
        inscripcion = self.getCantidad_recomendada_inscripcion()
        return (pasaje + viaticos + inscripcion)

    def pasarValorComisionado(self):
        pasaje = self.getCantidadPasaje()
        viaticos = self.getCantidadViaticos()
        inscripcion = self.getCantidadInscripcion()

        self.setCantidad_recomendada_pasaje(pasaje)
        self.setCantidad_recomendada_viaticos(viaticos)
        self.setCantidad_recomendada_inscripcion(inscripcion)
        return

    def pasarValorConsejero(self):
        self.setComentario_ci(self.getComentario_ce())
        self.setCantidad_consejo_pasaje(self.getCantidad_recomendada_pasaje())
        self.setCantidad_consejo_viaticos(
            self.getCantidad_recomendada_viaticos())
        self.setCantidad_consejo_inscripcion(
            self.getCantidad_recomendada_inscripcion())
        return

    def pasarValorAutorizado(self):
        pasaje = self.getCantidad_consejo_pasaje()
        viaticos = self.getCantidad_consejo_viaticos()
        inscripcion = self.getCantidad_consejo_inscripcion()

        self.setCantidad_autorizada_pasaje(pasaje)
        self.setCantidad_autorizada_viaticos(viaticos)
        self.setCantidad_autorizada_inscripcion(inscripcion)
        return

    def sendMail(self, state='aprobada'):
        mt = getToolByName(self, 'portal_membership')
        member = mt.getMemberById(self.getIdOwner())
        mail_to = member.getProperty('email', None)
        mail_from = 'solicitudes@matem.unam.mx'
        subject = '[matem] Su solicitud ha sido ' + state
        msg = """
Su solicitud de %s - %s, %s, del %s al %s ha sido %s.

Objetivo: %s

Para más información vaya a %s.

Las siguientes cantidades se refieren a su asignación anual:

La cantidad que se le ha autorizado en esta solicitud: %s.
La cantidad total que se le ha aprobado en lo que va del año: %s.

Cantidad total de días de licencia aprobados en lo que va del año: %d
Cantidad total de días de comisión aprobados en lo que va del año: %d

Nota: Si en su viaje dispuso de una cantidad menor de recursos, deberá acudir a la administración del Instituto para que los datos sean corregidos.
------------------------------------------------------------------
Éste es un correo electrónico automático, por favor no lo responda
"""
        msg = msg % (self.getLicenciacomision(),
                     self.getInstitucion(),
                     self.getPais(),
                     self.getFechaDesde().strftime('%d/%m/%Y'),
                     self.getFechaHasta().strftime('%d/%m/%Y'),
                     state,
                     self.getObjetoViaje(),
                     self.absolute_url(),
                     self.getCantidadConsejoTotal(),
                     self.aq_parent.getPresupuesto_asignado_solicitantes()[0].get(self.getIdOwner(), 0.0),
                     self.aq_parent.getDias_licencia_utilizados_solicitantes()[0].get(self.getIdOwner(), 0),
                     self.aq_parent.getDias_comision_utilizados_solicitantes()[0].get(self.getIdOwner(), 0))
        getToolByName(self, 'MailHost').send(msg, mail_to, mail_from, subject)
        return

    def getCantidadDeDias(self):
        # metodo original
        # t1=str(self.getFecha_desde()).split("/")
        # t2=str(self.getFecha_hasta()).split("/")
        # d1=datetime(int(t1[0]),int(t1[1]),int(t1[2]))
        # d2=datetime(int(t2[0]),int(t2[1]),int(t2[2]))
        # return int((d2-d1).days)+1

        t1 = str(DateTime(self.getFecha_desde())).split("/")
        t2 = str(DateTime(self.getFecha_hasta())).split("/")
        d1 = datetime(int(t1[0]), int(t1[1]), int(t1[2].split(" ")[0]))
        d2 = datetime(int(t2[0]), int(t2[1]), int(t2[2].split(" ")[0]))
        return int((d2 - d1).days) + 1

    def actualizarInvestigador(self):
        folder = self.aq_parent

        solicitante = self.getIdOwner()
        dias = self.getCantidadDeDias()
        if (dias < 0):
            dias = 0

        if(self.getLicenciacomision() == "Licencia"):
            esComision = False
        else:
            esComision = True

        folder.sumarACantidadAutorizada(
            esComision, self.getCantidadAutorizadaTotal(), dias, solicitante, self.getCargo_presupuesto())
        return

    def desactualizarInvestigador(self):
        folder = self.aq_parent

        solicitante = self.getIdOwner()
        dias = self.getCantidadDeDias()
        if (dias < 0):
            dias = 0

        if(self.getLicenciacomision() == "Licencia"):
            esComision = False
        else:
            esComision = True

        folder.restarACantidadAutorizada(
            esComision, self.getCantidadAutorizadaTotal(), dias, solicitante)
        return

    def aprobada(self):
        wf_state = self.getWFState()
        if (wf_state == 'aprobada'):
            return True

    def rechazada(self):
        wf_state = self.getWFState()
        if (wf_state == 'rechazada'):
            return True

    def recomiendaAprobar(self):
        if self.getRecomienda_aprobar() == "Si":
            return True
        else:
            return False

    def enviada(self):
        wf_state = self.getWFState()
        if (wf_state == 'revisioncomision' or wf_state == 'revisionconsejo'):
            return True

    def enviadaTexto(self):
        wf_state = self.getWFState()
        if (wf_state == 'revisioncomision'):
            return "Revision por Comision Especial"
        elif (wf_state == 'revisionconsejo'):
            return "Revision por Consejo Interno"

    def getDefaultDate(self):
        return DateTime('2016/1/1')

    def getPersonWrapper(self, userid):
        mb = getToolByName(self, MEMBRANE_TOOL)
        person = mb.getUserObject(user_id=userid)
        fsdperson = PersonWrapper(person)
        return fsdperson

    def getCountriesVocabulary(self):
        # This function is defined in config.py
        return getCountriesVocabulary(self)

    def getAddExtraTopInformation(self):
        """ Return information dependent of application type and user
        """
        if self.getWFState() != 'borrador':
            return None

        folder = self.aq_parent
        mt = getToolByName(self, 'portal_membership')
        member = mt.getAuthenticatedMember()
        roles = member.getRoles()
        if 'Solicitante Auxiliar' in roles and 'Manager' not in roles:
            return None
        balance = folder.getBalance(member.getId())
        if not balance:
            return None

        money = balance['yearly'] - balance['yearly_spent']
        return [
            {
                'label': _(u'Available Annual Allocation'),
                'quantity': '${0:,.2f}'.format(money)
            },
            {
                'label': _(u'Available licence days'),
                'quantity': LICENCEDAYS - balance['licence_days']
            },
        ]

registerType(Solicitud, PROJECTNAME)
