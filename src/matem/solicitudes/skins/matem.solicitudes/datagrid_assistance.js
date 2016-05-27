/**
 * JavaScript for the history widgets
 *
 * disabled
 * readonly
 * pointer-events
 $(".row-neditable").closest('tr').find('input:text').attr('disabled', 'disabled')
 $(".row-neditable").closest('tr').find('select').attr('disabled', 'disabled')

  $('.row-neditable').closest('tr').find('input:text').css('pointer-events','none');
  $('.row-neditable').closest('tr').find('select').css('pointer-events','none');


  academic_type = $("#eventtype_assistance_0").val()
  $("#othereventtype_assistance_0").show()
  $("#othereventtype_assistance_0").hide()
  $("#othereventtype_assistance_0").parent().show()

  $("#eventtype_assistance_0").attr('onchange', 'othervisibility()')


  $("#datagridwidget-tbody-assistance").children().length




 */

(function($) {
  $(document).ready(function () {

    /*var emptyrow = $("#datagridwidget-tbody-assistance").children().last()*/
    $("#institucion").change(function() {
      var general_institution = $("#institucion").val()
      $("#institution_assistance_new").val(general_institution);
    });

    /*var general_institution = $("#institucion").val()*/
    var year = $("#edit_form_fecha_desde_0_year").val()
    var month = $("#edit_form_fecha_desde_0_month").val()
    var day = $("#edit_form_fecha_desde_0_day").val()


    /* For master select */
    $("#datagridwidget-tbody-assistance").children().length;
    console.log('Entra!!!')
    $("#eventtype_assistance_1").change(function() {
      academic_type = $("#eventtype_assistance_1").val()
      if (academic_type == 'other')
        $("#othereventtype_assistance_1").parent().show()
      else
        $("#othereventtype_assistance_1").parent().hide()
    });
  });
})(jQuery);