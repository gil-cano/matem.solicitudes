# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class ConferenceWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
        # 'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()

registerWidget(
    ConferenceWidget,
    title='ConferenceWidget',
    description=('Widget for display course on DataGridConferenceField type format'),
    used_for=('matem.solicitudes.widgets.conference.DataGridConferenceField',)
)


class DataGridConferenceField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridconferencefield',
        # 'validators': DateFreeValidator(),
        'widget': ConferenceWidget,
        # 'rows': [],
        'label_item': _(u'Conference'),
        'label_button': _(u'+ Conference'),
    })
