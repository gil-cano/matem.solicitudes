# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles
from Products.validation import validation
from validators import isFloat

# try:
#     validation.register(isFloat('isFloat'))
# except:
#     print "error validator isfloat"


setDefaultRoles('Solicitud: Revisar Solicitud', ())
setDefaultRoles('SolicitudBecario: Add SolicitudBecario', ())
setDefaultRoles('SolicitudVisitante: Add SolicitudVisitante', ())
setDefaultRoles('SolicitudFolder: Add SolicitudFolder', ())
setDefaultRoles('Solicitud: Modificar Solicitud', ())
setDefaultRoles('Solicitud: Investigador Revisa Solicitud', ())
setDefaultRoles('Solicitud: Comision Revisa Solicitud', ())
setDefaultRoles('Solicitud: Consejo Revisa Solicitud', ())
setDefaultRoles('Solicitud: Consejo Cambia Solicitud', ())
setDefaultRoles('Solicitud: Datos Perennes Consejo', ())
setDefaultRoles('Solicitud: Cambiar Solicitante', ())
setDefaultRoles('Programar Presupuesto', ())
setDefaultRoles('Importacion de Solicitudes', ())
