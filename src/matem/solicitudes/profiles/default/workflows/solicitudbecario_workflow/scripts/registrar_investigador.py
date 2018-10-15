## Script (Python) "registrar_investigador"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sti
##title=
##


obj=sti.object.mandarInvestigador()
try:
    sti.object.sendMail('enviarainvestigador')
except:
    print "No se pudo mandar correo a investigador"
