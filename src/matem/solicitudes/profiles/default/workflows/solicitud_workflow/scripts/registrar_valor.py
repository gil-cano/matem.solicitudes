## Script (Python) "registrar_valor"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sti
##title=
##

if sti.new_state.id == 'aprobada':
    sti.object.pasarValorAutorizado()
    sti.object.actualizarInvestigador()

try:
    sti.object.sendMail(sti.new_state.id)
except:
    print "No se pudo registrar investigador"
