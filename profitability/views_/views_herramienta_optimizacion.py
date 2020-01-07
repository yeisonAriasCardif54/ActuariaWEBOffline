from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import traceback
import os
import pandas as pd
from profitability.models import Plantillas_presupuesto
from profitability.views_.obtener_presupuesto.get_data import get_data
from profitability.views_.obtener_presupuesto.register import create_register
from profitability.views_.obtener_presupuesto.register import update_register
from profitability.views_.obtener_presupuesto.register import get_register_byID
from profitability.views_.obtener_presupuesto.register import get_register_byListIDs
from profitability.views_.obtener_presupuesto.register import update_favorite
from profitability.views_.obtener_presupuesto.register import change_state
from profitability.views_.obtener_presupuesto.validate import validate
from profitability.views_.obtener_presupuesto.register import get_id_group
from profitability.views_.obtener_presupuesto.register import get_id_users_by_idGroup


def index(request):
    plantillas = Plantillas_presupuesto.objects.all()
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'plantillas': plantillas,
        'title': 'Herramienta de optimización de presupuesto',
        'area': 'Profitability',
        'herramienta': 'Optimizacion',
        'file': 'profitability/optimizacion.html',
    }
    return render(request, "principal/base.html", configurationView)


def generate(request):
    folder = 'static/profitability/update_presupuesto'
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        filename = myfile.name
        file_ext = filename[-4:]
        fs = FileSystemStorage(location=folder)
        filename = fs.save(myfile.name, myfile)
        file = folder + '/' + filename
        if file_ext == 'xlsx':
            # Inicio validación del archivo
            validation, message = validate(file)
            if validation == False:
                fs.delete(myfile.name)
                status = 0
                message = 'Error en validación: ' + message
                file_return = ''
            else:
                registro, insert_id = create_register(request, filename)
                # Guardar registro (Log de eventos)
                if registro < 1:
                    status = 0
                    message = 'ERROR: Se presento un error al intentar guardar el intento (Log de eventos).'
                    file_return = ''
                else:
                    try:
                        total_time, file_output = get_data(file)
                        status = 1
                        message = 'Presupuesto generado con éxito.'
                        file_return = file_output
                        update_register(insert_id=insert_id, file_output=file_output, success=1, total_time=total_time, error='')
                    except:
                        status = 0
                        error = traceback.format_exc()
                        message = 'ERROR:<br>Se presento un error al momento de generar el presupuesto, por favor contacte con el administrador.'
                        file_return = ''
                        update_register(insert_id=insert_id, file_output='Error al generar archivo', success=0, total_time=0, error=error)
        else:
            fs.delete(myfile.name)
            status = 0
            message = "ERROR:<br>Por favor seleccione el archivo en formato 'Libro de Excel (*.xlsx)'."
            file_return = ''
    else:
        status = 0
        message = 'ERROR:<br>Por favor seleccione un archivo.'
        file_return = ''
    data = {"status": status, "message": message, "file_return": file_return}
    return JsonResponse(data, safe=False)