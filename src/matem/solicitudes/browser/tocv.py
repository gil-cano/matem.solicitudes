# -*- coding: utf-8 -*-

from matem.solicitudes.content.solicitudvisitante import SolicitudVisitante
from plone import api
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import ObjectEditedEvent
from z3c.form import button
from z3c.form import form
from zope import event

import logging


# from Acquisition import aq_base
# from UNAM.imateCVct.vocabularies import RESEARCH
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import IIDNormalizer
# import re

class ApplicationstoCVForm(form.Form):
    """docstring for ApplicationstoCVForm"""

    @button.buttonAndHandler(u'Dump applications to cv')
    def dump_to_cv(self, action):
        """Create cv items form applications"""
        logging.info('Dumpping applications')
        folder = api.content.get(
            path='/servicios/servicios-internos/solicitudes/2016')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            path={'query': '/'.join(folder.getPhysicalPath()), 'depth': 1},
            review_state='aprobada',
            portal_type=('Solicitud', 'SolicitudInstitucional', 'SolicitudVisitante'),
            sort_on='created'
        )
        for brain in brains:
            # test for applications in old format
            aux_folder = api.content.get(
                path='/servicios/servicios-internos/solicitudes/2006')
            application = brain.getObject()
            userid = application.getIdOwner()
            if brain.id in aux_folder:
                application = aux_folder[brain.id]
            # prides = ['rajsbaum', 'folchgab', 'dolivero', 'flopez', 'geronimo', 'adolfo', 'acano', 'omendoza']
            prides = ['rajsbaum', ]
            if userid not in prides:
                continue

            if isinstance(application, SolicitudVisitante):
                self.app2cv_guest(application, userid)

    def get_folder(self, userid, content_type):
        path = '/fsd/{id}/cv/{ctype}folder'.format(id=userid, ctype=content_type)
        return api.content.get(path=path)

    def app2cv_guest(self, application, userid):
        logging.info('{0} - {1}'.format(application.id, userid))
        content_type = 'CVGuest'
        folder = self.get_folder(userid, content_type.lower())
        id = application.id.replace('solicitudvisitante', 'sv')
        date = application.fecha_desde
        begin_date = {
            'Year': date.year(), 'Month': date.month(), 'Day': date.day()}
        date = application.fecha_hasta
        end_date = {
            'Year': date.year(), 'Month': date.month(), 'Day': date.day()}
        fields = {
            'institutionCountry': application.getPais_procedencia()[0],
            'otherinstitution': application.getInstitucion_procedencia(),
            'goalGuest': application.ObjetoViaje(),
            'begin_date': begin_date,
            'end_date': end_date,
            'interchangeProgram': (application.getExchangeProgram() == 'yes') and 'si' or '',
            'creators': (userid, ),
        }
        obj = api.content.create(
            type=content_type,
            id=id,
            title=application.invitado,
            container=folder,
            **fields)
        is_new_object = obj.checkCreationFlag()
        obj.unmarkCreationFlag()

        if is_new_object:
            event.notify(ObjectInitializedEvent(obj))
            obj.at_post_create_script()
        else:
            event.notify(ObjectEditedEvent(obj))
            obj.at_post_edit_script()
        obj.reindexObject()
        # event.notify(ObjectInitializedEvent(obj))
        # event.notify(ObjectEditedEvent(obj))
        # obj.reindexObject()


def _compare(fieldval, itemval):
    """Compare a AT Field value with an item value

    Because AT fields return utf8 instead of unicode and item values may be
    unicode, we need to special-case this comparison. In case of fieldval
    being a str and itemval being a unicode value, we'll decode fieldval and
    assume utf8 for the comparison.

    """
    if isinstance(fieldval, str) and isinstance(itemval, unicode):
        return fieldval.decode('utf8', 'replace') == itemval
    return fieldval == itemval


def get(field, obj):
    if field.accessor is not None:
        return getattr(obj, field.accessor)()
    return field.get(obj)


def set(field, obj, val):
    if field.mutator is not None:
        getattr(obj, field.mutator)(val)
    else:
        field.set(obj, val)


