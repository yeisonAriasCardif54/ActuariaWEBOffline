from django.shortcuts import render
from django.http import JsonResponse
#from pyexcel.internal.sheets import column
from recursos.views_.implementacion_libraries.register import get_register_all, get_register_byId, get_all_coberturas
import pandas as pd
import time
import os
from django.http import HttpResponse
import configparser
import cx_Oracle
import numpy as np
import sqlite3


def conexion():
    """
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    return cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    return sqlite3.connect('actuariaDatabase')

def dashboard(request):
    cnxn3 = conexion()

    # Consultar socios
    sql1 = """ SELECT * FROM RECURSOS_SUPERINTENDENCIA """
    data = pd.read_sql(sql1, cnxn3)
    print('\n\n\n - data - \n\n\n')
    print(data.to_string())
    #data['FECHA'] = data['FECHA'].dt.strftime('%m/%d/%y')
    data.FECHA = pd.to_datetime(data.FECHA, format='%d/%m/%y')

    anios = data['ANIO'].unique()
    fechas = data['FECHA'].unique()
    grupos = data['GRUPO'].unique()
    socios = data['NOMBRE'].unique()

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
        'anios': anios,
        'fechas': fechas,
        'grupos': grupos,
        'socios': socios,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': 'Informes Superintendencia Financiera - Dashboard',
        'area': 'Recursos',
        'herramienta': 'dashboard',
        'file': 'recursos/superintendencia/dashboard.html',
    }
    return render(request, "principal/base.html", configurationView)


def dashboard_graficar(request):
    cnxn3 = conexion()

    where2 = ' WHERE 1=1 '

    # PRIMER FILTRO, ANALIZAR POR
    where1 = request.POST.get('analizar_por')

    # APLICAR SEGUNDO FILTRO POR Año
    if request.POST.get('anio') != '':
        prueba = request.POST.get('anio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND ANIO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR fecha
    if request.POST.get('fecha') != '':
        prueba = request.POST.get('fecha')
        prueba2 = prueba.split(',')
        prueba3 = ", ".join("TO_DATE('{0}','MM/DD/YY')".format(w) for w in prueba2)
        where2 = where2 + " AND FECHA in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR grupo
    if request.POST.get('grupo') != '':
        prueba = request.POST.get('grupo')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND GRUPO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR socio
    if request.POST.get('socio') != '':
        prueba = request.POST.get('socio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND NOMBRE in (" + prueba3 + ") "
    sql2 = """ SELECT """ + where1 + """ AS LABEL, AVG(CREDITOS) AS CREDITOS, AVG(MONTO_PROMEDIO) AS MONTO, AVG(TASA) AS TASA  FROM (
        SELECT
        ANIO,
        FECHA,
        GRUPO,
        NOMBRE,
        MODALIDAD,
        SUM(CREDITOS) AS CREDITOS,SUM(MONTO) AS MONTO, AVG(TASA) AS TASA,
        SUM(MONTO)/SUM(CREDITOS) AS MONTO_PROMEDIO
        FROM RECURSOS_SUPERINTENDENCIA
        GROUP BY
        ANIO,
        FECHA,
        GRUPO,
        NOMBRE,
        MODALIDAD
        ) """ + where2 + """ GROUP BY """ + where1
    result = pd.read_sql(sql2, cnxn3)
    result = result.reset_index()
    result['TASA'] = result['TASA'] * 100
    result['MONTO'] = result['MONTO'] / 1000000
    result = result.fillna(0)
    data = []
    for i, row in result.iterrows():
        CREDITOS = '{:,.0f}'.format(row['CREDITOS'])
        MONTO = '{:.0f}'.format(row['MONTO'])
        TASA = '{:.0f}'.format(row['TASA'])
        TASA = TASA
        data.append({
            "label": str(row['LABEL']),
            "CREDITOS": CREDITOS,
            "MONTO": MONTO,
            "TASA": TASA,
        })

    cnxn3.close()

    return render(request, "recursos/superintendencia/dashboard_resultado.html", {'data': data})


def historico(request):
    cnxn3 = conexion()

    # Consultar socios
    sql1 = """ SELECT * FROM RECURSOS_SUPERINTENDENCIA """
    data = pd.read_sql(sql1, cnxn3)
    data = data.fillna(0)
    print('\n\n\n - data FECHA - \n\n\n')
    print(data['FECHA'])
    #data['FECHA'] = data['FECHA'].dt.strftime('%m/%d/%y')
    data.FECHA = pd.to_datetime(data.FECHA, format='%d/%m/%y')
    data['FECHA'] = data['FECHA'].dt.strftime('%m/%d/%y')

    print('\n\n\n - data FECHA - \n\n\n')
    print(data['FECHA'].dt.year)

    anios = data['ANIO'].unique()
    fechas = data['FECHA'].unique()
    grupos = data['GRUPO'].unique()
    socios = data['NOMBRE'].unique()
    modalidades = data['MODALIDAD'].unique()

    print('\n\n\n - fechas - \n\n\n')
    print(fechas)

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
        'anios': anios,
        'fechas': fechas,
        'grupos': grupos,
        'socios': socios,
        'modalidades': modalidades,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': 'Informes Superintendencia Financiera - Histórico',
        'area': 'Recursos',
        'herramienta': 'historico',
        'file': 'recursos/superintendencia/historico.html',
    }
    return render(request, "principal/base.html", configurationView)


def historico_graficar(request):
    cnxn3 = conexion()

    where2 = ' WHERE 1=1 '

    # APLICAR SEGUNDO FILTRO POR modalidad
    if request.POST.get('modalidad') != '':
        prueba = request.POST.get('modalidad')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND MODALIDAD in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR Año
    if request.POST.get('anio') != '':
        prueba = request.POST.get('anio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND ANIO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR fecha
    if request.POST.get('fecha') != '':
        prueba = request.POST.get('fecha')
        prueba2 = prueba.split(',')
        prueba3 = ", ".join("TO_DATE('{0}','MM/DD/YY')".format(w) for w in prueba2)
        where2 = where2 + " AND FECHA in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR grupo
    if request.POST.get('grupo') != '':
        prueba = request.POST.get('grupo')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND GRUPO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR socio
    if request.POST.get('socio') != '':
        prueba = request.POST.get('socio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND NOMBRE in (" + prueba3 + ") "

    sql2 = """ SELECT FECHA, AVG(CREDITOS) AS CREDITOS, AVG(MONTO_PROMEDIO) AS MONTO, AVG(TASA) AS TASA  FROM (
        SELECT
        ANIO,
        FECHA,
        GRUPO,
        NOMBRE,
        MODALIDAD,
        SUM(CREDITOS) AS CREDITOS,SUM(MONTO) AS MONTO, AVG(TASA) AS TASA,
        SUM(MONTO)/SUM(CREDITOS) AS MONTO_PROMEDIO
        FROM RECURSOS_SUPERINTENDENCIA
        GROUP BY
        ANIO,
        FECHA,
        GRUPO,
        NOMBRE,
        MODALIDAD
        ) """ + where2 + """ GROUP BY FECHA ORDER BY FECHA """

    result = pd.read_sql(sql2, cnxn3)
    result = result.reset_index()

    result['TASA'] = result['TASA'] * 100
    result['MONTO'] = result['MONTO'] / 1000000
    result = result.fillna(0)

    data1 = []
    data2 = []
    data3 = []
    for i, row in result.iterrows():
        CREDITOS = '{:,.0f}'.format(row['CREDITOS'])
        MONTO = '{:.0f}'.format(row['MONTO'])
        TASA = '{:.1f}'.format(row['TASA'])
        data1.append({
            "date": str(row['FECHA']),
            "value": CREDITOS,
        })
        data2.append({
            "date": str(row['FECHA']),
            "value": MONTO,
        })
        data3.append({
            "date": str(row['FECHA']),
            "value": TASA,
        })

    cnxn3.close()

    return JsonResponse([data1, data2, data3], safe=False)


def simulador(request):
    cnxn3 = conexion()

    # Consultar socios
    sql1 = """ SELECT * FROM RECURSOS_SUPERINTENDENCIA """
    data = pd.read_sql(sql1, cnxn3)
    data['FECHA'] = data['FECHA'].dt.strftime('%m/%d/%y')

    modalidades = data['MODALIDAD'].unique()
    socios = data['NOMBRE'].unique()

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
        'socios': socios,
        'modalidades': modalidades,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': 'Informes Superintendencia Financiera - Simulador',
        'area': 'Recursos',
        'herramienta': 'simulador',
        'file': 'recursos/superintendencia/simulador.html',
    }
    return render(request, "principal/base.html", configurationView)


def simulador_graficar(request):
    cnxn3 = conexion()

    where2 = ' WHERE 1=1 '

    # APLICAR SEGUNDO FILTRO POR modalidad
    if request.POST.get('modalidad') != '':
        prueba = request.POST.get('modalidad')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND MODALIDAD in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR socio
    if request.POST.get('socio') != '':
        prueba = request.POST.get('socio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND NOMBRE in (" + prueba3 + ") "

    sql2 = """ SELECT AVG(CREDITOS) AS CREDITOS, AVG(MONTO_PROMEDIO) AS MONTO, AVG(TASA) AS TASA  FROM (
        SELECT
        ANIO,
        FECHA,
        GRUPO,
        NOMBRE,
        MODALIDAD,
        SUM(CREDITOS) AS CREDITOS,SUM(MONTO) AS MONTO, AVG(TASA) AS TASA,
        SUM(MONTO)/SUM(CREDITOS) AS MONTO_PROMEDIO
        FROM RECURSOS_SUPERINTENDENCIA
        WHERE 
        FECHA > ADD_MONTHS(TO_DATE((SELECT MAX(FECHA) FROM RECURSOS_SUPERINTENDENCIA),'DD/MM/YY'), -12)
        GROUP BY
        ANIO,
        FECHA,
        GRUPO,
        NOMBRE,
        MODALIDAD
        ) """ + where2 + """ ORDER BY FECHA """

    result = pd.read_sql(sql2, cnxn3)
    result = result.reset_index()

    listadoPlazosPorDefecto = {
        'Consumo': 48,
        'Microcréditos': 24,
        'Tarjetas': 12,
        'Vehiculo': 48,
        'Vivienda': 120,
        'Libranzas': 48
    }

    # -- Definir variable Tasa
    Tasa = result['TASA'][0]
    if request.POST.get('tasa') != '':
        Tasa = request.POST.get('tasa')

    if Tasa is None:
        Tasa = 0

    print('\n\n\n - Tasa - \n\n\n')
    print(Tasa)

    # -- Definir variable Plazo
    Plazo = listadoPlazosPorDefecto[request.POST.get('modalidad')]
    if request.POST.get('plazo') != '':
        Plazo = request.POST.get('plazo')

    # -- Definir variable Monto
    Monto = result['MONTO'][0]
    if request.POST.get('valor') != '':
        Monto = request.POST.get('valor')

    if Monto is None:
        Monto = 0

    TasaRecalculo = np.where(
        float(Tasa) > 0,
        (1 + float(Tasa)) ** (1 / 12) - 1,
        0
    )

    cuota = np.pmt(float(TasaRecalculo), float(Plazo), float(Monto)) * -1

    Tasa = float(Tasa) * 100
    Tasa = '{:.2f}'.format(float(Tasa))
    Monto = '{:,.0f}'.format(float(Monto))
    cuota = '{:,.0f}'.format(float(cuota))

    return render(request, "recursos/superintendencia/simulador_resultado.html", {'result': result, 'Tasa': Tasa, 'Plazo': Plazo, 'Monto': Monto, 'TasaRecalculo': TasaRecalculo, 'cuota': cuota})
