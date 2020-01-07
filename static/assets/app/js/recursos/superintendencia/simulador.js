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
    $('body').delegate('.simular', 'click', function () {
        $("#resultado").html("");
        $('.simular').button('loading');
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());

        data.append('socio', $("#socio").val());
        data.append('modalidad', $("#modalidad").val());
        data.append('valor', $("#valor").val());
        data.append('plazo', $("#plazo").val());
        data.append('tasa', $("#tasa").val());
        $.ajax({
            url: '/recursos/ISF-simulador_graficar',
            type: 'POST',
            dataType: 'HTML',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (_data) {
                $('.simular').button('reset');
                $('#grafica').css('display', 'block');
                $("#resultado").html(_data)
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Se presento un error al momento de consultar los datos..[:(]");
                $('.simular').button('reset');
                $("#resultado").html("")
            }
        });
    });
});