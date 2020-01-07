$(document).ready(function () {
    $('body').delegate('#generateOPT', 'click', function () {
        $('#file_download').css('visibility', 'hidden');
        $('#generateOPT').addClass('m-loader m-loader--light m-loader--left');
        $('#generateOPT').prop('disabled', true);
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('mes', $("#mes").val());
        data.append('anio', $("#anio").val());
        data.append('meses', $("#meses").val());
        data.append('file', $('#file')[0].files[0]);

        if (data.get("file") == 'undefined') {
            toast2('info', 'Por favor asegúrese de seleccionar un archivo.');
            $('#generateOPT').removeClass('m-loader m-loader--light m-loader--left');
            $('#generateOPT').prop('disabled', false);
            return false
        }
        $.ajax({
            url: '/herramienta_optimizacion/generate',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json['status']) {
                    toast2('success', data_json['message']);
                    $('#generateOPT').prop('disabled', false);
                    $('#file_download').css('visibility', 'visible');
                    $('#file_download').attr('href', data_json['file_return']);
                } else {
                    toast2('error', data_json['message'])
                }
                $('#generateOPT').removeClass('m-loader m-loader--light m-loader--left');
                $('#generateOPT').prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toast2('error', 'Se presento un error al generar el archivo.');
                $('#generateOPT').removeClass('m-loader m-loader--light m-loader--left');
                $('#generateOPT').prop('disabled', false);
            }
        });
    });


    var e = document.getElementById("m_nouislider_3");
    noUiSlider.create(e, {start: [6, 12], connect: !0, direction: "ltr", tooltips: [!0, wNumb({decimals: 1})], step: 1, range: {min: 1, max: 12}});
    var n = document.getElementById("m_nouislider_3_input"), t = [document.getElementById("m_nouislider_3.1_input"), n];
    e.noUiSlider.on("update", function (e, n) {
        t[n].value = e[n]
    })
});