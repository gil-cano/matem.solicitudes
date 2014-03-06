# -*- coding: utf-8 -*-
# copy this file in matem.solicitudes.browser/export.py

from Products.Five.browser import BrowserView
from matem.solicitudes.browser.queries import Queries
import os
import csv

INSTANCEHOME = '/Users/gil/projects/plone/infomatem-p3/parts/instance'
SOLFILE = os.path.join(INSTANCEHOME, 'Extensions/solicitudes.csv')


class ExportView(BrowserView):

    def __call__(self):
        queryObj = Queries(self.context, self.request)

        log = ''
        # preparamos archivo para escritura. Agregamos extensión csv
        csvWriter = csv.writer(open(SOLFILE, 'w'), delimiter=',')

        # Hide the editable-str(obj.)ct border
        self.request.set('disable_border', True)
        self.request.response.setHeader('Content-Type', 'application/octet-stream')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename=exportadas.csv')

        encabezado = []
        encabezado.append("portal_type")
        encabezado.append("id")
        encabezado.append("applicantsId")
        encabezado.append("intendedApplicantsId")
        encabezado.append("draftReviewersId")
        encabezado.append("degree")
        encabezado.append("draftReviewerAdditionalComments")
        encabezado.append("visitorFullname")
        encabezado.append("formType")
        encabezado.append("country")
        encabezado.append("city")
        encabezado.append("institution")
        encabezado.append("fromDate")
        encabezado.append("toDate")
        encabezado.append("dayCount")
        encabezado.append("objective")
        encabezado.append("researchAreas")
        encabezado.append("isPresentingPaper")
        encabezado.append("papersTitle")
        encabezado.append("hasTransportationCosts")
        encabezado.append("transportationMeans")
        encabezado.append("transportationCosts")
        encabezado.append("hasTravelExpenses")
        encabezado.append("travelExpenses")
        encabezado.append("hasRegistrationCosts")
        encabezado.append("registrationCosts")
        encabezado.append("formDate")
        encabezado.append("attachments")
        encabezado.append("additionalComments")

        ################COMMISSION FIELDS####################

        encabezado.append("commissionSessionDate")
        encabezado.append("commissionComments")
        encabezado.append("recommendedTransportationCosts")
        encabezado.append("recommendedTravelExpenses")
        encabezado.append("recommendedRegistrationCosts")
        encabezado.append("recommendApproval")

        ################COUNCIL FIELDS####################

        encabezado.append("councilSessionDate")
        encabezado.append("councilRecord")
        encabezado.append("councilComments")
        encabezado.append("authorizedTransportationCosts")
        encabezado.append("authorizedTravelExpenses")
        encabezado.append("authorizedRegistrationCosts")
        encabezado.append("willBeApproved")

        ################COUNCIL CHANGING FIELDS####################

        encabezado.append("lastCouncilComments")
        encabezado.append("previouslyAuthorizedTransportationCosts")
        encabezado.append("previouslyAuthorizedTravelExpenses")
        encabezado.append("previouslyAuthorizedRegistrationCosts")
        encabezado.append("lastAuthorizedTransportationCosts")
        encabezado.append("lastAuthorizedTravelExpenses")
        encabezado.append("lastAuthorizedRegistrationCosts")

        encabezado.append("approved")
        encabezado.append("review_state")

        csvWriter.writerow(encabezado)
        for obj in queryObj.getCurrentFolderApplicationObjects():
            #lcform

            renglon = []

            portal_type = "matem.solicitudes.lcform"
            formType = ""
            isPresentingPaper = False
            papersTitle = ""
            hasTransportationCosts = False
            transportationCosts = 0.0
            transportationMeans = []
            hasTravelExpenses = False
            travelExpenses = 0.0
            hasRegistrationCosts = False
            registrationCosts = 0.0
            recommendedRegistrationCosts = 0.0
            authorizedRegistrationCosts = 0.0
            lastAuthorizedRegistrationCosts = 0.0
            attachments = []
            recommendApproval = False
            approved = False
            review_state = "draft"

            #stform
            draftReviewersId = ""
            degree = "none"
            draftReviewerAdditionalComments = ""

            #visitorform
            visitorFullname = ""

            try:
                if obj.meta_type in ["Solicitud", "SolicitudInstitucional"]:
                    if self.context.getSolicitantes()[0][obj.getOwner().getId()][3] in "Investigador":
                        portal_type = "matem.solicitudes.lcform"
                        if obj.getLicenciacomision() in "Comision":
                            formType = "commission"
                        else:
                            formType = "license"
                    else:
                        portal_type = "matem.solicitudes.stform"
                        formType = "technician"
                        draftReviewersId = "rajsbaum"
                        degree = "none"
                elif obj.meta_type in "SolicitudBecario":
                    portal_type = "matem.solicitudes.sbform"
                    formType = "student"
                    draftReviewersId = obj.getAsesor()
                    if 'Licenciatura' in obj.getGrado():
                        degree = "undergraduate"
                    elif 'Maestria' in obj.getGrado():
                        degree = "masters"
                    elif 'Doctorado' in obj.getGrado():
                        degree = "phd"
                    else:
                        degree = "none"
                else:
                    portal_type = "matem.solicitudes.visitorform"
                    visitorFullname = obj.getNombreInvitado()
                    formType = "Visitor"
            except:
                pass

            try:
                if obj.getTrabajo().lower() in "si":
                    isPresentingPaper = True
                    papersTitle = obj.getTituloTrabajo()
            except:
                pass

            try:
                if obj.getPasaje().lower() in "si":
                    hasTransportationCosts = True
                    transportationCosts = obj.getCantidad_pasaje()

                for transport in obj.getTipo_pasaje():
                    if transport in "auto":
                        transportationMeans.append("car")
                    elif transport in "autobus":
                        transportationMeans.append("bus")
                    elif transport in "avion":
                        transportationMeans.append("flight")

            except:
                pass

            try:
                if obj.getInscripcion().lower() in "si":
                    hasRegistrationCosts = True
                    registrationCosts = obj.getCantidad_inscripcion()
                recommendedRegistrationCosts = obj.getCantidad_recomendada_inscripcion()
                authorizedRegistrationCosts = obj.getCantidad_consejo_inscripcion()
                lastAuthorizedRegistrationCosts = obj.getCantidad_autorizada_inscripcion()
            except:
                pass

            try:
                if obj.getViaticos().lower() in "si":
                    hasTravelExpenses = True
                    travelExpenses = obj.getCantidad_viaticos()
            except:
                pass

            for attachment in obj.getDisplayAttachments():
                attachments.append(attachment)

            if obj.getRecomienda_aprobar().lower() in "si":
                recommendApproval = True

            if obj.getWFState() in "preeliminar":
                review_state = "draftreview"
            elif obj.getWFState() in "revisioncomision":
                review_state = "commissionreview"
            elif obj.getWFState() in "revisionconsejo":
                review_state = "councilreview"
            elif obj.getWFState() in "rechazada":
                review_state = "rechazada"
            elif obj.getWFState() in "aprobada":
                approved = True
                review_state = "reviewed"

            if approved:
                renglon.append(portal_type)
                renglon.append(str(obj.getId()) + "-" + portal_type)
                renglon.append(str(obj.getOwner().getId()))
                renglon.append(str(obj.getOwner().getId()))
                renglon.append(draftReviewersId)
                renglon.append(degree)
                renglon.append(draftReviewerAdditionalComments.replace("\"", "'").replace("\r", " ").replace("\n", ""))
                renglon.append(visitorFullname.replace("\"", "'"))
                renglon.append(formType)
                renglon.append(str(obj.getPaisCodigo()[0]))
                renglon.append(str(obj.getCiudadPais()))
                renglon.append(str(obj.getInstitucion()).replace("\"", "'"))
                renglon.append(str(obj.getFecha_desde()).replace("/", "-"))
                renglon.append(str(obj.getFecha_hasta()).replace("/", "-"))
                renglon.append(str(obj.getCantidadDeDias()))
                renglon.append(str(obj.getObjetoViaje()).replace("\"", "'").replace("\r", " ").replace("\n", ""))
                renglon.append(str(obj.getInvestigacionArea()).replace("(", "").replace(")", "").replace(" ", "").rstrip(","))
                renglon.append(str(isPresentingPaper))
                renglon.append(papersTitle.replace("\"", "'").replace("\r", " ").replace("\n", ""))
                renglon.append(str(hasTransportationCosts))
                renglon.append(str(transportationMeans).replace("[", "").replace("]", "").replace(" ", "").rstrip(","))
                renglon.append(str(obj.getCantidadPasaje()))
                renglon.append(str(hasTravelExpenses))
                renglon.append(str(obj.getCantidadViaticos()))
                renglon.append(str(hasRegistrationCosts))
                renglon.append(str(registrationCosts))
                renglon.append(str(obj.getCreationDate()))
                renglon.append(str(attachments).replace("[", "").replace("]", "").rstrip(","))
                renglon.append(str(obj.getComentario_owner()).replace("\"", "'").replace("\r", " ").replace("\n", ""))

                ################COMMISSION FIELDS####################

                renglon.append(str(obj.getFecha_sesionce()).replace("/", "-"))
                renglon.append(str(obj.getComentario_ce()).replace("\"", "'").replace("\r", " ").replace("\n", ""))
                renglon.append(str(obj.getCantidad_recomendada_pasaje()))
                renglon.append(str(obj.getCantidad_recomendada_viaticos()))
                renglon.append(str(recommendedRegistrationCosts))
                renglon.append(str(recommendApproval))

                ################COUNCIL FIELDS####################

                renglon.append(str(obj.getFecha_sesionci()).replace("/", "-"))
                renglon.append(str(obj.getActaci()))
                renglon.append(str(obj.getComentario_ci()).replace("\"", "'").replace("\r", " ").replace("\n", ""))
                renglon.append(str(obj.getCantidad_consejo_pasaje()))
                renglon.append(str(obj.getCantidad_consejo_viaticos()))
                renglon.append(str(authorizedRegistrationCosts))
                renglon.append(str(approved))

                ################COUNCIL CHANGING FIELDS####################

                renglon.append(str(obj.getComentario_ci()).replace("\"", "'").replace("\r", " ").replace("\n", ""))
                renglon.append(str(obj.getCantidad_consejo_pasaje()))
                renglon.append(str(obj.getCantidad_consejo_viaticos()))
                renglon.append(str(authorizedRegistrationCosts))
                renglon.append(str(obj.getCantidad_autorizada_pasaje()))
                renglon.append(str(obj.getCantidad_autorizada_viaticos()))
                renglon.append(str(lastAuthorizedRegistrationCosts))

                renglon.append(str(approved))
                renglon.append(review_state)

                csvWriter.writerow(renglon)

        return log
