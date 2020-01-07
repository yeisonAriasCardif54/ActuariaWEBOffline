import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser
import os
from os.path import dirname, join
import sqlite3

global list_anual, frame_anual

list_anual = []
frame_anual = pd.DataFrame()


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
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "title": 'RT Ocurr_Q General',
        "area": 'ExPost',
        "herramienta": 'rt_ocurr_q',
        "file": 'expost/rt_ocurr_q.html',
    }
    return render(request, "principal/base.html", configurationView)


def selects(request):
    """
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
                             """
    cnxn = sqlite3.connect('actuariaDatabase')

    # Aplicar filtros
    socio_seleccionado = request.POST.getlist('socios')
    socio_seleccionado = [i for i in socio_seleccionado if i != '']
    socio_seleccionado = [sub_item for item in socio_seleccionado for sub_item in item.split(",")]

    linea_seleccionado = request.POST.getlist('linea')
    linea_seleccionado = [i for i in linea_seleccionado if i != '']
    linea_seleccionado = [sub_item for item in linea_seleccionado for sub_item in item.split(",")]

    linea_fina_seleccionado = request.POST.getlist('linea_negocio')
    linea_fina_seleccionado = [i for i in linea_fina_seleccionado if i != '']
    linea_fina_seleccionado = [sub_item for item in linea_fina_seleccionado for sub_item in item.split(",")]

    risk_seleccionado = request.POST.getlist('risk')
    risk_seleccionado = [i for i in risk_seleccionado if i != '']
    risk_seleccionado = [sub_item for item in risk_seleccionado for sub_item in item.split(",")]

    canal_seleccionado = request.POST.getlist('canal')
    canal_seleccionado = [i for i in canal_seleccionado if i != '']
    canal_seleccionado = [sub_item for item in canal_seleccionado for sub_item in item.split(",")]

    producto_seleccionado = request.POST.getlist('productos')
    producto_seleccionado = [i for i in producto_seleccionado if i != '']
    producto_seleccionado = [sub_item for item in producto_seleccionado for sub_item in item.split(",")]

    tipo_seleccionado = request.POST.getlist('tipo')
    tipo_seleccionado = [i for i in tipo_seleccionado if i != '']
    tipo_seleccionado = [sub_item for item in tipo_seleccionado for sub_item in item.split(",")]

    media_ = request.POST.get('media')
    media_ = int(media_)
    where2 = ' WHERE 1=1 '

    if len(socio_seleccionado) > 0:
        a = tuple(socio_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        socio_seleccionado = tuple(l)
        where2 = where2 + " AND SOCIO IN " + str(socio_seleccionado)

    if len(linea_seleccionado) > 0:
        a = tuple(linea_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        linea_seleccionado = tuple(l)
        where2 = where2 + " AND LINEA IN " + str(linea_seleccionado)

    if len(linea_fina_seleccionado) > 0:
        a = tuple(linea_fina_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        linea_fina_seleccionado = tuple(l)
        where2 = where2 + " AND PRODUCTO_FINANCIERO IN " + str(linea_fina_seleccionado)

    if len(risk_seleccionado) > 0:
        a = tuple(risk_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        risk_seleccionado = tuple(l)
        where2 = where2 + " AND RISK IN " + str(risk_seleccionado)

    if len(canal_seleccionado) > 0:
        a = tuple(canal_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        canal_seleccionado = tuple(l)
        where2 = where2 + " AND CANAL IN " + str(canal_seleccionado)

    if len(producto_seleccionado) > 0:
        a = tuple(producto_seleccionado);
        b = 0
        l = list(a);
        l.append(b)
        producto_seleccionado = tuple(l)
        where2 = where2 + " AND CODPRODUCTO IN " + str(producto_seleccionado)

    if len(tipo_seleccionado) > 0:
        a = tuple(tipo_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        tipo_seleccionado = tuple(l)
        where2 = where2 + " AND TIPO IN " + str(tipo_seleccionado)

    #############################################################################################################

    # Consultar Base de Datos

    # Query RT_OCURR_Q
    sql1 = """  SELECT CODPRODUCTO, RISK, LINEA, SOCIO, TIPO, PRODUCTO_FINANCIERO, CANAL, 
                SUM(EP) AS EP, SUM(INCURRIDO) AS INCURRIDO,  SUM(IE) AS IE,
                SUM(PAGOS) AS PAGOS, SUM(VAR_RBNS) AS VAR_RBNS, SUM(VAR_IBNR) AS VAR_IBNR, 
                SUM(RBNS_EOP) AS RBNS_EOP, SUM(IBNR_EOP) AS IBNR_EOP, 
                SUM(EC) AS EC, SUM(PU_EOP) AS PU_EOP, SUM(E_IVAND) AS E_IVAND, 
                PERIODOTRUNC AS PERIODO, AÑO 
                FROM RT_RIESGO_OCURR 
    """ + where2 + """ AND AÑO >= 2015 
    GROUP BY SOCIO, RISK, LINEA, TIPO, PRODUCTO_FINANCIERO, CANAL, CODPRODUCTO, PERIODOTRUNC , AÑO 
    """;

    # Dataframe RT_OCURR_Q
    df_tecn_orig = pd.read_sql(sql1, cnxn);

    df_tecn_orig.PERIODO = pd.to_datetime(df_tecn_orig.PERIODO, format='%d/%m/%y')
    df_tecn_orig['PERIODO'] = df_tecn_orig['PERIODO'].astype(str).str[:4] + df_tecn_orig['PERIODO'].astype(str).str[5:7]
    df_tecn_orig['PERIODO'] = df_tecn_orig['PERIODO'].astype(int)
    df_tecn_orig['PRODUCTO_FINANCIERO'] = df_tecn_orig['PRODUCTO_FINANCIERO'].fillna('NA')
    df_tecn_orig['TIPO'] = df_tecn_orig['TIPO'].fillna('NA')
    df_tecn_orig['CANAL'] = df_tecn_orig['CANAL'].fillna('NA')

    cnxn.close();

    #####################################################################################################################
    df_tecn = df_tecn_orig.copy()

    # drop columnas no necesarias
    selec_3 = df_tecn.drop(['CODPRODUCTO', 'RISK', 'LINEA', 'SOCIO', 'TIPO', 'PRODUCTO_FINANCIERO', 'CANAL'], axis=1)

    # Calculate SUM
    selec_3 = selec_3.groupby(['AÑO', 'PERIODO'])[
        'EP', 'IE', 'INCURRIDO', 'PAGOS', 'RBNS_EOP', 'IBNR_EOP', 'EC', 'PU_EOP', 'E_IVAND'].sum().reset_index()

    # Aplicar Medias Móviles
    selec_3['PORC_INCU'] = (selec_3['IE'].rolling(min_periods=1, window=media_).sum()) / (
        selec_3['EP'].rolling(min_periods=1, window=media_).sum())
    selec_3.loc[~np.isfinite(selec_3['PORC_INCU']), 'PORC_INCU'] = np.nan

    selec_3['PORC_PAGOS'] = (selec_3['PAGOS'].rolling(min_periods=1, window=media_).sum()) / (
        selec_3['EP'].rolling(min_periods=1, window=media_).sum())
    selec_3.loc[~np.isfinite(selec_3['PORC_PAGOS']), 'PORC_PAGOS'] = np.nan

    selec_3['PORC_RBNS_EOP'] = (selec_3['RBNS_EOP'].rolling(min_periods=1, window=media_).sum()) / (
        selec_3['EP'].rolling(min_periods=1, window=media_).sum())
    selec_3.loc[~np.isfinite(selec_3['PORC_RBNS_EOP']), 'PORC_RBNS_EOP'] = np.nan

    selec_3['PORC_IBNR_EOP'] = (selec_3['IBNR_EOP'].rolling(min_periods=1, window=media_).sum()) / (
        selec_3['EP'].rolling(min_periods=1, window=media_).sum())
    selec_3.loc[~np.isfinite(selec_3['PORC_IBNR_EOP']), 'PORC_IBNR_EOP'] = np.nan

    selec_3['PORC_EC'] = (selec_3['EC'].rolling(min_periods=1, window=media_).sum()) / (
        selec_3['EP'].rolling(min_periods=1, window=media_).sum())
    selec_3.loc[~np.isfinite(selec_3['PORC_EC']), 'PORC_EC'] = np.nan

    selec_3['PORC_ICT'] = ((selec_3['EC'].rolling(min_periods=1, window=media_).sum())
                           + (selec_3['IE'].rolling(min_periods=1, window=media_).sum())
                           + (selec_3['PU_EOP'].rolling(min_periods=1, window=media_).sum())
                           + (selec_3['E_IVAND'].rolling(min_periods=1, window=media_).sum())) / (
                              selec_3['EP'].rolling(min_periods=1, window=media_).sum())
    selec_3.loc[~np.isfinite(selec_3['PORC_ICT']), 'PORC_ICT'] = np.nan

    # Fill NA
    selec_3 = selec_3.replace(np.inf, np.nan).fillna(0)

    selec_3['FILTER'] = 'MENSUALES'

    # *********Acumulados Anuales************

    df_tot = selec_3[
        ['AÑO', 'PERIODO', 'EP', 'IE', 'INCURRIDO', 'PAGOS', 'RBNS_EOP', 'IBNR_EOP', 'EC', 'PU_EOP', 'E_IVAND']]

    filt_year = df_tot['AÑO'].max()

    df_tot_pre = df_tot[df_tot['AÑO'] < filt_year]
    df_tot_post = df_tot[df_tot['AÑO'] == filt_year]

    media_12 = 4
    media_post = df_tot_post['AÑO'].count()

    # EP ANUAL
    df_tot_pre['EP_ANUAL'] = df_tot_pre.groupby('AÑO')['EP'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_post['EP_ANUAL'] = df_tot_post.groupby('AÑO')['EP'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())

    # INCURRED ANUAL
    df_tot_pre['INCU_A'] = df_tot_pre.groupby('AÑO')['INCURRIDO'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_pre['INCU_ANUAL'] = df_tot_pre['INCU_A'] / df_tot_pre['EP_ANUAL']
    df_tot_post['INCU_A'] = df_tot_post.groupby('AÑO')['INCURRIDO'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())
    df_tot_post['INCU_ANUAL'] = df_tot_post['INCU_A'] / df_tot_post['EP_ANUAL']

    # PAID ANUAL
    df_tot_pre['PAGOS_A'] = df_tot_pre.groupby('AÑO')['PAGOS'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_pre['PAGOS_ANUAL'] = df_tot_pre['PAGOS_A'] / df_tot_pre['EP_ANUAL']
    df_tot_post['PAGOS_A'] = df_tot_post.groupby('AÑO')['PAGOS'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())
    df_tot_post['PAGOS_ANUAL'] = df_tot_post['PAGOS_A'] / df_tot_post['EP_ANUAL']

    # RBNS_EOP ANUAL
    df_tot_pre['VAR_RBNS_A'] = df_tot_pre.groupby('AÑO')['RBNS_EOP'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_pre['VAR_RBNS_ANUAL'] = df_tot_pre['VAR_RBNS_A'] / df_tot_pre['EP_ANUAL']
    df_tot_post['VAR_RBNS_A'] = df_tot_post.groupby('AÑO')['RBNS_EOP'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())
    df_tot_post['VAR_RBNS_ANUAL'] = df_tot_post['VAR_RBNS_A'] / df_tot_post['EP_ANUAL']

    # IBNR_EOP ANUAL
    df_tot_pre['VAR_IBNR_A'] = df_tot_pre.groupby('AÑO')['IBNR_EOP'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_pre['VAR_IBNR_ANUAL'] = df_tot_pre['VAR_IBNR_A'] / df_tot_pre['EP_ANUAL']
    df_tot_post['VAR_IBNR_A'] = df_tot_post.groupby('AÑO')['IBNR_EOP'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())
    df_tot_post['VAR_IBNR_ANUAL'] = df_tot_post['VAR_IBNR_A'] / df_tot_post['EP_ANUAL']

    # VAR_IBNR ANUAL
    df_tot_pre['EC_A'] = df_tot_pre.groupby('AÑO')['EC'].apply(lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_pre['EC_ANUAL'] = df_tot_pre['EC_A'] / df_tot_pre['EP_ANUAL']
    df_tot_post['EC_A'] = df_tot_post.groupby('AÑO')['EC'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())
    df_tot_post['EC_ANUAL'] = df_tot_post['EC_A'] / df_tot_post['EP_ANUAL']

    # TCR ANUAL
    df_tot_pre['EC_A'] = df_tot_pre.groupby('AÑO')['EC'].apply(lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_post['EC_A'] = df_tot_post.groupby('AÑO')['EC'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())

    #
    df_tot_pre['PU_INCUR_A'] = df_tot_pre.groupby('AÑO')['PU_EOP'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_post['PU_INCUR_A'] = df_tot_post.groupby('AÑO')['PU_EOP'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())

    df_tot_pre['E_IVAND_A'] = df_tot_pre.groupby('AÑO')['E_IVAND'].apply(
        lambda x: x.rolling(center=False, window=media_12).sum())
    df_tot_post['E_IVAND_A'] = df_tot_post.groupby('AÑO')['E_IVAND'].apply(
        lambda x: x.rolling(center=False, window=media_post).sum())

    df_tot_pre['TCR_ANUAL'] = (df_tot_pre['EC_A'] + df_tot_pre['PU_INCUR_A'] + df_tot_pre['E_IVAND_A'] + df_tot_pre[
        'INCU_A']) / df_tot_pre['EP_ANUAL']
    df_tot_post['TCR_ANUAL'] = (df_tot_post['EC_A'] + df_tot_post['PU_INCUR_A'] + df_tot_post['E_IVAND_A'] +
                                df_tot_post['INCU_A']) / df_tot_post['EP_ANUAL']

    # Union DataFrames
    frames = [df_tot_pre, df_tot_post]
    df_tot_end = pd.concat(frames)

    df_tot_end = df_tot_end.drop(
        ['EC_A', 'PU_INCUR_A', 'E_IVAND_A', 'EC_A', 'VAR_IBNR_A', 'VAR_RBNS_A', 'PAGOS_A', 'INCU_A', 'RBNS_EOP',
         'IBNR_EOP', 'EC', 'PU_EOP', 'E_IVAND', 'EP', 'INCURRIDO', 'PAGOS'], axis=1)

    max_row = df_tot_end.loc[df_tot_end.reset_index().groupby(['AÑO'])['PERIODO'].idxmax()]
    max_row = max_row.sort_index()
    max_row = max_row.reset_index(drop=True)

    max_row['FILTER'] = 'ANUALES'

    # Concatenar Data Final Gráficos
    df_tot_last = selec_3[
        ['AÑO', 'PERIODO', 'EP', 'IE', 'PORC_INCU', 'PORC_PAGOS', 'PORC_RBNS_EOP', 'PORC_IBNR_EOP', 'PORC_EC',
         'PORC_ICT',
         'FILTER']]
    new_cols = {x: y for x, y in zip(max_row.columns, df_tot_last.columns)}
    selec_4 = df_tot_last.append(max_row.rename(columns=new_cols))

    # Filter Quarters
    file = 'static/expost/INPUT.xlsx'
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
    quarter_ocurr = pd.read_excel(file,
                                  sheetname='QUARTERS_OCURR')
    maximo = quarter_ocurr['QUARTER'].max()
    selec_4 = selec_4[(selec_4.PERIODO <= maximo)]

    selec_4['PERIODO'] = np.where((selec_4.PERIODO.astype(str).str[-1:]) == '1',
                                  selec_4['PERIODO'].astype(str).str[:4] + 'Q1',

                                  (np.where((selec_4.PERIODO.astype(str).str[-1:]) == '4',
                                            selec_4['PERIODO'].astype(str).str[:4] + 'Q2',

                                            (np.where((selec_4.PERIODO.astype(str).str[-1:]) == '7',
                                                      selec_4['PERIODO'].astype(str).str[:4] + 'Q3',

                                                      selec_4['PERIODO'].astype(str).str[:4] + 'Q4'

                                                      )))))

    #############################################################################################################################################################
    # Data Table 01

    data_table_1 = selec_4[(selec_4.FILTER == 'MENSUALES')]
    data_table_1 = data_table_1.loc[data_table_1['AÑO'] >= 2015]

    data_table_1['PORC_ICT'] = data_table_1['PORC_ICT'] * 100
    data_table_1['PORC_INCU'] = data_table_1['PORC_INCU'] * 100
    data_table_1['PORC_PAGOS'] = data_table_1['PORC_PAGOS'] * 100
    data_table_1['PORC_RBNS_EOP'] = data_table_1['PORC_RBNS_EOP'] * 100
    data_table_1['PORC_IBNR_EOP'] = data_table_1['PORC_IBNR_EOP'] * 100
    data_table_1['PORC_EC'] = data_table_1['PORC_EC'] * 100

    data_table_1['EP'] = data_table_1['EP'] / 1000000

    decimals = 1
    data_table_1['PORC_ICT'] = data_table_1['PORC_ICT'].apply(lambda x: round(x, decimals))

    # delimitar Data
    data_table_1 = data_table_1[-15:]

    data_table_01 = []
    for i, row in data_table_1.iterrows():
        # EP = '{0:,.2f}'.format(row['EP'])
        PORC_INCU = '{:.2%}'.format(row['PORC_INCU'])
        PORC_PAGOS = '{:.2%}'.format(row['PORC_PAGOS'])
        PORC_RBNS_EOP = '{:.2%}'.format(row['PORC_RBNS_EOP'])
        PORC_IBNR_EOP = '{:.2%}'.format(row['PORC_IBNR_EOP'])
        PORC_EC = '{:.2%}'.format(row['PORC_EC'])
        # PORC_ICT = '{:.1%}'.format(row['PORC_ICT'])

        data_table_01.append({

            "ANUAL": str(row['AÑO']),
            "PERIODO": (row['PERIODO']),
            "EP": row['EP'],
            "%_INCU_CLAIMS": row['PORC_INCU'],
            "%_PAID_CLAIMS": row['PORC_PAGOS'],
            "%_RBNS_EOP": row['PORC_RBNS_EOP'],
            "%_IBNR_EOP": row['PORC_IBNR_EOP'],
            "%_EC": row['PORC_EC'],
            "%_TCR": row['PORC_ICT'],
        })

    #############################################################################################################################################################
    # Data Table 02

    data_table_2 = selec_4[(selec_4.FILTER == 'ANUALES')]
    data_table_2 = data_table_2.loc[data_table_2['AÑO'] >= 2015]
    data_table_2['AÑO'] = data_table_2['AÑO'].astype(str)

    data_table_2['PORC_ICT'] = data_table_2['PORC_ICT'] * 100
    data_table_2['PORC_INCU'] = data_table_2['PORC_INCU'] * 100
    data_table_2['PORC_PAGOS'] = data_table_2['PORC_PAGOS'] * 100

    # round 1 decimals
    decimals = 1
    data_table_2['PORC_ICT'] = data_table_2['PORC_ICT'].apply(lambda x: round(x, decimals))

    data_table_02 = []
    for i, row in data_table_2.iterrows():
        # EP = '{0:,.2f}'.format(row['EP'])
        PORC_INCU = '{:.2%}'.format(row['PORC_INCU'])
        PORC_PAGOS = '{:.2%}'.format(row['PORC_PAGOS'])
        PORC_RBNS_EOP = '{:.2%}'.format(row['PORC_RBNS_EOP'])
        PORC_IBNR_EOP = '{:.2%}'.format(row['PORC_IBNR_EOP'])
        PORC_EC = '{:.2%}'.format(row['PORC_EC'])
        # PORC_ICT = '{:.1%}'.format(row['PORC_ICT'])

        data_table_02.append({

            "ANUAL": str(row['AÑO']),
            # "PERIODO": (row['PERIODO']),
            # "EP": row['EP'],
            "%_INCU_CLAIMS": row['PORC_INCU'],
            "%_PAID_CLAIMS": row['PORC_PAGOS'],
            "%_RBNS_EOP": row['PORC_RBNS_EOP'],
            "%_IBNR_EOP": row['PORC_IBNR_EOP'],
            "%_EC": row['PORC_EC'],
            "%_TCR": row['PORC_ICT'],
        })

    # UNICOS SELECT
    socios = list(df_tecn_orig['SOCIO'].unique());
    socios.sort();

    linea = list(df_tecn_orig['LINEA'].unique());
    linea.sort();

    linea_negocio = list(df_tecn_orig['PRODUCTO_FINANCIERO'].unique())
    # linea_negocio.sort();

    risk = list(df_tecn_orig['RISK'].unique());
    risk.sort();

    canal = list(df_tecn_orig['CANAL'].unique());
    canal.sort();

    productos = list(df_tecn_orig['CODPRODUCTO'].unique());
    productos.sort(key=int)

    tipo = list(df_tecn_orig['TIPO'].unique());
    # tipo.sort();

    return JsonResponse([socios, linea, linea_negocio, risk, canal, productos, tipo, data_table_01],
                        safe=False)



