import configparser
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from openpyxl import load_workbook
from pricing.models import Detalles_tabla
import pandas as pd
import cx_Oracle
import configparser
import sqlite3


def index(request):
    detalles_tabla = Detalles_tabla.objects.all()

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
        'detalles_tabla': detalles_tabla,
        'title': 'Indicators Pricing',
        'area': 'Pricing',
        'herramienta': 'Table',
        'file': 'pricing/table.html',
    }
    return render(request, "principal/base.html", configurationView)


def get_table_ajax(request):
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
    sql1 = """ SELECT * FROM PRICING """
    prising = pd.read_sql(sql1, cnxn3)

    data2 = []
    prising = prising.fillna('')
    for i, row in prising.iterrows():
        data2.append({
            "PRODUCT_NAME": row['PRODUCT_NAME'],
            "DATE_CREATE": row['DATE_CREATE'],
            "PARTNER": row['PARTNER'],
            "CODE": row['CODE'],
            "PREVIOUS_PRODUCT": row['PREVIOUS_PRODUCT'],
            "LINE": row['LINE'],
            "CHANNEL": row['CHANNEL'],
            "LINE_OF_CREDIT": row['LINE_OF_CREDIT'],
            "TYPE_OF_PREMIUM": row['TYPE_OF_PREMIUM'],
            "MONTHLY_PREMIUM": row['MONTHLY_PREMIUM'],
            "BRANCH_WITHOUT_VAT": row['BRANCH_WITHOUT_VAT'],
            "LIFE": row['LIFE'],
            "AVERAGE_INSURED_CAPITAL_COP": row['AVERAGE_INSURED_CAPITAL_COP'],
            "CARDIF_MARGIN": row['CARDIF_MARGIN'],
            "CLAIMS_RATIO": row['CLAIMS_RATIO'],
            "QUOTED_LOSS": row['QUOTED_LOSS'],
            "PARTNER_COMMISSIONS": row['PARTNER_COMMISSIONS'],
            "BROKER_COMMISSIONS": row['BROKER_COMMISSIONS'],
            "INTERMEDIARY_COMMISSIONS": row['INTERMEDIARY_COMMISSIONS'],
            "COMMISSIONS_NONINT": row['COMMISSIONS_NONINT'],
            "ADMIN": row['ADMIN'],
            "QUOTED_ACQUISITION_COSTS_COP": row['QUOTED_ACQUISITION_COSTS_COP'],
            "QUOTED_AVERAGE_POLICY_DURATION": row['QUOTED_AVERAGE_POLICY_DURATION'],
            "LAPSES_RATES_YEARLY": row['LAPSES_RATES_YEARLY'],
            "PARTNER_PROFIT_SHARE": row['PARTNER_PROFIT_SHARE'],
            "DURACION_CREDITO": row['DURACION_CREDITO'],
            "BASE": row['BASE'],
            "RUTA_COTIZACION": row['RUTA_COTIZACION'],
            "ASSISTANCE": row['ASSISTANCE'],
        })

    return JsonResponse(data2, safe=False)


def generate(request):
    folder = 'static/profitability/update_presupuesto'

    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        filename = myfile.name
        file_ext = filename[-4:]

        if file_ext == 'xlsx':
            fs = FileSystemStorage(location=folder)
            filename = fs.save(myfile.name, myfile)
            file_url = fs.url(filename)
            file = folder + '/' + file_url

            wb = load_workbook(file)
            if wb.properties.version == '1.0.0':
                status = 1
                message = 'generando...' + file_url
            else:
                status = 0
                message = 'ERROR: Por favor descargue la ultima version de la plantilla.'

        else:
            status = 0
            message = 'ERROR: Por favor seleccione el archivo en formato Excel (.xlsx)'

    else:
        status = 0
        message = 'ERROR: Por favor seleccione el archivo.'

    data = {"status": status, "message": message}
    return JsonResponse(data, safe=False)
