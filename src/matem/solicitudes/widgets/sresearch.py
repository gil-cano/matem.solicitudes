# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class SResearchWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
        # 'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()

registerWidget(
    SResearchWidget,
    title='SResearchWidget',
    description=('Widget for display research stays on DataGridSResearchField type format'),
    used_for=('matem.solicitudes.widgets.sresearch.DataGridSResearchField',)
)


class DataGridSResearchField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridsresearchfield',
        # 'validators': DateFreeValidator(),
        'widget': SResearchWidget,
        # 'rows': [],
        'label_item': _(u'Research Stay'),
        'label_button': _(u'+ Research Stay'),
        'help_button': _(u'Use this option if you will do a reseracher stay'),
    })
