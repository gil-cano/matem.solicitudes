# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class AssistanceWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
    })

    security = ClassSecurityInfo()

registerWidget(
    AssistanceWidget,
    title='AssistanceWidget',
    description=('Widget for display assistance on DataGridAssistanceField type format'),
    used_for=('matem.solicitudes.widgets.assistance.DataGridAssistanceField',)
)


class DataGridAssistanceField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridassistancefield',
        'widget': AssistanceWidget,
        'label_item': _(u'Assistance'),
        'label_button': _(u'+ Assistance'),
    })
