# -*- coding: utf-8 -*-
from plone.app.content.browser.folderfactories import FolderFactoriesView

import urllib

events = {
    2012: {
        'CLAM': {
            'event_title': 'IV Congreso Latinoamericano de Matemáticos (IV CLAM 2012)',
            'pais': 'AR',
            'ciudad_pais': 'Córdoba',
            'institucion': 'Universidad Nacional de Córdoba',
            'fecha_desde': '2012-08-06 00:00 ',
            'fecha_hasta': '2012-08-10 00:00 ',
            'objeto_viaje': 'Asistir al IV Congreso Latinoamericano de Matemáticos (IV CLAM 2012)'},
        'EMALCA': {
            'event_title': 'Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2012)',
            'pais': 'MX',
            'ciudad_pais': 'Xalapa, Ver.',
            'institucion': 'Universidad Veracruzana',
            'fecha_desde': '2012-06-25 00:00 ',
            'fecha_hasta': '2012-07-05 00:00 ',
            'objeto_viaje': 'Asistir a la Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2012)'},
        'SMM': {
            'event_title': 'XLV Congreso Nacional de la Sociedad Matemática Mexicana (XLV SMM 2012)',
            'pais': 'MX',
            'ciudad_pais': 'Querétaro, Qro.',
            'institucion': 'Universidad Autónoma de Querétaro',
            'fecha_desde': '2012-10-29 00:00 ',
            'fecha_hasta': '2012-11-02 00:00 ',
            'objeto_viaje': 'Asistir al XLV Congreso Nacional de la Sociedad Matemática Mexicana (XLV SMM 2012)'},
        'KNOT': {
            'event_title': 'School on Knot and 3-Manifolds',
            'pais': 'MX',
            'ciudad_pais': 'Guanajuato',
            'institucion': 'CIMAT',
            'fecha_desde': '2012-12-17 00:00 ',
            'fecha_hasta': '2012-12-20 00:00 ',
            'objeto_viaje': 'Asistir a School of knot and 3-Manifolds para celebrar el cumpleaños 70 del Dr. Francisco González Acuña'}
    },
    2013: {
        'AlbertoFest': {
            'event_title': 'AlbertoFest: Geometría Compleja, Sistemas Dinámicos y Teoría de Números',
            'pais': 'MX',
            'ciudad_pais': 'Cuernavaca',
            'institucion': 'Instituto de Matemáticas, UNAM',
            'fecha_desde': '2013-01-07 00:00 ',
            'fecha_hasta': '2013-01-11 00:00 ',
            'objeto_viaje': 'Asistir al AlbertoFest. Geometría Compleja. Sistemas Dinámicos y Teoría de Números: Celebrando los 70 años de Alberto Verjovsky'},
        'MCA': {
            'event_title': 'Congreso Matemático de las Américas (MCA 2013)',
            'pais': 'MX',
            'ciudad_pais': 'Guanajuato',
            'institucion': 'Centro de Convenciones de Guanajuato',
            'fecha_desde': '2013-08-05 00:00 ',
            'fecha_hasta': '2013-08-09 00:00 ',
            'objeto_viaje': 'Asistir al Congreso Matemático de las Américas (MCA 2013)'},
        'EMALCA': {
            'event_title': 'Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2013)',
            'pais': 'MX',
            'ciudad_pais': 'Morelia, Michoacán',
            'institucion': 'Universidad Michoacana de San Nicolás de Hidalgo y Centro de Ciencias Matemáticas',
            'fecha_desde': '2013-07-23 00:00 ',
            'fecha_hasta': '2013-08-01 00:00 ',
            'objeto_viaje': 'Asistir a la Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2013)'},
        'SMM': {
            'event_title': 'XLVI Congreso Nacional de la Sociedad Matemática Mexicana (XLVI SMM 2013)',
            'pais': 'MX',
            'ciudad_pais': 'Mérida, Yucatán',
            'institucion': 'Universidad Autónoma de Yucatán',
            'fecha_desde': '2013-10-27 00:00 ',
            'fecha_hasta': '2013-11-01 00:00 ',
            'objeto_viaje': 'Asistir al XLVI Congreso Nacional de la Sociedad Matemática Mexicana (XLVI SMM 2013)'},
    },
    2014: {
        'SMESMM': {
            'event_title': 'III Reunión Conjunta de la Real Sociedad Matemática Española-Sociedad Matemática Mexicana',
            'pais': 'MX',
            'ciudad_pais': 'Zacatecas',
            'institucion': '',
            'fecha_desde': '2014-09-01 00:00 ',
            'fecha_hasta': '2014-09-05 00:00 ',
            'objeto_viaje': 'Asistir ala III Reunión Conjunta de la Real Sociedad Matemática Española-Sociedad Matemática Mexicana'},
        'SMM': {
            'event_title': 'XLVII Congreso Nacional de la Sociedad Matemática Mexicana (XLVII SMM 2014)',
            'pais': 'MX',
            'ciudad_pais': 'Durango',
            'institucion': 'Universidad Juárez del Estado de Durango',
            'fecha_desde': '2014-10-26 00:00 ',
            'fecha_hasta': '2014-10-31 00:00 ',
            'objeto_viaje': 'Asistir al XLVII Congreso Nacional de la Sociedad Matemática Mexicana (XLVII SMM 2014)'},
    },
    2015: {
        'UMISMM': {
            'event_title': 'Primera Reunión Conjunta de la Unión Matemática de Israel y la Sociedad Matemática Mexicana',
            'pais': 'MX',
            'ciudad_pais': 'Oaxaca',
            'institucion': 'Instituto Tecnológico de Oaxaca',
            'fecha_desde': '2015-09-07 00:00 ',
            'fecha_hasta': '2015-09-11 00:00 ',
            'objeto_viaje': 'Asistir ala Primera Reunión Conjunta de la Unión Matemática de Israel y la Sociedad Matemática Mexicana'},
        'SMM': {
            'event_title': 'XLVIII Congreso Nacional de la Sociedad Matemática Mexicana (XLVIII SMM 2015)',
            'pais': 'MX',
            'ciudad_pais': 'Sonora',
            'institucion': 'Universidad de Sonora',
            'fecha_desde': '2015-10-18 00:00 ',
            'fecha_hasta': '2015-10-23 00:00 ',
            'objeto_viaje': 'Asistir al XLVIII Congreso Nacional de la Sociedad Matemática Mexicana (XLVIII SMM 2015)'},
    },
    2016: {
        'CLAM': {
            'event_title': 'V Congreso Latinoamericano de Matemáticos (V CLAM 2016)',
            'pais': 'CO',
            'ciudad_pais': 'Barranquilla',
            'institucion': 'Universidad del Norte',
            'fecha_desde': '2016-07-11 00:00 ',
            'fecha_hasta': '2016-07-15 00:00 ',
            'objeto_viaje': 'Asistir al V Congreso Latinoamericano de Matemáticos (V CLAM 2016)'},
        'SMM': {
            'event_title': 'XLIX Congreso Nacional de la Sociedad Matemática Mexicana (XLIX SMM 2016)',
            'pais': 'MX',
            'ciudad_pais': 'Aguascalientes',
            'institucion': 'Universidad Autónoma de Aguascalientes',
            'fecha_desde': '2016-10-23 00:00 ',
            'fecha_hasta': '2016-10-28 00:00 ',
            'objeto_viaje': 'Asistir al XLIX Congreso Nacional de la Sociedad Matemática Mexicana (XLIX SMM 2016)'},
        'EEPM': {
            'event_title': 'Segundo Encuentro de Estudiantes del Posgrado en Matemáticas',
            'pais': 'MX',
            'ciudad_pais': 'Cuernavaca',
            'institucion': 'IMATE, Unidad Cuernavaca',
            'fecha_desde': '2016-08-20',
            'fecha_hasta': '2016-08-23',
            'objeto_viaje': 'Asistir al Segundo Encuentro de Estudiantes del Posgrado en Matemáticas'},
    },
    2017: {
        'SMM': {
            'event_title': 'L Congreso Nacional de la Sociedad Matemática Mexicana (L SMM 2017)',
            'pais': 'MX',
            'ciudad_pais': 'CDMX',
            'institucion': 'Instituto de Matemáticas y la Facultad de Ciencias, UNAM',
            'fecha_desde': '2017-10-22 00:00 ',
            'fecha_hasta': '2017-10-27 00:00 ',
            'objeto_viaje': 'Asistir al L Congreso Nacional de la Sociedad Matemática Mexicana (L SMM 2017)'},
        'RSME-SMM': {
            'event_title': 'IV Encuentro Conjunto entre la Real Sociedad Matemática Española y la Sociedad Matemática Mexicana (RSME-SMM)',
            'pais': 'ES',
            'ciudad_pais': 'Valladolid',
            'institucion': 'Universidad de Valladolid',
            'fecha_desde': '2017-06-19 00:00 ',
            'fecha_hasta': '2017-06-22 00:00 ',
            'objeto_viaje': 'Asistir al IV Encuentro Conjunto RSME-SMM'},
        'PRIMA': {
            'event_title': 'The Third Pacific Rim Mathematical Association (PRIMA)',
            'pais': 'MX',
            'ciudad_pais': 'Oaxaca',
            'institucion': 'Instituto Tecnológico de Oaxaca',
            'fecha_desde': '2017-08-14 00:00 ',
            'fecha_hasta': '2017-08-18 00:00 ',
            'objeto_viaje': 'Asistir a The Third Pacific Rim Mathematical Association'},
        'CMA': {
            'event_title': 'Congreso Matemático de las Américas (CMA 2017)',
            'pais': 'CA',
            'ciudad_pais': 'Montreal',
            'institucion': 'Unversidad Mc Gill',
            'fecha_desde': '2017-07-24 00:00 ',
            'fecha_hasta': '2017-07-28 00:00 ',
            'objeto_viaje': 'Asistir al Congreso Matemático de las Américas (CMA 2017)'},
    },
    2018: {
        'SMM': {
            'event_title': 'LI Congreso Nacional de la Sociedad Matemática Mexicana (LI SMM 2018)',
            'pais': 'MX',
            'ciudad_pais': 'Tabasco',
            'institucion': 'Universidad Juárez Autónoma de Tabasco',
            'fecha_desde': '2018-10-21 00:00 ',
            'fecha_hasta': '2018-10-26 00:00 ',
            'objeto_viaje': 'Asistir al LI Congreso Nacional de la Sociedad Matemática Mexicana (LI SMM 2018)'},
        'ICM': {
            'event_title': 'XXVII Congreso Internacional de Matemáticos (ICM) 2018',
            'pais': 'BR',
            'ciudad_pais': 'Río de Janeiro',
            'institucion': 'Centro de Convenciones Riocentro en la Barra da Tijuca de Río de Janeiro, Brasil.',
            'fecha_desde': '2018-08-01 00:00 ',
            'fecha_hasta': '2018-08-09 00:00 ',
            'objeto_viaje': 'Asistir al IXXVII Congreso Internacional de Matemáticos (ICM) 2018'},
        'SCM': {
            'event_title': 'Encuentro de Sociedades de Matemáticas de Colombia y México',
            'pais': 'CO',
            'ciudad_pais': 'Barranquilla',
            'institucion': 'Universidad del Norte',
            'fecha_desde': '2018-05-30 00:00 ',
            'fecha_hasta': '2018-06-02 00:00 ',
            'objeto_viaje': 'Asistir al Encuentro de Sociedades de Matemáticas de Colombia y México'},
        'EMMM': {
            'event_title': '2o Encuentro de Mujeres Matemáticas Mexicanas',
            'pais': 'MX',
            'ciudad_pais': 'San Luis Potosí',
            'institucion': 'Universidad Autónoma de San Luis Potosí',
            'fecha_desde': '2018-04-19 00:00 ',
            'fecha_hasta': '2018-04-21 00:00 ',
            'objeto_viaje': 'Asistir al 2o Encuentro de Mujeres Matemáticas Mexicanas'},
    },
    2019: {

    }
}


class FolderFactoriesView(FolderFactoriesView):
    """The folder_factories view - show addable types
    """

    def __call__(self):
        if 'form.button.Add' in self.request.form:
            url = self.request.form.get('url')
            year = int(self.aq_parent.id)
            if 'event' in self.request.form and self.request.form.get('event') in events[year]:
                url = self.context.createObject(type_name='SolicitudInstitucional')
                event = events[year][self.request.form.get('event')]
                params = urllib.urlencode(event)
                if '?' in url:
                    url = url + '&' + params
                else:
                    url = url + '?' + params
            self.request.response.redirect(url)
            return ''
        else:
            return self.index()

    def institutional_events(self):
        year = int(self.aq_parent.id)
        return [{'value': k, 'title': v['event_title']} for k, v in events[year].items()]
