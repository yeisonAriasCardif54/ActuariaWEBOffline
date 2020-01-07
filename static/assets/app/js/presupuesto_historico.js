
function update_AllHistory() {
    $.ajax({
        url: '/herramienta_presupuestoH/get_history_all',
        type: 'GET',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: [],
        success: function (data) {
            $('#logHistory').DataTable({
                data: data,
                "lengthMenu": [[-1], ["Todos"]],
                columns: [
                    {"data": "ID"},
                    {
                        "mRender": function (data, type, row) {
                            var FIRST_NAME = row.FIRST_NAME;
                            var LAST_NAME = row.LAST_NAME;
                            return FIRST_NAME + ' ' + LAST_NAME;
                        }
                    },
                    {"data": "DATETIME"},
                    {
                        "mRender": function (data, type, row) {
                            var F_INPUT = row.FILE_INPUT;
                            return "<a href='/static/profitability/update_presupuesto/" + F_INPUT + "'>" + F_INPUT + "</a>";
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
                            var F_OUTPUT = row.FILE_OUTPUT;
                            var FAVORITE = row.FAVORITE;
                            var SUCCESS = row.SUCCESS;
                            favorite = (FAVORITE == 1) ? "btn-warning" : "btn-outline-warning";
                            html = '';
                            if (SUCCESS == 1) {
                                html = '<button type="button" data-file="' + F_OUTPUT + '"  title="ver Resumen" class="btn btn-outline-dark m-btn m-btn--icon btn-sm m-btn--icon-only m-btn--pill m-btn--air button_get_summary view_summary" style="margin-right: 5px;">' +
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
    update_AllHistory();
});