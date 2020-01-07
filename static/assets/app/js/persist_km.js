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


    var linea_fina_seleccionado = $("#linea_negocio").val();
    if (linea_fina_seleccionado != "") {
        var linea_fina_seleccionado = linea_fina_seleccionado + ","
        var linea_fina_seleccionado = linea_fina_seleccionado.split(",");
        var linea_fina_seleccionado = linea_fina_seleccionado.slice(0, -1);
    } else {
        var linea_fina_seleccionado = [""]
    }

    var periodo_seleccionado = $("#periodo").val();
    if (periodo_seleccionado != "") {
        var periodo_seleccionado = periodo_seleccionado + ","
        var periodo_seleccionado = periodo_seleccionado.split(",");
        var periodo_seleccionado = periodo_seleccionado.slice(0, -1);
    } else {
        var periodo_seleccionado = [""]
    }

    var canal_seleccionado = $("#canal").val();
    if (canal_seleccionado != "") {
        var canal_seleccionado = canal_seleccionado + ","
        var canal_seleccionado = canal_seleccionado.split(",");
        var canal_seleccionado = canal_seleccionado.slice(0, -1);
    } else {
        var canal_seleccionado = [""]
    }

    var producto_seleccionado = $("#productos").val();
    if (producto_seleccionado != "") {
        var producto_seleccionado = producto_seleccionado + ","
        var producto_seleccionado = producto_seleccionado.split(",");
        var producto_seleccionado = producto_seleccionado.slice(0, -1);
    } else {
        var producto_seleccionado = [""]
    }

    var media_seleccionado = $("#media").val();
    if (media_seleccionado != "") {
        var media_seleccionado = media_seleccionado + ","
        var media_seleccionado = media_seleccionado.split(",");
        var media_seleccionado = media_seleccionado.slice(0, -1);
    } else {
        var media_seleccionado = [""]
    }

    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    data.append('socios', socio_seleccionado);
    data.append('linea_negocio', linea_fina_seleccionado);
    data.append('periodo', periodo_seleccionado);
    data.append('canal', canal_seleccionado);
    data.append('productos', producto_seleccionado);
    data.append('media', media_seleccionado);

    mApp.block(".block", {overlayColor: "#000000", type: "loader", state: "primary", message: "Procesando..."});

    $.ajax({
        url: '/persist_km_selects',
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


                /******* ACTUALIZAR LINEA NEGOCIO *******/
                if (objeto_origen != 'linea_negocio' | $("#" + objeto_origen).val() == '') {
                    $('#linea_negocio').html('', true);
                    linea_negocio = data_json[1];
                    for (i = 0; i < linea_negocio.length; i++) {
                        if (linea_fina_seleccionado.includes(linea_negocio[i])) {
                            var data = '<option selected>' + linea_negocio[i] + '</option>';
                        } else {
                            var data = '<option>' + linea_negocio[i] + '</option>';
                        }
                        $('#linea_negocio').append(data);
                    }
                }

                /******* ACTUALIZAR PERIODICIDAD *******/

                if (objeto_origen != 'periodo' | $("#" + objeto_origen).val() == '') {
                    $('#periodo').html('', true);
                    periodo = data_json[2];
                    for (i = 0; i < periodo.length; i++) {
                        if (periodo_seleccionado.includes(periodo[i])) {
                            var data = '<option selected>' + periodo[i] + '</option>';
                        } else {
                            var data = '<option>' + periodo[i] + '</option>';
                        }
                        $('#periodo').append(data);
                    }
                }

                /******* ACTUALIZAR CANAL *******/
                if (objeto_origen != 'canal' | $("#" + objeto_origen).val() == '') {
                    $('#canal').html('', true);
                    canal = data_json[3];
                    for (i = 0; i < canal.length; i++) {
                        if (canal_seleccionado.includes(canal[i])) {
                            var data = '<option selected>' + canal[i] + '</option>';
                        } else {
                            var data = '<option>' + canal[i] + '</option>';
                        }
                        $('#canal').append(data);
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


                var BootstrapSelect = {
                    init: function () {
                        $(".m_selectpicker").selectpicker('refresh')
                    }
                };
                BootstrapSelect.init();


                $('#table_q1').DataTable(
                    {
                    searching: false, paging: false, info: false,
                    data: data_json[5],
                    //"lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    columns: [
                        {"data": "Av_rate"},
                        {"data": "Duration_2", render: $.fn.dataTable.render.number( ',', '.', 1 )},
                        {"data": "VIGENTES",   render: $.fn.dataTable.render.number( ',', '.', 0 )}
                    ],
                    "bDestroy": true,
                    //"order": [[ 1, "desc" ]]
                });

                $('#table_q2').DataTable({
                    searching: false, paging: false, info: false,
                    data: data_json[6],
                    //"lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    columns: [
                        {"data": "t"},
                        {"data": "S_t_2"},
                        {"data": "Lapse_rate"}
                    ],
                    "bDestroy": true,
                    //"order": [[ 1, "desc" ]]
                });

                 $('#table_q3').DataTable({
                     searching: false, paging: false, info: false,
                    data: data_json[7],
                    //"lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    columns: [
                        {"data": "RANGE"},
                        {"data": "d"},
                        {"data": "c"},
                        {"data": "TOTAL"},
                        {"data": "q_x"}
                    ],
                    "bDestroy": true,
                    //"order": [[ 5, "desc" ]]
                });

                //Data Graphs
                data_graph_01 = data_json[8];
                data_graph_03 = data_json[9];
                data_graph_04 = data_json[10];

                /*************************************************************************************************************************/
                /*************************************** GRAPH 1 ******************************************************/
                /*************************************************************************************************************************/

                var chart = AmCharts.makeChart("chartdiv31", {
                    "type": "serial",
                    "theme": "light",
                    "dataDateFormat": "YYYY-MM-DD",
                    "precision": 2,

                    "valueAxes":
                        [{
                            "id": "v1",
                            "unit": "%",
                            "position": "left",
                            "autoGridCount": false,
                        },
                        ],

                    "graphs":
                        [
                            {
                                "id": "g1",
                                "valueAxis": "v1",
                                "bullet": "round",
                                "bulletBorderAlpha": 1,
                                "bulletColor": "#FFFFFF",
                                "bulletSize": 7,
                                "hideBulletsCount": 50,
                                "lineThickness": 5,
                                "lineColor": "#20acd4",
                                "type": "smoothedLine",
                                "title": "S(t)",
                                "useLineColorForBulletBorder": true,
                                "valueField": "S_t_2",
                                "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]%</b>"
                            },
                        ],
                    "chartCursor": {
                        "pan": true,
                        "valueLineEnabled": true,
                        "valueLineBalloonEnabled": true,
                        "cursorAlpha": 0,
                        "valueLineAlpha": 0.2
                    },
                    "categoryField": "t",
                    //"categoryField": "date",
                    "categoryAxis": {
                        //"parseDates": true,
                        "dashLength": 1,
                        "minorGridEnabled": true,
                        "gridCount": 50,
                        "labelRotation": 50
                    },
                    "legend": {
                        "useGraphSettings": true,
                        "position": "top"
                    },
                    "balloon": {
                        "borderThickness": 1,
                        "shadowAlpha": 0
                    },
                    "export": {
                        enabled: true
                    },
                    "dataProvider": data_graph_01,
                });

                var chart = AmCharts.makeChart("chartdiv32", {
                    "type": "serial",
                    "theme": "light",
                    "dataDateFormat": "YYYY-MM-DD",
                    "precision": 2,

                    "valueAxes":
                        [{
                            "id": "v1",
                            "unit": "%",
                            "position": "left",
                            "autoGridCount": false,
                        },
                        ],

                    "graphs":
                        [
                            {
                                "id": "g1",
                                "valueAxis": "v1",
                                "bullet": "round",
                                "bulletBorderAlpha": 1,
                                "bulletColor": "#FFFFFF",
                                "bulletSize": 7,
                                "hideBulletsCount": 50,
                                "lineThickness": 5,
                                "lineColor": "#20acd4",
                                "type": "smoothedLine",
                                "title": "Lapse_rate",
                                "useLineColorForBulletBorder": true,
                                "valueField": "Lapse_rate",
                                "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]%</b>"
                            },

                             {
                                "id": "h1",
                                "valueAxis": "v1",
                                "bullet": "round",
                                "lineThickness": 3,
                                "bulletSize": 1,
                                "bulletBorderAlpha": 1,
                                "bulletColor": "#FFFFFF",
                                "useLineColorForBulletBorder": true,
                                "bulletBorderThickness": 1,
                                "fillAlphas": 0,
                                "lineAlpha": 1,
                                "title": "Av_rate",
                                "valueField": "Av_rate",
                                "dashLengthField": "dashLengthLine",
                                "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]%</b>"
                            }
                        ],
                    "chartCursor": {
                        "pan": true,
                        "valueLineEnabled": true,
                        "valueLineBalloonEnabled": true,
                        "cursorAlpha": 0,
                        "valueLineAlpha": 0.2
                    },
                    "categoryField": "t",
                    //"categoryField": "date",
                    "categoryAxis": {
                        //"parseDates": true,
                        "dashLength": 1,
                        "minorGridEnabled": true,
                        "gridCount": 50,
                        "labelRotation": 50
                    },
                    "legend": {
                        "useGraphSettings": true,
                        "position": "top"
                    },
                    "balloon": {
                        "borderThickness": 1,
                        "shadowAlpha": 0
                    },
                    "export": {
                        enabled: true
                    },
                    "dataProvider": data_graph_01,
                });

                var chart = AmCharts.makeChart("chartdiv33", {
                    "type": "serial",
                    "theme": "light",
                    "dataDateFormat": "YYYY-MM-DD",
                    "precision": 2,

                    "valueAxes":
                        [{
                            "id": "v1",
                            "unit": "%",
                            "gridAlpha": 0,
                            "position": "left",
                            "autoGridCount": false,
                        },
                        ],

                    "graphs":
                        [
                            {
                                "id": "zz",
                                "valueAxis": "v1",
                                "lineColor": "#62cf73",
                                "fillColors": "#62cf73",
                                "fillAlphas": 1,
                                "type": "column",
                                "title": "q_x",
                                "valueField": "q_x",
                                "clustered": false,
                                "columnWidth": 0.8,
                                "balloonText": "[[title]]<br/><b style='font-size: 90%'>[[value]]%</b>"
                            },

                        ],
                    "chartCursor": {
                        "pan": true,
                        "valueLineEnabled": true,
                        "valueLineBalloonEnabled": true,
                        "cursorAlpha": 0,
                        "valueLineAlpha": 0.2
                    },
                    "categoryField": "RANGE",
                    //"categoryField": "date",
                    "categoryAxis": {
                        //"parseDates": true,
                        "dashLength": 1,
                        "minorGridEnabled": true,
                        "gridCount": 50,
                        "labelRotation": 50
                    },
                    "legend": {
                        "useGraphSettings": true,
                        "position": "top"
                    },
                    "balloon": {
                        "borderThickness": 1,
                        "shadowAlpha": 0
                    },
                    "export": {
                        enabled: true
                    },
                    "dataProvider": data_graph_03,
                });

                var chart = AmCharts.makeChart("chartdiv34", {
                    "type": "serial",
                    "theme": "light",
                    "dataDateFormat": "YYYY-MM-DD",
                    "precision": 0,

                    "valueAxes":
                        [{
                            "id": "v1",
                            //"unit": "%",
                            "gridAlpha": 0,
                            "position": "left",
                            "autoGridCount": false,
                        },
                        ],

                    "graphs":
                        [
                            {
                                "id": "zz",
                                "valueAxis": "v1",
                                "lineColor": "#3498DB",
                                "fillColors": "#3498DB",
                                "fillAlphas": 1,
                                "type": "column",
                                "title": "VIGENTES",
                                "valueField": "CONTEO",
                                "clustered": false,
                                "columnWidth": 0.8,
                                "balloonText": "[[title]]<br/><b style='font-size: 90%'>[[value]]</b>"
                            },

                        ],
                    "chartCursor": {
                        "pan": true,
                        "valueLineEnabled": true,
                        "valueLineBalloonEnabled": true,
                        "cursorAlpha": 0,
                        "valueLineAlpha": 0.2
                    },
                    "categoryField": "ANUAL",
                    //"categoryField": "date",
                    "categoryAxis": {
                        //"parseDates": true,
                        "dashLength": 1,
                        "minorGridEnabled": true,
                        "gridCount": 50,
                        "labelRotation": 50
                    },
                    "legend": {
                        "useGraphSettings": true,
                        "position": "top"
                    },
                    "balloon": {
                        "borderThickness": 1,
                        "shadowAlpha": 0
                    },
                    "export": {
                        enabled: true
                    },
                    "dataProvider": data_graph_04,
                });

                 /**************************************************************************************/
                mApp.unblock(".block");

            },
        error: function (xhr, ajaxOptions, thrownError) {
            toast2('error', 'No se cargaron los datos con éxito')
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


