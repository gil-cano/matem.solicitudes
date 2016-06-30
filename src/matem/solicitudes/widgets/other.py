# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class OtherWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
    })

    security = ClassSecurityInfo()

registerWidget(
    OtherWidget,
    title='OtherWidget',
    description=('Widget for display organizaed activity on DataGridOtherField type format'),
    used_for=('matem.solicitudes.widgets.other.DataGridOtherField',)
)


class DataGridOtherField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridotherfield',
        'widget': OtherWidget,
        'label_item': _(u'Other Activity'),
        'label_button': _(u'+ Other Activity'),
    })
