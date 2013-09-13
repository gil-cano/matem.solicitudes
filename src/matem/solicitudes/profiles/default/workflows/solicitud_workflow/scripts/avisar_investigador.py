## Script (Python) "avisar_investigador"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sti
##title=
##

try:
    sti.object.sendMail(sti.new_state.id)
except:
    print "No se pudo registrar investigador"
