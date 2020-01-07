$(document).ready(function () {
    var BootstrapSelect = {
        init: function () {
            $(".m_selectpicker").selectpicker()
        }
    };
    jQuery(document).ready(function () {
        BootstrapSelect.init()
    });
    $('#myModalSummary').on('hidden.bs.modal', function () {
        $('.modal-summary').html('');
    })
});
$(document).delegate('.view_summary', 'click', function () {
    //Deshabilitar y agregar loader al botón
    $('.view_summary').prop('disabled', true);
    $('.view_summary').addClass('m-loader m-loader--danger m-loader--center');

    //Serialize el formulario de filtro
    var x = $("#form_presupuestoSummary").serializeArray();

    mApp.block("#form_presupuestoSummary", {overlayColor: "#000000", type: "loader", state: "primary", message: "Procesando..."});
    var data = new FormData();
    $.each(x, function (i, field) {
        data.append(field.name, field.value);
    });

    //Inicio validar input valores
    var contador = 0;
    for (var pair of data.entries()) {
        if (pair[0] == 'valores') {
            contador++;
        }
    }
    if (contador != 0 && contador != 2) {
        $('.view_summary').removeClass('m-loader m-loader--danger m-loader--center');
        $('.view_summary').prop('disabled', false);
        toast2('error', 'Por favor seleccione 2 valores.');
        mApp.unblock("#form_presupuestoSummary");
        return false;
    }

    //Fin validar input valores

    file = $(this).data('file');
    data.append('file_summary', file);
    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    // Determinar tab activo
    data.append('id_tab_content', $('#tab-content .active').attr('id'));

    $.ajax({
        url: '/herramienta_presupuestoR/resumen',
        type: 'POST',
        dataType: 'HTML',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success: function (data) {
            $('.modal-summary').html(data);
            $('#myModalSummary').modal('show');
            var BootstrapSelect = {
                init: function () {
                    $(".m_selectpicker").selectpicker()
                }
            };
            BootstrapSelect.init();
            mApp.unblock("#form_presupuestoSummary");
            $('.view_summary').removeClass('m-loader m-loader--danger m-loader--center');
            $('.view_summary').prop('disabled', false);
        },
        error: function (request, status, error) {
            $('.view_summary').removeClass('m-loader m-loader--danger m-loader--center');
            $('.view_summary').prop('disabled', false);
            toast2('error', 'Se presento un error al generar el resumen.');
            mApp.unblock("#form_presupuestoSummary");
        }
    });
});