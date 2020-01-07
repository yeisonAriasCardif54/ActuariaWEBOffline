import pandas as pd
from django.shortcuts import render
import cx_Oracle
import configparser
import csv
from django.http import HttpResponse


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
        'title': 'Data Expost',
        'area': 'ExPost',
        'herramienta': 'data_expost',
        'file': 'expost/data_expost.html',
    }
    return render(request, "principal/base.html", configurationView)


def export_expu(request):

    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'),
                             dsn_tns)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expuestos.csv"'

    # Query Expuestos
    sql2 = """ SELECT t2.PRODUCTO,(TO_CHAR(EXTRACT(YEAR FROM (T2.PERIODO)) || '-' || SUBSTR((T2.PERIODO),4,3))) AS PERIODO,
    T2.IDPLAN,SUM(ROUND(T2.EXPUESTO, 0)) AS SUM_EXPUESTO 
    FROM ACTUARIA.CART_EXPUESTOS T2 
    WHERE t2.PLAN_SN != 'N' AND t2.PERIODO >= TO_DATE('2013-01-01', 'YYYY-MM-DD') 
    GROUP BY t2.PRODUCTO,T2.IDPLAN,T2.PERIODO ORDER BY t2.PRODUCTO,T2.IDPLAN,T2.PERIODO
                """;

    # Dataframe expu_df
    expu_df = pd.read_sql(sql2, cnxn);     expu_df = expu_df.fillna('NA')
    expu_df['PERIODO'] = pd.to_datetime(expu_df['PERIODO'], format='%Y-%b')
    expu_df['PERIODO'] = expu_df['PERIODO'].astype(str).str[:4] + expu_df['PERIODO'].astype(str).str[5:7]
    cnxn.close();

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['PRODUCTO', 'PERIODO', 'IDPLAN', 'EXPUESTO'])

    users = [x for x in expu_df.values]
    for user in users:
        writer.writerow(user)

    return response

def export_vige(request):
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'),
                             dsn_tns)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vigentes.csv"'

    # Query Expuestos
    sql2 = """ SELECT t1.PRODUCTO,t1.FECHA_INICIO_EMITE AS PRIMER_EMISION,t1.FECHA_INICIO AS PERIODO,SUM(t1.TOTAL_VIGENTES) AS TOTAL
    FROM ACTUARIA.CART_VIGENTES t1 
    GROUP BY t1.PRODUCTO,t1.FECHA_INICIO_EMITE,t1.FECHA_INICIO ORDER BY t1.PRODUCTO,t1.FECHA_INICIO_EMITE,T1.FECHA_INICIO
           """;

    # Dataframe vig_df
    vig_df = pd.read_sql(sql2, cnxn);     vig_df = vig_df.fillna('NA')
    #expu_df['PERIODO'] = pd.to_datetime(expu_df['PERIODO'], format='%Y-%b')
    #expu_df['PERIODO'] = expu_df['PERIODO'].astype(str).str[:4] + expu_df['PERIODO'].astype(str).str[5:7]
    cnxn.close();

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['PRODUCTO', 'PRIMER_EMISION', 'PERIODO', 'TOTAL'])

    users = [x for x in vig_df.values]
    for user in users:
        writer.writerow(user)

    return response


def export_rrc(request):
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'),
                             dsn_tns)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RRC.csv"'

    # Query Expuestos
    sql3 = """ SELECT FEC_LIBERACION,PRODUCTO,DEVENGO_RESE_PRIMA,COM_SOCIO FROM ACTUARIA.CART_RRC 
    ORDER BY FEC_LIBERACION,PRODUCTO
           """;

    # Dataframe vig_df
    rrc_df = pd.read_sql(sql3, cnxn);     rrc_df = rrc_df.fillna('NA')
    rrc_df['FEC_LIBERACION'] = rrc_df["FEC_LIBERACION"].astype(int)
    rrc_df['PRODUCTO'] = rrc_df["PRODUCTO"].astype(int)
    rrc_df[['DEVENGO_RESE_PRIMA', 'COM_SOCIO']] = rrc_df[['DEVENGO_RESE_PRIMA', 'COM_SOCIO']].applymap("{0:.2f}".format)
    cnxn.close();

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['FEC_LIBERACION', 'PRODUCTO', 'DEVENGO_RESE_PRIMA', 'COM_SOCIO'])

    users = [x for x in rrc_df.values]
    for user in users:
        writer.writerow(user)

    return response

def export_nuevos(request):
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'),
                             dsn_tns)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nuevos_mes.csv"'

    # Query Nuevos
    sql3 = """ SELECT T1.PRODUCTO, T1.FECHA_INICIO , T1.TOTAL_VIGENTES FROM( 
                SELECT PRODUCTO, (CASE WHEN FECHA_INICIO_EMITE = FECHA_INICIO THEN 1 ELSE 0 END) AS VALIDA,
                FECHA_INICIO_EMITE, FECHA_INICIO , TOTAL_VIGENTES FROM ACTUARIA.CART_VIGENTES
                WHERE TIPO_QUERY != 1
                ORDER BY PRODUCTO, FECHA_INICIO_EMITE, FECHA_INICIO )T1 WHERE T1.VALIDA = 1
           """;

    # Dataframe vig_df
    new_df = pd.read_sql(sql3, cnxn);     new_df = new_df.fillna('NA')
    #rrc_df['FEC_LIBERACION'] = rrc_df["FEC_LIBERACION"].astype(int)
    #rrc_df['PRODUCTO'] = rrc_df["PRODUCTO"].astype(int)
    #rrc_df[['DEVENGO_RESE_PRIMA', 'COM_SOCIO']] = rrc_df[['DEVENGO_RESE_PRIMA', 'COM_SOCIO']].applymap("{0:.2f}".format)
    cnxn.close();

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['PRODUCTO', 'FECHA_INICIO', 'TOTAL_VIGENTES'])

    users = [x for x in new_df.values]
    for user in users:
        writer.writerow(user)

    return response