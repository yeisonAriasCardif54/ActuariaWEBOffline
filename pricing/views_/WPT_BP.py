import traceback
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from pricing.views_.calcular_bp.get_data_bp import get_data_bp
from pricing.views_.calcular_bp.register import create_register, update_register, get_categories, get_register_all, update_favorite, change_state, get_Tarificador, update_registeren_tarificador
import os
import pandas as pd


def index(request):
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
        'title': 'Web Pricing Tool  ║  Business Plan',
        'area': 'Pricing',
        'herramienta': 'WPT-BP',
        'file': 'pricing/business_plan.html',
    }
    return render(request, "principal/base.html", configurationView)


def generate(request):
    folder = 'static/pricing/business_plan_input'
    if request.method == 'POST' and request.FILES['file']:
        myFile = request.FILES['file']
        filename = myFile.name
        file_ext = filename[-4:]
        if file_ext == 'xlsx':
            registro, insert_id = 1,1
            if registro < 1:
                status = 0
                message = 'ERROR: Se presento un error al intentar guardar el intento (Log de eventos).'
                file_return = ''
            else:
                fs = FileSystemStorage(location=folder)
                filename = fs.save(myFile.name, myFile)
                file_url = fs.url(filename)
                file = folder + '/' + filename
                try:
                    total_time, file_output = get_data_bp(file, request.POST.get('mas_detalles'))
                    status = 1
                    message = 'Se genero con éxito el archivo en ' + total_time + ' segundos.'
                    file_return = 'static/pricing/business_plan_output/' + file_output
                    #update_register(insert_id=insert_id, file_output=file_output, success=1, total_time=total_time, error='')
                except ValueError as exp:
                    error = traceback.format_exc()
                    obtener_data = ''
                    status = 0
                    message = str(error)
                    file_return = ''
                    #update_register(insert_id=insert_id, file_output='Error al generar archivo', success=0, total_time=0, error=error)
                except:
                    error = traceback.format_exc()
                    obtener_data = ''
                    status = 0
                    message = 'Se presento un error al momento de generar el archivo, por favor contacte con el administrador. ***' + error + ' *** '
                    #update_register(insert_id=insert_id, file_output='Error al generar archivo', success=0, total_time=0, error=error)
                    file_return = ''
        else:
            status = 0
            message = 'ERROR: Por favor seleccione el archivo en formato Excel (.xlsx)'
            file_return = ''
    else:
        status = 0
        message = 'ERROR: Por favor seleccione un archivo.'
        file_return = ''

    data = {"status": status, "message": message, "file_return": file_return}
    return JsonResponse(data, safe=False)


def history(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
    # Consultar categorías
    categories = get_categories()
    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'categories': categories.to_records(),
        'title': 'Web Pricing Tool  ║  Histórico Business Plan',
        'area': 'Pricing',
        'herramienta': 'WPT-HI-BP',
        'file': 'pricing/history_business_plan.html',
    }
    return render(request, "principal/base.html", configurationView)


def historyTable(request, category):
    log = get_register_all(category)
    data = []
    for i, row in log.iterrows():
        data.append({
            "ID": str(row['ID']),
            "USER_ID": str(row['USER_ID']),
            "FIRST_NAME": str(row['FIRST_NAME']),
            "LAST_NAME": str(row['LAST_NAME']),
            "DATETIME": str(row['DATETIME']),
            "FILE_INPUT": str(row['FILE_INPUT']),
            "FILE_OUTPUT": str(row['FILE_OUTPUT']),
            "SUCCESS": str(row['SUCCESS']),
            "TOTAL_TIME": str(row['TOTAL_TIME']),
            "ERROR": str(row['ERROR']),
            "STATUS": str(row['STATUS']),
            "CATEGORY": str(row['CATEGORY']),
            "NOMBRE": str(row['NOMBRE']),
            "COLOR": str(row['COLOR'])
        })
    # Consultar categorías
    categories = get_categories()
    data2 = []
    for i, row in categories.iterrows():
        data2.append({
            "ID": str(row['ID']),
            "NOMBRE": str(row['NOMBRE']),
            "COLOR": str(row['COLOR'])
        })
    return JsonResponse({'DTable': data, 'categories': data2}, safe=False)


def change_category(request):
    update = update_favorite(request.POST.get('id'), request.POST.get('idcategory'))
    return JsonResponse(update, safe=False)


def update_state(request):
    update = change_state(request.POST.get('id'), 0)
    return JsonResponse(update, safe=False)


def generate_from_tarificador(request, idTarificador):
    # -- Consultar registro del tarificador
    tarificador = get_Tarificador(idTarificador)
    # -- Validar que se encuentren las hojas 'Inputs' y SolvenciaII
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../static/pricing/tarificadores_inputs/' + tarificador['FILE_INPUT'][0])
    xlsxFile = pd.ExcelFile(path)
    try:
        Inputs = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Inputs'))
        SolvenciaII = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='SolvenciaII'))
        validateSheets = 1
    except:
        status = 0
        message = 'ERROR: El archivo no contiene las hojas "Inputs" y/o "SolvenciaII"'
        file_return = ''
        validateSheets = 0
    if validateSheets:
        # -- Verificar si ya se ejecuto el BP -- #
        if tarificador['SUCCESS_BP'][0] == 1:
            status = 1
            message = 'Archivo generado con éxito.'
            file_return = 'static/pricing/business_plan_output/' + tarificador['FILE_OUTPUT_BP'][0]
        else:
            # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #
            file = '/static/pricing/tarificadores_inputs/' + tarificador['FILE_INPUT'][0]
            try:
                total_time, file_output = get_data_bp(file, ver_mas_detalles='NO')
                status = 1
                message = 'Se genero con éxito el archivo en ' + total_time + ' segundos.'
                file_return = 'static/pricing/business_plan_output/' + file_output
                update_registeren_tarificador(insert_id=idTarificador, file_output=file_output, success=1, total_time=total_time, error='')
            except ValueError as exp:
                error = traceback.format_exc()
                status = 0
                message = str(error)
                file_return = ''
                update_registeren_tarificador(insert_id=idTarificador, file_output='Error al generar archivo', success=0, total_time=0, error=error)
            except:
                error = traceback.format_exc()
                status = 0
                message = 'Se presento un error al momento de generar el archivo, por favor contacte con el administrador. ***' + error + ' *** '
                file_return = ''
                update_registeren_tarificador(insert_id=idTarificador, file_output='Error al generar archivo', success=0, total_time=0, error=error)
    data = {"status": status, "message": message, "file_return": file_return}
    return JsonResponse(data, safe=False)
