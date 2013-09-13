## Script (Python) "avisar_investigador"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sti
##title=
##

obj = sti.object
try:
    obj.sendMail('enviarainvestigador')
except:
    print "No se envio mail becario"
