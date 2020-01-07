function update_AllHistoryBP(category) {
    $.ajax({
        url: '/recursos/tableAjax/' + category,
        type: 'GET',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: [],
        success: function (dataAJAX) {
            var data = dataAJAX.DTable;
            var categories = dataAJAX.categories;

            $('#logHistoryCategory' + category).DataTable({
                data: data,
                "lengthMenu": [[-1], ["Todos"]],
                columns: [
                    {"data": "ID"},
                    {
                        "mRender": function (data, type, row) {
                            var CATEGORIA = row.NOMBRE;
                            var CATEGORIA_COLOR = row.COLOR;
                            var FIRST_NAME = row.FIRST_NAME;
                            var LAST_NAME = row.LAST_NAME;
                            return FIRST_NAME + ' ' + LAST_NAME;
                        }
                    },
                    {"data": "DATETIME"},
                    {
                        "mRender": function (data, type, row) {
                            var ID = row.ID;
                            var FILE_OUTPUT_BP = row.FILE_OUTPUT_BP;
                            var ERROR_BP = row.ERROR_BP;
                            if (FILE_OUTPUT_BP == 'Error al generar archivo') {
                                return '<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#m_modal_' + ID + '">' + F_OUTPUT + '</button>' +
                                    '<div class="modal fade" id="m_modal_' + ID + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" data-vivaldi-spatnav-clickable="1" aria-hidden="true" style="display: none;">\n' +
                                    '\t<div class="modal-dialog modal-lg" role="document">\n' +
                                    '\t\t<div class="modal-content">\n' +
                                    '\t\t\t<div class="modal-header">\n' +
                                    '\t\t\t\t<h5 class="modal-title" id="exampleModalLabel">Mensaje de Error</h5>\n' +
                                    '\t\t\t\t<button type="button" class="close" data-dismiss="modal" aria-label="Close">\n' +
                                    '\t\t\t\t\t<span aria-hidden="true">×</span>\n' +
                                    '\t\t\t\t</button>\n' +
                                    '\t\t\t</div>\n' +
                                    '\t\t\t<div class="modal-body">\n' + '<pre>' + ERROR_BP + '</pre>' +
                                    '\t\t\t</div>\n' +
                                    '\t\t\t<div class="modal-footer">\n' +
                                    '\t\t\t\t<button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>\n' +
                                    '\t\t\t</div>\n' +
                                    '\t\t</div>\n' +
                                    '\t</div>\n' +
                                    '</div>'
                            } else {
                                return "<a target='_blank' href='/recursos/formato/" + ID + "'><i class='la la-file-excel-o' style='color: #13e112;font-size: 28px;'></i></i></a>";
                            }
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
    update_AllHistoryBP(0);
});