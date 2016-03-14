# -*- coding: utf-8 -*-
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.public import DisplayList
from zope.interface import implements

from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

# Vocabularies for the widgets


class EventTypeVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('congress', _(u'Congress')),
            ('seminary', _(u'Seminary')),
            ('coloquio', _(u'Coloquio')),
            ('school', _(u'School')),
            ('workshop', _('Workshop')),
            ('other', _(u'Other')),
        ])


class BooleanTypeVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('yes', _(u'Yes')),
            ('no', _(u'No')),
        ])


class ConferenceAssistantVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('invitation', _(u'By Invitation')),
            ('application', _(u'By Application')),
        ])


def ConferenceTypeVocabulary(context):
    """Vocabulary factory for conference type"""
    return SimpleVocabulary([
        SimpleTerm(value='research', title=_(u'Research')),
        SimpleTerm(value='divulgation', title=_(u'Divulgation')),
        SimpleTerm(value='human_resources', title=_(u'Human resources training')),
    ])
directlyProvides(ConferenceTypeVocabulary, IVocabularyFactory)

# class ConferenceTypeVocabulary:
#     implements(IVocabulary)

#     def getDisplayList(self, instance):
#         return DisplayList([
#             ('research', _(u'Research')),
#             ('divulgation', _(u'Divulgation')),
#             ('human_resources', _(u'Human resources training')),
#         ])


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


# TOD0 Unify the course level vocabularies
def CourselevelVocabularyFactory(context):
    """Vocabulary factory for conference type"""
    return SimpleVocabulary([
        SimpleTerm(value='highschool', title=_(u'High School')),
        SimpleTerm(value='bachelor', title=_(u'Bachelor')),
        SimpleTerm(value='master', title=_(u'Master')),
        SimpleTerm(value='phd', title=_(u'PhD')),
        SimpleTerm(value='other', title=_(u'Other')),
    ])
directlyProvides(CourselevelVocabularyFactory, IVocabularyFactory)

# class CoursetypeVocabulary:
#     implements(IVocabulary)

#     def getDisplayList(self, instance):
#         return DisplayList([
#             ('research', _(u'Research')),
#             ('teaching', _(u'Teaching')),
#             ('divulgation', _(u'Divulgation')),
#         ])


def ResearcherPositionVocabulary(context):
    """Vocabulary factory for conference type"""
    return SimpleVocabulary([
        SimpleTerm(value='organizer', title=_(u'Organizer')),
        SimpleTerm(value='co-organizer', title=_(u'Co-Organizer')),
        SimpleTerm(value='responsible', title=_(u'Responsible of session')),
        SimpleTerm(value='scientific', title=_(u'Scientific Comittee')),
        SimpleTerm(value='localc', title=_(u'Local Comitte')),
        SimpleTerm(value='directivec', title=_(u'Directive Comitte')),
        SimpleTerm(value='other', title=_(u'Other')),
    ])
directlyProvides(ResearcherPositionVocabulary, IVocabularyFactory)

# class ResearcherPositionVocabulary:
#     implements(IVocabulary)

#     def getDisplayList(self, instance):
#         return DisplayList([
#             ('organizer', _(u'Organizer')),
#             ('co-organizer', _(u'Co-Organizer')),
#             ('responsible', _(u'Responsible of session')),
#             ('scientificc', _(u'Scientific Comittee')),
#             ('localc', _(u'Local Comitte')),
#             ('directivec', _(u'Directive Comitte')),
#             ('other', _(u'Other')),
#         ])


def IMPositionVocabulary(context):
    """Vocabulary factory for conference type"""
    return SimpleVocabulary([
        SimpleTerm(value='sponsor', title=_(u'Sponsor')),
        SimpleTerm(value='campus', title=_(u'Campus')),
        SimpleTerm(value='support', title=_(u'Support for the diffusion')),
        SimpleTerm(value='other', title=_(u'Other')),
    ])
directlyProvides(IMPositionVocabulary, IVocabularyFactory)