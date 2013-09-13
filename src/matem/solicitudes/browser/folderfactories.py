from plone.app.content.browser.folderfactories import FolderFactoriesView

events = {
2012: {
'CLAM': {'event_title': 'IV Congreso Latinoamericano de Matemáticos (IV CLAM 2012)',
         'pais': 'AR',
         'ciudad_pais': 'Córdoba',
         'institucion': 'Universidad Nacional de Córdoba',
         'fecha_desde': '2012-08-06 00:00 ',
         'fecha_hasta': '2012-08-10 00:00 ',
         'objeto_viaje': 'Asistir al IV Congreso Latinoamericano de Matemáticos (IV CLAM 2012)'},
'EMALCA': {'event_title': 'Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2012)',
           'pais': 'MX',
           'ciudad_pais': 'Xalapa, Ver.',
           'institucion': 'Universidad Veracruzana',
           'fecha_desde': '2012-06-25 00:00 ',
           'fecha_hasta': '2012-07-05 00:00 ',
           'objeto_viaje': 'Asistir a la Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2012)'},
'SMM': {'event_title': 'XLV Congreso Nacional de la Sociedad Matemática Mexicana (XLV SMM 2012)',
        'pais': 'MX',
        'ciudad_pais': 'Querétaro, Qro.',
        'institucion': 'Universidad Autónoma de Querétaro',
        'fecha_desde': '2012-10-29 00:00 ',
        'fecha_hasta': '2012-11-02 00:00 ',
        'objeto_viaje': 'Asistir al XLV Congreso Nacional de la Sociedad Matemática Mexicana (XLV SMM 2012)'},
'KNOT': {'event_title': 'School on Knot and 3-Manifolds',
        'pais': 'MX',
        'ciudad_pais': 'Guanajuato',
        'institucion': 'CIMAT',
        'fecha_desde': '2012-12-17 00:00 ',
        'fecha_hasta': '2012-12-20 00:00 ',
        'objeto_viaje': 'Asistir a School of knot and 3-Manifolds para celebrar el cumpleaños 70 del Dr. Francisco González Acuña'}
},

2013: {
'AlbertoFest': {'event_title': 'AlbertoFest: Geometría Compleja, Sistemas Dinámicos y Teoría de Números',
        'pais': 'MX',
        'ciudad_pais': 'Cuernavaca',
        'institucion': 'Instituto de Matemáticas, UNAM',
        'fecha_desde': '2013-01-07 00:00 ',
        'fecha_hasta': '2013-01-11 00:00 ',
        'objeto_viaje': 'Asistir al AlbertoFest. Geometría Compleja. Sistemas Dinámicos y Teoría de Números: Celebrando los 70 años de Alberto Verjovsky'},
'MCA': {'event_title': 'Congreso Matemático de las Américas (MCA 2013)',
        'pais': 'MX',
        'ciudad_pais': 'Guanajuato',
        'institucion': 'Centro de Convenciones de Guanajuato',
        'fecha_desde': '2013-08-05 00:00 ',
        'fecha_hasta': '2013-08-09 00:00 ',
        'objeto_viaje': 'Asistir al Congreso Matemático de las Américas (MCA 2013)'},
'EMALCA': {'event_title': 'Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2013)',
        'pais': 'MX',
        'ciudad_pais': 'Morelia, Michoacán',
        'institucion': 'Universidad Michoacana de San Nicolás de Hidalgo y Centro de Ciencias Matemáticas',
        'fecha_desde': '2013-07-23 00:00 ',
        'fecha_hasta': '2013-08-01 00:00 ',
        'objeto_viaje': 'Asistir a la Escuela de Matemáticas de América Latina y el Caribe (EMALCA 2013)'},
'SMM': {'event_title': 'XLVI Congreso Nacional de la Sociedad Matemática Mexicana (XLVI SMM 2013)',
        'pais': 'MX',
        'ciudad_pais': 'Mérida, Yucatán',
        'institucion': 'Universidad Autónoma de Yucatán',
        'fecha_desde': '2013-10-27 00:00 ',
        'fecha_hasta': '2013-11-01 00:00 ',
        'objeto_viaje': 'Asistir al XLVI Congreso Nacional de la Sociedad Matemática Mexicana (XLVI SMM 2013)'},
},

2014: {

},

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
                parameters = ['%s=%s' % (k, v) for k, v in event.iteritems()]
                url += '?%s' % '&'.join(parameters)
            self.request.response.redirect(url)
            return ''
        else:
            return self.index()

    def institutional_events(self):
        year = int(self.aq_parent.id)
        return [{'value': k, 'title': v['event_title']} for k, v in events[year].items()]
