# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from collective.datagridcolumns.MultiSelectColumn import MultiSelectColumn


class CourseWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
    })

    security = ClassSecurityInfo()

    security.declarePublic('getResquestValues')

    def getResquestValues(self, form, value, context, field, columnId):
        columndef = self.getColumnDefinition(field, columnId)

        newValue = []
        if type(columndef) is not MultiSelectColumn:
            return newValue

        if not form.has_key(field.getName()):
            return newValue

        for row in value:

            # we must clone row since
            # row is readonly ZPublished.HTTPRequest.record object
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]

            orderIndex = row["orderindex_"]
            # pageColumns.options.required.64

            newRow[columnId] = []
            for vitem in columndef.getVocabulary(context).keys():
                cellId = "%s.%s.%s.%s" % (field.getName(), columnId, vitem, orderIndex)
                if form.has_key(cellId):
                    # If radio button is set in HTML form
                    # it's id appears in form of field.column.orderIndex
                    newRow[columnId].append(vitem)

            newValue.append(newRow)
        return newValue

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
        'widget': CourseWidget,
        'label_item': _(u'Course'),
        'label_button': _(u'+ Course'),
        'help_button': _(u'Use this option if you will give a course'),
    })
