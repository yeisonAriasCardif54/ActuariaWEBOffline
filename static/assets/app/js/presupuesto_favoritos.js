$(document).ready(function () {
    $('body').delegate('#generateHistorico', 'click', function () {
        $.ajax({
            url: '/herramienta_presupuesto/get_history_group',
            dataType: 'JSON',
            success: function (data) {
                $('#logFavoritosGrupo').DataTable({
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
                                if (F_OUTPUT == 'Error al generar archivo') {
                                    return "<div>" + F_OUTPUT + "</div>";
                                } else {
                                    if (F_OUTPUT.includes("csv")) {
                                        return "<a target='_blank' href='static/profitability/update_presupuesto/" + F_OUTPUT + "'>" + F_OUTPUT + "</a>" + "<br>" +
                                            "<a target='_blank' href='herramienta_presupuesto/convert_xlsx?file=" + F_OUTPUT + "&to=puntoycoma'>Descargar CSV (;)</a>" + "<br>" +
                                            "<a target='_blank' href='herramienta_presupuesto/convert_xlsx?file=" + F_OUTPUT + "&to=excel'>Descargar Excel</a>"
                                    } else {
                                        return "<a target='_blank' href='static/profitability/update_presupuesto/" + F_OUTPUT + "'>" + F_OUTPUT + "</a>"
                                    }
                                }
                            }
                        }
                    ],
                    "bDestroy": true,
                    "order": [[0, "desc"]]
                });
                $('#myModal').modal('show');
            },
            error: function (request, status, error) {
                toast2('error', 'Error al consultar los presupuestos generados marcados como "favoritos"');
            }
        });
    });
});