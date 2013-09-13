## Script (Python) "registrar_valor"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sti
##title=
##

sti.object.pasarValorAutorizado()
sti.object.actualizarInvestigador()
try:
    sti.object.sendMail('aprobar')
except:
    print "No se registro becario"
