# -*- coding: utf-8 -*-
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.public import DisplayList
from zope.interface import implements

from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component.hooks import getSite
from plone import api
from AccessControl import getSecurityManager

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
            ('phd', _(u'PhD')),
            ('master', _(u'Master')),
            ('bachelor', _(u'Bachelor')),
            ('highschool', _(u'High School')),
            ('other', _(u'Other')),
        ])

class ExpectedNumbersVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            ('stage0', _(u'No one')),
            ('stage1', _(u'1 - 20')),
            ('stage2', _(u'21 - 40')),
            ('stage3', _(u'41 - 60')),
            ('stage4', _(u'61 - 80')),
            ('stage5', _(u'80 - 100')),
            ('stage6', _(u'More than 100')),
        ])

# TOD0 Unify the course level vocabularies
def CourselevelVocabularyFactory(context):
    """Vocabulary factory for conference type"""
    return SimpleVocabulary([
        SimpleTerm(value='phd', title=_(u'PhD')),
        SimpleTerm(value='master', title=_(u'Master')),
        SimpleTerm(value='bachelor', title=_(u'Bachelor')),
        SimpleTerm(value='highschool', title=_(u'High School')),
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


def IMCampusVocabulary(context):
    """Vocabulary factory for campus"""
    return SimpleVocabulary([
        SimpleTerm(value='C.U.', title='C.U.'),
        SimpleTerm(value='Cuernavaca', title='Cuernavaca'),
        SimpleTerm(value='Juriquilla', title='Juriquilla'),
        SimpleTerm(value='Oaxaca', title='Oaxaca'),
    ])
directlyProvides(IMCampusVocabulary, IVocabularyFactory)


class SolResponsibleVocabulary:
    implements(IVocabulary)

    # local_roles = self.context.portal_membership.getAuthenticatedMember().getRolesInContext(getSite())
    # if 'Manager' in local_roles:
    #     return 'enable_border'
    # return 'disable_border'

    def getDisplayList(self, instance):
        # import pdb; pdb.set_trace()

        canview = [('----', '----')]
        # # localroles = instance.portal_membership.getAuthenticatedMember().getRolesInContext(getSite())
        # current = api.user.get_current()
        # # userid = current.id
        # # member.getRolesInContext(portal)
        # roles = current.getRolesInContext(instance)
        # import pdb; pdb.set_trace()

        # if 'Comisionado' in roles or 'Manager' in roles:
        #     canview.append((current.id, current.getProperty('fullname')))

        for comuser in api.user.get_users():
            roles = comuser.getRolesInContext(instance)
            if 'Comisionado' in roles and 'Manager' not in roles:
                canview.append((comuser.id, comuser.getProperty('fullname')))

        # import pdb; pdb.set_trace()
        # sm = getSecurityManager()
        # sm.checkPermission('UNAM.imateCVct: Add portal cv content', self.context)
        # # Comisionado
        # permissions = [p['name'] for p in self.context.permissionsOfRole('Owner') if p['selected']]

        # (Pdb) from AccessControl import getSecurityManager
        # (Pdb) sm = getSecurityManager()
        # (Pdb) sm.checkPermission('UNAM.imateCVct: Add portal cv content', self.context)


        # return DisplayList([
        #     ('C.U.', 'C.U.'),
        #     ('Cuernavaca', 'Cuernavaca'),
        #     ('Juriquilla', 'Juriquilla'),
        #     ('Oaxaca', 'Oaxaca'),
        # ])
        return DisplayList(canview)


