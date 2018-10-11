
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from matem.solicitudes.browser.folder import SolicitudFolderView
from matem.solicitudes.browser.queries import Queries
from plone.app.portlets.portlets import base
from plone.memoize import forever
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements


class IAvisos(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IAvisos)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Portlet Avisos"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('avisos.pt')

    @property
    def available(self):
        esVisible=False

        if self.context.meta_type == "Solicitud":
            esVisible=True
        elif self.context.meta_type == "SolicitudBecario":
            esVisible=True
        elif self.context.meta_type == "SolicitudVisitante":
            esVisible=True
        elif self.context.meta_type == "SolicitudFolder":
            esVisible=True
        elif self.context.meta_type == 'SolicitudInstitucional':
            esVisible=True

        return esVisible

#    def (self):
#        for brain in self._data():
#            promotion = brain.getObject()
#            banner_provider = IBannerProvider(promotion)
#            yield dict(title=promotion.title,
#                       summary=promotion.summary,
#                       url=brain.getURL(),
#                       image_tag=banner_provider.tag)

    def getHeader(self):
        usuarioActual=self.context.portal_membership.getAuthenticatedMember().getId()
        header="Desconocido"

        if self.context.meta_type == "Solicitud":
            header="Solicitud de Licencia"
        elif self.context.meta_type == "SolicitudBecario":
            header="Solicitud de Becario"
        elif self.context.meta_type == "SolicitudVisitante":
            header="Solicitud de Visitante"
        elif self.context.meta_type == "SolicitudFolder":
            header="Folder de Solicitudes"
        elif self.context.meta_type == "SolicitudInstitucional":
            header="Solicitud de Licencia"

        if self.esPropietario(usuarioActual):
            return "Tu "+header

        return header

    def esPropietario(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getIdOwner()==usuarioActual:
            return True
        return False

    def esComisionado(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Comisionado' in list(member.getRoles()):
            return True
        return False

    def esConsejero(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Consejero' in list(member.getRoles()):
            return True
        return False

    def esBecario(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Becario' in list(member.getRoles()):
            return True
        return False

    def esInvestigador(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Investigador' in list(member.getRoles()):
            return True
        return False

    def esTecnicoAcademico(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Tecnico Academico' in list(member.getRoles()):
            return True
        return False

    def esImportadorDeSolicitudes(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Importador de Solicitudes' in list(member.getRoles()):
            return True
        return False

    def esProgramadorDePresupuesto(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False

        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Programador de Presupuesto' in list(member.getRoles()):
            return True
        return False

    def esTecnicoAcademicoG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Tecnico Academico' in list(member.getRoles()):
            return True
        return False

    def esImportadorDeSolicitudesG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Importador de Solicitudes' in list(member.getRoles()):
            return True
        return False

    def esProgramadorDePresupuestoG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Programador de Presupuesto' in list(member.getRoles()):
            return True
        return False


    def esComisionadoG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Comisionado' in list(member.getRoles()):
            return True
        return False

    def esConsejeroG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Consejero' in list(member.getRoles()):
            return True
        return False

    def esComisionadoResponsableG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Responsable de la Comision' in list(member.getRoles()):
            return True
        return False

    def esConsejeroResponsableG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Responsable del Consejo' in list(member.getRoles()):
            return True
        return False

    def esSolicitanteAuxiliarG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Solicitante Auxiliar' in list(member.getRoles()):
            return True
        return False

    def esBecarioG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Becario' in list(member.getRoles()):
            return True
        return False

    def esInvestigadorG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Investigador' in list(member.getRoles()):
            return True
        return False

    def esTecnicoAcademicoG(self, usuarioActual):
        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Tecnico Academico' in list(member.getRoles()):
            return True
        return False

    def esInvestigadorACargo(self, usuarioActual):
        if self.context.meta_type == "SolicitudFolder":
            return False
        elif self.context.meta_type == "Solicitud":
            return False
        elif self.context.meta_type == "SolicitudVisitante":
            return False
        elif self.context.meta_type == "SolicitudInstitucional":
            return False


        member=self.context.portal_membership.getMemberById(usuarioActual)
        if 'Investigador' in list(member.getRoles()):
            return True
        return False

    def esFolder(self):
        if self.context.meta_type == "SolicitudFolder":
            return True
        return False

    def esBorrador(self):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getWFState()=="borrador":
            return True
        return False

    def esRevisionComision(self):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getWFState()=="revisioncomision":
            return True
        return False

    def esRevisionConsejo(self):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getWFState()=="revisionconsejo":
            return True
        return False

    def esAprobada(self):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getWFState()=="aprobada":
            return True
        return False

    def esRechazada(self):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getWFState()=="rechazada":
            return True
        return False

    def esPreeliminar(self):
        if self.context.meta_type == "SolicitudFolder":
            return False

        if self.context.getWFState()=="preeliminar":
            return True
        return False

    def getPresupuestoAprobadoSolicitud(self):
        return self.context.getCantidadAutorizadaTotal()

    def getNombreAsesor(self, asesor):
        return self.context.portal_membership.getMemberById(asesor).getProperty('fullname')

    @forever.memoize
    def hasPendingReviews(self, usuarioActual):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog

        if catalog(path={'query': folder_path, 'depth': 1},
                           portal_type=('Solicitud', 'SolicitudVisitante', 'SolicitudBecario', 'SolicitudInstitucional'),
                           review_state=('borrador', 'preeliminar'),
                           Creator=usuarioActual):
            return True

        member = self.context.portal_membership.getMemberById(usuarioActual)
        if 'Comisionado' in member.getRoles() and catalog(portal_type=('Solicitud', 'SolicitudVisitante', 'SolicitudBecario', 'SolicitudInstitucional'),
                                                          review_state=('revisioncomision',)):
            return True
        if 'Consejero' in member.getRoles() and catalog(portal_type=('Solicitud', 'SolicitudVisitante', 'SolicitudBecario', 'SolicitudInstitucional'),
                                                          review_state=('revisionconsejo',)):
            return True
        return False

    def hasSentReviews(self, usuarioActual):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        results1 = catalog(path={'query': folder_path, 'depth': 1}, portal_type=('Solicitud', 'SolicitudVisitante', 'SolicitudBecario', 'SolicitudInstitucional'), review_state=('revisioncomision', 'revisionconsejo'), Creator=usuarioActual)

        if len(results1) == 0:
            return False
        else:
            return True

class AddForm(base.NullAddForm):
    """Portlet add form.
    """
    def create(self):
        return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml
