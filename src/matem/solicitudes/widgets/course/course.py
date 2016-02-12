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
import types
ListTypes = (types.TupleType, types.ListType)
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Field import encode



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


class CourseWidget(CompoundWidget):
    _properties = CompoundWidget._properties.copy()
    _properties.update({
        'macro': 'widget_course',
        'helper_css': ('course.css',),
        'helper_js': ('course.js',),
    })

    security = ClassSecurityInfo()


registerWidget(
    CourseWidget,
    title='CourseWidget',
    description=('Widget for display course on CourseField type format'),
    used_for=('matem.solicitudes.widgets.course.course.CourseField',)
)


class CourseField(CompoundField):
    """
    """
    _properties = CompoundField._properties.copy()
    _properties.update({
        'type': 'coursefield',
        # 'validators': DateFreeValidator(),
        'widget': CourseWidget,
        'rows': [],
    })

    schema = schema

    security = ClassSecurityInfo()
    security.declarePrivate('set')
    security.declarePrivate('get')
    security.declarePrivate('getRaw')

    def set(self, instance, value, **kwargs):
        """
        The passed in object should be a records object, or a sequence of dictionaries
        """
        # import pdb; pdb.set_trace()

        if not value:
            return

        for f in self.Schema().fields():
            if value.has_key(f.old_name):
                v = value[f.old_name]
                isarray = type(v) in ListTypes and len(v)==2 and type(v[1]) == types.DictType
                if v and isarray:
                    kw=v[1]
                else:
                    kw={}

                request = instance.REQUEST
                if (v or \
                    f.type == 'lines' and \
                    not ('controller_state' in request and \
                         request['controller_state'].getErrors())):
                    if isarray or (type(v) in ListTypes and len(v) ==1) and f.type != 'datagrid':
                        f.set(instance, v[0], **kw)
                    else:
                        f.set(instance, v, **kw)

    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)

        # ObjectField.set(self, instance, value, **kwargs)

    def get(self, instance, **kwargs):
        """ Return CourseField value
        """
        value = ObjectField.get(self, instance, **kwargs) or ()
        data = [encode(v, instance, **kwargs) for v in value]
        return data



        # import pdb; pdb.set_trace()
        # res = dict()
        # for field in self.Schema().fields():
        #     res[field.old_name] = field.get(instance,**kwargs)
        # # if getattr(self, 'value_class', None):
        # #     res = self.raw2ValueClass(res)
        # return res


registerField(
    CourseField,
    title='CourseField',
    description=('Fields required for solicitud corses.'),
)
