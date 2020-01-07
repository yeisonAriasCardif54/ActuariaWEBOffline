function update_state(id) {
    var r = confirm("Eliminar el registro?");
    if (r == true) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('id', id);
        $.ajax({
            url: '/herramienta_presupuesto/update_state',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json) {
                    update_history();
                    toast2('success', 'Registro Eliminado');
                } else {
                    toast2('error', 'Error al eliminar el registro');
                }
            }
        });
    } else {
        return false;
    }
}

function update_favorite(id, FAVORITE) {
    var data = new FormData();
    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    data.append('id', id);
    data.append('value', FAVORITE);
    $.ajax({
        url: '/herramienta_presupuesto/history_favorite',
        type: 'POST',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success: function (data_json) {
            if (data_json) {
                update_history();
                toast2('success', 'Registro Actualizado');
            } else {
                toast2('error', 'Error al actualizar el registro: <br>Recuerde que solo debe seleccionar una simulación como favorita.');
                $('#favorite_' + id).blur();
            }
        }
    });
}

function update_history() {
    $.ajax({
        url: '/herramienta_presupuesto/get_history',
        type: 'GET',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: [],
        success: function (data) {
            $('#log').DataTable({
                data: data,
                "lengthMenu": [[-1], ["Todos"]],
                columns: [
                    {"data": "ID"},
                    {"data": "DATETIME"},
                    {
                        "mRender": function (data, type, row) {
                            var F_INPUT = row.FILE_INPUT;
                            var IS_UNION = row.IS_UNION;
                            if (IS_UNION == 1) {
                                // Como el resultado se genero con base en varios archivos, se realiza separación de los mismos.
                                var inputs = F_INPUT.split("||");
                                var htmlInputs = '<i class="fa fa-code-branch"></i><ul>';
                                for (var key in inputs) {
                                    if (inputs[key] != '') {
                                        htmlInputs += "<li><a href='static/profitability/update_presupuesto/" + inputs[key] + "'>" + inputs[key] + "</a></li>";
                                    }
                                }
                                return htmlInputs + '</ul>'
                            } else {
                                return "<a href='static/profitability/update_presupuesto/" + F_INPUT + "'>" + F_INPUT + "</a>";
                            }
                        }
                    },
                    {
                        "mRender": function (data, type, row) {
                            var ID = row.ID;
                            var F_OUTPUT = row.FILE_OUTPUT;
                            var ERROR = row.ERROR;
                            var SUCCESS = row.SUCCESS;
                            if (F_OUTPUT == 'Error al generar archivo') {
                                return '<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#m_modal_' + ID + '">' + F_OUTPUT + '</button>' +
                                    '<div class="modal fade" id="m_modal_' + ID + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" data-vivaldi-spatnav-clickable="1" aria-hidden="true" style="display: none;">\n' +
                                    '\t\t\t\t\t\t\t<div class="modal-dialog modal-lg" role="document">\n' +
                                    '\t\t\t\t\t\t\t\t<div class="modal-content">\n' +
                                    '\t\t\t\t\t\t\t\t\t<div class="modal-header">\n' +
                                    '\t\t\t\t\t\t\t\t\t\t<h5 class="modal-title" id="exampleModalLabel">Mensaje de Error</h5>\n' +
                                    '\t\t\t\t\t\t\t\t\t\t<button type="button" class="close" data-dismiss="modal" aria-label="Close">\n' +
                                    '\t\t\t\t\t\t\t\t\t\t\t<span aria-hidden="true">×</span>\n' +
                                    '\t\t\t\t\t\t\t\t\t\t</button>\n' +
                                    '\t\t\t\t\t\t\t\t\t</div>\n' +
                                    '\t\t\t\t\t\t\t\t\t<div class="modal-body">\n' + '<pre>' + ERROR + '</pre>' +
                                    '\t\t\t\t\t\t\t\t\t</div>\n' +
                                    '\t\t\t\t\t\t\t\t\t<div class="modal-footer">\n' +
                                    '\t\t\t\t\t\t\t\t\t\t<button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>\n' +
                                    '\t\t\t\t\t\t\t\t\t</div>\n' +
                                    '\t\t\t\t\t\t\t\t</div>\n' +
                                    '\t\t\t\t\t\t\t</div>\n' +
                                    '\t\t\t\t\t\t</div>'
                            } else if (SUCCESS == 1) {
                                if (F_OUTPUT.includes("xlsx")) {
                                    return "<a target='_blank' href='static/profitability/update_presupuesto/" + F_OUTPUT + "'>" + F_OUTPUT + "</a>"
                                } else {
                                    return "<a target='_blank' href='static/profitability/update_presupuesto/" + F_OUTPUT + "'>" + F_OUTPUT + "</a>" + "<br>" +
                                        "<a target='_blank' href='herramienta_presupuesto/convert_xlsx?file=" + F_OUTPUT + "&to=puntoycoma'>Descargar CSV (;)</a>" + "<br>" +
                                        "<a target='_blank' href='herramienta_presupuesto/convert_xlsx?file=" + F_OUTPUT + "&to=excel'>Descargar Excel</a>"
                                }
                            }else{
                                return "";
                            }
                        }
                    },
                    {
                        "mRender": function (data, type, row) {
                            var ID = row.ID;
                            var F_OUTPUT = row.FILE_OUTPUT;
                            var FAVORITE = row.FAVORITE;
                            var SUCCESS = row.SUCCESS;
                            favorite = (FAVORITE == 1) ? "btn-warning" : "btn-outline-warning";
                            html = '<button type="button" onclick="update_state(' + ID + ')"  title="Eliminar" class="btn btn-outline-danger m-btn m-btn--icon btn-sm m-btn--icon-only m-btn--pill m-btn--air" style="margin-right: 5px;">' +
                                '<i class="la la-close"></i>' +
                                '</button>';
                            if (SUCCESS == 1) {
                                html += '<button type="button" id="favorite_' + ID + '" onclick="update_favorite(' + ID + ',\'' + FAVORITE + '\')" title="Agregar a favoritos" class="btn ' + favorite + ' m-btn m-btn--icon btn-sm m-btn--icon-only m-btn--pill m-btn--air" style="margin-right: 5px;">' +
                                    '<i class="la la-star"></i>' +
                                    '</button>' +
                                    '<button type="button" data-file="' + F_OUTPUT + '"  title="ver Resumen" class="btn btn-outline-dark m-btn m-btn--icon btn-sm m-btn--icon-only m-btn--pill m-btn--air button_get_summary view_summary" style="margin-right: 5px;">' +
                                    '<i class="fa fa-chart-line"></i>' +
                                    '</button>';
                            }
                            return html
                        }
                    }
                ],
                "bDestroy": true,
                "order": [[0, "desc"]]
            });
        },
        error: function (xhr, ajaxOptions, thrownError) {
            toast2('error', 'Se presento un error al cargar el historial.')
        }
    });
}

