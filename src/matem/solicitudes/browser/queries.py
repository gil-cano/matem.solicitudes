# -*- coding: utf-8 -*-
import sys
from Products.Five.browser import BrowserView
from matem.solicitudes.extender import PersonWrapper

from plone.memoize import forever


class Queries(BrowserView):
    """A class for querying the site for applications"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @forever.memoize
    def getProductUsers(self):
        mt = self.context.portal_membership
        fsd_tool = self.context.facultystaffdirectory_tool
        member=mt.getAuthenticatedMember()
        users = {}

        for fsdperson in list(fsd_tool.getDirectoryRoot().getSortedPeople()):
            member=mt.getMemberById(fsdperson.getId())

            esPermitido=False
            roles=""
            if 'Becario' in list(member.getRoles()):
                esPermitido=True
                roles+='Becario,'
            if 'Investigador' in list(member.getRoles()):
                esPermitido=True
                roles+='Investigador,'
            if 'Postdoc' in list(member.getRoles()):
                esPermitido=True
                roles+='Postdoc,'
            if 'Tecnico Academico' in list(member.getRoles()):
                esPermitido=True
                roles+='Tecnico Academico,'
            if 'Comisionado' in list(member.getRoles()):
                esPermitido=True
                roles+='Comisionado,'
            if 'Consejero' in list(member.getRoles()):
                esPermitido=True
                roles+='Consejero,'
            if 'Responsable de la Comision' in list(member.getRoles()):
                esPermitido=True
                roles+='Responsable de la Comision,'
            if 'Responsable del Consejo' in list(member.getRoles()):
                esPermitido=True
                roles+='Responsable del Consejo,'

            if esPermitido:
                users[fsdperson.getId()]=[fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),roles]

        return users

    @forever.memoize
    def getMiembrosComision(self):
        mt = self.context.portal_membership
        g = self.context.portal_groups.getGroupById('comision-viaticos')
        members = list(g.getGroupMembers())
        users = {}

        for member in members:
            fsdperson=self.getPersonWrapper(member.getId())

            esPermitido=False
            roles=""
            if 'Comisionado' in list(member.getRoles()):
                esPermitido=True
                roles+='Comisionado,'
            if 'Consejero' in list(member.getRoles()):
                roles+='Consejero,'
            if 'Responsable de la Comision' in list(member.getRoles()):
                esPermitido=True
                roles+='Responsable de la Comision,'
            if 'Responsable del Consejo' in list(member.getRoles()):
                roles+='Responsable del Consejo,'

            if esPermitido:
                users[fsdperson.getId()]=[fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),roles]

        return users

    @forever.memoize
    def getProductReviewers(self):
        mt = self.context.portal_membership
        fsd_tool = self.context.facultystaffdirectory_tool
        member=mt.getAuthenticatedMember()
        users = {}

        for fsdperson in list(fsd_tool.getDirectoryRoot().getSortedPeople()):
            member=mt.getMemberById(fsdperson.getId())

            esPermitido=False
            roles=""
            if 'Comisionado' in list(member.getRoles()):
                esPermitido=True
                roles+='Comisionado,'
            if 'Consejero' in list(member.getRoles()):
                esPermitido=True
                roles+='Consejero,'
            if 'Responsable de la Comision' in list(member.getRoles()):
                esPermitido=True
                roles+='Responsable de la Comision,'
            if 'Responsable del Consejo' in list(member.getRoles()):
                esPermitido=True
                roles+='Responsable del Consejo,'

            if esPermitido:
                users[fsdperson.getId()]=[fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),roles]

        return users

    @forever.memoize
    def getProductCreators(self):

        mt = self.context.portal_membership
        fsd_tool = self.context.facultystaffdirectory_tool
        member=mt.getAuthenticatedMember()
        users = {}

        for fsdperson in list(fsd_tool.getDirectoryRoot().getSortedPeople()):
            member=mt.getMemberById(fsdperson.getId())

            esPermitido=False
            roles=""
            if 'Becario' in list(member.getRoles()):
                esPermitido=True
                roles+='Becario,'
            if 'Investigador' in list(member.getRoles()):
                esPermitido=True
                roles+='Investigador,'
            if 'Postdoc' in list(member.getRoles()):
                esPermitido=True
                roles+='Postdoc,'
            if 'Tecnico Academico' in list(member.getRoles()):
                esPermitido=True
                roles+='Tecnico Academico,'

            if esPermitido:
                users[fsdperson.getId()]=[fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),roles]

        return users

    @forever.memoize
    def getProductCreatorsList(self):

        mt = self.context.portal_membership
        fsd_tool = self.context.facultystaffdirectory_tool
        member=mt.getAuthenticatedMember()
        listUsers=list(fsd_tool.getDirectoryRoot().getSortedPeople())
        users = []

        for fsdperson in listUsers:
            member=mt.getMemberById(fsdperson.getId())

            esPermitido=False
            roles=""
            if 'Becario' in list(member.getRoles()):
                esPermitido=True
                roles+='Becario,'
            if 'Investigador' in list(member.getRoles()):
                esPermitido=True
                roles+='Investigador,'
            if 'Postdoc' in list(member.getRoles()):
                esPermitido=True
                roles+='Postdoc,'
            if 'Tecnico Academico' in list(member.getRoles()):
                esPermitido=True
                roles+='Tecnico Academico,'

            if esPermitido:
                users.append([fsdperson.getId(),fsdperson.getLastName()+", "+fsdperson.getFirstName()+" "+fsdperson.getMiddleName(),roles])
        return users

    @forever.memoize
    def getApplicationContainers(self):
        catalog = self.context.portal_catalog
        results = catalog(portal_type='SolicitudFolder')
        folders={}

        try:
            for brain in results:
                start=brain.start
                url=brain.getURL()
                folder=brain.getObject()
                folders[folder.getId()]=[folder.getFecha_desde(),folder.getFecha_hasta(),folder.getPresupuesto_inicial(),folder.getPresupuesto_asignado(),folder.getWFState()]

            return folders
        except Exception, err:
            print obj.getId()+": "+str(err);
            return []
        return folders

    @forever.memoize
    def getAllApplications(self):
        catalog = self.context.portal_catalog
        results = catalog(portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'))
        applications=[]


        for brain in results:
          start=brain.start
          url=brain.getURL()
          obj=brain.getObject()
          try:
              if obj.meta_type == "Solicitud":
                  special_dictionary={
                      'type':obj.getLicenciacomision(),
                      'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                      'inscription_quantity':obj.getCantidadInscripcion(),
                      'work_title':obj.getTituloTrabajo(),
                  }
              elif obj.meta_type == "SolicitudBecario":
                  special_dictionary={
                      'readable_meta_type': "Solicitud de Becario",
                      'researcher_name':obj.getNombreAsesor(),
                      'researcher_id':obj.getIdAsesor(),
                      'researcher_comments':obj.getComentario_asesor(),
                      'inscription_quantity':obj.getCantidadInscripcion(),
                      'work_title':obj.getTituloTrabajo(),
                  }
              elif obj.meta_type == "SolicitudVisitante":
                  special_dictionary={
                      'readable_meta_type': "Solicitud de Visitante",
                      'visitor_name':obj.getNombreInvitado(),
                  }
              else:
                  #'SolicitudInstitucional'
                  special_dictionary={
                      'type':obj.getLicenciacomision(),
                      'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                      'inscription_quantity':obj.getCantidadInscripcion(),
                      'work_title':obj.getTituloTrabajo(),
                  }

              applications.append({
                          'meta_type':obj.meta_type,
                          'id':obj.getId(),
                          'sede':obj.getSede(),
                          'owner_name':obj.getNombreOwner(),
                          'owner_id':obj.getIdOwner(),
                          'institution':obj.getInstitucion(),
                          'city':obj.getCiudadPais(),
                          'country':obj.getPais(),
                          'country_code':obj.getPaisCodigo(),
                          'from':obj.getFechaDesde().strftime('%d/%m/%Y'),
                          'to':obj.getFechaHasta().strftime('%d/%m/%Y'),
                          'quantity_of_days':obj.getCantidadDeDias(),
                          'research_areas':obj.getInvestigacionArea(),
                          'objective':obj.getObjetoViaje(),
                          'owner_comments':obj.getComentario_owner(),
                          'transportation_means':obj.getTipo_pasaje(),
                          'travel_expense_quantity':obj.getCantidadViaticos(),
                          'transportation_quantity':obj.getCantidadPasaje(),
                          'total_quantity':obj.getTotal(),
                          'total_recommended_quantity':obj.getCantidadRecomendadaTotal(),
                          'total_consejo_quantity':obj.getCantidadConsejoTotal(),
                          'total_approved_quantity':obj.getCantidadAutorizadaTotal(),
                          'creation_date':obj.creation_date.strftime('%d/%m/%Y'),
                          'revision_ci_date':obj.getFecha_sesionci(),
                          'revision_ce_date':obj.getFecha_sesionce(),
                          'acta_ci':obj.getActaci(),
                          'workflow_state':obj.getWFState(),
                          'workflow_state_name':obj.getWFStateName(),
                          'url':obj.absolute_url(),
                          'special_fields':special_dictionary,
                          'cargo_presupuesto':obj.getCargo_presupuesto(),
              })
          except Exception, err:
              print obj.getId()+": "+str(err);
              pass;
        return applications

    @forever.memoize
    def getMyApplications(self):
        mt = self.context.portal_membership
        member=mt.getAuthenticatedMember()
        userid=member.getId()
        return self.getUserApplications(userid)

    @forever.memoize
    def getUserApplications(self,userid):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        results = catalog(path={'query': folder_path, 'depth': 1},portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'),Creator=userid)
        applications=[]

        for brain in results:
            start=brain.start
            url=brain.getURL()
            obj=brain.getObject()

            try:
                if obj.meta_type == "Solicitud":
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudBecario":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Becario",
                        'researcher_name':obj.getNombreAsesor(),
                        'researcher_id':obj.getIdAsesor(),
                        'researcher_comments':obj.getComentario_asesor(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudVisitante":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Visitante",
                        'visitor_name':obj.getNombreInvitado(),
                    }
                else:
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }

                applications.append({
                            'meta_type':obj.meta_type,
                            'id':obj.getId(),
                            'sede':obj.getSede(),
                            'owner_name':obj.getNombreOwner(),
                            'owner_id':obj.getIdOwner(),
                            'institution':obj.getInstitucion(),
                            'city':obj.getCiudadPais(),
                            'country':obj.getPais(),
                            'country_code':obj.getPaisCodigo(),
                            'from':obj.getFechaDesde().strftime('%d/%m/%Y'),
                            'to':obj.getFechaHasta().strftime('%d/%m/%Y'),
                            'quantity_of_days':obj.getCantidadDeDias(),
                            'research_areas':obj.getInvestigacionArea(),
                            'objective':obj.getObjetoViaje(),
                            'owner_comments':obj.getComentario_owner(),
                            'transportation_means':obj.getTipo_pasaje(),
                            'travel_expense_quantity':obj.getCantidadViaticos(),
                            'transportation_quantity':obj.getCantidadPasaje(),
                            'total_quantity':obj.getTotal(),
                            'total_recommended_quantity':obj.getCantidadRecomendadaTotal(),
                            'total_consejo_quantity':obj.getCantidadConsejoTotal(),
                            'total_approved_quantity':obj.getCantidadAutorizadaTotal(),
                            'creation_date':obj.creation_date.strftime('%d/%m/%Y'),
                            'revision_ci_date':obj.getFecha_sesionci(),
                            'revision_ce_date':obj.getFecha_sesionce(),
                            'acta_ci':obj.getActaci(),
                            'workflow_state':obj.getWFState(),
                            'workflow_state_name':obj.getWFStateName(),
                            'url':obj.absolute_url(),
                            'special_fields':special_dictionary,
                            'cargo_presupuesto':obj.getCargo_presupuesto(),
                })
            except Exception, err:
                print obj.getId()+": "+str(err);
                pass;
        return applications

    @forever.memoize
    def getCurrentFolderApplications(self):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        results = catalog(path={'query': folder_path, 'depth': 1},portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'))
        applications=[]

        for brain in results:
            start=brain.start
            url=brain.getURL()
            obj=brain.getObject()
            try:
                if obj.meta_type == "Solicitud":
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudBecario":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Becario",
                        'researcher_name':obj.getNombreAsesor(),
                        'researcher_id':obj.getIdAsesor(),
                        'researcher_comments':obj.getComentario_asesor(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudVisitante":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Visitante",
                        'visitor_name':obj.getNombreInvitado(),
                    }
                else:
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }

                applications.append({
                            'meta_type':obj.meta_type,
                            'id':obj.getId(),
                            'sede':obj.getSede(),
                            'owner_name':obj.getNombreOwner(),
                            'owner_id':obj.getIdOwner(),
                            'institution':obj.getInstitucion(),
                            'city':obj.getCiudadPais(),
                            'country':obj.getPais(),
                            'country_code':obj.getPaisCodigo(),
                            'from':obj.getFechaDesde().strftime('%d/%m/%Y'),
                            'to':obj.getFechaHasta().strftime('%d/%m/%Y'),
                            'quantity_of_days':obj.getCantidadDeDias(),
                            'research_areas':obj.getInvestigacionArea(),
                            'objective':obj.getObjetoViaje(),
                            'owner_comments':obj.getComentario_owner(),
                            'transportation_means':obj.getTipo_pasaje(),
                            'travel_expense_quantity':obj.getCantidadViaticos(),
                            'transportation_quantity':obj.getCantidadPasaje(),
                            'total_quantity':obj.getTotal(),
                            'total_recommended_quantity':obj.getCantidadRecomendadaTotal(),
                            'total_consejo_quantity':obj.getCantidadConsejoTotal(),
                            'total_approved_quantity':obj.getCantidadAutorizadaTotal(),
                            'creation_date':obj.creation_date.strftime('%d/%m/%Y'),
                            'revision_ci_date':obj.getFecha_sesionci(),
                            'revision_ce_date':obj.getFecha_sesionce(),
                            'acta_ci':obj.getActaci(),
                            'workflow_state':obj.getWFState(),
                            'workflow_state_name':obj.getWFStateName(),
                            'url':obj.absolute_url(),
                            'special_fields':special_dictionary,
                            'cargo_presupuesto':obj.getCargo_presupuesto(),
                })

            except Exception, err:
                print obj.getId()+": "+str(err);
                pass;
        return applications

    @forever.memoize
    def getFolderApplicationsByState(self,wfstateid):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        if wfstateid == 'aprobada' or wfstateid == 'rechazada':
            results = catalog(path={'query': folder_path, 'depth': 1},portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'),review_state=wfstateid)
        else:
            results = catalog(portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'),review_state=wfstateid)
        applications=[]

        for brain in results:
            start=brain.start
            url=brain.getURL()
            obj=brain.getObject()
            try:
                if obj.meta_type == "Solicitud":
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudBecario":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Becario",
                        'researcher_name':obj.getNombreAsesor(),
                        'researcher_id':obj.getIdAsesor(),
                        'researcher_comments':obj.getComentario_asesor(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudVisitante":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Visitante",
                        'visitor_name':obj.getNombreInvitado(),
                    }
                else:
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                # standar date format for no required fields
                date_sesionci = ''
                if obj.getFecha_sesionci():
                  date_sesionci = obj.getFecha_sesionci().strftime('%d/%m/%Y')
                date_sesionce = ''
                if obj.getFecha_sesionce():
                  date_sesionce = obj.getFecha_sesionce().strftime('%d/%m/%Y')

                try:
                  iregistration = obj.getCantidad_inscripcion_apoyo()
                except Exception:
                  iregistration = 0.0

                try:
                  aregistration = obj.getCantidad_inscripcion()
                except Exception:
                  aregistration = 0.0

                try:
                  itransport = obj.getCantidad_pasaje_apoyo()
                except Exception:
                  itransport = 0.0

                try:
                  ifood = obj.getCantidad_viaticos_apoyo()
                except Exception:
                  ifood = 0.0

                applications.append({
                            'meta_type':obj.meta_type,
                            'id':obj.getId(),
                            'parentid':obj.aq_parent.getId(),
                            'sede':obj.getSede(),
                            'owner_name':obj.getNombreOwner(),
                            'owner_id':obj.getIdOwner(),
                            'institution':obj.getInstitucion(),
                            'city':obj.getCiudadPais(),
                            'country':obj.getPais(),
                            'country_code':obj.getPaisCodigo(),
                            'from':obj.getFechaDesde().strftime('%d/%m/%Y'),
                            'to':obj.getFechaHasta().strftime('%d/%m/%Y'),
                            'quantity_of_days':obj.getCantidadDeDias(),
                            'research_areas':obj.getInvestigacionArea(),
                            'objective':obj.getObjetoViaje(),
                            'owner_comments':obj.getComentario_owner(),
                            'transportation_means':obj.getTipo_pasaje(),
                            'travel_expense_quantity':obj.getCantidadViaticos(),
                            'transportation_quantity':obj.getCantidadPasaje(),
                            'total_quantity':obj.getTotal(),
                            'total_recommended_quantity':obj.getCantidadRecomendadaTotal(),
                            'total_consejo_quantity':obj.getCantidadConsejoTotal(),
                            'total_approved_quantity':obj.getCantidadAutorizadaTotal(),
                            'creation_date':obj.creation_date.strftime('%d/%m/%Y'),
                            'revision_ci_date':date_sesionci,
                            'revision_ce_date':date_sesionce,
                            'acta_ci':obj.getActaci(),
                            'workflow_state':obj.getWFState(),
                            'workflow_state_name':obj.getWFStateName(),
                            'url':obj.absolute_url(),
                            'special_fields':special_dictionary,
                            'cargo_presupuesto':obj.getCargo_presupuesto(),
                            'institutional_budget': {
                                'transport_expenses': itransport,
                                'registration_expenses': iregistration,
                                'food_expenses': ifood
                            },
                            'annual_budget': {
                                'transport_expenses': obj.getCantidad_pasaje(),
                                'registration_expenses': aregistration,
                                'food_expenses': obj.getCantidad_viaticos()
                            },
                            'parent_folder': obj.aq_parent,
                })

            except Exception, err:
                print obj.getId()+": "+str(err);
                pass;
        return applications

    @forever.memoize
    def getFolderApplicationsByStateAndUser(self,wfstateid,userid):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        results = catalog(path={'query': folder_path, 'depth': 1},portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario','SolicitudInstitucional'),review_state=wfstateid,Creator=userid)

        applications=[]
        for brain in results:
            start=brain.start
            url=brain.getURL()
            obj=brain.getObject()
            try:
                if obj.meta_type == "Solicitud":
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudBecario":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Becario",
                        'researcher_name':obj.getNombreAsesor(),
                        'researcher_id':obj.getIdAsesor(),
                        'researcher_comments':obj.getComentario_asesor(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudVisitante":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Visitante",
                        'visitor_name':obj.getNombreInvitado(),
                    }
                else:
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }

                #Las fechas fueron modificadas DateTime(obj....)
                applications.append({
                            'meta_type':obj.meta_type,
                            'id':obj.getId(),
                            'parentid':obj.aq_parent.getId(),
                            'sede':obj.getSede(),
                            'owner_name':obj.getNombreOwner(),
                            'owner_id':obj.getIdOwner(),
                            'institution':obj.getInstitucion(),
                            'city':obj.getCiudadPais(),
                            'country':obj.getPais(),
                            'country_code':obj.getPaisCodigo(),
                            'from':obj.getFechaDesde().strftime('%d/%m/%Y'),
                            'to':obj.getFechaHasta().strftime('%d/%m/%Y'),
                            'quantity_of_days':obj.getCantidadDeDias(),
                            'research_areas':obj.getInvestigacionArea(),
                            'objective':obj.getObjetoViaje(),
                            'owner_comments':obj.getComentario_owner(),
                            'transportation_means':obj.getTipo_pasaje(),
                            'travel_expense_quantity':obj.getCantidadViaticos(),
                            'transportation_quantity':obj.getCantidadPasaje(),
                            'total_quantity':obj.getTotal(),
                            'total_recommended_quantity':obj.getCantidadRecomendadaTotal(),
                            'total_consejo_quantity':obj.getCantidadConsejoTotal(),
                            'total_approved_quantity':obj.getCantidadAutorizadaTotal(),
                            'creation_date':obj.creation_date.strftime('%d/%m/%Y'),
                            'revision_ci_date':obj.getFecha_sesionci(),
                            'revision_ce_date':obj.getFecha_sesionce(),
                            'acta_ci':obj.getActaci(),
                            'workflow_state':obj.getWFState(),
                            'workflow_state_name':obj.getWFStateName(),
                            'url':obj.absolute_url(),
                            'special_fields':special_dictionary,
                            'cargo_presupuesto':obj.getCargo_presupuesto(),
                })

            except Exception, err:
                print obj.getId()+": "+str(err);
                pass;

        return applications

    def searchWithCatalog(self,*args,**kwargs):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        results = catalog(path={'query': folder_path, 'depth': 1},portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'),**kwargs)
        applications=[]
        for brain in results:
            start=brain.start
            url=brain.getURL()
            obj=brain.getObject()
            try:
                if obj.meta_type == "Solicitud":
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudBecario":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Becario",
                        'researcher_name':obj.getNombreAsesor(),
                        'researcher_id':obj.getIdAsesor(),
                        'researcher_comments':obj.getComentario_asesor(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }
                elif obj.meta_type == "SolicitudVisitante":
                    special_dictionary={
                        'readable_meta_type': "Solicitud de Visitante",
                        'visitor_name':obj.getNombreInvitado(),
                    }
                else:
                    special_dictionary={
                        'type':obj.getLicenciacomision(),
                        'readable_meta_type': "Solicitud de " + obj.getLicenciacomision(),
                        'inscription_quantity':obj.getCantidadInscripcion(),
                        'work_title':obj.getTituloTrabajo(),
                    }

                applications.append({
                            'meta_type':obj.meta_type,
                            'id':obj.getId(),
                            'sede':obj.getSede(),
                            'owner_name':obj.getNombreOwner(),
                            'owner_id':obj.getIdOwner(),
                            'institution':obj.getInstitucion(),
                            'city':obj.getCiudadPais(),
                            'country':obj.getPais(),
                            'country_code':obj.getPaisCodigo(),
                            'from':obj.getFechaDesde().strftime('%d/%m/%Y'),
                            'to':obj.getFechaHasta().strftime('%d/%m/%Y'),
                            'quantity_of_days':obj.getCantidadDeDias(),
                            'research_areas':obj.getInvestigacionArea(),
                            'objective':obj.getObjetoViaje(),
                            'owner_comments':obj.getComentario_owner(),
                            'transportation_means':obj.getTipo_pasaje(),
                            'travel_expense_quantity':obj.getCantidadViaticos(),
                            'transportation_quantity':obj.getCantidadPasaje(),
                            'total_quantity':obj.getTotal(),
                            'total_recommended_quantity':obj.getCantidadRecomendadaTotal(),
                            'total_consejo_quantity':obj.getCantidadConsejoTotal(),
                            'total_approved_quantity':obj.getCantidadAutorizadaTotal(),
                            'creation_date':obj.creation_date.strftime('%d/%m/%Y'),
                            'revision_ci_date':obj.getFecha_sesionci(),
                            'revision_ce_date':obj.getFecha_sesionce(),
                            'acta_ci':obj.getActaci(),
                            'workflow_state':obj.getWFState(),
                            'workflow_state_name':obj.getWFStateName(),
                            'url':obj.absolute_url(),
                            'special_fields':special_dictionary,
                            'cargo_presupuesto':obj.getCargo_presupuesto(),
                })

            except Exception, err:
                print obj.getId()+": "+str(err);
                pass;

        return applications

    def getPersonWrapper(self,userId):
        mt = self.context.portal_membership
        fsdtool = self.context.facultystaffdirectory_tool
        portal_catalog = self.context.portal_catalog

        results = portal_catalog(path='/'.join(fsdtool.getDirectoryRoot().getPhysicalPath()), portal_type='FSDPerson', id=userId,depth=1)
        encontrados=[brain.getObject() for brain in results]

        investigador = PersonWrapper(encontrados[0])
        return investigador

    @forever.memoize
    def getCurrentFolderApplicationObjects(self):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = self.context.portal_catalog
        results = catalog(path={'query': folder_path, 'depth': 1},portal_type=('Solicitud','SolicitudVisitante','SolicitudBecario', 'SolicitudInstitucional'))
        applications=[]

        for brain in results:
            start=brain.start
            url=brain.getURL()
            obj=brain.getObject()
            try:
                applications.append(obj)
            except Exception, err:
                print obj.getId()+": "+str(err);
                pass;
        return applications
