# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from zope.interface import implements
from Products.Archetypes.public import *
from matem.solicitudes.config import *
from matem.solicitudes.extender import PersonWrapper
from matem.solicitudes.interfaces import ISolicitud
from matem.solicitudes.interfaces import ISolicitudVisitante
from Products.Archetypes import atapi
from Products.Archetypes.atapi import *
from Products.ATContentTypes.utils import DT2dt

try:
  from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
  from Products.Archetypes.public import *

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent, aq_base, ImplicitAcquisitionWrapper
from Products.ATCountryWidget.Widget import CountryWidget, AreaWidget
from Products.ATCountryWidget.config import COUNTRIES
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

from DateTime.DateTime import DateTime

from archetypes.multifile.MultiFileField import MultiFileField
from archetypes.multifile.MultiFileWidget import MultiFileWidget

from matem.solicitudes.config import getCountriesVocabulary




schema = BaseSchema + Schema((
        ComputedField(name='title',
                           required=1,
                           searchable=1,
                           expression="((here.getOwner() and 'Solicitud (Visitante) de %s por %s (%s, %s, %s)' % (here.getNombreOwner(), here.getTotal(), here.getProcedencia(), here.getInstitucion(), here.getFechaDesde() )) or 'Nueva solicitud')",
                           accessor='Title',
                           widget=ComputedWidget(visible={'view':'invisible','edit':'invisible'}),
                           ),
        ComputedField(name='text',
                           required=0,
                           searchable=1,
                           expression="""(here.getOwner() and '%s %s %s %s %s %s' %
                                        (here.esSolcitudBorrador(), here.esSolcitudPendiente(),
                                        here.setFechaSolicitud(), here.esAcuseRecibo(), here.getResponsable(),
                                        here.setFechaSesionCI() ))""",
                           widget=ComputedWidget(visible={'view':'invisible','edit':'invisible'}),
                           ),
        ComputedField(name='description',
                           required=0,
                           searchable=1,
                           expression="(here.getOwner() and ' %s, %s ' % (here.getWFTitle(), here.getWFTString() ))",
                           widget=StringWidget(visible={'view':'invisible','edit':'invisible'}),
                           ),

        StringField(name='id',
                           required=0,
                           searchable=1,
                           expression=" ",
                           widget=StringWidget(visible={'view':'invisible','edit':'invisible'}),
                           ),

        StringField(name='sede',
                           required=0,
                           searchable=1,
                           vocabulary=SEDE,
                           widget=SelectionWidget(label='Sede',
                                 label_msgid='label_sede',
                                 i18n_domain='matem.solicitudes',
                                 description='Especifica de donde es el investigador que pide la licencia',
                                 description_msgid='help_sede',
                                 visible={'view':'invisible','edit':'invisible'},
                                ),
                           ),

        ComputedField(name='responsable',
                           required=1,
                           searchable=1,
                           expression="here.getIdOwner()",
                           widget=StringWidget(visible={'view':'invisible','edit':'invisible'}),
                           ),

        ComputedField(name='nombrecompletoresponsable',
                           required=1,
                           searchable=1,
                           expression="here.getNombreOwner()",
                           widget=StringWidget(label='Responsible researcher',
                                               label_msgid='label_responsable',
                                               i18n_domain='matem.solicitudes',
                                               description='Name of the responsible researcher',
                                               description_msgid='help_responsable',
                                               visible={'view':'visible','edit':'visible'}),
                           ),

        StringField('solicitante',
            searchable=0,
            required=1,
            vocabulary='getCreators',
            default_method='getSolicitanteDefault',
            widget=SelectionWidget(label="Solicitante",
                                   label_msgid="label_solicitante",
                                   i18n_domain='matem.solicitudes',
                                   description="Nombre del investigador a nombre del cual es esta solicitud.",
                                   description_msgid="help_solicitante"),
            write_permission="Solicitud: Cambiar Solicitante",
        ),

        StringField('nombre_owner',
            searchable=0,
            required=0,
            widget=StringWidget(visible={'view':'invisible','edit':'invisible'}),
        ),

        StringField('invitado',
            searchable=1,
            required=1,
#            accessor='CiudadPais',
            widget=StringWidget(label='Visitor',
                                label_msgid='label_invitado',
                                i18n_domain='matem.solicitudes',
                                description='Name of the guest',
                                description_msgid='help_invitado'),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        StringField('semblanza',
            searchable=1,
            required=1,
            widget=TextAreaWidget(label='Semblanza',
                                label_msgid='label_semblanza',
                                i18n_domain='matem.solicitudes',
                                description='Breve semblanza curricular para el anuncio en la página web del Instituto',
                                description_msgid='help_semblanza'),
            write_permission="Solicitud: Modificar Solicitud",
        ),

        ImageField(
            name='image',
            required=0,
            widget=ImageWidget(label='Foto Visitante',
                    label_msgid='label_image',
                    i18n_domain='matem.solicitudes',
                    description='Foto del visitante para el anuncio en la página web del Instituto (el formato del archivo debe ser gif, jpg o png)',
                    description_msgid='help_foto_visitante',
                    default_content_type='image/gif'),
            storage=AttributeStorage(),
            original_size=(400, 500),
            sizes={'thumb': (100, 125), 'normal': (200, 250)},
            default_output_type='image/jpeg',
            allowable_content_types=('image/gif','image/jpeg','image/png'),
            write_permission="Solicitud: Modificar Solicitud",
        ),


        LinesField(
          name='pais_procedencia',
          required=True,
          default='MX',
          #storage=atapi.AnnotationStorage(),
          widget=SelectionWidget(
            label='Country',
            label_msgid='label_pais_procedencia',
            description='Country of origin',
            description_msgid='help_pais_procedencia',
            i18n_domain='matem.solicitudes',
          ),
          vocabulary="getCountriesVocabulary",
          write_permission="Solicitud: Modificar Solicitud",
        ),

#         LinesField('pais_procedencia',
#             searchable=1,
#             required=1,
#             default=('MX'),
#             widget=CountryWidget(label='Country',
#                                 label_msgid='label_pais_procedencia',
#                                 provideNullValue=1,   # this is default
#                                 omitCountries=None,   # this is default, can be a
#                                                       # list of country codes which
#                                                       # are not displayed
#                                 description='Country of origin',
#                                 description_msgid='help_pais_procedencia',
#                                 i18n_domain='matem.solicitudes',),
# #            read_permission="Solicitud: Modificar Solicitud",
#             write_permission="Solicitud: Modificar Solicitud",

#         ),

        StringField('procedencia',
            searchable=1,
            required=1,
#            accessor='CiudadPais',
            widget=StringWidget(label='City',
                                label_msgid='label_procedencia',
                                i18n_domain='matem.solicitudes',
                                description='City of origin',
                                description_msgid='help_procedencia'),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),
        StringField('institucion_procedencia',
            searchable=1,
            required=1,
#            accessor='Institucion',
            widget=StringWidget(label='Institution',
                                label_msgid='label_institucion_procedencia',
                                i18n_domain='matem.solicitudes',
                                description='Institution of origin',
                                description_msgid='help_institucion_procedencia'),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),
        DateTimeField('fecha_desde',
            searchable=1,
            required=1,
            default_method='getDefaultDate',
            widget=CalendarWidget(label='Start date',
                                  label_msgid='label_fecha_desde',
                                  i18n_domain='matem.solicitudes',
                                  description='Date on wich the visit will start (it can be approximate)',
                                  description_msgid='help_fecha_desde',
                                  starting_year=2011,
                                  future_years=1,
                                  show_hm=False),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),
        DateTimeField('fecha_hasta',
            searchable=1,
            required=1,
            default_method='getDefaultDate',
            widget=CalendarWidget(label='End date',
                                  label_msgid='label_fecha_hasta',
                                  i18n_domain='matem.solicitudes',
                                  description='Date on wich the visit will end (it can be approximate)',
                                  description_msgid='help_fecha_hasta',
                                  starting_year=2011,
                                  future_years=1,
                                  show_hm=False),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
            validators='isGreaterthanStart',
        ),
        StringField('objeto_viaje',
            searchable=1,
            required=1,
            accessor='ObjetoViaje',
            widget=TextAreaWidget(label='Objective',
                                  label_msgid='label_objeto_viaje',
                                  i18n_domain='matem.solicitudes',
                                  description='Enter the expected objective of the visit',
                                  description_msgid='help_objeto_viaje'),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        LinesField('investigacionarea',
#            mode='rw',
#            read_permission=VIEW_PUBLIC_PERMISSION,
#            write_permission=EDIT_PROPERTIES_PERMISSION,
            required=1,
            default=(),
            widget=PicklistWidget(
                              label='Research areas',
                              label_msgid='label_investigacionarea',
                              description="Doubts about the classification and how to find an area, go to the official website of the <a href=\"http://www.ams.org/msc\">ams</a>",
                              description_msgid='help_investigacionarea',
                              i18n_domain='matem.solicitudes',),
            multiValued=1,
            vocabulary=AREAS_INVESTIGACION,
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        StringField('cargo_presupuesto',
            required=1,
            vocabulary=DisplayList((('Asignación anual', 'Asignación anual'),
                                    ('Apoyo institucional', 'Apoyo institucional'))),
            default='Asignación anual',
            widget=SelectionWidget(label='Con cargo a',
                                label_msgid='label_cargo_a',
                                i18n_domain='matem.solicitudes',
                                description="Seleccione el presupuesto de donde se descontara el total de está solicitud",
                                description_msgid='help_cargo_a',
                                visible={'view': 'invisible', 'edit': 'invisible'}),
            write_permission="Solicitud: Modificar Solicitud",
        ),

        StringField('pasaje',
            searchable=1,
            required=0,
            default='',
            vocabulary=DisplayList((
                                    ('No', 'No'), ('si', 'Si')
                                    )),
            widget=MasterSelectWidget(label='Transportation expenses',
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
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),
        LinesField('tipo_pasaje',
#            mode='rw',
#            read_permission=VIEW_PUBLIC_PERMISSION,
#            write_permission=EDIT_PROPERTIES_PERMISSION,
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
#            read_permission="Solicitud: Modificar Solicitud",
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
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        StringField('viaticos',
            searchable=1,
            required=0,
            default='No',
            vocabulary=DisplayList((
                                    ('No', 'No'), ('Si', 'Si')
                                    )),
            widget=MasterSelectWidget(label='Travel allowances',
                                 label_msgid='label_viaticos',
                                 i18n_domain='matem.solicitudes',
                                 description='Specify if daily expenses are requested. 900 daily pesos (Mexico) and 1200 daily pesos (other countries), it is necessary to deliver receipts for the total',
                                 description_msgid='help_viaticos',
                                 slave_fields = ({'name': 'cantidad_viaticos',
                                                'action': 'hide',
                                                'hide_values': ('No',),
                                                },)
                                ),
#            read_permission="Solicitud: Modificar Solicitud",
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

        StringField('fecha_solicitud',
            searchable=1,
            required=0,
            default='',
            widget=StringWidget(label='Date of application',
                                  label_msgid='label_fecha_solicitud',
                                  i18n_domain='matem.solicitudes',
                                  description='Date on which the request is sent',
                                  description_msgid='help_fecha_solicitud',
                                  visible={'view':'invisible','edit':'hidden'}
                                  ),
#            read_permission="Solicitud: Modificar Solicitud",
            write_permission="Solicitud: Modificar Solicitud",
        ),

        MultiFileField('displayAttachments',
            primary=True,
            languageIndependent=True,
            storage = AnnotationStorage(migrate=True),
            widget = MultiFileWidget(
                     label= "Attachments",
                     label_msgid='label_adjuntos',
                     description = "Please attach invitation letter or any other related documents",
                     description_msgid='help_adjuntos',
                     show_content_type = False,
                     i18n_domain='matem.solicitudes',),
            write_permission="Solicitud: Modificar Solicitud",
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
            widget=StringWidget(label='Recommended amount for transportation expenses',
                                label_msgid='label_cantidad_recomendada_pasaje',
                                i18n_domain='matem.solicitudes',
                                description="Amount recommended for transportation expenses for this request",
                                description_msgid='help_recomendada_pasaje',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Comision Revisa Solicitud",
            write_permission="Solicitud: Comision Revisa Solicitud",
        ),

        FloatField('cantidad_recomendada_viaticos',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(label='Recommended amount for travel allowences',
                                label_msgid='label_cantidad_recomendada_viaticos',
                                i18n_domain='matem.solicitudes',
                                description="Amount recommended for travel allowences for this request",
                                description_msgid='help_recomendada_viaticos',
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
                                i18n_domain='matem.solicitudes',
                                description="Diga si recomienda aprobar esta solicitud",
                                description_msgid='help_recomienda_aprobar'),
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
            widget=StringWidget(#label='Number of record',
                                label='Número de acta de CI',
                                label_msgid='label_actaci',
                                i18n_domain='matem.solicitudes',
                                description="Number of record where the request was reviewed",
                                description_msgid='help_actaci',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        FloatField('cantidad_consejo_pasaje',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(label='Approved amount for transportation expenses',
                                label_msgid='label_cantidad_consejo_pasaje',
                                i18n_domain='matem.solicitudes',
                                description="Amount approved for transportation expenses for this request",
                                description_msgid='help_cantidad_consejo_pasaje',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),
        FloatField('cantidad_consejo_viaticos',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(label='Approved amount for travel allowences',
                                label_msgid='label_cantidad_consejo_viaticos',
                                i18n_domain='matem.solicitudes',
                                description="Amount approved for travel allowences for this request",
                                description_msgid='help_cantidad_consejo_viaticos',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Consejo Revisa Solicitud",
            write_permission="Solicitud: Consejo Revisa Solicitud",
        ),

        FloatField('cantidad_autorizada_pasaje',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(label='Approved amount for transportation expenses',
                                label_msgid='label_cantidad_autorizada_pasaje',
                                i18n_domain='matem.solicitudes',
                                description="Amount approved for transportation expenses for this request",
                                description_msgid='help_cantidad_autorizada_pasaje',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Consejo Cambia Solicitud",
            write_permission="Solicitud: Consejo Cambia Solicitud",
        ),
        FloatField('cantidad_autorizada_viaticos',
            searchable=1,
            required=1,
            default='0.0',
            widget=StringWidget(label='Approved amount for travel allowences',
                                label_msgid='label_cantidad_autorizada_viaticos',
                                i18n_domain='matem.solicitudes',
                                description="Amount approved for travel allowences for this request",
                                description_msgid='help_cantidad_autorizada_viaticos',
                                tarifas=False,
                                size=12),
            read_permission="Solicitud: Consejo Cambia Solicitud",
            write_permission="Solicitud: Consejo Cambia Solicitud",
        ),

        BooleanField('estadoBorrador',
            label = "Review data, if it is correct, you should send it to revision, by selecting 'state: solicitud no enviada' then 'enviar solicitud' inside the transitions menu in the top right corner",
            label_msgid='label_estado_borrador',
            widget=BooleanWidget(visible={'view':'invisible','edit':'hidden'}),
        ),
        BooleanField('estadoPendiente',
            label = "If your request is ready, you should send it to revision, by selecting 'state: pendiente' then 'reenviar solicitud' inside the transitions menu in the top right corner",
            label_msgid='label_estado_pendiente',
            widget=BooleanWidget(visible={'view':'invisible','edit':'hidden'}),
        ),
        BooleanField('acuseRecibo',
            label = "Your request has been received successfully, you can print this page as acknowledgement of receipt",
            label_msgid='label_acuse_recibo',
            default=False,
            widget=BooleanWidget(visible={'view':'invisible','edit':'hidden'}),
        ),

#        StringField(
#            'allowDiscussion',
#            accessor="isDiscussable",
#            mutator="allowDiscussion",
#            edit_accessor="editIsDiscussable",
#            default="1",
#            enforceVocabulary=1,
#            vocabulary=DisplayList((
#        ('1',    'Enabled', 'label_discussion_enabled'),
#        ('0',    'Disabled', 'label_discussion_disabled'),
#        ('None', 'Default', 'label_discussion_default'),
#        )),
#            widget=SelectionWidget(
#                visible={'view':'invisible','edit':'invisible'},
#                label="Allow Discussion on this item",
#                label_msgid="label_allow_discussion",
#                description_msgid="help_allow_discussion",
#                i18n_domain="plone"),
#        ),
#        ReferenceField('relatedItems',
#            relationship = 'relatesTo',
#            multiValued = True,
#            isMetadata = True,
#            languageIndependent = False,
#            index = 'KeywordIndex',
#            widget = StringWidget(
#                label = "Related Item(s)",
#                label_msgid = "label_related_items",
#                description = "",
#                description_msgid = "help_related_items",
#                i18n_domain = "plone",
#                visible = {'edit' : 'invisible', 'view' : 'invisible' }
#                )
#        ),

    ),)


for f in schema.filterFields(isMetadata=True):
    f.widget.visible = { "edit" : "invisible" }


class SolicitudVisitante(BaseContent):
    "A simple quotation content type."

    implements(ISolicitudVisitante)

    schema = schema

    _at_rename_after_creation = False

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
            end = DateTime(rendDate)
        except:
            errors['fecha_hasta'] = u'La fecha de término no es valida'

        try:
            start = DateTime(rstartDate)
        except:
            errors['fecha_desde'] = u'La fecha de inicio no es valida'

        if 'fecha_desde' in errors or 'fecha_hasta' in errors:
            # No point in validating bad input
            return

        if start > end:
            errors['fecha_hasta'] = u'La fecha de término debe ser posterior a la de inicio'
        else:
            start_dt = DT2dt(start)
            end_dt = DT2dt(end)
            ndays = int((end_dt - start_dt).days) + 1
            img = REQUEST.get('image_file', None)
            img_del = REQUEST.get('image_delete', None)

            # Editing content whith previous image
            if img_del:
                if img_del == 'nochange':
                    img = 'nochange'
                else:
                    img = None  # delete

            if ndays > 13 and not img:
                errors['image'] = u'La Foto es requerida para visitas con duración mayor a 13 días.'

    # Metodos mios para hacer algunas cosas

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

    def toState(self,State):
        workflowTool = getToolByName(self, "portal_workflow")
        mt = getToolByName(self, "portal_membership")
        member = mt.getAuthenticatedMember()
        nivel=0

        if not State.lower().find("com") == -1:
            nivel=1
        elif not State.lower().find("con") == -1 or not State.lower().find("cou") == -1:
            nivel=2
        elif not State.lower().find("ap") == -1:
            nivel=3

        if "Importador de Solicitudes" in list(member.getRoles()):
            if nivel > 0:
                workflowTool.doActionFor(self, 'enviar',comment='')
#                getToolByName(self,'plone_utils').changeOwnershipOf(self,idPropietario)
            if nivel > 1:
                workflowTool.doActionFor(self, 'enviaraconsejo',comment='')
            if nivel > 2:
                workflowTool.doActionFor(self, 'aprobar',comment='')

#        getToolByName(self,'plone_utils').changeOwnershipOf(self,idPropietario)

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
#        mt = getToolByName(self, 'portal_membership')
#        member = mt.getAuthenticatedMember()
        member = self.getIdActual()
        fsdperson = self.getPersonWrapper(member.getId())
        return fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName()

    def getIdCreator(self):
        return self.getOwner().getId()

    def getIdOwner(self):
        return self.getOwner().getId()

    def getNombreOwner(self):
#        creator = self.getOwner().getId()
        creator = self.getIdOwner()
        try:
            fsdperson = self.getPersonWrapper(creator)
            return fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName()
        except:
            print "Error SolicitudVisitante no encontrada persona "+ creator + ", "+self.getId()
            return creator

    def getNombreInvitado(self):
        return self.getField('invitado').get(self)

    def getNombreResponsable(self):
        return self.getField('responsable').get(self)

    def getFechaSolicitud(self):
        return self.getField('fecha_solicitud').get(self)

    def getCiudadPais(self):
        return self.getField('procedencia').get(self)

    def getPaisCodigo(self):
        return self.getField('pais_procedencia').get(self)

    def getPais(self):
        pais=self.getField('pais_procedencia').get(self)
        try:
            pais=COUNTRIES[pais[0]]
            return pais
        except Exception, e:
            pais=""
            return pais

    def getTituloTrabajo(self):
        return "N1o2A3p4L5i6C7a"

    def getInvestigacionArea(self):
        return self.getField('investigacionarea').get(self)

    def getInstitucion(self):
        return self.getField('institucion_procedencia').get(self)

    #Estan en solicitud
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

    def getSolicitanteDefault(self):
        mt = getToolByName(self, 'portal_membership')
        member=mt.getAuthenticatedMember()
        tupla=(member.getId(),)

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
        users=[]
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
            return 0.0

    def getCantidad_inscripcion(self):
            return 0.0

    def getCantidadAutorizadaPasaje(self):
        try:
            f = self.setCantidadAutorizadaPasaje()
            return self.getCantidad(f)
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

    def setCantidadAutorizadaPasaje(self):
        f = self.getField('cantidad_autorizada_pasaje')
        try:
            return self.setCantidad(f)
        except:
            a = sys.exc_info()
            raise a[0], a[1], a[2]

    def getCantidadAutorizadaInscripcion(self):
        return ' '

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
        return (pasaje + viaticos)

    def getCantidadRecomendadaTotal(self):
        pasaje=self.getCantidad_recomendada_pasaje()
        viaticos=self.getCantidad_recomendada_viaticos()
        return (pasaje + viaticos)

    def pasarValorComisionado(self):
        pasaje = self.getCantidadPasaje()
        viaticos = self.getCantidadViaticos()

        self.setCantidad_recomendada_pasaje(pasaje)
        self.setCantidad_recomendada_viaticos(viaticos)
        return

    def pasarValorConsejero(self):
        pasaje=self.getCantidad_recomendada_pasaje()
        viaticos=self.getCantidad_recomendada_viaticos()

        self.setCantidad_consejo_pasaje(pasaje)
        self.setCantidad_consejo_viaticos(viaticos)
        return

    def pasarValorAutorizado(self):
        pasaje=self.getCantidad_consejo_pasaje()
        viaticos=self.getCantidad_consejo_viaticos()

        self.setCantidad_autorizada_pasaje(pasaje)
        self.setCantidad_autorizada_viaticos(viaticos)
        return

    def getCantidadConsejoTotal(self):
        pasaje=self.getCantidad_consejo_pasaje()
        viaticos=self.getCantidad_consejo_viaticos()
        return (pasaje + viaticos)

    def getCantidadAutorizadaTotal(self):
        pasaje=self.getCantidadAutorizadaPasaje()
        viaticos=self.getCantidadAutorizadaViaticos()
        return (pasaje + viaticos)

    def sendMail(self, state='aprobada'):
        mt = getToolByName(self, 'portal_membership')
        member = mt.getMemberById(self.getIdOwner())
        mail_to = member.getProperty('email', None)
        mail_from = 'solicitudes@matem.unam.mx'
        subject = '[matem] Su solicitud ha sido ' + state
        msg = """
Su solicitud de visitante (%s), del %s al %s ha sido %s.

Objetivo: %s

Para más información vaya a %s.

Las siguientes cantidades se refieren a su asignación anual:

La cantidad que se le ha autorizado en esta solicitud: %s.
La cantidad total que se le ha aprobado en lo que va del año: %s.

------------------------------------------------------------------
Éste es un correo electrónico automático, por favor no lo responda
"""
        msg = msg % (self.getNombreInvitado(),
                     self.getFechaDesde().strftime('%d/%m/%Y'),
                     self.getFechaHasta().strftime('%d/%m/%Y'),
                     state,
                     self.getObjetoViaje(),
                     self.absolute_url(),
                     self.getCantidadConsejoTotal(),
                     self.aq_parent.getPresupuesto_asignado_solicitantes()[0].get(self.getIdOwner(), 0.0))
        getToolByName(self, 'MailHost').send(msg, mail_to, mail_from, subject)
        return

    def getCantidadDeDias(self):
        # t1=str(self.getFecha_desde()).split("/")
        # t2=str(self.getFecha_hasta()).split("/")
        # d1=datetime(int(t1[0]),int(t1[1]),int(t1[2]))
        # d2=datetime(int(t2[0]),int(t2[1]),int(t2[2]))
        # return int((d2-d1).days)+1
        t1 = str(DateTime(self.getFecha_desde())).split("/")
        t2 = str(DateTime(self.getFecha_hasta())).split("/")
        d1=datetime(int(t1[0]),int(t1[1]),int(t1[2].split(" ")[0]))
        d2=datetime(int(t2[0]),int(t2[1]),int(t2[2].split(" ")[0]))
        return int((d2-d1).days)+1


    def actualizarInvestigador(self):
        folder = self.aq_parent

        solicitante=self.getIdOwner()

        folder.sumarACantidadAutorizada(None,self.getCantidadAutorizadaTotal(),0,solicitante,
                                        self.getCargo_presupuesto())
        return

    def desactualizarInvestigador(self):
        folder = self.aq_parent

        solicitante=self.getIdOwner()

        folder.restarACantidadAutorizada(None,self.getCantidadAutorizadaTotal(),0,solicitante)
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
        return DateTime('2014/1/1')

    def getPersonWrapper(self,userid):
        fsdtool = getToolByName(self,'facultystaffdirectory_tool')
        portal_catalog = getToolByName(self, 'portal_catalog')

        results = portal_catalog(path='/'.join(fsdtool.getDirectoryRoot().getPhysicalPath()), portal_type='FSDPerson', id=userid,depth=1)
        encontrados=[brain.getObject() for brain in results]

        fsdperson = PersonWrapper(encontrados[0])

        return fsdperson

    # enable FTP/WebDAV and friends
    #PUT = ATDocument.PUT

    def getCountriesVocabulary(self):
        #This function is defined in config.py
        return getCountriesVocabulary(self)

registerType(SolicitudVisitante, PROJECTNAME)
