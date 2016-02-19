# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget


class CourseWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
        # 'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()

registerWidget(
    CourseWidget,
    title='CourseWidget',
    description=('Widget for display course on DataGridCourseField type format'),
    used_for=('matem.solicitudes.widgets.course.DataGridCourseField',)
)


class DataGridCourseField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridcoursefield',
        # 'validators': DateFreeValidator(),
        'widget': CourseWidget,
        # 'rows': [],
        'label_item': _(u'Course'),
        'label_button': _(u'+ Course'),
    })
