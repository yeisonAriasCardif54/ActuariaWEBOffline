$(document).ready(function () {
    var BootstrapSelect = {
        init: function () {
            $(".m_selectpicker").selectpicker()
        }
    };
    jQuery(document).ready(function () {
        BootstrapSelect.init()
    });
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
            url: '/pgv2_graficar',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {

                $('.graficar').button('reset');
                $('#grafica').css('display', 'block');

                $('#example').DataTable({
                    "lengthMenu": [[-1], ["Todos"]],
                    data: data_json[1],
                    columns: [
                        {"data": "label"},
                        {
                            "mRender": function (data, type, row) {
                                var VALUE_CREATION = row.VALUE_CREATION;
                                return '<span class="m-badge m-badge--success m-badge--wide">' + VALUE_CREATION + '</span>';
                            }
                        },
                        {"data": "VALUE_CREATION_ACCUMULATED"},
                        {"data": "PROFIT_MARGIN"}
                    ],
                    "bDestroy": true,
                    "order": [[1, "desc"]]
                });
                $('#example2').DataTable({
                    "lengthMenu": [[-1], ["Todos"]],
                    data: data_json[2],
                    columns: [
                        {"data": "label"},
                        {
                            "mRender": function (data, type, row) {
                                var VALUE_CREATION = row.VALUE_CREATION;
                                return '<span class="m-badge m-badge--danger m-badge--wide">' + VALUE_CREATION + '</span>';
                            }
                        },
                        {"data": "VALUE_CREATION_ACCUMULATED"},
                        {"data": "PROFIT_MARGIN"}
                    ],
                    "bDestroy": true,
                    "order": [[1, "asc"]]
                });

                //var data = data_json[0];
                // -- Gráfica
                am4core.ready(function () {

                    // Themes begin
                    am4core.useTheme(am4themes_animated);
                    // Themes end

                    var chart = am4core.create("chartdiv", am4charts.XYChart);
                    chart.paddingRight = 20;

                    var data2 = [
                        {
                            "date": "UNO",
                            "value": 20,
                            "color": '#20c997'
                        }, {
                            "date": "DOS",
                            "value": 40,
                            "color": chart.colors.getIndex(0)
                        }, {
                            "date": "TRES",
                            "value": 30,
                            "color": '#f4516c'
                        },
                    ];

                    chart.data = data_json[0];

                    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
                    categoryAxis.dataFields.category = "label";
                    //categoryAxis.title.text = "Item";
                    categoryAxis.renderer.grid.template.location = 0;
                    categoryAxis.renderer.minGridDistance = 20;
                    categoryAxis.renderer.labels.template.rotation = 300;
                    categoryAxis.renderer.grid.template.disabled = true;

                    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                    valueAxis.tooltip.disabled = true;
                    valueAxis.renderer.minWidth = 35;
                    valueAxis.renderer.axisFills.template.disabled = true;
                    valueAxis.renderer.ticks.template.disabled = true;
                    valueAxis.renderer.grid.template.disabled = true;


                    var series = chart.series.push(new am4charts.LineSeries());
                    series.dataFields.categoryX = "label";
                    series.dataFields.valueY = "VALUE_CREATION_ACCUMULATED";
                    series.strokeWidth = 2;
                    series.tooltipText = "Value Creation: {valueY}, Item: {categoryX}";
                    //series.bullets.push(new am4charts.CircleBullet());

                    // set stroke property field
                    series.propertyFields.stroke = "color";
                    series.propertyFields.fill = "color";

                    var closeBullet = series.bullets.create(am4charts.CircleBullet);
                    closeBullet.propertyFields.fill = "color";
                    closeBullet.propertyFields.stroke = "color";

                    var maleLabel = series.bullets.push(new am4charts.LabelBullet());
                    maleLabel.label.text = "{valueY}";
                    maleLabel.label.hideOversized = false;
                    maleLabel.label.truncate = false;
                    maleLabel.label.horizontalCenter = "left";
                    maleLabel.label.verticalCenter = "button";
                    //maleLabel.label.dx = -10;

                    chart.cursor = new am4charts.XYCursor();

                    //var scrollbarX = new am4core.Scrollbar();
                    //chart.scrollbarX = scrollbarX;

                    // Add ExportMenu
                    chart.exporting.menu = new am4core.ExportMenu();

                }); // end am4core.ready()

            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Se presento un error al momento de consultar los datos..[:()]")
                $('.graficar').button('reset');
            }
        });
    });
});