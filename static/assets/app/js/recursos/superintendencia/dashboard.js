$(document).ready(function () {
    var BootstrapSelect = {
        init: function () {
            $(".m_selectpicker").selectpicker()
        }
    };
    jQuery(document).ready(function () {
        BootstrapSelect.init()
    });
});

$(document).ready(function () {
    $('body').delegate('.filtrar', 'click', function () {
        $("#resultado").html("")
        $('.filtrar').button('loading');
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('analizar_por', $("#analizar_por").val());
        data.append('anio', $("#anio").val());
        data.append('fecha', $("#fecha").val());
        data.append('grupo', $("#grupo").val());
        data.append('socio', $("#socio").val());
        $.ajax({
            url: '/recursos/ISF-dashboard-graficar',
            type: 'POST',
            dataType: 'HTML',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (_data) {
                $('.filtrar').button('reset');
                $('#grafica').css('display', 'block');
                $("#resultado").html(_data)
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Se presento un error al momento de consultar los datos..[:()]")
                $('.filtrar').button('reset');
                $("#resultado").html("")
            }
        });
    });
});