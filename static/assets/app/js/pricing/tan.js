$(document).ready(function () {
    $('body').delegate('#getTan', 'click', function () {

        // -- Deshabilitamos el button
        $('#getTan').addClass('m-loader m-loader--light m-loader--left');
        $('#getTan').prop('disabled', true);

        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('file', $('#file')[0].files[0]);

        //Validar si la generación del presupuesto se realiza teniendo en cuenta los favoritos del grupo
        url = '/tan/generate';

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,

            xhrFields: {
                onprogress: function (e) {
                    console.log(e)
                }
            },

            success: function (data_json) {
                if (data_json['status']) {
                    toast2('success', data_json['message']);
                    window.open('/static/pricing/tan_output/' + data_json['file'], "_blank");
                    //$('#table').empty();
                    //updateTableAcquisitionCost();
                } else {
                    toast2('info', data_json['message']);
                }
                $('#getTan').removeClass('m-loader m-loader--light m-loader--left');
                $('#getTan').prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toast2('error', 'Se presento un error al actualizar la información.');
                $('#getTan').removeClass('m-loader m-loader--light m-loader--left');
                $('#getTan').prop('disabled', false);
            }
        });
    });
});