def upload_solicitudes(self):
    log = 'Initializing upload_solicitudes ' + str(DateTime()) + '...\n'
    ttool = getToolByName(self, 'portal_types')

    csvReader = csv.reader(open(CSVFILE), delimiter=',')
    HEADER = csvReader.next()
    normalizer = getUtility(IIDNormalizer)

    for row in csvReader:
        item = {}
        item['portal_type'] = row[HEADER.index('portal_type')]
        item['applicantsId'] = row[HEADER.index('applicantsId')]
        item['objective'] = row[HEADER.index('objective')]
        item['fromDate'] = row[HEADER.index('fromDate')].split()[0]
        item['toDate'] = row[HEADER.index('toDate')].split()[0]
        item['isPresentingPaper'] = row[HEADER.index('isPresentingPaper')]

        # ignore technicians and students applications
        if item['portal_type'] in ['matem.solicitudes.stform', 'matem.solicitudes.sbform']:
            continue

        # only process user's appliance
        if item['applicantsId'] in ['mclapp', ]:
            continue

        # fsd_path/${login}/cv/${content_type}folder/${id}
        path = 'fsd/%s/cv/%sfolder/%s'
        if item['portal_type'] == 'matem.solicitudes.visitorform':
            item['_type'] = 'CVGuest'
        else:
            item['_type'] = 'CVVisit'
            if item['isPresentingPaper'] == 'True':
                plus = re.compile('.*plenaria.*|.*magistral.*', re.IGNORECASE)
                if plus.match(item['objective']):
                    item['_type'] = 'CVConferencePlus'
                else:
                    item['_type'] = 'CVConference'

        item['id'] = normalizer.normalize('%s%s' % (item['_type'].lower(), item['fromDate']))
        item['_path'] = path % (item['applicantsId'], item['_type'].lower(), item['id'])


        # More data
        item['institutionCountry'] = row[HEADER.index('country')]
        item['otherinstitution'] = row[HEADER.index('institution')]
        item['institution'] = ''
        fecha = item['fromDate'].split("-")
        item['begin_date'] = {'Year': fecha[0], 'Month': fecha[1], 'Day': fecha[2]}
        fecha = item['toDate'].split("-")
        item['end_date'] = {'Year': fecha[0], 'Month': fecha[1], 'Day': fecha[2]}

        # guest fields
        if item['_type'] == 'CVGuest':
            item['title'] = row[HEADER.index('visitorFullname')]
            item['goalGuest'] = item['objective']
        # visit fileds
        elif item['_type'] == 'CVVisit':
            item['goalVisit'] = item['objective']
            item['sabbaticalLeave'] = False
            item['researchVisit'] = True
            item['participationMeeting'] = False
        # conference fields
        else:
            item['title'] = row[HEADER.index('papersTitle')]
            # keep default values
            item['modality'] = 'conference'
            item['conftype'] = RESEARCH
            item['where'] = u'institution'
            item['event_date'] = item['begin_date']
            # item['assist'] = 'Por invitaciÃ³n'
            # item['city'] = item['city']
            item['researchTopic'] = [i.strip("'") for i in row[HEADER.index('researchAreas')].split(',')]
            item['eventNotes'] = item['objective']

        # metadata fields
        item['language'] = 'es'
        item['creators'] = (item['applicantsId'], )

        # Constructor
        fti = ttool.getTypeInfo(item['_type'])
        if fti is None:
            print item;
            continue

        path = item['_path'].encode('ASCII')
        elems = path.strip('/').rsplit('/', 1)
        container, id = (len(elems) == 1 and ('', elems[0]) or elems)
        context = self.unrestrictedTraverse(container, None)

        # container doesn't exist
        if context is None:
            print 'Container %s does not exist for item %s' % (container, path)
            continue
        # item exists
        if getattr(aq_base(context), id, None) is not None:
            print 'item exists %s/%s' % (path, id)
            continue

        obj = fti._constructInstance(context, id)

        if obj.getId() != id:
            item['_path'] = '%s/%s' % (container, obj.getId())


        is_new_object = obj.checkCreationFlag()
        for k,v in item.iteritems():
            if k.startswith('_'):
                continue
            field = obj.getField(k)
            if field is None:
                continue
            if not _compare(get(field, obj), v):
                set(field, obj, v)
                changed = True
        obj.unmarkCreationFlag()

        if is_new_object:
            event.notify(ObjectInitializedEvent(obj))
            obj.at_post_create_script()
        elif changed:
            event.notify(ObjectEditedEvent(obj))
            obj.at_post_edit_script()
        obj.reindexObject()
    # log += "Imported %d\n" % addeditems
    log += 'Finish upload_FCcourses ' + str(DateTime()) + '.\n'
    return log
