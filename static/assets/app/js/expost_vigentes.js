// Función para obtener listas desplegables actualizadas
function get_selects(objeto_origen) {
    var data = new FormData();
    var producto_seleccionado = $("#productos").val();
    var socio_seleccionado = $("#socios").val();

    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    data.append('productos', producto_seleccionado);
    data.append('socios', socio_seleccionado);

    $.ajax({
        url: '/vigentes_selects',
        type: 'POST',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success:
            function (data_json) {

                /******* ACTUALIZAR PRODUCTOS *******/
                if (objeto_origen != 'productos' | $("#"+objeto_origen).val() == 'ALL') {
                    $('#productos').html('', true);
                    productos = data_json[0];
                    for (i = 0; i < productos.length; i++) {
                        if (productos[i] == producto_seleccionado) {
                            var data = '<option selected>' + productos[i] + '</option>';
                        } else {
                            var data = '<option>' + productos[i] + '</option>';
                        }
                        $('#productos').append(data);
                    }
                }

                /******* ACTUALIZAR SOCIOS *******/
                if (objeto_origen != 'socios' | $("#"+objeto_origen).val() == 'ALL') {
                    $('#socios').html('', true);
                    socios = data_json[1];
                    for (i = 0; i < socios.length; i++) {
                        if (socios[i] == socio_seleccionado) {
                            var data = '<option selected>' + socios[i] + '</option>';
                        } else {
                            var data = '<option>' + socios[i] + '</option>';
                        }
                        $('#socios').append(data);
                    }
                }
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
    // Actualizar gráfico

    // Actualizar listas desplegables
    get_selects(objeto_origen)
}