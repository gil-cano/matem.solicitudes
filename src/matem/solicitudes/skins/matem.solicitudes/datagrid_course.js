/**
 * JavaScript for the history widgets course
 *
 *
 */

(function($) {
  $(document).ready(function () {

    var general_institution = $("#institucion").val()
    $("#institution_courses_new").val(general_institution);
    var year = $("#edit_form_fecha_desde_0_year").val()
    var month = $("#edit_form_fecha_desde_0_month").val()
    var day = $("#edit_form_fecha_desde_0_day").val()
    var newdate = day + '/' + month + '/' + year
    $("#coursedate_courses_new").val(newdate);


    $("#institucion").change(function() {
      var general_institution = $("#institucion").val()
      $("#institution_courses_new").val(general_institution);
    });

    $("#edit_form_fecha_desde_0_year").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#coursedate_courses_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_month").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#coursedate_courses_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_day").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#coursedate_courses_new").val(newdate);
    });

  });
})(jQuery);