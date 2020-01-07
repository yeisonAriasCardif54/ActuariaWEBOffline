from django.shortcuts import render
import pandas as pd
import numpy as np
from .colors import linear_gradient
import json
import cx_Oracle
import configparser
import sqlite3


def reporte2(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

    # Cargar archivo de configuración principal
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME') # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID) # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    cnxn3 = sqlite3.connect('actuariaDatabase')

    # Consultar socios
    sql1 = """ SELECT * FROM PROFITABILITY_DEPARTAMENTOS """
    dptos = pd.read_sql(sql1, cnxn3)

    # Colores para escala de valor de siniestros
    colores = ['#ffc107', '#ffb822', '#fd7e14', '#dc3545']

    # IMAGES - CÍRCULOS
    ancho_maximo = 50
    siniestros_maximos = max(dptos['VALOR'])
    data = []

    dptos['COLOR'] = np.where(
        dptos['VALOR'] <= int(siniestros_maximos * 0.25),
        colores[0],
        np.where(
            dptos['VALOR'] <= int(siniestros_maximos * 0.50),
            colores[1],
            np.where(
                dptos['VALOR'] <= int(siniestros_maximos * 0.75),
                colores[2],
                colores[3]
            )
        )
    )

    for i, row in dptos.iterrows():
        valor_longitud_maxima = (row['VALOR'] * 100) / siniestros_maximos
        valor_longitud_maxima = ancho_maximo * (valor_longitud_maxima / 100)
        if valor_longitud_maxima <= 5:
            valor_longitud_maxima = 5
        ancho = valor_longitud_maxima
        valor = valor_longitud_maxima

        VALOR_SINIESTROS = '{:,}'.format(row['VALOR'])

        data.append({
            'type': "circle",
            "theme": "light",
            "width": ancho,
            "height": ancho,
            "latitude": row['LATITUDE'],
            "longitude": row['LONGITUDE'],
            "title": row['NOMBRE'] + ": <br> Valor Siniestros: $" + str(VALOR_SINIESTROS),
            "value": valor,
            "color": row['COLOR'],
            "alpha": 0.9
        })

    # COLORES
    data2 = []
    for i, row in dptos.iterrows():
        data2.append({
            'id': row['ID'],
            "color": '#5299ad'
        })

    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'images': json.dumps(data),
        'areas': json.dumps(data2),
        'numero_siniestros': '{:,}'.format(sum(dptos['SUMA_PERSONAS'])),
        'total_siniestros': '$ {:,}'.format(sum(dptos['VALOR'])),
        'title': 'Reporte 2',
        'area': 'Profitability',
        'herramienta': 'reporte2',
        'file': 'profitability/reporte2.html',
    }
    cnxn3.close()
    return render(request, "principal/base.html", configurationView)


def reporte3(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

    # Cargar archivo de configuración principal
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME') # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID) # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """

    cnxn3 = sqlite3.connect('actuariaDatabase')

    # Consultar socios
    sql1 = """ SELECT * FROM PROFITABILITY_DEPARTAMENTOS """
    dptos = pd.read_sql(sql1, cnxn3)
    zonas = dptos.groupby(['ZONA', 'LATITUDE_ZONA', 'LONGITUDE_ZONA'], as_index=False)['VALOR'].sum()

    colores = ['#ffc107', '#ffb822', '#fd7e14', '#dc3545']

    # IMAGES - CÍRCULOS
    ancho_maximo = 50
    siniestros_maximos = max(zonas['VALOR'])
    data = []

    zonas['COLOR'] = np.where(
        zonas['VALOR'] <= int(siniestros_maximos * 0.25),
        colores[0],
        np.where(
            zonas['VALOR'] <= int(siniestros_maximos * 0.50),
            colores[1],
            np.where(
                zonas['VALOR'] <= int(siniestros_maximos * 0.75),
                colores[2],
                colores[3]
            )
        )
    )

    for i, row in zonas.iterrows():
        valor_longitud_maxima = (row['VALOR'] * 100) / siniestros_maximos
        valor_longitud_maxima = ancho_maximo * (valor_longitud_maxima / 100)
        if valor_longitud_maxima <= 5:
            valor_longitud_maxima = 5
        ancho = valor_longitud_maxima
        valor = valor_longitud_maxima

        VALOR_SINIESTROS = '{:,}'.format(row['VALOR'])

        data.append({
            'type': "circle",
            "theme": "light",
            "width": ancho,
            "height": ancho,
            "latitude": row['LATITUDE_ZONA'],
            "longitude": row['LONGITUDE_ZONA'],
            "title": row['ZONA'] + ": <br> Valor Siniestros: $" + str(VALOR_SINIESTROS),
            "value": valor,
            "color": row['COLOR'],
            "alpha": 0.9
        })

    # COLORES EN AREAS
    colores = linear_gradient("#7db5dc", "#0c4643", len(zonas))
    colores = colores['hex']

    colores = ['#67b7dc', '#8e8c82', '#83c2ba', '#db8383', '#dbb383', '#547e90', '#83dbd2', '#a28f8f']

    del (zonas['VALOR'])

    zonas['COLOR_ZONA_2'] = colores
    dptos = pd.merge(zonas, dptos, left_on='ZONA', right_on='ZONA', how='left')

    data2 = []
    for i, row in dptos.iterrows():
        data2.append({
            'id': row['ID'],
            "color": row['COLOR_ZONA_2'],
            "balloonText": row['NOMBRE'] + ' - ' + row['ZONA'],
            "customData": row['ZONA'],
            "groupId": row['ZONA'],
        })

    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'images': json.dumps(data),
        'numero_siniestros': '{:,}'.format(sum(dptos['SUMA_PERSONAS'])),
        'total_siniestros': '$ {:,}'.format(sum(dptos['VALOR'])),
        'areas': json.dumps(data2),
        'title': 'Reporte 3',
        'area': 'Profitability',
        'herramienta': 'reporte3',
        'file': 'profitability/reporte2.html',
    }
    cnxn3.close()
    return render(request, "principal/base.html", configurationView)


def reporte4(request):
    username = ''
    email = ''
    first_name = ''
    last_name = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name

    # Cargar archivo de configuración principal
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME') # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID) # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    cnxn3 = sqlite3.connect('actuariaDatabase')

    # Consultar socios
    sql1 = """ SELECT * FROM PROFITABILITY_MUNICIPIOS """
    municipios = pd.read_sql(sql1, cnxn3)

    municipios['LATITUD'] = municipios['LATITUD'].str.replace(',', '.')
    municipios['LONGITUD'] = municipios['LONGITUD'].str.replace(',', '.')

    data = []
    data2 = []

    for i, row in municipios.iterrows():
        data.append({
            'type': "circle",
            "theme": "light",
            "width": 5,
            "height": 5,
            "latitude": row['LATITUD'],
            "longitude": row['LONGITUD'],
            "title": str(row['DEPARTAMENTO']) + " - " + str(row['MUNICIPIO']),
            "value": 100,
            "color": '#ff0000',
            "alpha": 0.6
        })

    configurationView = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'images': json.dumps(data),
        'areas': json.dumps(data2),
        'title': 'Reporte 3',
        'area': 'Profitability',
        'herramienta': 'reporte3',
        'file': 'profitability/reporte2.html',
    }
    cnxn3.close()
    return render(request, "principal/base.html", configurationView)
