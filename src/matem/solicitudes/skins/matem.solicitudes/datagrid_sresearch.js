/**
 * JavaScript for the history widgets stay research
 *
 *
 */

(function($) {
  $(document).ready(function () {

    $("#institucion").change(function() {
      var general_institution = $("#institucion").val()
      $("#institution_sresearch_new").val(general_institution);
    });
    /* start date*/
    $("#edit_form_fecha_desde_0_year").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#sresearchinitdate_sresearch_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_month").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#sresearchinitdate_sresearch_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_day").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#sresearchinitdate_sresearch_new").val(newdate);
    });

    /*End date*/
    $("#edit_form_fecha_hasta_1_year").change(function() {
      var year = $("#edit_form_fecha_hasta_1_year").val()
      var month = $("#edit_form_fecha_hasta_1_month").val()
      var day = $("#edit_form_fecha_hasta_1_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#sresearchenddate_sresearch_new").val(newdate);
    });

    $("#edit_form_fecha_hasta_1_month").change(function() {
      var year = $("#edit_form_fecha_hasta_1_year").val()
      var month = $("#edit_form_fecha_hasta_1_month").val()
      var day = $("#edit_form_fecha_hasta_1_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#sresearchenddate_sresearch_new").val(newdate);
    });

    $("#edit_form_fecha_hasta_1_day").change(function() {
      var year = $("#edit_form_fecha_hasta_1_year").val()
      var month = $("#edit_form_fecha_hasta_1_month").val()
      var day = $("#edit_form_fecha_hasta_1_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#sresearchenddate_sresearch_new").val(newdate);
    });

  });
})(jQuery);