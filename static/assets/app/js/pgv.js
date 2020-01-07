$(document).ready(function(){
  var BootstrapSelect={init:function(){$(".m_selectpicker").selectpicker()}};jQuery(document).ready(function(){BootstrapSelect.init()});
});

$(document).ready(function () {
    $('body').delegate('.graficar', 'click', function () {

        $('.graficar').button('loading');

        var data = new FormData();

        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('analizar_por', $("#analizar_por").val());
        data.append('periodo', $("#periodo").val());
        data.append('tipo', $("#tipo").val());
        data.append('tipo_socio', $("#tipo_socio").val());
        data.append('socio', $("#socio").val());
        data.append('producto', $("#producto").val());
        data.append('tipo_oferta', $("#tipo_oferta").val());
        data.append('capa', $("#capa").val());
        data.append('linea', $("#linea").val());
        data.append('tipo_prima', $("#tipo_prima").val());

        $.ajax({
            url: '/pgv_graficar',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {

                $('.graficar').button('reset');
                $('#grafica').css('display','block');


                  $('#example').DataTable( {
                      data: data_json[1],
                      columns: [
                        { "data": "label" },
                        { "data": "VALUE_CREATION" },
                        { "data": "PVGWP" },
                        { "data": "PROFIT_MARGIN" }
                      ],
                      "bDestroy": true,
                      "order": [[ 1, "desc" ]]
                   });

                  //var data = JSON.parse(data;
                  var chart = AmCharts.makeChart("chartdiv", {
                  	"theme": "light",
                  	"type": "serial",
                  	"dataProvider": data_json[0],
                  	"categoryField": "label",

                  	"categoryAxis": {
                  		"gridAlpha": 0.1,
                  		"axisAlpha": 1,
                  		"widthField": "PVGWP",
                  		"gridPosition": "start",
                  		"labelRotation": 90,
                  	},

                  	"startDuration": 1,

                  	"valueAxes": [
                      {
                        "position": "left",
                        "dashLength": 6,
                        "guides": [
                                    /*{
                                      //"label": "Limite 6% ",
                                      "dashLength": 6,
                                      "inside": false,
                                      "fillAlpha": 0.5,
                                      "value": 6,
                                      //"toValue": 6,
                                      "lineColor": "#ff9800",
                                      "lineAlpha": 2,
                                      "fillAlpha": 0.5,
                                      //"fillColor": "#ceb228",
                                      "axisAlpha": 0,
                                      "above": true
                                  },*/{
                                      //  "label": "Limite 5% ",
                                      "dashLength": 5,
                                      "lineThickness":2,
                                      "inside": true,
                                      //"fillAlpha": 0.1,
                                      "value": 5,
                                      //"toValue": 5,
                                      "lineColor": "#ff9800",
                                      "lineAlpha": 2,
                                      //"fillAlpha": 0.5,
                                      //"fillColor": "#ceb228",
                                      //"axisAlpha": 0,
                                      "above": true
                                  }
                                ]
                      },
                      ,
                      {
                          "dashLength": 0.8,
                      		"stackType": "stacked",
                      		"gridAlpha": 0.10,
                      		"unit": "%",
                      		"axisAlpha": 0
                      	},
                      ],


                  	"graphs": [
                  		{
                  			"title": "PROFIT_MARGIN",
                  			//"labelText": "[[PVGWP]] M",
                  			"pointPosition":"middle",
                  			"numberFormatter": {precision:-5, decimalSeparator:'.', thousandsSeparator:','},
                  			"valueField": "PROFIT_MARGIN",
                  			"colorField": "color",
                  			"lineColor": "color",
                  			"lineAlpha": 0.2,
                  			"type": "column",
                  			"fillAlphas": 1,
                  			//"balloonText": "[[category]] <br><b><span style='font-size:14px;'>PVGWP: [[PVGWP]] M</span></b> <br><b><span style='font-size:14px;'>PROFIT_MARGIN: [[value]] %</span></b>",
                  			"balloonText": "[[label]]<br/>VALUE CREATION: [[VALUE_CREATION_LABEL]] M COP<br/> PVGWP: [[PVGWP_LABEL]] M COP<br/> PROFIT MARGIN: [[PROFIT_MARGIN_LABEL]]",
                  			/*"balloonFunction": function(item, graph) {
                  				var result = graph.balloonText;
                  				for (var key in item.dataContext) {
                  					if (item.dataContext.hasOwnProperty(key) && !isNaN(item.dataContext[key])) {
                  						var formatted = AmCharts.formatNumber(item.dataContext[key], {
                  							precision: chart.precision,
                  							decimalSeparator: chart.decimalSeparator,
                  							thousandsSeparator: chart.thousandsSeparator
                  						}, 2);
                  						result = result.replace("[[" + key + "]]", formatted);
                  					}
                  				}
                  				return result;
                  			}*/
                  		}
                  	],

                  	"legend": {},
                  	"export":
                  	{
                  		"enabled":true
                  	}
                  });


            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Se presento un error al momento de consultar los datos..[:()]")
                $('.graficar').button('reset');
            }
        });
    });


});
