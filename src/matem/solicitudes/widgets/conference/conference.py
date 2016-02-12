# -*- coding: utf-8 -*-

from Products.DataGridField import DataGridField
from archetypes.schemaextender.field import ExtensionField
from Products.DataGridField import DataGridWidget
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget


class ConferenceWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'widget_conference',
        # 'helper_css': ('course.css',),
        # 'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()

registerWidget(
    ConferenceWidget,
    title='ConferenceWidget',
    description=('Widget for display course on DataGridConferenceField type format'),
    used_for=('matem.solicitudes.widgets.conference.conference.DataGridConferenceField',)
)


class DataGridConferenceField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridconferencefield',
        # 'validators': DateFreeValidator(),
        'widget': ConferenceWidget,
        # 'rows': [],
    })
