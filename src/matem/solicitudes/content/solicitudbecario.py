# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from zope.interface import implements
from Products.Archetypes.public import *
from matem.solicitudes.config import *
from matem.solicitudes.interfaces import ISolicitudBecario
from matem.solicitudes.extender import PersonWrapper
from Products.Archetypes.atapi import *

from Products.Archetypes.public import *

from Products.CMFCore.utils import getToolByName
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

from Acquisition import aq_parent
from Products.ATCountryWidget.Widget import CountryWidget
from Products.ATCountryWidget.config import COUNTRIES
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from archetypes.multifile.MultiFileField import MultiFileField
from archetypes.multifile.MultiFileWidget import MultiFileWidget

from DateTime.DateTime import *
from matem.solicitudes.config import getCountriesVocabulary
from matem.solicitudes import solicitudesMessageFactory as _


SolicitudBecarioSchema = BaseSchema + Schema((
    ComputedField(name='title',
        required=1,
        searchable=1,
        expression="((here.getOwner() and 'Solicitud (Becario) de %s (%s en %s, %s, %s)' % (here.getNombreOwner(), here.getCiudadPais(), here.translate(here.getPais()).encode('utf-8'), here.getInstitucion(), here.getFechaDesde().strftime('%d/%m/%Y') )) or 'Nueva solicitud')",
        accessor='Title',
        widget=ComputedWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    ComputedField(name='text',
        required=0,
        searchable=1,
        expression="""(here.getOwner() and '%s %s %s %s %s %s' %
                     (here.esSolcitudBecario(), here.esSolcitudBorrador(),
                     here.esSolcitudPendiente(), here.setFechaSolicitud(),
                     here.esAcuseRecibo(), here.setFechaSesionCI() ))""",
        widget=ComputedWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    ComputedField(name='description',
        required=0,
        searchable=1,
        expression="(here.getOwner() and ' %s, %s ' % (here.getWFTitle(), here.getWFTString() ))",
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    StringField(name='id',
        required=0,
        searchable=1,
        expression=" ",
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    StringField(name='sede',
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

    StringField('solicitante',
        searchable=0,
        required=1,
        vocabulary='getBecarios',
        default_method='getSolicitanteDefault',
        widget=SelectionWidget(
            label="Solicitante",
            label_msgid="label_solicitante",
            i18n_domain='matem.solicitudes',
            description="Nombre del becario a nombre del cual es esta solicitud.",
            description_msgid="help_solicitante",
        ),
        write_permission="Solicitud: Cambiar Solicitante",
    ),

    StringField('nombre_owner',
        searchable=0,
        required=0,
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    ComputedField(name='nombrebecario',
        required=1,
        searchable=1,
        expression="here.getIdOwner()",
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),

    ComputedField(name='nombrecompletobecario',
        required=1,
        searchable=1,
        expression="here.getNombreOwner()",
        widget=StringWidget(
            label='Scholarship holder',
            label_msgid='label_nombre_becario',
            i18n_domain='matem.solicitudes',
            description='Name of the scholarship holder',
            description_msgid='help_nombre_becario',
            visible={'view': 'visible', 'edit': 'visible'}
        ),
    ),

    LinesField(
        name='grado',
        required=1,
        default='',
        vocabulary=DisplayList((
            ('Doctorado', 'PHD'),
            ('Maestria', 'Mastery'),
            ('Licenciatura', 'Undergraduate'),
        )),
        widget=SelectionWidget(
            label='Degree',
            label_msgid='label_grado',
            i18n_domain='matem.solicitudes',
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='asesor',
        required=1,
        vocabulary='getInvestigadores',
        enforceVocabulary=True,
        widget=SelectionWidget(
            label="Advisor",
            label_msgid="label_asesor",
            i18n_domain='matem.solicitudes',
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField('nombre_asesor',
        searchable=0,
        required=0,
        widget=StringWidget(
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
    ),


    LinesField(
          name='pais',
          required=True,
          default=('MX'),
          #storage=atapi.AnnotationStorage(),
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

    # LinesField('pais',
    #     searchable=1,
    #     required=1,
    #     default=('MX'),
    #     widget=CountryWidget(
    #         label='Country',
    #         label_msgid='label_pais',
    #         provideNullValue=1,
    #         omitCountries=None,
    #         description='Country to visit',
    #         description_msgid='help_pais',
    #         i18n_domain='matem.solicitudes',
    #     ),
    #     write_permission="Solicitud: Modificar Solicitud",
    # ),

    StringField('ciudad_pais',
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

    StringField('institucion',
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

    DateTimeField('fecha_desde',
        searchable=1,
        required=1,
        default_method='getDefaultDate',
        widget=CalendarWidget(
            label='Start date',
            label_msgid='label_fecha_desde',
            i18n_domain='matem.solicitudes',
            description='Date on wich the visit will start (it can be approximate)',
            description_msgid='help_fecha_desde',
            starting_year=2011,
            future_years=1,
            show_hm=False
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    DateTimeField('fecha_hasta',
        searchable=1,
        required=1,
        default_method='getDefaultDate',
        widget=CalendarWidget(
            label='End date',
            label_msgid='label_fecha_hasta',
            i18n_domain='matem.solicitudes',
            description='Date on wich the visit will end (it can be approximate)',
            description_msgid='help_fecha_hasta',
            starting_year=2011,
            future_years=1,
            show_hm=False
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField('objeto_viaje',
        searchable=1,
        required=1,
        accessor='ObjetoViaje',
        widget=TextAreaWidget(
            label='Objective',
            label_msgid='label_objeto_viaje',
            i18n_domain='matem.solicitudes',
            description='Enter the expected objective of the visit',
            description_msgid='help_objeto_viaje'
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    LinesField('investigacionarea',
        required=1,
        default=(),
        widget=PicklistWidget(
            label='Research areas',
            label_msgid='label_investigacionarea',
            description="Doubts about the classification and how to find an area, go to the official website of the <a href=\"http://www.ams.org/msc\">ams</a>",
            description_msgid='help_investigacionarea',
            i18n_domain='matem.solicitudes',
        ),
        multiValued=1,
        vocabulary=AREAS_INVESTIGACION,
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='apoyo_extra',
        required=1,
        default='No',
        vocabulary=DisplayList(
            (('No', 'No'), ('Si', 'Si'))),
        widget=MasterSelectWidget(
            label=_(u'label_apoyo_extra', default='Extra support'),
            description=_(u'help_apoyo_extra', default='Specify if you requested support to the post-degree or another instance'),
            i18n_domain='matem.solicitudes',
            slave_fields=({
                'name': 'apoyo_texto',
                'action': 'hide',
                'hide_values': ('Never',),
            },)
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField(
        name='apoyo_texto',
        required=1,
        default='',
        widget=TextAreaWidget(
            label=_(u'label_apoyo_texto', default=u'Detail the obtained support'),
            i18n_domain='matem.solicitudes'),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField('trabajo',
        searchable=1,
        required=0,
        default='No',
        vocabulary=DisplayList((
            ('No', 'No'), ('Si', 'Si')
        )),
        widget=MasterSelectWidget(
            label='Paper',
            label_msgid='label_trabajo',
            i18n_domain='matem.solicitudes',
            description='Specify if a paper will be presented',
            description_msgid='help_trabajo',
            slave_fields=({'name': 'titulo_trabajo',
                           'action': 'hide',
                           'hide_values': ('No',),
                           },)
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField('titulo_trabajo',
        searchable=1,
        required=0,
        default='',
        widget=TextAreaWidget(
            label='Title of the work to be presented',
            label_msgid='label_titulo_trabajo',
            i18n_domain='matem.solicitudes',
            description='Enter the title of the paper to present',
            description_msgid='help_titulo_trabajo'
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField('cargo_presupuesto',
        required=1,
        vocabulary=DisplayList((
            ('Asignación anual', 'Asignación anual'),
            ('Apoyo institucional', 'Apoyo institucional')
        )),
        default='Asignación anual',
        widget=SelectionWidget(label='Con cargo a',
            label_msgid='label_cargo_a',
            i18n_domain='matem.solicitudes',
            description="Seleccione el presupuesto de donde se descontara el total de está solicitud",
            description_msgid='help_cargo_a',
            visible={'view': 'invisible', 'edit': 'invisible'}
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

    StringField('pasaje',
        searchable=1,
        required=0,
        default='',
        vocabulary=DisplayList((('No', 'No'), ('si', 'Si'))),
        widget=MasterSelectWidget(
            label='Transportation expenses',
            label_msgid='label_pasaje',
            i18n_domain='matem.solicitudes',
            description='Specify if the airfare or other travel expenses are requested',
            description_msgid='help_pasaje',
            slave_fields=({'name': 'tipo_pasaje',
                           'action': 'hide',
                           'hide_values': ('No',),
                           },
                           {'name': 'cantidad_pasaje',
                           'action': 'hide',
                           'hide_values': ('No',),
                           },)
        ),
        write_permission="Solicitud: Modificar Solicitud",
    ),

        LinesField('tipo_pasaje',
            required=0,
            default=(),
            widget=MultiSelectionWidget(
                              label='Transportation means',
                              i18n_domain='matem.solicitudes',
                              label_msgid='label_tipo_pasaje',
                              description="Specify the type of travel mean to be used'",
                              description_msgid='help_tipo_pasaje',
                              format='checkbox'),
            multiValued=1,
            vocabulary=DisplayList((
                                    ('auto', 'Car'), ('autobus', 'Bus'), ('avion', 'Airplane')
                                    )),
            write_permission="Solicitud: Modificar Solicitud",
        ),
        FloatField('cantidad_pasaje',
            searchable=1,
            required=1,
            default='0',
            relationship="c_pasaje",
            widget=StringWidget(label='Transportation cost',
                                label_msgid='label_cantidad_pasaje',
                                i18n_domain='matem.solicitudes',
                                description="Amount requested for travel expenses in mexican pesos",
                                description_msgid='help_cantidad_pasaje',
                                tarifas=False,
                                size=12),
            write_permission="Solicitud: Modificar Solicitud",
        ),

    StringField(
        name='viaticos_becario',
        required=0,
        default='No',
        vocabulary=DisplayList(
            (('No', 'No'), ('Si', 'Si'))),
        widget=MasterSelectWidget(
            label='Travel allowances',
            label_msgid='label_viaticos',
            i18n_domain='matem.solicitudes',
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

        FloatField('cantidad_viaticos',
            searchable=1,
            required=1,
            default='0',
            relationship="viaticos",
            widget=StringWidget(label='Travel allowances',
                                label_msgid='label_cantidad_viaticos',
                                i18n_domain='matem.solicitudes',
                                description="Amount requested for travel allowances, in mexican pesos",
                                description_msgid='help_cantidad_viaticos',
                                tarifas=False,
                                size=12),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        StringField('inscripcion',
            searchable=1,
            required=0,
            default='No',
            vocabulary=DisplayList((
                                    ('No', 'No'), ('Si', 'Si')
                                    )),
            widget=MasterSelectWidget(label='Registration',
                                 label_msgid='label_inscripcion',
                                 i18n_domain='matem.solicitudes',
                                 description='Specify if the registration cost is requested',
                                 description_msgid='help_inscripcion',
                                 slave_fields=({'name': 'cantidad_inscripcion',
                                                'action': 'hide',
                                                'hide_values': ('No',),
                                                },)
                                 ),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),
        FloatField('cantidad_inscripcion',
            searchable=1,
            required=1,
            default='0',
            relationship="inscripcion",
            widget=StringWidget(label='Registration amount',
                                label_msgid='label_cantidad_inscripcion',
                                i18n_domain='matem.solicitudes',
                                description="Amount requested for registration in mexican pesos",
                                description_msgid='help_cantidad_inscripcion',
                                tarifas=False,
                                size=12),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        StringField('fecha_solicitud',
            searchable=1,
            required=0,
            default='',
            widget=StringWidget(label='Date of application',
                                  label_msgid='label_fecha_solicitud',
                                  i18n_domain='matem.solicitudes',
                                  description='Date on which the request is sent',
                                  description_msgid='help_fecha_solicitud',
                                  visible={'view': 'invisible', 'edit': 'hidden'}
                                  ),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),



#Archivos ...
        MultiFileField('displayAttachments',
            primary=True,
            languageIndependent=True,
            storage=AnnotationStorage(migrate=True),
            widget=MultiFileWidget(
                     label="Attachments",
                     label_msgid='label_adjuntos',
                     description="Please attach invitation letter or any other related documents",
                     description_msgid='help_adjuntos',
                     show_content_type=False,
                     i18n_domain='matem.solicitudes',),
            write_permission="Solicitud: Modificar Solicitud",
        ),
#Comentarios del asesor
        StringField('comentario_asesor',
            searchable=1,
            required=0,
            default='',
            widget=TextAreaWidget(label='Comments by advisor in charge',
                                label_msgid='label_comentario_asesor',
                                i18n_domain='matem.solicitudes',
                                tarifas=False),
            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Add Solicitud",
        ),


#Comentarios del owner
        StringField('comentario_owner',
            searchable=1,
            required=0,
            default='',
            widget=TextAreaWidget(label='Additional comments',
                                label_msgid='label_comentario_owner',
                                i18n_domain='matem.solicitudes',
                                description="Add any comment that you consider important for your request",
                                description_msgid='help_comentario_owner',
                                tarifas=False),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

#Campos del CE
        DateTimeField('fecha_sesionce',
            searchable=1,
            required=1,
            default_method='',
            widget=CalendarWidget(label='Fecha de Revisión por la Comisión Especial',
                                  label_msgid='label_fecha_sesionce',
                                  i18n_domain='matem.solicitudes',
                                  description='Fecha en que la comisión revisó la solicitud.',
                                  description_msgid='help_fecha_sesionce',
                                  starting_year=2010,
                                  future_years=1,
                                  show_hm=False),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

        StringField('comentario_ce',
            searchable=1,
            required=0,
            default='',
            widget=TextAreaWidget(label='Recommendation by special commission',
                                label_msgid='label_comentario_ce',
                                i18n_domain='matem.solicitudes',
                                description="Add any comment related to your recommendation for this request",
                                description_msgid='help_comentario_ce',
                                tarifas=False),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

        FloatField('cantidad_recomendada_pasaje',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_recomendada_pasaje', default=u'Recommended amount for transportation expenses'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

        FloatField('cantidad_recomendada_viaticos',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_recomendada_viaticos', default=u'Recommended amount for travel allowences'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

        FloatField('cantidad_recomendada_inscripcion',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_recomendada_inscripcion', default=u'Recommended amount for registration'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

        StringField('recomienda_aprobar',
            searchable=0,
            required=1,
            vocabulary=DisplayList((
                                    ('No', 'No'), ('Si', 'Si')
                                    )),
            default='Si',
            widget=SelectionWidget(label='Recomiendo Aprobar',
                                label_msgid='label_recomienda_aprobar',
                                i18n_domain='matem.solicitudes',),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

#Campos del CI
        StringField('comentario_ci',
            searchable=1,
            required=0,
            default='',
            widget=TextAreaWidget(label='Comments by Consejo Interno',
                                label_msgid='label_comentario_ci',
                                i18n_domain='matem.solicitudes',
                                description="Add any comment related to the resolution taken for this request",
                                description_msgid='help_comentario_ci',
                                tarifas=False),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        DateTimeField('fecha_sesionci',
            searchable=1,
            required=1,
            default_method='',
            widget=CalendarWidget(label='Date of revision by the CI',
                                  label_msgid='label_fecha_sesionci',
                                  i18n_domain='matem.solicitudes',
                                  description='Date on which the request was revised',
                                  description_msgid='help_fecha_sesionci',
                                  starting_year=2010,
                                  future_years=1,
                                  show_hm=False),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        StringField('actaci',
            searchable=1,
            required=0,
            default='',
            widget=StringWidget(
                                label='Número de acta de CI',
                                label_msgid='acta_number',
                                i18n_domain='matem.solicitudes',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        FloatField('cantidad_consejo_pasaje',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_consejo_pasaje', default=u'Approved amount for transportation expenses'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        FloatField('cantidad_consejo_viaticos',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_consejo_viaticos', default=u'Approved amount for travel allowences'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        FloatField('cantidad_consejo_inscripcion',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_consejo_inscripcion', default=u'Approved amount for registration'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        FloatField('cantidad_autorizada_pasaje',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_autorizada_pasaje', default=u'Approved amount for transportation expenses'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Consejo Cambia Solicitud",
            write_permission="Solicitud: Consejo Cambia Solicitud",
        ),
        FloatField('cantidad_autorizada_viaticos',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_autorizada_viaticos', default='Approved amount for travel allowences'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Consejo Cambia Solicitud",
            write_permission="Solicitud: Consejo Cambia Solicitud",
        ),
        FloatField('cantidad_autorizada_inscripcion',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(
                label=_(u'label_cantidad_autorizada_inscripcion', default=u'Approved amount for registration'),
                i18n_domain='matem.solicitudes',
                tarifas=False,
                size=12),
            read_permission="Solicitud: Consejo Cambia Solicitud",
            write_permission="Solicitud: Consejo Cambia Solicitud",
        ),
        BooleanField('estadoBecario',
            label="Review data, if it is correct, you should send it to your tutor, by selecting 'state: solicitud no enviada al tutor' then 'enviar al tutor' inside the transitions menu in the top right corner",
            label_msgid='label_estado_becario',
            widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
        ),
        BooleanField('estadoBorrador',
            label="If your request is ready, you should send it to revision, by selecting 'state: solicitud no enviada' then 'enviar solicitud' inside the transitions menu in the top right corner",
            label_msgid='label_estado_borrador',
            widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
        ),
        BooleanField('estadoPendiente',
            label="If your request is ready, you should send it to revision, by selecting 'state: pendiente' then 'reenviar solicitud' inside the transitions menu in the top right corner",
            label_msgid='label_estado_pendiente',
            widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
        ),
        BooleanField('acuseRecibo',
            label="Your request has been received successfully, you can print this page as acknowledgement of receipt",
            label_msgid='label_acuse_recibo',
            default=False,
            widget=BooleanWidget(visible={'view': 'invisible', 'edit': 'hidden'}),
        ),
    ),)


for f in SolicitudBecarioSchema.filterFields(isMetadata=True):
    f.widget.visible = { "edit" : "invisible" }


class SolicitudBecario(BaseContent):
    """Request Scholarship Commission"""

    implements(ISolicitudBecario)

    portal_type = meta_type = 'SolicitudBecario'
    schema = SolicitudBecarioSchema

    _at_rename_after_creation = False

    message_cierre = ''

    def canSetDefaultPage(self):
        return False

    def post_validate(self, REQUEST=None, errors=None):
        """Validates start and end date
        End date must be after start date.
        If There is more than 15 days image is required.
        """
        if not 'fecha_desde' in REQUEST or not 'fecha_hasta' in REQUEST:
            # No point in validating bad input
            return

        rstartDate = REQUEST.get('fecha_desde', None)
        rendDate = REQUEST.get('fecha_hasta', None)

        try:
            end = DateTime(rendDate + ' GMT-5')
        except:
            errors['fecha_hasta'] = u'La fecha de término no es valida'

        try:
            start = DateTime(rstartDate + ' GMT-5')
        except:
            errors['fecha_desde'] = u'La fecha de inicio no es valida'

        # if 'fecha_desde' in errors or 'fecha_hasta' in errors:
        #     # No point in validating bad input
        #     return

        if start > end:
            errors['fecha_hasta'] = u'La fecha de término debe ser posterior a la de inicio'


        # Fix hiden fields errors
        if REQUEST.get('pasaje', '') == 'No':
            try:
                float(REQUEST.get('cantidad_pasaje', 0))
            except Exception:
                del errors['cantidad_pasaje']
                REQUEST['cantidad_pasaje'] = '0.0'
                REQUEST.form['cantidad_pasaje'] = '0.0'

        if REQUEST.get('viaticos_becario', '') == 'No':
            try:
                float(REQUEST.get('cantidad_viaticos', 0))
            except Exception:
                del errors['cantidad_viaticos']
                REQUEST['cantidad_viaticos'] = '0.0'
                REQUEST.form['cantidad_viaticos'] = '0.0'

        if REQUEST.get('inscripcion', '') == 'No':
            try:
                float(REQUEST.get('cantidad_inscripcion', 0))
            except Exception:
                del errors['cantidad_inscripcion']
                REQUEST['cantidad_inscripcion'] = '0.0'
                REQUEST.form['cantidad_inscripcion'] = '0.0'


        # return
        # # TODO: save dates in other space
        # local_roles = self.portal_membership.getAuthenticatedMember().getRolesInContext(self)

        # if 'Manager' not in local_roles:

        #     envios = []
        #     shistory = self.workflow_history.get('solicitud_workflow', [])

        #     for i in shistory:
        #         if i.get('action', None) == 'enviarainvestigador':
        #             envios.append(i.get('time', None))

        #     envios.sort()

        #     # This dates must be the same in getLegalTransitions() method
        #     # and in the class browser/folder.py
        #     close_prep = DateTime('2017/10/15 23:59:00 GMT-5')
        #     close_year = DateTime('2017/12/31 23:59:00 GMT-5')
        #     next_year = DateTime('2018/01/01 00:00:00 GMT-5')

        #     # Inician y terminan en 2017
        #     if start <= close_year and end <= close_year:
        #         if envios:
        #             # Este caso ya no pasará sólo el primer año que se aplique el cirre
        #             if envios[0] > close_prep:
        #                 if REQUEST.get('pasaje', '') == 'si':
        #                     errors['pasaje'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                 if REQUEST.get('viaticos_becario', '') == 'Si':
        #                     errors['viaticos_becario'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                 if REQUEST.get('inscripcion', '') == 'Si':
        #                     errors['inscripcion'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'
        #         else:
        #             if DateTime() > close_prep:
        #                 if REQUEST.get('pasaje', '') == 'si':
        #                     errors['pasaje'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                 if REQUEST.get('viaticos_becario', '') == 'Si':
        #                     errors['viaticos_becario'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                 if REQUEST.get('inscripcion', '') == 'Si':
        #                     errors['inscripcion'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #     # si inician en el 2017 y terminan en el 2018
        #     elif start <= close_year and end >= next_year:

        #         parentid = self.aq_parent.id
        #         # Si viven en el 2017 hay que aplicar cambios de cierre de presupuesto
        #         if parentid == str(close_year.year()):
        #             if envios:
        #                 if envios[0] > close_prep:
        #                     if REQUEST.get('pasaje', '') == 'si':
        #                         errors['pasaje'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                     if REQUEST.get('viaticos_becario', '') == 'Si':
        #                         errors['viaticos_becario'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                     if REQUEST.get('inscripcion', '') == 'Si':
        #                         errors['inscripcion'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'
        #             else:
        #                 if DateTime() > close_prep:
        #                     if REQUEST.get('pasaje', '') == 'si':
        #                         errors['pasaje'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                     if REQUEST.get('viaticos_becario', '') == 'Si':
        #                         errors['viaticos_becario'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #                     if REQUEST.get('inscripcion', '') == 'Si':
        #                         errors['inscripcion'] = u'El cierre de presupuesto ya fue aplicado, por favor elija No'

        #     # End money validator


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


    def getMessageCierre(self):
        return self.message_cierre

    def getLegalTransitions(self):
        workflowTool = getToolByName(self, "portal_workflow")
        transitions = workflowTool.getTransitionsFor(self)
        return transitions
        # # Not validation for Managers
        # local_roles = self.portal_membership.getAuthenticatedMember().getRolesInContext(self)
        # if 'Manager' in local_roles:
        #     self.message_cierre = ''
        #     return transitions

        # envios = []
        # envios_tutor = []

        # shistory = self.workflow_history.get('solicitud_workflow', [])
        # for i in shistory:
        #     if i.get('action', None) == 'enviarainvestigador':
        #         envios.append(i.get('time', None))

        #     if i.get('action', None) == 'enviar':
        #         envios_tutor.append(i.get('time', None))

        # envios.sort()
        # envios_tutor.sort()

        # close_prep = DateTime('2017/10/15 23:59:00 GMT-5')
        # close_year = DateTime('2017/12/31 23:59:00 GMT-5')
        # next_year = DateTime('2018/01/01 00:00:00 GMT-5')

        # start = self.getFechaDesde()  # DateTime('2017/12/01 00:00:00 US/Central')
        # end = self.getFechaHasta()
        # realtransitions = []

        # # Inician y terminan en 2017
        # if start <= close_year and end <= close_year:
        #     if envios:
        #         # Este caso ya no pasará sólo el primer año que se aplique el cirre
        #         if envios[0] > close_prep:
        #             if self.getPasaje() == 'si' or self.getViaticos_becario() == 'Si' or self.getInscripcion() == 'Si':
        #                 for item in transitions:
        #                     if item['id'] != 'enviarainvestigador':
        #                         realtransitions.append(item)
        #                 self.message_cierre = 'Ya se aplicó el cierre de presupuesto: Para ver el botón de Enviar a Investigador, por favor elija No en Pasaje, Viáticos  o Inscripción'
        #                 return realtransitions
        #     else:
        #         if DateTime() > close_prep:
        #             if self.getPasaje() == 'si' or self.getViaticos_becario() == 'Si' or self.getInscripcion() == 'Si':
        #                 for item in transitions:
        #                     if item['id'] != 'enviarainvestigador':
        #                         realtransitions.append(item)
        #                 self.message_cierre = 'Ya se aplicó el cierre de presupuesto: Para ver el botón de Enviar a Investigador, por favor elija No en Pasaje, Viáticos  o Inscripción'
        #                 return realtransitions

        #     if envios_tutor:
        #         if envios_tutor[0] > close_prep:
        #             if self.getPasaje() == 'si' or self.getViaticos_becario() == 'Si' or self.getInscripcion() == 'Si':
        #                 for item in transitions:
        #                     if item['id'] != 'enviar':
        #                         realtransitions.append(item)
        #                 self.message_cierre = 'Ya se aplicó el cierre de presupuesto: Para ver el botón de Enviar, por favor elija No en Pasaje, Viáticos  o Inscripción'
        #                 return realtransitions

        # # si inician en el 2017 y terminan en el 2018
        # elif start <= close_year and end >= next_year:

        #     parentid = self.aq_parent.id
        #     # Si viven en el 2017 hay que aplicar cambios de cierre de presupuesto
        #     if parentid == str(close_year.year()):
        #         if envios:
        #             if self.getPasaje() == 'si' or self.getViaticos_becario() == 'Si' or self.getInscripcion() == 'Si':
        #                 for item in transitions:
        #                     if item['id'] != 'enviarainvestigador':
        #                         realtransitions.append(item)
        #                 self.message_cierre = 'Ya se aplicó el cierre de presupuesto: Para ver el botón de Enviar a Investigador, por favor elija No en Pasaje, Viáticos  o Inscripción'
        #                 return realtransitions
        #         else:
        #             if DateTime() > close_prep:
        #                 if self.getPasaje() == 'si' or self.getViaticos_becario() == 'Si' or self.getInscripcion() == 'Si':
        #                     for item in transitions:
        #                         if item['id'] != 'enviarainvestigador':
        #                             realtransitions.append(item)
        #                     self.message_cierre = 'Ya se aplicó el cierre de presupuesto: Para ver el botón de Enviar a Investigador, por favor elija No en Pasaje, Viáticos  o Inscripción'
        #                     return realtransitions
        #         if envios_tutor:
        #             if envios_tutor[0] > close_prep:
        #                 if self.getPasaje() == 'si' or self.getViaticos_becario() == 'Si' or self.getInscripcion() == 'Si':
        #                     for item in transitions:
        #                         if item['id'] != 'enviar':
        #                             realtransitions.append(item)
        #                     self.message_cierre = 'Ya se aplicó el cierre de presupuesto: Para ver el botón de Enviar, por favor elija No en Pasaje, Viáticos  o Inscripción'
        #                     return realtransitions

        # self.message_cierre = ''
        # return transitions

    def toState(self, State):
        workflowTool = getToolByName(self, "portal_workflow")
        mt = getToolByName(self, "portal_membership")
        member = mt.getAuthenticatedMember()
        nivel = 0

        if not State.lower().find("res") == -1 or not State.lower().find("inv") == -1:
            nivel = 1
        elif not State.lower().find("com") == -1:
            nivel = 2
        elif not State.lower().find("con") == -1 or not State.lower().find("cou") == -1:
            nivel = 3
        elif not State.lower().find("ap") == -1:
            nivel = 4

        if "Importador de Solicitudes" in list(member.getRoles()):
            if nivel > 0:
                workflowTool.doActionFor(self, 'enviarainvestigador', comment='')
                self.manage_addLocalRoles(member.getId(), ('Owner',))
            if nivel > 1:
                workflowTool.doActionFor(self, 'enviar', comment='')
            if nivel > 2:
                workflowTool.doActionFor(self, 'enviaraconsejo', comment='')
            if nivel > 3:
                workflowTool.doActionFor(self, 'aprobar', comment='')
        return

    def getWFTransitionDate(self):
        workflowTool = getToolByName(self, "portal_workflow")
        current_date = workflowTool.getInfoFor(self, 'time', None)
        return current_date

    def getWFTString(self):
        wf_date = "%s" % self.getWFTransitionDate()
        return wf_date[0:10]

    def getPropietario(self):
        return self.getField('propietario')

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

    def setWFState(self, State):
        workflowTool = getToolByName(self, "portal_workflow")
        workflowTool.doActionFor(self, "EnviarSolicitud", comment='')
        return

    def getIdActual(self):
        mt = getToolByName(self, 'portal_membership')
        return mt.getAuthenticatedMember()

    def getNombreActual(self):
#        mt = getToolByName(self, 'portal_membership')
#        member = mt.getAuthenticatedMember()
        member = self.getIdActual()
        fsdperson = self.getPersonWrapper(member.getId())
        return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()

    def getIdOwner(self):
        return self.getOwner().getId()

    def getNombreOwner(self):
#        creator = self.getOwner().getId()
        creator = self.getIdOwner() or ''
        try:
            fsdperson = self.getPersonWrapper(creator)
            return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()
        except:
            print "Error SolicitudBecario no encontrada persona " + creator + ", " + self.getId()
            return creator

    def getNombreCreator(self):
        creator = self.Creator()
        fsdperson = self.getPersonWrapper(creator)
        return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()

    def getIdBecario(self):
        return self.getField('nombrebecario').get(self)

    def getIdCreator(self):
        return self.getField('nombrebecario').get(self)

    def getIdAsesor(self):
        return self.getField('asesor').get(self)

    def getNombreBecario(self):
        fsdperson = self.getPersonWrapper(self.getField('nombrebecario').get(self))
        return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()

    def getNombreAsesor(self):
        fsdperson = self.getPersonWrapper(self.getField('asesor').get(self))
        return fsdperson.getLastName() + ", " + fsdperson.getFirstName() + " " + fsdperson.getMiddleName()

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

    def getGrado(self):
        grado = self.getField('grado').get(self)
        try:
            grado = grado[0]
            return grado
        except Exception:
            grado = ""
            return grado

    def getInstitucion(self):
        return self.getField('institucion').get(self)

    def getInvestigacionArea(self):
        return self.getField('investigacionarea').get(self)

    def getTituloTrabajo(self):
        return self.getField('titulo_trabajo').get(self)

    def getFechaDesde(self):
        #return self.getField('fecha_desde').get(self)
        return DateTime(self.getField('fecha_desde').get(self))

    def getFechaHasta(self):
        #return self.getField('fecha_hasta').get(self)
        return DateTime(self.getField('fecha_hasta').get(self))

    def getObjetoViaje(self):
        return self.getField('objeto_viaje').get(self)

    def getComentarioCI(self):
        return self.getField('comentario_ci').get(self)

    def setCantidadPasaje(self):
        f = self.getField('cantidad_pasaje')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadPasaje(self):
        try:
            f = self.setCantidadPasaje()
            return self.getCantidad(f)
        except:
                a = sys.exc_info()
                raise a[0], a[1], a[2]

    def setCantidadViaticos(self):
        f = self.getField('cantidad_viaticos')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadViaticos(self):
        try:
            f = self.setCantidadViaticos()
            return self.getCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadInscripcion(self):
        f = self.getField('cantidad_inscripcion')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadInscripcion(self):
        try:
            f = self.setCantidadInscripcion()
            return self.getCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaPasaje(self):
        try:
            f = self.setCantidadAutorizadaPasaje()
            return self.getCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizadaPasaje(self):
        f = self.getField('cantidad_autorizada_pasaje')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizadaViaticos(self):
        f = self.getField('cantidad_autorizada_viaticos')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaViaticos(self):
        try:
            f = self.setCantidadAutorizadaViaticos()
            return self.getCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizadaInscripcion(self):
        f = self.getField('cantidad_autorizada_inscripcion')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaInscripcion(self):
        try:
            f = self.setCantidadAutorizadaInscripcion()
            return self.getCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def setCantidadAutorizada(self):
        f = self.getField('cantidad_autorizada')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizada(self):
        try:
            f = self.setCantidadAutorizada()
            return self.getCantidad(f)
        except:
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
            except:
                a = sys.exc_info()
                raise a[0], a[1], a[2]

    def getCantidad(self, field):
        try:
            f = field
            if (f == ''):
                return 0.0
            else:
                return float(f)
        except:
                a = sys.exc_info()
                raise a[0], a[1], a[2]

    def getTotal(self):
        pasaje = self.getCantidadPasaje()
        viaticos = self.getCantidadViaticos()
        inscripcion = self.getCantidadInscripcion()
        return (pasaje + viaticos + inscripcion)

    def getSolicitanteDefault(self):
        mt = getToolByName(self, 'portal_membership')
        member = mt.getAuthenticatedMember()
        tupla = (member.getId(),)

        return tupla

## regresa NombreCompleto_investigador (id_investigador)
    def getInvestigadores(self):
        ''' return list of Researchers
        '''
        portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog(
            portal_type='FSDPerson',
            person_classification=[
                'investigadores',
                'tecnicos-academicos',
                'catedras-conacyt'
            ],
            sort_on='getSortableName',
            review_state='active',
        )
        users=[]
        for brain in brains:
            person = brain.getObject()
            tupla = (
                person.getId(),
                person.getLastName() + ", " + person.getFirstName() + " " + person.getMiddleName()
            )
            users.append(tupla)
        return DisplayList(users)

    def getBecarios(self):
        portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog(
            portal_type='FSDPerson',
            person_classification='becarios',
            sort_on='getSortableName',
            review_state='active',
        )
        users=[]
        for brain in brains:
            person = brain.getObject()
            tupla = (
                person.getId(),
                person.getLastName() + ", " + person.getFirstName() + " " + person.getMiddleName()
            )
            users.append(tupla)
        return DisplayList(users)


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

    def sendMail(self, transition):
        mt = getToolByName(self, 'portal_membership')

        member = mt.getMemberById(self.getIdOwner())
        mail_to = member.getProperty('email', None)
        mail_from = 'solicitudes@matem.unam.mx'
        msg = ''
        subject = '[matem] Información sobre solicitud'
        obj_url = self.absolute_url()  # use portal_url + relative_url

        if transition == 'enviarainvestigador':
            msg = '''Una nueva solicitud de viáticos de %s ha sido enviada y espera su aprobación.
Vaya a %s y si la aprueba de click en el botón enviar para que sea revisada por la Comisión Especial.

Éste es un correo electrónico automático, por favor no lo responda.
            '''
            asesor = mt.getMemberById(self.getAsesor())
            mail_to = asesor.getProperty('email', None)
            msg = msg % (member.getProperty('fullname', ''), obj_url)
        elif transition == 'aprobar':
            msg = """Su solicitud ha sido aprobada.
Para más detalles vaya a %s.

Éste es un correo electrónico automático, por favor no lo responda
            """
            msg = msg % obj_url

        if mail_to is not None:
            getToolByName(self, 'MailHost').send(msg, mail_to, mail_from, subject)
        return

    #Esta definida en solicitud
    def getCantidadDeDias(self):
        # t1 = str(self.getFecha_desde()).split("/")
        # t2 = str(self.getFecha_hasta()).split("/")
        # d1 = datetime(int(t1[0]), int(t1[1]), int(t1[2]))
        # d2 = datetime(int(t2[0]), int(t2[1]), int(t2[2]))
        # return int((d2 - d1).days) + 1
        t1 = str(DateTime(self.getFecha_desde())).split("/")
        t2 = str(DateTime(self.getFecha_hasta())).split("/")
        d1=datetime(int(t1[0]),int(t1[1]),int(t1[2].split(" ")[0]))
        d2=datetime(int(t2[0]),int(t2[1]),int(t2[2].split(" ")[0]))
        return int((d2-d1).days)+1

    def actualizarInvestigador(self):
        folder = self.aq_parent

        solicitante = self.getIdOwner()

        folder.sumarACantidadAutorizada(None, self.getCantidadAutorizadaTotal(), 0, solicitante,
                                        self.getCargo_presupuesto())
        return

    def desactualizarInvestigador(self):
        folder = self.aq_parent

        solicitante = self.getIdOwner()

        folder.restarACantidadAutorizada(None, self.getCantidadAutorizadaTotal(), 0, solicitante)
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

    def enviadaTexto(self):
        wf_state = self.getWFState()
        if (wf_state == 'revisioncomision'):
            return "Revision por Comision Especial"
        elif (wf_state == 'revisionconsejo'):
            return "Revision por Consejo Interno"
        elif (wf_state == 'preeliminar'):
            return "Revision por Tutor"

    def enviada(self):
        wf_state = self.getWFState()
        if (wf_state == 'revisioncomision' or wf_state == 'revisionconsejo' or wf_state == 'preeliminar'):
            return True

    def mandarInvestigador(self):
#        getToolByName(self,'plone_utils').changeOwnershipOf(self,self.getField('asesor').get(self))
        self.manage_addLocalRoles(self.getField('asesor').get(self), ('Owner',))
        return

    def mandarBecario(self):
#        getToolByName(self,'plone_utils').changeOwnershipOf(self,self.getField('nombrebecario').get(self))
        return

    def getDefaultDate(self):
        return DateTime('2018/1/1')

    def getNumeroDeCuenta(self):
        person = self.getPersonWrapper(self.getIdOwner())
        return person.getNumeroDeCuenta()

    def getPersonWrapper(self, userid):
        mb = getToolByName(self, MEMBRANE_TOOL)
        person = mb.getUserObject(user_id=userid)
        fsdperson = PersonWrapper(person)
        return fsdperson

    def getCountriesVocabulary(self):
        #This function is defined in config.py
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
                'quantity': '${:,.2f}'.format(money)
            },
        ]


registerType(SolicitudBecario, PROJECTNAME)
