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
from pandas.io.excel import ExcelWriter
from pyexcelerate import Workbook
from datetime import datetime
from django.http import HttpResponse

# import pyexcel.ext.xlsx # no longer required if you use pyexcel >= 0.2.2
import glob


# from user_agents import parse


def index(request):
    # agent = request.META['HTTP_USER_AGENT']
    # ua_string = agent
    # user_agent = parse(ua_string)

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
        'title': 'Herramienta de presupuesto',
        'area': 'Profitability',
        'herramienta': 'Presupuesto',
        'file': 'profitability/presupuesto.html',
        'agent': 'ok'  # user_agent.browser.family,
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
                # registro, insert_id = create_register(request, filename)
                registro, insert_id = 1, 1
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
                        #update_register(insert_id=insert_id, file_output=file_output, success=1, total_time=total_time, error='')
                    except:
                        status = 0
                        error = traceback.format_exc()
                        print('\n\n\n - error - \n\n\n')
                        print(error)
                        message = 'ERROR:<br>Se presento un error al momento de generar el presupuesto, por favor contacte con el administrador.' + error
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


def generateFavorites(request):
    # Consultar el grupo actual del admin
    id_group = get_id_group(request.user.id)['GROUP_ID'][0]
    # Consultar ids de usuarios del grupo administrado
    ids_users = str(get_id_users_by_idGroup(id_group)['USER_ID'].tolist()).replace('[', '(').replace(']', ')')
    log = get_register_byListIDs(ids_users)
    folder = 'static/profitability/update_presupuesto'

    # Unificar parametros y desembolsos de "Nuevos"
    parametrosNvUnificados = pd.DataFrame()
    desembolsosNvUnificados = pd.DataFrame()
    identificadorUnico = 1000
    fileNames = ''
    for i, row in log.iterrows():
        fileNames = fileNames + '||' + str(row['FILE_INPUT'])
        Newfile = folder + '/' + row['FILE_INPUT']
        Newpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + Newfile)
        Newxlsx_inputs = pd.ExcelFile(Newpath)
        parametros_nv = pd.DataFrame(pd.read_excel(Newxlsx_inputs, sheet_name='ParametrosNv'))
        parametros_nv = parametros_nv.dropna(subset=['Id_Tool'])  # Eliminar registros cuyo Id_Tool sea nulo
        parametrosNvUnificados = pd.concat([parametrosNvUnificados, parametros_nv], sort=False)
        desembolsos_nv = pd.DataFrame(pd.read_excel(Newxlsx_inputs, sheet_name='DesembolsosNv'))
        desembolsos_nv = desembolsos_nv.dropna(subset=['Id_Tool'])  # Eliminar registros cuyo Id_Tool sea nulo
        desembolsosNvUnificados = pd.concat([desembolsosNvUnificados, desembolsos_nv], sort=False)
        # Agregar identificador único a Id_Tool
        parametrosNvUnificados['Id_Tool'] = parametrosNvUnificados['Id_Tool'] + identificadorUnico
        desembolsosNvUnificados['Id_Tool'] = desembolsosNvUnificados['Id_Tool'] + identificadorUnico
        identificadorUnico = identificadorUnico + 1000

    parametrosNvUnificados = parametrosNvUnificados.fillna(0).reset_index(drop=True)
    desembolsosNvUnificados = desembolsosNvUnificados.fillna(0).reset_index(drop=True)

    filename = log['FILE_INPUT'][0]
    file = folder + '/' + filename
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
    xlsx_inputs = pd.ExcelFile(path)

    registro, insert_id = create_register(request, fileNames, is_union=1)
    # Guardar registro (Log de eventos)
    if registro < 1:
        status = 0
        message = 'ERROR: Se presento un error al intentar guardar el intento (Log de eventos).'
        file_return = ''
    else:
        try:
            total_time, file_output = get_data(file, parametrosNvUnificados=parametrosNvUnificados, desembolsosNvUnificados=desembolsosNvUnificados)
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

    data = {"status": status, "message": message, "file_return": file_return}
    return JsonResponse(data, safe=False)


def history_favorite(request):
    update = update_favorite(request.POST.get('id'), request.POST.get('value'), request.user.id)
    return JsonResponse(update, safe=False)


def update_state(request):
    update = change_state(request.POST.get('id'), 0)
    return JsonResponse(update, safe=False)


def convert_xlsx(request):
    update = request.GET.get('file')
    to = request.GET.get('to')
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../static/profitability/update_presupuesto/' + update)
    data = pd.read_csv(path)

    newName = ''
    if to == 'excel':
        newName = update.replace("csv", "xlsx")
        newPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../static/profitability/update_presupuesto/temp/' + newName)
        data['Fecha'] = pd.to_datetime(data.Fecha).dt.strftime('%Y-%m-%d')
        data['Fecha'] = pd.to_datetime(data['Fecha'])
        # data.to_excel(newPath, sheet_name='OutPut', index=None, float_format='%.5f', startrow=0, header=True)

        values = [data.columns] + list(data.values)
        wb = Workbook()
        ws = wb.new_sheet('OutPut', data=values)
        ws.range("H1", "H" + str(len(data) + 1)).style.format.format = 'dd/mm/yyyy'
        wb.save(newPath)

        with open(newPath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(newPath)
            return response

    if to == 'puntoycoma':
        newName = update.replace("csv", "csv")
        newPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../static/profitability/update_presupuesto/temp/' + newName)
        data.to_csv(newPath, index=None, sep=';', encoding='utf-8-sig', float_format='%.5f', header=True, decimal=".")

    html = '<a href="/static/profitability/update_presupuesto/temp/' + newName + '">' + newName + '</a>'
    return HttpResponse(html)


def get_history(request):
    log = get_register_byID(request.user.id)
    data2 = []
    for i, row in log.iterrows():
        data2.append({
            "ID": str(row['ID']),
            "USER_ID": str(row['USER_ID']),
            "DATETIME": str(row['DATETIME']),
            "FILE_INPUT": str(row['FILE_INPUT']),
            "FILE_OUTPUT": str(row['FILE_OUTPUT']),
            "SUCCESS": str(row['SUCCESS']),
            "TOTAL_TIME": str(row['TOTAL_TIME']),
            "ERROR": str(row['ERROR']),
            "STATUS": str(row['STATUS']),
            "FAVORITE": str(row['FAVORITE']),
            "IS_UNION": str(row['IS_UNION'])
        })
    return JsonResponse(data2, safe=False)


def get_history_group(request):
    # Consultar el grupo actual del admin
    id_group = get_id_group(request.user.id)['GROUP_ID'][0]
    # Consultar ids de usuarios del grupo administrado
    ids_users = str(get_id_users_by_idGroup(id_group)['USER_ID'].tolist()).replace('[', '(').replace(']', ')')
    log = get_register_byListIDs(ids_users)
    data2 = []
    for i, row in log.iterrows():
        data2.append({
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
            "FAVORITE": str(row['FAVORITE'])
        })
    return JsonResponse(data2, safe=False)
