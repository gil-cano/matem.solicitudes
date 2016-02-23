# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class OrganizationWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
    })

    security = ClassSecurityInfo()

registerWidget(
    OrganizationWidget,
    title='OrganizationWidget',
    description=('Widget for display organizaed activity on DataGridOrganizationField type format'),
    used_for=('matem.solicitudes.widgets.organization.DataGridOrganizationField',)
)


class DataGridOrganizationField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridorganizationfield',
        'widget': OrganizationWidget,
        'label_item': _(u'Organized Activity'),
        'label_button': _(u'+ Organized Activity'),
    })
