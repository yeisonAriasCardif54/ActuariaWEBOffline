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

    var canal_seleccionado = $("#canales").val();
    if (canal_seleccionado != "") {
        var canal_seleccionado = canal_seleccionado + ","
        var canal_seleccionado = canal_seleccionado.split(",");
        var canal_seleccionado = canal_seleccionado.slice(0, -1);
    } else {
        var canal_seleccionado = [""]
    }

    var linea_fina_seleccionado = $("#linea_fina").val();
    if (linea_fina_seleccionado != "") {
        var linea_fina_seleccionado = linea_fina_seleccionado + ","
        var linea_fina_seleccionado = linea_fina_seleccionado.split(",");
        var linea_fina_seleccionado = linea_fina_seleccionado.slice(0, -1);
    } else {
        var linea_fina_seleccionado = [""]
    }

    var tipo_seleccionado = $("#tipos").val();
    if (tipo_seleccionado != "") {
        var tipo_seleccionado = tipo_seleccionado + ","
        var tipo_seleccionado = tipo_seleccionado.split(",");
        var tipo_seleccionado = tipo_seleccionado.slice(0, -1);
    } else {
        var tipo_seleccionado = [""]
    }

    var producto_seleccionado = $("#productos").val();
    if (producto_seleccionado != "") {
        var producto_seleccionado = producto_seleccionado + ","
        var producto_seleccionado = producto_seleccionado.split(",");
        var producto_seleccionado = producto_seleccionado.slice(0, -1);
    } else {
        var producto_seleccionado = [""]
    }

    var database_seleccionado = $("#database").val();
    if (database_seleccionado != "") {
        var database_seleccionado = database_seleccionado + ","
        var database_seleccionado = database_seleccionado.split(",");
        var database_seleccionado = database_seleccionado.slice(0, -1);
    } else {
        var database_seleccionado = [""]
    }

    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    data.append('socios', socio_seleccionado);
    data.append('canales', canal_seleccionado);
    data.append('tipos', tipo_seleccionado);
    data.append('linea_fina', linea_fina_seleccionado);
    data.append('productos', producto_seleccionado);
    data.append('database', database_seleccionado);

    mApp.block(".block", {overlayColor: "#000000", type: "loader", state: "primary", message: "Procesando..."});    ``

    $.ajax({
        url: '/life_eg_selects',
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

                /******* ACTUALIZAR CANALES *******/
                if (objeto_origen != 'canales' | $("#" + objeto_origen).val() == '') {
                    $('#canales').html('', true);
                    canales = data_json[1];
                    for (i = 0; i < canales.length; i++) {
                        if (canal_seleccionado.includes(canales[i])) {
                            var data = '<option selected>' + canales[i] + '</option>';
                        } else {
                            var data = '<option>' + canales[i] + '</option>';
                        }
                        $('#canales').append(data);
                    }
                }

                /******* ACTUALIZAR TIPO *******/
                if (objeto_origen != 'tipos' | $("#" + objeto_origen).val() == '') {
                    $('#tipos').html('', true);
                    tipos = data_json[2];
                    for (i = 0; i < tipos.length; i++) {
                        if (tipo_seleccionado.includes(tipos[i])) {
                            var data = '<option selected>' + tipos[i] + '</option>';
                        } else {
                            var data = '<option>' + tipos[i] + '</option>';
                        }
                        $('#tipos').append(data);
                    }
                }

                /******* ACTUALIZAR LINEA_NEGOCIO *******/
                if (objeto_origen != 'linea_fina' | $("#" + objeto_origen).val() == '') {
                    $('#linea_fina').html('', true);
                    linea_fina = data_json[3];
                    for (i = 0; i < linea_fina.length; i++) {
                        if (linea_fina_seleccionado.includes(linea_fina[i])) {
                            var data = '<option selected>' + linea_fina[i] + '</option>';
                        } else {
                            var data = '<option>' + linea_fina[i] + '</option>';
                        }
                        $('#linea_fina').append(data);
                    }
                }

                /******* ACTUALIZAR PRODUCTOS *******/
                if (objeto_origen != 'productos' | $("#" + objeto_origen).val() == '') {
                    $('#productos').html('', true);
                    productos = data_json[4];
                    for (i = 0; i < productos.length; i++) {
                        if (producto_seleccionado.includes(productos[i])) {
                            var data = '<option selected>' + productos[i] + '</option>';
                        } else {
                            var data = '<option>' + productos[i] + '</option>';
                        }
                        $('#productos').append(data);
                    }
                }

                /******* ACTUALIZAR DATABASE *******/
                if (objeto_origen != 'database' | $("#" + objeto_origen).val() == '') {
                    $('#database').html('', true);
                    database = data_json[5];
                    for (i = 0; i < database.length; i++) {
                        if (database_seleccionado.includes(database[i])) {
                            var data = '<option selected>' + database[i] + '</option>';
                        } else {
                            var data = '<option>' + database[i] + '</option>';
                        }
                        $('#database').append(data);
                    }
                }

                var BootstrapSelect = {
                    init: function () {
                        $(".m_selectpicker").selectpicker('refresh')
                    }
                };
                BootstrapSelect.init();

                //alert(data_json[3])

                $('#table_').DataTable({
                     searching: false, paging: false, info: false,
                    data: data_json[7],
                    //"lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    columns: [
                        {"data": "CATEGORIA"},
                        {"data": "Male"},
                        {"data": "Female"},
                        {"data": "No_Info"},
                        {"data": "TOTAL"},
                        {"data": "PORC"}
                    ],
                    "bDestroy": true,
                    //"order": [[ 5, "desc" ]]
                });


                $('#table_2').DataTable({
                     searching: false, paging: false, info: false,
                    data: data_json[8],
                    //"lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    columns: [
                        {"data": "Medidas"},
                        {"data": "Male"},
                        {"data": "Female"},
                        {"data": "Total"},
                    ],
                    "bDestroy": true,
                    //"order": [[ 5, "desc" ]]
                });


                //Data Graphs
                data_table = data_json[6];

                // PYRAMID GRAPHS //
                var chart = AmCharts.makeChart("chartdiv", {
                          "type": "serial",
                          "theme": "none",
                          "rotate": true,
                          "marginBottom": 50,
                          "dataProvider": data_table,

                          "startDuration": 1,

                          "graphs": [

                              {
                            "fillAlphas": 0.8,
                            "lineAlpha": 0.2,
                            "type": "column",

                            "lineColor": "#2A62E7",
                            "fillColors": "#2A62E7",
                            "fillAlphas": 1,

                            "valueField": "Male_Perc",
                            "title": "Male",
                            "labelText": "[[value]]",
                            "clustered": false,
                            "labelFunction": function(item) {
                              return Math.abs(item.values.value) + "%";
                            },
                            "balloonFunction": function(item) {
                              //return item.category + ": " + Math.abs(item.values.value) + "%";
                                return item.category + ": " + Math.abs(item.values.value) + "%";
                            }
                          },

                              {
                            "fillAlphas": 0.8,
                            "lineAlpha": 0.2,
                            "type": "column",
                              "lineColor": "#FF2D73",
                            "fillColors": "#FF2D73",
                            "fillAlphas": 1,

                            "valueField": "Female_Perc",
                            "title": "Female",
                            "labelText": "[[value]]",
                            "clustered": false,


                            "labelFunction": function(item) {
                              return Math.abs(item.values.value) + "%";
                            },
                            "balloonFunction": function(item) {
                              //return item.category + ": " + Math.abs(item.values.value) + "%";
                                return item.category + ": " + Math.abs(item.values.value) + "%";
                            }

                          }],
                          "categoryField": "CATEGORIA",
                          "categoryAxis": {
                            "gridPosition": "start",
                            "gridAlpha": 0.2,
                            "axisAlpha": 0
                          },
                          "valueAxes": [{
                            "gridAlpha": 0,
                            "ignoreAxisWidth": true,

                            "labelFunction": function(value) {
                              //return Math.abs(value) + '%';
                                return Math.abs(value);
                            },
                            "guides": [{
                              "value": 0,
                              "lineAlpha": 0.2
                            }]
                          }],
                          "balloon": {
                            "fixedPosition": true
                          },
                          "chartCursor": {
                            "valueBalloonsEnabled": false,
                            "cursorAlpha": 0.05,
                            "fullWidth": true
                          },
                          "allLabels": [{
                            "text": "Male",
                            "x": "28%",
                            "y": "97%",
                            "bold": true,
                            "align": "middle"
                          }, {
                            "text": "Female",
                            "x": "75%",
                            "y": "97%",
                            "bold": true,
                            "align": "middle"
                          }],

                        /*
                         "export": {
                            "enabled": true
                          }
                        */

                        })

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

}


