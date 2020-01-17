# -*- coding: utf-8 -*-
from matem.solicitudes import solicitudesMessageFactory as _
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.public import DisplayList
from zope.interface import implements

from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api


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
directlyProvides(ConferenceTypeVocabulary, IVocabularyFactory)  # noqa: E305


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
directlyProvides(CourselevelVocabularyFactory, IVocabularyFactory)  # noqa: E305


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
directlyProvides(ResearcherPositionVocabulary, IVocabularyFactory)  # noqa: E305


def IMPositionVocabulary(context):
    """Vocabulary factory for conference type"""
    return SimpleVocabulary([
        SimpleTerm(value='sponsor', title=_(u'Sponsor')),
        SimpleTerm(value='campus', title=_(u'Campus')),
        SimpleTerm(value='support', title=_(u'Support for the diffusion')),
        SimpleTerm(value='other', title=_(u'Other')),
    ])
directlyProvides(IMPositionVocabulary, IVocabularyFactory)  # noqa: E305


def IMCampusVocabulary(context):
    """Vocabulary factory for campus"""
    return SimpleVocabulary([
        SimpleTerm(value='C.U.', title='C.U.'),
        SimpleTerm(value='Cuernavaca', title='Cuernavaca'),
        SimpleTerm(value='Juriquilla', title='Juriquilla'),
        SimpleTerm(value='Oaxaca', title='Oaxaca'),
    ])
directlyProvides(IMCampusVocabulary, IVocabularyFactory)  # noqa: E305


def OrgClassificationVocabularyFactory(context):
    """Vocabulary."""
    return SimpleVocabulary([
        SimpleTerm(value='00', title=u'--'),
        SimpleTerm(value='01', title=u'Coloquios'),
        SimpleTerm(value='02', title=u'Conferencias'),
        SimpleTerm(value='03', title=u'Congresos'),
        SimpleTerm(value='04', title=u'Cursos'),
        SimpleTerm(value='05', title=u'Diplomados'),
        SimpleTerm(value='06', title=u'Encuentros'),
        SimpleTerm(value='07', title=u'Foros'),
        SimpleTerm(value='08', title=u'Jornadas'),
        SimpleTerm(value='09', title=u'Mesas redondas'),
        SimpleTerm(value='10', title=u'Módulos exposiciones'),
        SimpleTerm(value='11', title=u'Módulos ferias'),
        SimpleTerm(value='12', title=u'Reuniones'),
        SimpleTerm(value='13', title=u'Seminarios'),
        SimpleTerm(value='14', title=u'Simposios'),
        SimpleTerm(value='15', title=u'Talleres'),
        SimpleTerm(value='16', title=u'Videoconferencias'),
        SimpleTerm(value='17', title=u'Ferias'),
        SimpleTerm(value='32', title=u'Cátedras'),
        SimpleTerm(value='99', title=u'Otras actividades'),
    ])
directlyProvides(OrgClassificationVocabularyFactory, IVocabularyFactory)


class SolResponsibleVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        canview = [('----', '----')]
        for comuser in api.user.get_users():
            roles = comuser.getRolesInContext(instance)
            if 'Comisionado' in roles and 'Manager' not in roles:
                canview.append((comuser.id, comuser.getProperty('fullname')))
        return DisplayList(canview)
