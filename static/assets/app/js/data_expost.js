// Función para obtener listas desplegables actualizadas

function get_selects(objeto_origen) {

    var data = new FormData();

    var socio_seleccionado = $("#socios").val();
    if (socio_seleccionado != "") {
        var socio_seleccionado = socio_seleccionado + ","
        var socio_seleccionado = socio_seleccionado.split(",");
        var socio_seleccionado = socio_seleccionado.slice(0, -1);
    } else {
        var socio_seleccionado = [""]
    }

    var producto_seleccionado = $("#productos").val();
    if (producto_seleccionado != "") {
        var producto_seleccionado = producto_seleccionado + ","
        var producto_seleccionado = producto_seleccionado.split(",");
        var producto_seleccionado = producto_seleccionado.slice(0, -1);
    } else {
        var producto_seleccionado = [""]
    }

    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    data.append('socios', socio_seleccionado);
    data.append('productos', producto_seleccionado);

    mApp.block(".block", {overlayColor: "#000000", type: "loader", state: "primary", message: "Procesando..."});

    //data.append('risks', risks_seleccionado);

    $.ajax({
        url: '/data_expost_selects',
        type: 'POST',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success:
            function (data_json) {

                /******* ACTUALIZAR SOCIOS *******/
                if (objeto_origen != 'socios' | $("#" + objeto_origen).val() == '') {
                    $('#socios').html('', true);
                    socios = data_json[0];
                    for (i = 0; i < socios.length; i++) {
                        if (socio_seleccionado.includes(socios[i])) {
                            var data = '<option selected>' + socios[i] + '</option>';
                        } else {
                            var data = '<option>' + socios[i] + '</option>';
                        }
                        $('#socios').append(data);
                    }
                }

                 /******* ACTUALIZAR PRODUCTOS *******/
                if (objeto_origen != 'productos' | $("#" + objeto_origen).val() == '') {
                    $('#productos').html('', true);
                    productos = data_json[5];
                    for (i = 0; i < productos.length; i++) {
                        if (producto_seleccionado.includes(productos[i])) {
                            var data = '<option selected>' + productos[i] + '</option>';
                        } else {
                            var data = '<option>' + productos[i] + '</option>';
                        }
                        $('#productos').append(data);
                    }
                }

                var BootstrapSelect = {
                    init: function () {
                        $(".m_selectpicker").selectpicker('refresh')
                    }
                };
                BootstrapSelect.init();

                /*
                $('#example').DataTable({
                    searching: false, paging: false, info: false,
                    data: data_json[7],
                    "lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'Export to excel' }
                        //'csvHtml5', 'pdfHtml5'
                    ],
                    columns: [
                        {"data": "ANUAL"},
                        {"data": "OCURRENCIA"},
                        {"data": "EXPUESTO", render: $.fn.dataTable.render.number( ',', '.', 2 )},
                        {"data": "EP", render: $.fn.dataTable.render.number( ',', '.', 2 )},
                        {"data": "SEVERITY", render: $.fn.dataTable.render.number( ',', '.', 2 )},
                        {"data": "RISK_PREMIUM", render: $.fn.dataTable.render.number( ',', '.', 2 )},
                        {"data": "PRIC_RISK_PREM", render: $.fn.dataTable.render.number( ',', '.', 2 )},
                        {"data": "ULTIMATE LOSS", render: $.fn.dataTable.render.number( ',', '.', 2 )},
                        {"data": "LR_ACUM"},
                        {"data": "QX_ACUM"},
                    ],
                    "bDestroy": true,
                    //"order": [[ 1, "desc" ]]
                });
                */

                $('#tria_count_df').html(data_json[2]);
                $('.table_count').DataTable({
                    searching: false, paging: false, info: false,
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'Export to excel' }
                    ],
                    "scrollY":        "300px",
                    //"scrollX":        "300px",
                    //"scrollCollapse": true,
                    "paging":         false
                });
                /*
                $('#tria_incu_df').html(data_json[10]);
                $('.table_incu').DataTable({
                    searching: false, paging: false, info: false,
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'Export to excel' }
                    ],
                    "scrollY":        "300px",
                    //"scrollX":        "300px",
                    //"scrollCollapse": true,
                    "paging":         false
                });

                $('#tria_expu_df').html(data_json[11]);
                $('.table_expu').DataTable({
                    searching: false, paging: false, info: false,
                    dom: 'Bfrtip',
                    buttons: [
                        { extend: 'excelHtml5', text: 'Export to excel' }
                    ],
                    "scrollY":        "300px",
                    //"scrollX":        "300px",
                    //"scrollCollapse": true,
                    "paging":         false
                });
                */
                /**************************************************************************************/
            mApp.unblock(".block");
            },
        error: function (xhr, ajaxOptions, thrownError) {
            toast2('error', 'No se cargaron los datos con éxito')
            mApp.unblock(".block");
        }
    });
}


$(document).ready(function () {
    //Cargamos los selects
    get_selects()
});

// Función para actualizar gráfico y listas desplegables
function reload_data(objeto_origen) {

    // Actualizar listas desplegables
    get_selects(objeto_origen)

    //get_checkbox(objeto_origen)


    // Actualizar gráfico
    //get_data(objeto_origen)
}


