/**
 * JavaScript for the history widgets organization
 *
 *
 */

(function($) {
  $(document).ready(function () {

    var year = $("#edit_form_fecha_desde_0_year").val()
    var month = $("#edit_form_fecha_desde_0_month").val()
    var day = $("#edit_form_fecha_desde_0_day").val()
    var newdate = day + '/' + month + '/' + year
    $("#organizationdate_organization_new").val(newdate);

    $("#edit_form_fecha_desde_0_year").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#organizationdate_organization_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_month").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#organizationdate_organization_new").val(newdate);
    });

    $("#edit_form_fecha_desde_0_day").change(function() {
      var year = $("#edit_form_fecha_desde_0_year").val()
      var month = $("#edit_form_fecha_desde_0_month").val()
      var day = $("#edit_form_fecha_desde_0_day").val()
      var newdate = day + '/' + month + '/' + year
      $("#organizationdate_organization_new").val(newdate);
    });

  });
})(jQuery);