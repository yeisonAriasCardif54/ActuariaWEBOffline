$(document).ready(function () {
    $('body').delegate('#generateBP', 'click', function () {
        $('#file_download').css('visibility', 'hidden');
        $('#generateBP').addClass('m-loader m-loader--light m-loader--left');
        $('#generateBP').prop('disabled', true);
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('file', $('#file')[0].files[0]);
        data.append('mas_detalles', $("#mas_detalles_val").val());

        if (data.get("file") == 'undefined') {
            toast2('info', 'Por favor asegúrese de seleccionar un archivo.');
            $('#generateBP').removeClass('m-loader m-loader--light m-loader--left');
            $('#generateBP').prop('disabled', false);
            return false
        }
        $.ajax({
            url: 'business_plan_tool/generate',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json['status']) {
                    toast2('success', data_json['message']);
                    $('#generateBP').prop('disabled', false);
                    $('#file_download').css('visibility', 'visible');
                    $('#file_download').attr('href', data_json['file_return']);
                } else {
                    toast2('error', data_json['message'])
                }
                $('#generateBP').removeClass('m-loader m-loader--light m-loader--left');
                $('#generateBP').prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toast2('error', 'Se presento un error al generar el archivo.');
                $('#generateBP').removeClass('m-loader m-loader--light m-loader--left');
                $('#generateBP').prop('disabled', false);
            }
        });
    });
});