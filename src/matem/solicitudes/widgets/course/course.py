# -*- coding: utf-8 -*-
from Products.Archetypes import atapi
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.atapi import DisplayList
from Products.CompoundField.CompoundWidget import CompoundWidget
from Products.CompoundField.CompoundField import CompoundField
from matem.solicitudes import solicitudesMessageFactory as _

from AccessControl import ClassSecurityInfo


schema = atapi.Schema((
    atapi.StringField(
        'title',
        widget=atapi.StringWidget(
            label=_(u"Title"),
        ),
    ),

    atapi.StringField(
        'operator',
        schemata='default',
        required=True,
        vocabulary=DisplayList([('or', 'OR'), ('and', 'AND')]),
        default='or',
        widget=atapi.SelectionWidget(
            format='select',
            label=_(u'Default operator'),
            description=_(u'Search with AND/OR between elements'),
        )
    ),

    atapi.StringField(
        'title2',
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Este es otro campo"),
        ),
    ),

))


class CourseField(CompoundField):
    """
    """
    _properties = CompoundField._properties.copy()
    _properties.update({
        'type': 'coursefield',
        # 'validators': DateFreeValidator(),
    })

    schema = schema


registerField(
    CourseField,
    title='CourseField',
    description=('Fields required for solicitud corses.'),
)


class CourseWidget(CompoundWidget):
    _properties = CompoundWidget._properties.copy()
    _properties.update({
        'macro': 'widget_course',
        'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()

registerWidget(
    CourseWidget,
    title='CourseWidget',
    description=('Widget for display course on CourseField type format'),
    used_for=('matem.solicitudes.widgets.course.course.CourseField',)
)