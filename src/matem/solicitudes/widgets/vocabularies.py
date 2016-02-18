# -*- coding: utf-8 -*-
# from zope.interface import directlyProvides
# from zope.schema.interfaces import IVocabularyFactory
# from zope.schema.vocabulary import SimpleTerm
# from zope.schema.vocabulary import SimpleVocabulary
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.interfaces import IVocabulary
from zope.interface import implements
from Products.Archetypes.public import DisplayList

# Vocabularies for the widgets


class ConferenceTypeVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('congress', _(u'Congress')),
            ('seminary', _(u'Seminary')),
            ('coloquio', _(u'Coloquio')),
            ('school', _(u'School')),
        ])


class ConferenceAssistantVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('invitation', _(u'By Invitation')),
            ('application', _(u'By Application')),
        ])


# def ConferenceTypeVocabularyFactory(context):
#     """ Vocabulary factory for conference type """
#     return SimpleVocabulary([
#         SimpleTerm(value='congress', title=_(u'Congress')),
#         SimpleTerm(value='seminary', title=_(u'Seminary')),
#         SimpleTerm(value='coloquio', title=_(u'Coloquio')),
#         SimpleTerm(value='school', title=_(u'School')),
#     ])
# directlyProvides(ConferenceTypeVocabularyFactory, IVocabularyFactory)


# def ConferenceAssistantVocabularyFactory(context):
#     """Vocabulary factory for conference assist"""
#     return SimpleVocabulary([
#         SimpleTerm(value=u'invitation', title=_(u'By Invitation')),
#         SimpleTerm(value=u'application', title=_(u'By Application')),
#     ])
# directlyProvides(ConferenceAssistantVocabularyFactory, IVocabularyFactory)