$(document).ready(function () {
    update_history();
    $('body').delegate('#generate, #generateFavoritos', 'click', function () {
        $('#file_download').css('visibility', 'hidden');
        $('#view_summary').css('visibility', 'hidden');
        $('#generate, #generateFavoritos').addClass('m-loader m-loader--light m-loader--left');
        $('#generate, #generateFavoritos').prop('disabled', true);
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('file', $('#file')[0].files[0]);

        //Validar si la generación del presupuesto se realiza teniendo en cuenta los favoritos del grupo
        url = '/herramienta_presupuesto/generate';
        validateFavorite = $(this).data("favorite");
        if (validateFavorite == true) {
            url = '/herramienta_presupuesto/generateFavorites';
        } else if (data.get("file") == 'undefined') {
            toast2('info', 'Por favor asegúrese de seleccionar un archivo.');
            $('#generate, #generateFavoritos').removeClass('m-loader m-loader--light m-loader--left');
            $('#generate, #generateFavoritos').prop('disabled', false);
            return false
        }

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
                    $('#generate, #generateFavoritos').prop('disabled', false);
                    $('#file_download').css('visibility', 'visible');
                    $('#file_download_v1').attr('href', 'static/profitability/update_presupuesto/' + data_json['file_return']);
                    $('#file_download_v2').attr('href', 'herramienta_presupuesto/convert_xlsx?file=' + data_json['file_return'] + '&to=puntoycoma');
                    $('#file_download_v3').attr('href', 'herramienta_presupuesto/convert_xlsx?file=' + data_json['file_return'] + '&to=excel');

                    $('#view_summary').css('visibility', 'visible');
                    $('#view_summary').data('file', data_json['file_return']);
                    //$('#file_summary').val(data_json['file_return']);
                    //$('#file_download_csv').attr('href', 'static/profitability/update_presupuesto/' + data_json['file_return']);
                    //$('#file_download_xlsx').attr('href', 'herramienta_presupuesto/convert_xlsx?file=' + data_json['file_return']);
                    update_history()
                } else {
                    toast2('error', data_json['message'])
                    update_history()
                }
                $('#generate, #generateFavoritos').removeClass('m-loader m-loader--light m-loader--left');
                $('#generate, #generateFavoritos').prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toast2('error', 'Se presento un error al generar el presupuesto.');
                $('#generate, #generateFavoritos').removeClass('m-loader m-loader--light m-loader--left');
                $('#generate, #generateFavoritos').prop('disabled', false);
            }
        });
    });
});

$(document).ready(function () {
    $('body').delegate('#generateRRC', 'click', function () {
        $('#file_download').css('visibility', 'hidden');
        $('#generateRRC').addClass('m-loader m-loader--light m-loader--left');
        $('#generateRRC').prop('disabled', true);
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('mes', $("#mes").val());
        data.append('anio', $("#anio").val());
        data.append('meses', $("#meses").val());
        data.append('file', $('#file')[0].files[0]);

        if (data.get("file") == 'undefined') {
            toast2('info', 'Por favor asegúrese de seleccionar un archivo.')
            $('#generateRRC').removeClass('m-loader m-loader--light m-loader--left')
            $('#generateRRC').prop('disabled', false);
            return false
        }
        $.ajax({
            url: '/calcular_rrc/generate',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json['status']) {
                    toast2('success', data_json['message'])
                    $('#generateRRC').prop('disabled', false);
                    $('#file_download').css('visibility', 'visible');
                    $('#file_download').attr('href', data_json['file_return']);
                } else {
                    toast2('error', data_json['message'])
                }
                $('#generateRRC').removeClass('m-loader m-loader--light m-loader--left');
                $('#generateRRC').prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                toast2('error', 'Se presento un error al generar el archivo.');
                $('#generateRRC').removeClass('m-loader m-loader--light m-loader--left');
                $('#generateRRC').prop('disabled', false);
            }
        });
    });
});