/**
 * JavaScript for the history widgets assistance
 *
 *
 */

(function($) {
  $(document).ready(function () {

    var general_institution = $("#institucion").val()
    $("#institution_assistance_new").val(general_institution);
    var year = $("#edit_form_fecha_desde_0_year").val()
    var month = $("#edit_form_fecha_desde_0_month").val()
    var day = $("#edit_form_fecha_desde_0_day").val()
    var newdate = day + '/' + month + '/' + year
    $("#assistancedate_assistance_new").val(newdate);

    $("#institucion").change(function() {
      var general_institution = $("#institucion").val()
      $("#institution_assistance_new").val(general_institution);
    });

    $("#edit_form_fecha_desde_0_year").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#assistancedate_assistance_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_month").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#assistancedate_assistance_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_day").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#assistancedate_assistance_new").val(newdate);
    });

    /*$("#edit_form_fecha_desde_0").change(function() {
      console.log('Entra hide !!!')
      var hidedate = $("#edit_form_fecha_desde_0").val()
      var splitdate = hidedate.split('-')
      var year = splitdate[0]
      var month = splitdate[1]
      var day = splitdate[2]
      var newdate = day + '/' + month + '/' + year
      $("#assistancedate_assistance_new").val(newdate);
    });*/

    /* For master select*/
    /*$("#datagridwidget-tbody-assistance").children().length;
    console.log('Entra!!!')
    $("#eventtype_assistance_1").change(function() {
      academic_type = $("#eventtype_assistance_1").val()
      if (academic_type == 'other')
        $("#othereventtype_assistance_1").parent().show()
      else
        $("#othereventtype_assistance_1").parent().hide()
    });*/
  });
})(jQuery);