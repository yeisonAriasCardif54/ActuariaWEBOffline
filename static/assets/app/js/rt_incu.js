// Función para obtener listas desplegables actualizadas

function get_selects(objeto_origen) {

	//Serialize el formulario de filtro

    var x = $("#formulario").serializeArray();
    var data = new FormData();
    $.each(x, function (i, field) {
        data.append(field.name, field.value);
    });
    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    //alert(data)

    mApp.block(".block", {overlayColor: "#000000", type: "loader", state: "primary", message: "Procesando..."});

    $.ajax({
        url: '/rt_incu_selects',
        type: 'POST',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success:

            function (data_json) {

            console.log(data)


                /******* ACTUALIZAR LINEA *******/
                if (objeto_origen != 'linea' | $("#" + objeto_origen).val() == '') {
                    $('#linea').html('', true);
                    linea_a = data_json[1];
                    for (i = 0; i < linea_a.length; i++) {
                        if (linea_a.includes(linea[i])) {
                            var data = '<option selected>' + linea_a[i] + '</option>';
                        } else {
                            var data = '<option>' + linea_a[i] + '</option>';
                        }
                        $('#linea').append(data);
                    }
                }

                /******* ACTUALIZAR LINEA NEGOCIO *******/
                if (objeto_origen != 'linea_negocio' | $("#" + objeto_origen).val() == '') {
                    $('#linea_negocio').html('', true);
                    linea_negocio_a = data_json[2];
                    for (i = 0; i < linea_negocio_a.length; i++) {
                        if (linea_negocio_a.includes(linea_negocio[i])) {
                            var data = '<option selected>' + linea_negocio_a[i] + '</option>';
                        } else {
                            var data = '<option>' + linea_negocio_a[i] + '</option>';
                        }
                        $('#linea_negocio').append(data);
                    }
                }

                /******* ACTUALIZAR RISK *******/
                if (objeto_origen != 'risk' | $("#" + objeto_origen).val() == '') {
                    $('#risk').html('', true);
                    risk_a = data_json[3];
                    for (i = 0; i < risk_a.length; i++) {
                        if (risk_a.includes(risk[i])) {
                            var data = '<option selected>' + risk_a[i] + '</option>';
                        } else {
                            var data = '<option>' + risk_a[i] + '</option>';
                        }
                        $('#risk').append(data);
                    }
                }

                /******* ACTUALIZAR CANAL *******/
                if (objeto_origen != 'canal' | $("#" + objeto_origen).val() == '') {
                    $('#canal').html('', true);
                    canal_a = data_json[4];
                    for (i = 0; i < canal_a.length; i++) {
                        if (canal_a.includes(canal[i])) {
                            var data = '<option selected>' + canal_a[i] + '</option>';
                        } else {
                            var data = '<option>' + canal_a[i] + '</option>';
                        }
                        $('#canal').append(data);
                    }
                }


                /******* ACTUALIZAR TIPO *******/
                if (objeto_origen != 'tipo' | $("#" + objeto_origen).val() == '') {
                    $('#tipo').html('', true);
                    tipo_a = data_json[5];
                    for (i = 0; i < tipo_a.length; i++) {
                        if (tipo_a.includes(tipo[i])) {
                            var data = '<option selected>' + tipo_a[i] + '</option>';
                        } else {
                            var data = '<option>' + tipo_a[i] + '</option>';
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


                //Data Graphs
                data_01 = data_json[6];
				data_02 = data_json[7];

				//*****************************************************************************************************
				//*************************************** GRAPHS ******************************************************

				var chart = AmCharts.makeChart( "chartdiv01", {
				  "type": "serial",
				  "theme": "light",
				  "autoMargins": false,
				  "marginLeft": 50,
				  "marginRight": 15,
				  "marginTop": 15,
				  "marginBottom": 33,

				  "dataProvider": data_01,

                   "balloon": {
                    "borderThickness": 1,
                    "shadowAlpha": 0
                  },
                  "export": {
                    enabled: true
                  },
				    "graphs": data_02,
				    "categoryField": "PERIODO",
				    "categoryAxis": {
					"gridPosition": "start",
					"gridAlpha": 20,
					"unit": "%",
					//"tickPosition": "start",
					//"autoGridCount": false,
					"axisColor": "#555555",
					"gridColor": "#FFFFFF",
					"gridCount": 50,
					"labelRotation": 50
				  },
	   			} );

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


