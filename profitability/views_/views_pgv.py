from django.shortcuts import render
import pandas as pd
import numpy as np
from .colors import linear_gradient
from django.http import JsonResponse
import cx_Oracle
import sqlite3
import configparser


def pgv_graficar(request):
    # Cargar archivo de configuración principal
    """
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

    where1 = 'SOCIO'
    where2 = ' WHERE 1=1 '

    # PRIMER FILTRO, ANALIZAR POR
    where1 = request.POST.get('analizar_por')

    # APLICAR SEGUNDO FILTRO POR SOCIO
    if request.POST.get('socio') != '':
        # where2 = where2 + " AND SOCIO='" + request.POST.get('socio') + "' "

        prueba = request.POST.get('socio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND SOCIO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR PRODUCTO
    if request.POST.get('producto') != '':
        # where2 = where2 + " AND NOMBRE_PRODUCTO='" + request.POST.get('producto') + "' "

        prueba = request.POST.get('producto')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND NOMBRE_PRODUCTO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR TIPO DE OFERTA
    if request.POST.get('tipo_oferta') != '':
        prueba = request.POST.get('tipo_oferta')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND TIPO_OFERTA in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR CAPA
    if request.POST.get('capa') != '':
        # where2 = where2 + " AND CAPA='" + request.POST.get('capa') + "' "

        prueba = request.POST.get('capa')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND CAPA in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR LINES DE NEGOCIO
    if request.POST.get('linea') != '':
        # where2 = where2 + " AND LINEA_NEGOCIO_SOCIO='" + request.POST.get('linea') + "' "

        prueba = request.POST.get('linea')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND LINEA_NEGOCIO_SOCIO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR TIPO DE PRIMA
    if request.POST.get('tipo_prima') != '':
        # where2 = where2 + " AND TIPO_PRIMA='" + request.POST.get('tipo_prima') + "' "

        prueba = request.POST.get('tipo_prima')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND TIPO_PRIMA in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR TIPOS
    if request.POST.get('tipo') != '':
        # where2 = where2 + " AND TIPO='" + request.POST.get('tipo') + "' "

        prueba = request.POST.get('tipo')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND TIPO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR PERIODOS
    if request.POST.get('periodo') != '':
        # where2 = where2 + " AND PERIODO='" + request.POST.get('periodo') + "' "

        prueba = request.POST.get('periodo')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND PERIODO in (" + prueba3 + ") "

    # APLICAR SEGUNDO FILTRO POR TIPOS DE SOCIO
    if request.POST.get('tipo_socio') != '':
        # where2 = where2 + " AND TIPO_SOCIO='" + request.POST.get('tipo_socio') + "' "

        prueba = request.POST.get('tipo_socio')
        prueba2 = prueba.split(',')
        prueba3 = ', '.join("'{0}'".format(w) for w in prueba2)
        where2 = where2 + " AND TIPO_SOCIO in (" + prueba3 + ") "

    # Consultar grafrica
    sql2 = " SELECT " + where1 + " AS LABEL, (SUM(PVGWP)/1000000) AS PVGWP,(SUM(VALUE_CREATION)/1000000) AS VALUE_CREATION, SUM(VALUE_CREATION)/SUM(PVGWP) *100 AS PROFIT_MARGIN FROM PRF_PGV " + where2 + " GROUP BY " + where1

    pgv2 = pd.read_sql(sql2, cnxn3)
    pgv2 = pgv2.sort_values(by='VALUE_CREATION', ascending=False)
    pgv2 = pgv2.reset_index()
    pgv2['VALUE_CREATION'] = pgv2['VALUE_CREATION'].astype(np.int32)
    pgv2['PVGWP'] = pgv2['PVGWP'].astype(np.int32)

    color2 = linear_gradient("#7db5dc", "#0c2e46", len(pgv2))
    newColor = color2['hex']

    data = []
    for i, row in pgv2.iterrows():
        VALUE_CREATION_LABEL = '{:,}'.format(row['VALUE_CREATION'])
        PVGWP_LABEL = '{:,}'.format(row['PVGWP'])
        PROFIT_MARGIN_LABEL = '{:.2f}'.format(row['PROFIT_MARGIN']) + ' %'
        data.append({
            "label": str(row['LABEL']),
            "VALUE_CREATION": row['VALUE_CREATION'],
            "PVGWP": row['PVGWP'],
            "PROFIT_MARGIN": row['PROFIT_MARGIN'],
            "VALUE_CREATION_LABEL": VALUE_CREATION_LABEL,
            "PVGWP_LABEL": PVGWP_LABEL,
            "PROFIT_MARGIN_LABEL": PROFIT_MARGIN_LABEL,
            "color": newColor[i],
            "minimo1": 5
        })

    data2 = []

    for i, row in pgv2.iterrows():
        VALUE_CREATION = '{:,}'.format(row['VALUE_CREATION'])
        PVGWP = '{:,}'.format(row['PVGWP'])
        PROFIT_MARGIN = '{:.2f}'.format(row['PROFIT_MARGIN']) + ' %'
        data2.append({
            "label": str(row['LABEL']),
            "VALUE_CREATION": VALUE_CREATION,
            "PVGWP": PVGWP,
            "PROFIT_MARGIN": PROFIT_MARGIN,
            "color": newColor[i],
        })

    cnxn3.close();
    return JsonResponse([data, data2], safe=False)


def reporte1(request):
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
    sql1 = """ SELECT * FROM PRF_PGV """
    pgv = pd.read_sql(sql1, cnxn3)

    socios = pgv['SOCIO'].unique()
    codproductos = pgv['PRODUCTO'].unique()
    productos = pgv['NOMBRE_PRODUCTO'].unique()
    tipo_ofertas = pgv['TIPO_OFERTA'].unique()
    capas = pgv['CAPA'].unique()
    lineas = pgv['LINEA_NEGOCIO_SOCIO'].unique()
    tipos_prima = pgv['TIPO_PRIMA'].unique()
    tipos = pgv['TIPO'].unique()
    periodos = pgv['PERIODO'].astype(np.int32).unique()
    tipos_socio = pgv['TIPO_SOCIO'].unique()

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
        'title': 'PGV',
        'socios': socios,
        'codproductos': codproductos,
        'productos': productos,
        'tipo_ofertas': tipo_ofertas,
        'capas': capas,
        'lineas': lineas,
        'tipos_prima': tipos_prima,
        'tipos': tipos,
        'periodos': periodos,
        'tipos_socio': tipos_socio,
        'area': 'Profitability',
        'herramienta': 'PGV',
        'file': 'profitability/pgv.html',
    }
    cnxn3.close()
    return render(request, "principal/base.html", configurationView)
