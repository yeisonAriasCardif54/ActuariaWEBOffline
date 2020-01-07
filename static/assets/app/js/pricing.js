$(document).ready(function () {
    $.ajax({
        url: '/table_ajax',
        type: 'GET',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: [],
        success: function (data_json) {
            var test = JSON.parse(JSON.stringify(data_json))
              $('#table').DataTable( {
                  scrollY:"50vh",
                  scrollX:!0,
                  scrollCollapse:!0,
                  data: test,
                  columns: [
                    { "data": "PRODUCT_NAME" },
                    { "data": "DATE_CREATE" },
                    { "data": "PARTNER" },
                    { "data": "CODE" },
                    {"data": "PREVIOUS_PRODUCT"},
                    {"data": "LINE"},
                    {"data": "CHANNEL"},
                    {"data": "LINE_OF_CREDIT"},
                    {"data": "TYPE_OF_PREMIUM"},
                    {"data": "MONTHLY_PREMIUM"},
                    {"data": "BRANCH_WITHOUT_VAT"},
                    {"data": "LIFE"},
                    {"data": "AVERAGE_INSURED_CAPITAL_COP"},
                    {"data": "CARDIF_MARGIN"},
                    {"data": "CLAIMS_RATIO"},
                    {"data": "QUOTED_LOSS"},
                    {"data": "PARTNER_COMMISSIONS"},
                    {"data": "BROKER_COMMISSIONS"},
                    {"data": "INTERMEDIARY_COMMISSIONS"},
                    {"data": "COMMISSIONS_NONINT"},
                    {"data": "ADMIN"},
                    {"data": "QUOTED_ACQUISITION_COSTS_COP"},
                    {"data": "QUOTED_AVERAGE_POLICY_DURATION"},
                    {"data": "LAPSES_RATES_YEARLY"},
                    {"data": "PARTNER_PROFIT_SHARE"},
                    {"data": "DURACION_CREDITO"},
                    {"data": "BASE"},
                    {"data": "RUTA_COTIZACION"},
                    {"data": "ASSISTANCE"}
                  ],
                  //"bDestroy": true,
                  //"order": [[ 0, "desc" ]]
               });
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr)
            console.log(ajaxOptions)
            console.log(thrownError)
            alert("Se presento un error al momento de consultar los datos..[:()]")
        }
    });


});
