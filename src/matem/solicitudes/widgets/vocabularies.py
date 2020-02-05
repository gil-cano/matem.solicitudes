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

    # TO DO: Unify the values in the migration. Alert see line comments
    def getDisplayList(self, instance):
        return DisplayList([
            ('congress', _(u'Congress')),
            # ('03', 'Congresos'),
            ('seminary', _(u'Seminary')),
            # ('13', title=u'Seminarios'),
            ('coloquio', _(u'Coloquio')),
            # ('01', title=u'Coloquios'),
            ('school', _(u'School')),
            ('workshop', _('Workshop')),
            # ('15', title=u'Talleres'),
            ('02', _(u'Conferencias')),
            ('04', _(u'Cursos')),
            ('05', _(u'Diplomados')),
            ('06', _(u'Encuentros')),
            ('17', _(u'Ferias')),
            ('07', _(u'Foros')),
            ('08', _(u'Jornadas')),
            ('09', _(u'Mesas redondas')),
            ('10', _(u'Módulos exposiciones')),
            ('11', _(u'Módulos ferias')),
            ('12', _(u'Reuniones')),
            ('14', _(u'Simposios')),
            ('16', _(u'Videoconferencias')),
            ('32', _(u'Cátedras')),
            ('other', _(u'Other')),
            # ('99', title=u'Otras actividades'),
        ])


class ScopeTypeVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([

            ('01', _(u'Institutional')),
            ('02', _(u'Regional')),
            ('03', _(u'National')),
            ('04', _(u'International')),
            ('05', _(u'Local')),
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

class OrgClassificationVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        return DisplayList([
            # ('00', u'--'),
            ('01', u'Coloquio'),
            ('02', u'Conferencia'),
            ('03', u'Congreso'),
            ('04', u'Curso'),
            ('05', u'Diplomado'),
            ('06', u'Encuentro'),
            ('07', u'Foro'),
            ('08', u'Jornada'),
            ('09', u'Mesa redonda'),
            ('10', u'Módulo de exposición'),
            ('11', u'Módulo de feria'),
            ('12', u'Reunión'),
            ('13', u'Seminario'),
            ('14', u'Simposio'),
            ('15', u'Taller'),
            ('16', u'Videoconferencia'),
            ('17', u'Feria'),
            ('32', u'Cátedra'),
            ('99', u'Otra actividad'),
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


class SolResponsibleVocabulary:
    implements(IVocabulary)

    def getDisplayList(self, instance):
        canview = [('----', '----')]
        for comuser in api.user.get_users():
            roles = comuser.getRolesInContext(instance)
            if 'Comisionado' in roles and 'Manager' not in roles:
                canview.append((comuser.id, comuser.getProperty('fullname')))
        return DisplayList(canview)
