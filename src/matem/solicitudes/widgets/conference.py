# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.field import ExtensionField
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from collective.datagridcolumns.MultiSelectColumn import MultiSelectColumn


class ConferenceWidget(DataGridWidget):
    _properties = DataGridWidget._properties.copy()
    _properties.update({
        'macro': 'grid_widget',
        'helper_css': ('solwidgets.css',),
        # 'helper_js': ('course.js',),
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
    ConferenceWidget,
    title='ConferenceWidget',
    description=('Widget for display conferences on DataGridConferenceField type format'),
    used_for=('matem.solicitudes.widgets.conference.DataGridConferenceField',)
)


class DataGridConferenceField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridconferencefield',
        # 'validators': DateFreeValidator(),
        'widget': ConferenceWidget,
        'label_item': _(u'Conference to present'),
        'label_button': _(u'+ Conference'),
        'help_button': _(u'Use this option if you will give a talk (this cover assistants too)'),
    })


class DataGridConferenceGuestField(ExtensionField, DataGridField):

    _properties = DataGridField._properties.copy()
    _properties.update({
        'type': 'datagridconferencefield',
        # 'validators': DateFreeValidator(),
        'widget': ConferenceWidget,
        'label_item': _(u'Conference'),
        'label_button': _(u'+ Conference'),
        'help_button': _(u'Use this option if you guest will be give a talk'),
    })
