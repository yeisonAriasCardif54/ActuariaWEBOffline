from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import cx_Oracle
import configparser
import traceback
from pricing.views_.calcular_bp.register import update_pricing_acquisitionCost
import numpy as np
import sqlite3


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
        'title': 'Acquisition Cost',
        'area': 'Pricing',
        'herramienta': 'Acquisitioncost',
        'file': 'pricing/acquisitioncost.html',
    }
    return render(request, "principal/base.html", configurationView)


def get_ajax(request):
    """
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    cnxn3 = sqlite3.connect('actuariaDatabase')

    # Consultar socios
    sql1 = """ SELECT * FROM PRICING_DATA_ACQUISITION_COSTS """
    prising = pd.read_sql(sql1, cnxn3)

    data2 = []
    prising = prising.fillna('')
    for i, row in prising.iterrows():
        data2.append({
            #"ID": row['ID'],
            "COUNTRY": row['COUNTRY'],
            "BUSINESS_LINE": row['BUSINESS_LINE'],
            "PARTNER_GROUP": row['PARTNER_GROUP'],
            "DESTINATION": row['DESTINATION'],
            "COST_TYPE": row['COST_TYPE'],
            "UNIT_COST_IN_LC": row['UNIT_COST_IN_LC'],

        })

    return JsonResponse(data2, safe=False)


def update(request):
    #pd.set_option('display.float_format', '{:.7f}'.format)
    if request.method == 'POST' and request.FILES.get('file', False):
        myFile = request.FILES['file']
        filename = myFile.name
        file_ext = filename[-4:]
        if file_ext == 'xlsx':
            # Inicio validación del archivo
            validation, message = validate(myFile)
            if validation == False:
                status = 0
                message = 'Error en validación: ' + message
            else:
                try:
                    updateData(myFile)
                    status = 1
                    message = 'Base de datos de Acquisition Cost actualizada con éxito.'
                except:
                    status = 0
                    error = traceback.format_exc()
                    message = 'ERROR:<br>Se presento un error al momento de generar el presupuesto, por favor contacte con el administrador. <br>' + error
        else:
            status = 0
            message = "ERROR:<br>Por favor seleccione el archivo en formato 'Libro de Excel (*.xlsx)'."
    else:
        status = 0
        message = 'ERROR:<br>Por favor seleccione un archivo.'
    data = {"status": status, "message": message}
    return JsonResponse(data, safe=False)


def validate(myFile):
    xlsx_inputs = pd.ExcelFile(myFile)
    newData = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='acquisition_cost'))
    newData = newData.replace(np.inf, np.nan).fillna(0)
    # ---------------------------------------- #
    # -- Definir variables de configuración -- #
    # ---------------------------------------- #
    key = [
        'COUNTRY',
        'BUSINESS_LINE',
        'PARTNER_GROUP'
    ]
    # -- DESTINATION - COST_TYPE -- #
    requiredAndUniqueValues = [
        ['Acquisition', 'Fixed'],
        ['Acquisition', 'Variable'],
        ['Claims', 'Variable'],
        ['Administration', 'Fixed - Direct'],
        ['Administration', 'Fixed - Structure'],
        ['Administration', 'Variable'],
        ['FTS FTG', 'FTS FTG'],
    ]
    # -- DESTINATION -- #
    UniqueValuesDestination = [
        'Acquisition',
        'Claims',
        'Administration',
        'FTS FTG',
    ]
    UniqueValuesDCostType = [
        'Fixed',
        'Variable',
        'Fixed - Direct',
        'Fixed - Structure',
        'FTS FTG',
    ]
    # ------------------------------------- #
    # -- Definir numero de llaves únicas -- #
    # ------------------------------------- #
    keys = newData.groupby(key).mean().reset_index()[key]

    # --------------------------------------------------------- #
    # -- Realizar ciclo buscando valores únicos y requeridos -- #
    # --------------------------------------------------------- #
    errors = '<br><br>'
    errorValidate = 0
    for index, row in keys.iterrows():
        for df in requiredAndUniqueValues:
            # -- Buscar valor por llave actual
            find = newData['COUNTRY'][
                (newData['COUNTRY'] == row['COUNTRY']) &
                (newData['BUSINESS_LINE'] == row['BUSINESS_LINE']) &
                (newData['PARTNER_GROUP'] == row['PARTNER_GROUP']) &
                (newData['DESTINATION'] == df[0]) &
                (newData['COST_TYPE'] == df[1])
                ]
            if len(find) == 0:
                errorValidate = 1
                errors = errors + '<strong style="color:red !important">NO</strong> se encontró valor <br>' + df[0] + "_" + df[1] + '<br> para los datos: <br>' + row['COUNTRY'] + "_" + row['BUSINESS_LINE'] + "_" + row['PARTNER_GROUP'] + '.<br><br>'

            if len(find) > 1:
                errorValidate = 1
                errors = errors + 'Se encontró valor <strong style="color:red !important">DUPLICADO</strong> <br>' + df[0] + "_" + df[1] + '<br> para los datos: <br>' + row['COUNTRY'] + "_" + row['BUSINESS_LINE'] + "_" + row['PARTNER_GROUP'] + '.<br><br>'
    # --------------------------------------------------- #
    # -- Realizar ciclo buscando valores no permitidos -- #
    # --------------------------------------------------- #
    for index, row in newData.iterrows():
        if row['DESTINATION'] not in UniqueValuesDestination:
            errorValidate = 1
            errors = errors + 'El valor en DESTINATION ' + str(row['DESTINATION']) + " no esta permitido" + '.<br><br>'
    for index, row in newData.iterrows():
        if row['COST_TYPE'] not in UniqueValuesDCostType:
            errorValidate = 1
            errors = errors + 'El valor en COST_TYPE ' + str(row['COST_TYPE']) + " no esta permitido" + '.<br><br>'

    if errorValidate:
        return False, errors
    else:
        # -- Guardar datos
        update_pricing_acquisitionCost(newData)
        return True, ''


def updateData(myFile):
    #print('myFile', myFile)
    return True
