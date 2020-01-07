function update_AllHistoryBP(category) {
    $.ajax({
        url: '/business_plan_tool/historyTable/' + category,
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
                            icon_category = '';
                            if (CATEGORIA != 'None') {
                                icon_category += '<i title="' + CATEGORIA + '" class="la la-star" style="font-size: 11px !important; color: ' + CATEGORIA_COLOR + ' !important;"></i> '
                            }
                            return icon_category + FIRST_NAME + ' ' + LAST_NAME;
                        }
                    },
                    {"data": "DATETIME"},
                    {
                        "mRender": function (data, type, row) {
                            var F_INPUT = row.FILE_INPUT;
                            return "<a href='/static/pricing/business_plan_input/" + F_INPUT + "'>" + F_INPUT + "</a>";
                        }
                    },
                    {
                        "mRender": function (data, type, row) {
                            var ID = row.ID;
                            var F_OUTPUT = row.FILE_OUTPUT;
                            var ERROR = row.ERROR;
                            if (F_OUTPUT == 'Error al generar archivo') {
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
                                    '\t\t\t<div class="modal-body">\n' + '<pre>' + ERROR + '</pre>' +
                                    '\t\t\t</div>\n' +
                                    '\t\t\t<div class="modal-footer">\n' +
                                    '\t\t\t\t<button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>\n' +
                                    '\t\t\t</div>\n' +
                                    '\t\t</div>\n' +
                                    '\t</div>\n' +
                                    '</div>'
                            } else {
                                return "<a href='/static/pricing/business_plan_output/" + F_OUTPUT + "'>" + F_OUTPUT + "</a>";
                            }
                        }
                    },
                    {
                        "mRender": function (data, type, row) {
                            var SUCCESS = row.SUCCESS;
                            var CATEGORIA = row.NOMBRE;
                            var ID = row.ID;
                            var name_category = 'Ninguna';
                            if (CATEGORIA != 'None') {
                                name_category = CATEGORIA
                            }
                            html = '';
                            if (SUCCESS == 1) {
                                html = '<button class="btn btn-secondary btn-sm dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-vivaldi-spatnav-clickable="1">\n' +
                                    name_category +
                                    '</button>' +
                                    '<div class="dropdown-menu" x-placement="bottom-start" style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(0px, 31px, 0px);">\n';
                                if ('Ninguna' != name_category) {
                                    html += '<a class="dropdown-item cambiar_categoria" style="cursor: pointer !important" data-idcategory="0" data-id="' + ID + '"><i title="Ninguna" class="la la-star" style="font-size: 11px !important; color: #c4c5d6  !important;"></i> Ninguna</a>\n';
                                }
                                // -- Recorrer todas las categorías
                                var categoriesHTML = '';
                                $.each(categories, function (i, val) {
                                    if (categories[i]['NOMBRE'] != name_category) {
                                        categoriesHTML += '<a class="dropdown-item cambiar_categoria" style="cursor: pointer !important" data-idcategory="' + categories[i]['ID'] + '" data-id="' + ID + '"><i title="' + categories[i]['NOMBRE'] + '" class="la la-star" style="font-size: 11px !important; color: ' + categories[i]['COLOR'] + '  !important;"></i> ' + categories[i]['NOMBRE'] + '</a>\n';
                                    }
                                });
                                html += categoriesHTML;
                                html += '</div>';
                            }
                            return html
                        }
                    },
                    {
                        "mRender": function (data, type, row) {
                            var SUCCESS = row.SUCCESS;
                            var CATEGORIA = row.NOMBRE;
                            var ID = row.ID;
                            var name_category = 'Ninguna';

                            html = '<a onclick="update_state('+ID+')" class="m-portlet__nav-link btn m-btn m-btn--hover-danger m-btn--icon m-btn--icon-only m-btn--pill" title="View">\n' +
                            '<i class="la la-times-circle"></i>\n' +
                            '</a>';
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
    // -- Cargar histórico en categoría 'Todos'
    update_AllHistoryBP(0);
});

$(document).delegate('.cambiar_categoria', 'click', function () {
    idcategory = $(this).data('idcategory');
    id = $(this).data('id');

    var data = new FormData();
    data.append('idcategory', idcategory);
    data.append('id', id);
    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());

    $.ajax({
        url: '/business_plan_tool/change_category',
        type: 'POST',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success: function (data_json) {
            if (data_json) {
                toast2('success', 'Registro Actualizado');
                // update_AllHistoryBP(0);
                $(".m-tabs__item--active").click()
            } else {
                toast2('error', 'Error al actualizar el registro');
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            toast2('error', 'Error al actualizar el registro');
        }
    });
});

function update_state(id) {
    var r = confirm("Eliminar el registro?");
    if (r === true) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('id', id);
        $.ajax({
            url: '/business_plan_tool/update_state',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json) {
                    $(".m-tabs__item--active").click();
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