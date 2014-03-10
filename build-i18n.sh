#!/bin/sh
I18NDUDE=../../bin/i18ndude
I18NPATH=src/matem/solicitudes
DOMAIN=matem.solicitudes
$I18NDUDE rebuild-pot --pot $I18NPATH/locales/$DOMAIN.pot --create $DOMAIN $I18NPATH
$I18NDUDE sync --pot $I18NPATH/locales/$DOMAIN.pot $I18NPATH/locales/*/LC_MESSAGES/$DOMAIN.po
$I18NDUDE sync --pot $I18NPATH/locales/manual.pot $I18NPATH/locales/*/LC_MESSAGES/plone.po

# domain=matem.solicitudes
# i18ndude rebuild-pot --pot $domain.pot --create $domain ../
# i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po

# i18ndude sync --pot plone-manual.pot */LC_MESSAGES/plone.po