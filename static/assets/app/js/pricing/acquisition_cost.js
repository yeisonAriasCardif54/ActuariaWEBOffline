$(document).ready(function () {
    updateTableAcquisitionCost();
});

function updateTableAcquisitionCost() {
    $.ajax({
        url: '/acquisition_cost_ajax',
        type: 'GET',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: [],
        success: function (data_json) {
            var test = JSON.parse(JSON.stringify(data_json));
            $('#table').DataTable({
                scrollY: "50vh",
                scrollX: !0,
                scrollCollapse: !0,
                data: test,
                destroy: true,
                columns: [
                    //{"data": "ID"},
                    {"data": "COUNTRY"},
                    {"data": "BUSINESS_LINE"},
                    {"data": "PARTNER_GROUP"},
                    {"data": "DESTINATION"},
                    {"data": "COST_TYPE"},
                    {"data": "UNIT_COST_IN_LC"}
                ],
                //dom: 'Bfrtip',
                dom: "<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>\n\t\t\t<'row'<'col-sm-12'tr>>\n\t\t\t<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>",
                buttons: [
                    'excelHtml5'
                ]
                //"bDestroy": true,
                //"order": [[ 0, "desc" ]]
            });
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr);
            console.log(ajaxOptions);
            console.log(thrownError);
            alert("Se presento un error al momento de consultar los datos..[:()]")
        }
    });
}


$(document).ready(function () {
    $('body').delegate('#update_acquisition_cost', 'click', function () {

        // -- Deshabilitamos el button
        $('#update_acquisition_cost').addClass('m-loader m-loader--light m-loader--left');
        $('#update_acquisition_cost').prop('disabled', true);

        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('file', $('#file')[0].files[0]);

        //Validar si la generación del presupuesto se realiza teniendo en cuenta los favoritos del grupo
        url = '/acquisition_cost/update';

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json['status']) {
                    toast2('success', data_json['message']);
                    //$('#table').empty();
                    updateTableAcquisitionCost();
                } else {
                    toast2('info', data_json['message']);
                }
                $('#update_acquisition_cost').removeClass('m-loader m-loader--light m-loader--left');
                $('#update_acquisition_cost').prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toast2('error', 'Se presento un error al actualizar la información.');
                $('#update_acquisition_cost').removeClass('m-loader m-loader--light m-loader--left');
                $('#update_acquisition_cost').prop('disabled', false);
            }
        });
    });
});

