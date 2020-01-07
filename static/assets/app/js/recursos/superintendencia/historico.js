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
    am4core.useTheme(am4themes_animated);

    $('body').delegate('.filtrar', 'click', function () {
        //$("#resultado").html("")
        mApp.blockPage({overlayColor: "#000000", type: "loader", state: "success", message: "Cargando gráficas..."});
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('modalidad', $("#modalidad").val());
        data.append('anio', $("#anio").val());
        data.append('fecha', $("#fecha").val());
        data.append('grupo', $("#grupo").val());
        data.append('socio', $("#socio").val());
        $.ajax({
            url: '/recursos/ISF-historico_graficar',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (_data) {

                $('#grafica').css('display', 'block');
                //*************************************************************************//
                //*******************GRÁFICA AMCHARTS DESEMBOLSOS NUEVOS*******************//
                //*************************************************************************//
                var chart = am4core.create("chartdiv", am4charts.XYChart);
                chart.paddingRight = 20;
                chart.data = _data[0];
                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.grid.template.location = 0;
                dateAxis.renderer.grid.template.disabled = true;
                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.tooltip.disabled = true;
                valueAxis.renderer.grid.template.disabled = true;
                valueAxis.renderer.minWidth = 35;
                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.dateX = "date";
                series.dataFields.valueY = "value";
                series.tooltipText = "{valueY}";
                series.tooltip.pointerOrientation = "vertical";
                series.tooltip.background.fillOpacity = 0.5;
                chart.cursor = new am4charts.XYCursor();
                chart.cursor.snapToSeries = series;
                chart.cursor.xAxis = dateAxis;
                var scrollbarX = new am4charts.XYChartScrollbar();
                scrollbarX.series.push(series);
                chart.scrollbarX = scrollbarX;
                var title = chart.titles.create();
                title.text = 'DESEMBOLSOS NUEVOS';
                title.fontSize = 20;
                title.marginBottom = 5;
                chart.exporting.menu = new am4core.ExportMenu();
                var bullet = series.bullets.push(new am4charts.CircleBullet());
                bullet.circle.strokeWidth = 1;

                //*********************************************************************//
                //*******************GRÁFICA AMCHARTS MONTO PROMEDIO*******************//
                //*********************************************************************//
                var chart = am4core.create("chartdiv2", am4charts.XYChart);
                chart.paddingRight = 20;
                chart.data = _data[1];
                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.grid.template.location = 0;
                dateAxis.renderer.grid.template.disabled = true;
                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.tooltip.disabled = true;
                valueAxis.renderer.grid.template.disabled = true;
                valueAxis.renderer.minWidth = 35;
                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.dateX = "date";
                series.dataFields.valueY = "value";
                series.tooltipText = "{valueY}";
                series.tooltip.pointerOrientation = "vertical";
                series.tooltip.background.fillOpacity = 0.5;
                chart.cursor = new am4charts.XYCursor();
                chart.cursor.snapToSeries = series;
                chart.cursor.xAxis = dateAxis;
                var scrollbarX = new am4charts.XYChartScrollbar();
                scrollbarX.series.push(series);
                chart.scrollbarX = scrollbarX;
                var title = chart.titles.create();
                title.text = 'MONTO PROMEDIO';
                title.fontSize = 20;
                title.marginBottom = 5;
                chart.exporting.menu = new am4core.ExportMenu();
                var bullet = series.bullets.push(new am4charts.CircleBullet());
                bullet.circle.strokeWidth = 1;
                //*********************************************************************//
                //*******************GRÁFICA AMCHARTS TASA EA**************************//
                //*********************************************************************//
                var chart = am4core.create("chartdiv3", am4charts.XYChart);
                chart.paddingRight = 20;
                chart.data = _data[2];
                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                dateAxis.renderer.grid.template.location = 0;
                dateAxis.renderer.grid.template.disabled = true;
                var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis.tooltip.disabled = true;
                valueAxis.renderer.grid.template.disabled = true;
                valueAxis.renderer.minWidth = 35;
                var series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.dateX = "date";
                series.dataFields.valueY = "value";
                series.tooltipText = "{valueY}";
                series.tooltip.pointerOrientation = "vertical";
                series.tooltip.background.fillOpacity = 0.5;
                chart.cursor = new am4charts.XYCursor();
                chart.cursor.snapToSeries = series;
                chart.cursor.xAxis = dateAxis;
                var scrollbarX = new am4charts.XYChartScrollbar();
                scrollbarX.series.push(series);
                chart.scrollbarX = scrollbarX;
                var title = chart.titles.create();
                title.text = 'TASA EA';
                title.fontSize = 20;
                title.marginBottom = 5;
                chart.exporting.menu = new am4core.ExportMenu();
                var bullet = series.bullets.push(new am4charts.CircleBullet());
                bullet.circle.strokeWidth = 1;

                mApp.unblockPage();
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("Se presento un error al momento de consultar los datos..[:()]")
                mApp.unblockPage();
                //$("#resultado").html("")
            }
        });
    });
});