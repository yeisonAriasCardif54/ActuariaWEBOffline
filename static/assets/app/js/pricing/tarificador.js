$(document).ready(function () {

    var CSRF_TOKEN = $("input[name=csrfmiddlewaretoken]").val();
    $(".dropzonev2").dropzone({
        sending: function (file, xhr, formData) {
            $('#divMessages').html('');
            formData.append("csrfmiddlewaretoken", CSRF_TOKEN);
        },
        url: "/tarificador/preUpload",
        dictResponseError: 'Error cargando el archivo!',
        maxFiles: 1,
        maxFilesize: 5, // MB
        addRemoveLinks: true,
        acceptedFiles: '.xlsx',
        dictRemoveFile: 'Remover archivo',
        timeout: 30000, // Milisegundos
        processing: function () {
            mApp.blockPage({overlayColor: "#000000", type: "loader", state: "success", message: "Cargando archivo y generando TAN..."});
        },
        error: function () {
            mApp.unblockPage();
            AC_message('error', '....Error de comunicación con el servidor....<i class="fa fa-frown" style="color: #f2aa25; font-size: 24px;"></i>');
            this.removeAllFiles();
        },
        success: function (data_json) {
            mApp.unblockPage()
            var response = JSON.parse(data_json.xhr.response);
            if (response['status']) {
                AC_message('success', response['message'], response['insert_id']);
                AC_message('download', response['file'], response['insert_id']);
                this.removeAllFiles();
            } else {
                AC_message('error', response['message']);
                this.removeAllFiles();
            }
        },
    });
});


function AC_message(type, message, insert_id) {
    var divMessages = $('#divMessages').html();
    switch (type) {
        case 'error':
            var numberRandom = Math.floor(Math.random() * 100);
            modalError = '<div class="modal fade" id="m_modal_' + numberRandom + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">\n' +
                '\t<div class="modal-dialog modal-lg" role="document">\n' +
                '\t\t<div class="modal-content">\n' +
                '\t\t\t<div class="modal-header">\n' +
                '\t\t\t\t<h5 class="modal-title" id="exampleModalLabel">Contenido del error</h5>\n' +
                '\t\t\t\t<button type="button" class="close" data-dismiss="modal" aria-label="Close">\n' +
                '\t\t\t\t\t<span aria-hidden="true">×</span>\n' +
                '\t\t\t\t</button>\n' +
                '\t\t\t</div>\n' +
                '\t\t\t<div class="modal-body">\n' +
                '\t\t\t<pre>\n' +
                message +
                '\t\t\t</pre>\n' +
                '\t\t\t</div>\n' +
                '\t\t\t<div class="modal-footer">\n' +
                '\t\t\t\t<button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar ventana</button>\n' +
                '\t\t\t</div>\n' +
                '\t\t</div>\n' +
                '\t</div>\n' +
                '</div>';
            text = modalError + '<div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show" role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #F44336;">\n' +
                '\t\t<i class="la la-warning"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong>Se presento el siguiente error:</strong> <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#m_modal_' + numberRandom + '">Clic para ver</button> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div>';
            $('#divMessages').html(divMessages + text);
            break;
        case 'success':
            text = '<div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show"  role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #51e187;">\n' +
                '\t\t<i class="la la-check-square"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong>Se cargo con éxito el archivo, ID: </strong><span class="m-badge m-badge--warning m-badge--wide">' + insert_id + '</span> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div>';
            $('#divMessages').html(divMessages + text);
            break;
        case 'download':
            text = '<div class="row">';
            text += '<div class="col-6"><div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show" role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #5777e1;">\n' +
                '\t\t<i class="la la-file-word-o"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong><a target="_blank" href="/static/pricing/tan_output/' + message + '" style="color: #5777e1">Descargar TAN</a></strong> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div></div>';
            text += '<div class="col-6"><div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show" role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #13e112;">\n' +
                '\t\t<i class="la la-file-excel-o"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong><a href="javascript:;" style="color: #13e112;" onclick="generateBP(' + insert_id + ')">generar BP</a></strong> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div></div>';
            text += '<div class="col-6"><div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show" role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #515138;">\n' +
                '\t\t<i class="la la-gear"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong><a href="/tarificador/administrador" style="color: #515138">Administrar</a></strong> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div></div>';
            text += '<div class="col-6"><div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show" role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #5e875f;">\n' +
                '\t\t<i class="la la-file-excel-o"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong><a target="_blank" href="/recursos/formato/' + insert_id + '" style="color: #5E875F">Visualizar formato de implementación</a></strong> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div></div>';
            text += '<div class="col-6"><div class="m-alert m-alert--icon m-alert--air alert alert-dismissible fade show" role="alert">\n' +
                '\t<div class="m-alert__icon" style="color: #c11d1a;">\n' +
                '\t\t<i class="la la-trash-o"></i>\n' +
                '\t</div>\n' +
                '\t<div class="m-alert__text">\n' +
                '\t\t<strong><a href="javascript:;" onclick="update_state(' + insert_id + ')" style="color: #c11d1a; cursor: pointer">Eliminar</a></strong> \n' +
                '\t</div>\n' +
                '\t<div class="m-alert__close">\n' +
                '\t\t<button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
                '\t\t</button>\n' +
                '\t</div>\n' +
                '</div></div>';
            text += '</div>';

            text += '</div>';
            $('#divMessages').html(divMessages + text);
            break;
    }
}

function update_state(id) {
    var r = confirm("Eliminar el registro?");
    if (r === true) {
        var data = new FormData();
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        data.append('id', id);
        $.ajax({
            url: '/tarificador/update_state',
            type: 'POST',
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            data: data,
            success: function (data_json) {
                if (data_json) {
                    toast2('success', 'Registro Eliminado');
                    $('#divMessages').html('');
                } else {
                    toast2('error', 'Error al eliminar el registro');
                    $('#divMessages').html('');
                }
            }
        });
    } else {
        return false;
    }
}

function generateBP(idTarificador) {
    mApp.blockPage({overlayColor: "#000000", type: "loader", state: "success", message: "Generando business plan..."});
    var data = new FormData();
    data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
    data.append('idTarificador', idTarificador);
    $.ajax({
        url: '/business_plan_tool/generate_from_tarificador/' + idTarificador,
        type: 'POST',
        dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        data: data,
        success: function (data_json) {
            if (data_json['status']) {
                toast2('success', data_json['message']);
                mApp.unblockPage()
                $('#file_download').css('visibility', 'visible');
                $('#file_download').attr('href', data_json['file_return']);
                location.href = data_json['file_return'];
            } else {
                toast2('error', data_json['message'])
            }
            mApp.unblockPage()
        },
        error: function (xhr, ajaxOptions, thrownError) {
            toast2('error', 'Se presento un error al generar el archivo.');
            mApp.unblockPage()
        }
    });
}