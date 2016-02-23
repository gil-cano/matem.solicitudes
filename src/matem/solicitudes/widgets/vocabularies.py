# -*- coding: utf-8 -*-
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.public import DisplayList
from zope.interface import implements

# Vocabularies for the widgets


class ConferenceTypeVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('congress', _(u'Congress')),
            ('seminary', _(u'Seminary')),
            ('coloquio', _(u'Coloquio')),
            ('school', _(u'School')),
            ('other', _(u'Other')),
        ])


class ConferenceAssistantVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('invitation', _(u'By Invitation')),
            ('application', _(u'By Application')),
        ])


class CourselevelVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('highschool', _(u'High School')),
            ('bachelor', _(u'Bachelor')),
            ('master', _(u'Master')),
            ('phd', _(u'PhD')),
            ('other', _(u'Other')),
        ])


class CoursetypeVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('research', _(u'Research')),
            ('teaching', _(u'Teaching')),
            ('divulgation', _(u'Divulgation')),
        ])


class ResearchPositionVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('organizer', _(u'Organizer')),
            ('co-organizer', _(u'Co-Organizer')),
            ('responsible', _(u'Responsible of session')),
            ('scientificc', _(u'Scientific Comittee')),
            ('localc', _(u'Local Comitte')),
            ('directivec', _(u'Directive Comitte')),
            ('other', _(u'Other')),
        ])
