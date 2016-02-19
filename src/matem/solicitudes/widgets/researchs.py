# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class ResearchsWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
        # 'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()

registerWidget(
    ResearchsWidget,
    title='ResearchsWidget',
    description=('Widget for display research stays on DataGridResearchsField type format'),
    used_for=('matem.solicitudes.widgets.researchs.DataGridResearchsField',)
)


class DataGridResearchsField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridresearchsfield',
        # 'validators': DateFreeValidator(),
        'widget': ResearchsWidget,
        # 'rows': [],
        'label_item': _(u'Research Stay'),
        'label_button': _(u'+ Research Stay'),
    })
