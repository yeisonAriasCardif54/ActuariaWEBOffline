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

    var linea_seleccionado = $("#linea").val();
    if (linea_seleccionado != "") {
        var linea_seleccionado = linea_seleccionado + ","
        var linea_seleccionado = linea_seleccionado.split(",");
        var linea_seleccionado = linea_seleccionado.slice(0, -1);
    } else {
        var linea_seleccionado = [""]
    }

    var linea_fina_seleccionado = $("#linea_negocio").val();
    if (linea_fina_seleccionado != "") {
        var linea_fina_seleccionado = linea_fina_seleccionado + ","
        var linea_fina_seleccionado = linea_fina_seleccionado.split(",");
        var linea_fina_seleccionado = linea_fina_seleccionado.slice(0, -1);
    } else {
        var linea_fina_seleccionado = [""]
    }

    var risk_seleccionado = $("#risk").val();
    if (risk_seleccionado != "") {
        var risk_seleccionado = risk_seleccionado + ","
        var risk_seleccionado = risk_seleccionado.split(",");
        var risk_seleccionado = risk_seleccionado.slice(0, -1);
    } else {
        var risk_seleccionado = [""]
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

    var tipo_seleccionado = $("#tipo").val();
    if (tipo_seleccionado != "") {
        var tipo_seleccionado = tipo_seleccionado + ","
        var tipo_seleccionado = tipo_seleccionado.split(",");
        var tipo_seleccionado = tipo_seleccionado.slice(0, -1);
    } else {
        var tipo_seleccionado = [""]
    }

    /*
    var qx_seleccionado = $("#qx_select").val();
    if (qx_seleccionado != "") {
        var qx_seleccionado = qx_seleccionado + ","
        var qx_seleccionado = qx_seleccionado.split(",");
        var qx_seleccionado = qx_seleccionado.slice(0, -1);
    } else {
        var qx_seleccionado = [""]
    }
    */

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
    data.append('linea', linea_seleccionado);
    data.append('linea_negocio', linea_fina_seleccionado);
    data.append('risk', risk_seleccionado);
    data.append('canal', canal_seleccionado);
    data.append('productos', producto_seleccionado);
    data.append('tipo', tipo_seleccionado);
    data.append('media', media_seleccionado);

    mApp.block(".block", {overlayColor: "#000000", type: "loader", state: "primary", message: "Procesando..."});

    //data.append('risks', risks_seleccionado);

    $.ajax({
        url: '/frecuencia_selects',
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

                /******* ACTUALIZAR LINEA *******/
                if (objeto_origen != 'linea' | $("#" + objeto_origen).val() == '') {
                    $('#linea').html('', true);
                    linea = data_json[1];
                    for (i = 0; i < linea.length; i++) {
                        if (linea_seleccionado.includes(linea[i])) {
                            var data = '<option selected>' + linea[i] + '</option>';
                        } else {
                            var data = '<option>' + linea[i] + '</option>';
                        }
                        $('#linea').append(data);
                    }
                }

                /******* ACTUALIZAR LINEA NEGOCIO *******/
                if (objeto_origen != 'linea_negocio' | $("#" + objeto_origen).val() == '') {
                    $('#linea_negocio').html('', true);
                    linea_negocio = data_json[2];
                    for (i = 0; i < linea_negocio.length; i++) {
                        if (linea_fina_seleccionado.includes(linea_negocio[i])) {
                            var data = '<option selected>' + linea_negocio[i] + '</option>';
                        } else {
                            var data = '<option>' + linea_negocio[i] + '</option>';
                        }
                        $('#linea_negocio').append(data);
                    }
                }

                /******* ACTUALIZAR RISK *******/
                if (objeto_origen != 'risk' | $("#" + objeto_origen).val() == '') {
                    $('#risk').html('', true);
                    risk = data_json[3];
                    for (i = 0; i < risk.length; i++) {
                        if (risk_seleccionado.includes(risk[i])) {
                            var data = '<option selected>' + risk[i] + '</option>';
                        } else {
                            var data = '<option>' + risk[i] + '</option>';
                        }
                        $('#risk').append(data);
                    }
                }

                /******* ACTUALIZAR CANAL *******/
                if (objeto_origen != 'canal' | $("#" + objeto_origen).val() == '') {
                    $('#canal').html('', true);
                    canal = data_json[4];
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

                /******* ACTUALIZAR TIPO *******/
                if (objeto_origen != 'tipo' | $("#" + objeto_origen).val() == '') {
                    $('#tipo').html('', true);
                    tipo = data_json[6];
                    for (i = 0; i < tipo.length; i++) {
                        if (tipo_seleccionado.includes(tipo[i])) {
                            var data = '<option selected>' + tipo[i] + '</option>';
                        } else {
                            var data = '<option>' + tipo[i] + '</option>';
                        }
                        $('#tipo').append(data);
                    }
                }

                var BootstrapSelect = {
                    init: function () {
                        $(".m_selectpicker").selectpicker('refresh')
                    }
                };
                BootstrapSelect.init();


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

                $('#tria_count_df').html(data_json[9]);
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

                /*
                $('#example2').DataTable({
                    searching: false, paging: false, info: false,
                    data: data_json[9],
                    "lengthMenu": [[-1, 12], ["Todos", 12]],
                    //"display": NONE;
                    dom: 'Bfrtip',
                    buttons: [
                        'excelHtml5',
                        //'csvHtml5', 'pdfHtml5'
                    ],
                    columns: [
                        {"data": "Q_OCURR"},

                    ],
                    "bDestroy": true,
                    //"order": [[ 1, "desc" ]]
                });*/


                //productos3 = data_json[6];
                //console.log(productos3)

                //Data Graph 2 y 3
                data_2_3 = data_json[8];

                /*************************************************************************************************************************/
                /*************************************** GRAPH 1 SEVERITY - FREQUENCY ******************************************************/
                /*************************************************************************************************************************/

                var chart = AmCharts.makeChart("chartdiv2", {
                    "type": "serial",
                    "theme": "light",
                    "dataDateFormat": "YYYY-MM-DD",
                    "precision": 3,

                    "valueAxes":
                        [{
                            "id": "v1",
                            //"unit": "%",
                            //"title": "TCR",
                            "position": "left",
                            "autoGridCount": false,
                            /*
                            "labelFunction": function(value) {
                              return "$" + Math.round(value) + "M";
                            }
                            */
                        },
                            {
                                "id": "v2",
                                "unit": "%",
                                //"title": "INCU - PAID",
                                "gridAlpha": 0,
                                "position": "right",
                                "autoGridCount": false
                            }
                        ],

                    "graphs":
                        [
                            {
                                "id": "g4",
                                "valueAxis": "v1",
                                "lineColor": "#62cf73",
                                "fillColors": "#62cf73",
                                "fillAlphas": 1,
                                "type": "column",
                                "title": "Severity",
                                "valueField": "SEVERITY",
                                "clustered": false,
                                "columnWidth": 0.8,
                                //"legendValueText": "$[[value]]M",
                                "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]</b>"
                            },
                            {
                                "id": "g1",
                                "valueAxis": "v2",
                                "bullet": "round",
                                "bulletBorderAlpha": 1,
                                "bulletColor": "#FFFFFF",
                                "bulletSize": 7,
                                "hideBulletsCount": 50,
                                "lineThickness": 2,
                                "lineColor": "#20acd4",
                                "type": "smoothedLine",
                                "title": "qx",
                                "useLineColorForBulletBorder": true,
                                "valueField": "QX_ACUM",
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
                    "categoryField": "OCURRENCIA",
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
                    "dataProvider": data_2_3,
                });


                /*************************************************************************************************************************/
                /*************************************** GRAPH 2 EXPOSURE & LR ******************************************************/
                /*************************************************************************************************************************/

                var chart = AmCharts.makeChart("chartdiv4", {
                    "type": "serial",
                    "theme": "none",
                    "dataDateFormat": "YYYY-MM-DD",
                    "precision": 2,

                    "valueAxes": [
                        {
                            "id": "v1",
                            "stackType": "regular",
                            "axisAlpha": 0,
                            "gridAlpha": 0,
                            "position": "left",
                            "title": "Exposure",
                            "autoGridCount": false,
                        },
                        {
                            "id": "v2",
                            "unit": "%",
                            //"title": "INCU - PAID",
                            "gridAlpha": 0,
                            "position": "right",
                            "autoGridCount": false
                        }
                    ],

                    "graphs":
                        [
                            /*
                          {
                          "id": "g1",
                          "valueAxis": "v1",
                          "fillAlphas": 0.7,
                          "fillColors": "#0D6DC8",    //0D6DC8
                          "dashLength": 5,
                          "title": "Expuesto",
                          "useLineColorForBulletBorder": true,
                          "valueField": "EXPUESTO",
                          "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]</b>"
                        },
                        */

                            {
                                "id": "g1",
                                "valueAxis": "v1",
                                "fillAlphas": 0.7,
                                "fillColors": "#0D6DC8",
                                "dashLength": 5,
                                "useLineColorForBulletBorder": true,
                                "valueField": "EXPUESTO",
                                "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]</b>"
                            },


                            {
                                "valueAxis": "v2",
                                "bullet": "diamond",
                                "bulletBorderAlpha": 1,
                                "bulletColor": "#95e829",
                                "bulletBorderColor": "#95e829",
                                "bulletSize": 7,
                                "connect": false,
                                "lineColor": "#95e829",
                                "bulletBorderAlpha": 1,
                                "bulletBorderThickness": 1,
                                "dashLengthField": "dashLength",
                                //"legendValueText": "[[value]]",
                                "useLineColorForBulletBorder": true,
                                "title": "LR",
                                "fillAlphas": 0,
                                "valueField": "LR_ACUM",
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
                    "categoryField": "OCURRENCIA",
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
                    "dataProvider": data_2_3,
                });


                /*************************************************************************************************************************/
                /*************************************** GRAPH A1 ******************************************************/
                /*************************************************************************************************************************/

                /*

                var chart = AmCharts.makeChart( "chartdiv8", {
                  "type": "serial",
                  "theme": "light",
                  "autoMargins": false,
                  "marginLeft": 50,
                  "marginRight": 15,
                  "marginTop": 15,
                  "marginBottom": 33,
                  "dataProvider": data_cons,



                  "guides": [ {
                    "dashLength": 4,
                    "inside": true,
                    "label": "average",
                    "lineAlpha": 1,
                    "value": 35		,

                    } ],
                  "graphs": df_cons,
                  "categoryField": "OCURRENCIA",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "autoGridCount": false,
                    "axisColor": "#555555",
                    "gridColor": "#FFFFFF",
                    "gridCount": 50,
                    "labelRotation": 50
                  },
                  //extra
                    "legend": {
                    "divId": "legend",
                    "equalWidths": false,
                    //"useGraphSettings": true,
                    "valueAlign": "left",
                    "listeners": [{
                      "event": "hideItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'hide');
                      }
                    }, {
                      "event": "showItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'show');
                      }
                    }]
                  }
                } );



                var chart = AmCharts.makeChart( "chartdiv9", {
                  "type": "serial",
                  "theme": "light",
                  "autoMargins": false,
                  "marginLeft": 50,
                  "marginRight": 15,
                  "marginTop": 15,
                  "marginBottom": 33,
                  "dataProvider": data_cuen,

                  "guides": [ {
                    "dashLength": 6,
                    "inside": true,
                    "label": "average",
                    "lineAlpha": 1,
                    "value": 35
                    } ],
                  "graphs": df_cuen,
                  "categoryField": "OCURRENCIA",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "autoGridCount": false,
                    "axisColor": "#555555",
                    "gridColor": "#FFFFFF",
                    "gridCount": 50,
                    "labelRotation": 50
                  },
                  //extra
                    "legend": {
                    "divId": "legend",
                    "equalWidths": false,
                    //"useGraphSettings": true,
                    "valueAlign": "left",
                    "listeners": [{
                      "event": "hideItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'hide');
                      }
                    }, {
                      "event": "showItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'show');
                      }
                    }]
                  }
                } );

                var chart = AmCharts.makeChart( "chartdiv10", {
                  "type": "serial",
                  "theme": "light",
                  "autoMargins": false,
                  "marginLeft": 50,
                  "marginRight": 15,
                  "marginTop": 15,
                  "marginBottom": 33,
                  "dataProvider": data_hipo,

                  "guides": [ {
                    "dashLength": 6,
                    "inside": true,
                    "label": "average",
                    "lineAlpha": 1,
                    "value": 35
                    } ],
                  "graphs": df_hipo,
                  "categoryField": "OCURRENCIA",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "autoGridCount": false,
                    "axisColor": "#555555",
                    "gridColor": "#FFFFFF",
                    "gridCount": 50,
                    "labelRotation": 50
                  },
                  //extra
                    "legend": {
                    "divId": "legend",
                    "equalWidths": false,
                    //"useGraphSettings": true,
                    "valueAlign": "left",
                    "listeners": [{
                      "event": "hideItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'hide');
                      }
                    }, {
                      "event": "showItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'show');
                      }
                    }]
                  }
                } );

                var chart = AmCharts.makeChart( "chartdiv11", {
                  "type": "serial",
                  "theme": "light",
                  "autoMargins": false,
                  "marginLeft": 50,
                  "marginRight": 15,
                  "marginTop": 15,
                  "marginBottom": 33,
                  "dataProvider": data_libr,

                  "guides": [ {
                    "dashLength": 6,
                    "inside": true,
                    "label": "average",
                    "lineAlpha": 1,
                    "value": 35
                    } ],
                  "graphs": df_libr,
                  "categoryField": "OCURRENCIA",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "autoGridCount": false,
                    "axisColor": "#555555",
                    "gridColor": "#FFFFFF",
                    "gridCount": 50,
                    "labelRotation": 50
                  },
                  //extra
                    "legend": {
                    "divId": "legend",
                    "equalWidths": false,
                    //"useGraphSettings": true,
                    "valueAlign": "left",
                    "listeners": [{
                      "event": "hideItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'hide');
                      }
                    }, {
                      "event": "showItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'show');
                      }
                    }]
                  }
                } );

                var chart = AmCharts.makeChart( "chartdiv12", {
                  "type": "serial",
                  "theme": "light",
                  "autoMargins": false,
                  "marginLeft": 50,
                  "marginRight": 15,
                  "marginTop": 15,
                  "marginBottom": 33,
                  "dataProvider": data_tarj,

                  "guides": [ {
                    "dashLength": 6,
                    "inside": true,
                    "label": "average",
                    "lineAlpha": 1,
                    "value": 35
                    } ],
                  "graphs": df_tarj,
                  "categoryField": "OCURRENCIA",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "autoGridCount": false,
                    "axisColor": "#555555",
                    "gridColor": "#FFFFFF",
                    "gridCount": 50,
                    "labelRotation": 50
                  },
                  //extra
                    "legend": {
                    "divId": "legend",
                    "equalWidths": false,
                    //"useGraphSettings": true,
                    "valueAlign": "left",
                    "listeners": [{
                      "event": "hideItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'hide');
                      }
                    }, {
                      "event": "showItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'show');
                      }
                    }]
                  }
                } );

                var chart = AmCharts.makeChart( "chartdiv13", {
                  "type": "serial",
                  "theme": "light",
                  "autoMargins": false,
                  "marginLeft": 50,
                  "marginRight": 15,
                  "marginTop": 15,
                  "marginBottom": 33,
                  "dataProvider": data_vehi,

                  "guides": [ {
                    "dashLength": 6,
                    "inside": true,
                    "label": "average",
                    "lineAlpha": 1,
                    "value": 35
                    } ],
                  "graphs": df_vehi,
                  "categoryField": "OCURRENCIA",
                  "categoryAxis": {
                    "gridPosition": "start",
                    "gridAlpha": 0,
                    "tickPosition": "start",
                    "autoGridCount": false,
                    "axisColor": "#555555",
                    "gridColor": "#FFFFFF",
                    "gridCount": 50,
                    "labelRotation": 50
                  },
                  //extra
                    "legend": {
                    "divId": "legend",
                    "equalWidths": false,
                    //"useGraphSettings": true,
                    "valueAlign": "left",
                    "listeners": [{
                      "event": "hideItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'hide');
                      }
                    }, {
                      "event": "showItem",
                      "method": function(item) {
                        toggleAllGraphs(item, 'show');
                      }
                    }]
                  }
                } );

                //function
                function toggleAllGraphs(item, action) {
                  for(var i = 0; i < AmCharts.charts.length; i++) {
                    var chart = AmCharts.charts[i];
                    if (chart == item.chart)
                      continue;
                    if (action == 'hide')
                      chart.hideGraph(chart.graphs[item.dataItem.index]);
                    else
                      chart.showGraph(chart.graphs[item.dataItem.index]);
                  }
                }
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


