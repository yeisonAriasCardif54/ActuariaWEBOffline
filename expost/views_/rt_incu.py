import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser
import os
import time
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
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "title": 'RT Ocurr_Q Socios',
        "area": 'ExPost',
        "herramienta": 'rt_incu',
        "file": 'expost/rt_incu.html',
    }
    return render(request, "principal/base.html", configurationView)


def selects(request):
    global cnxn

    #time.sleep(20)

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

    # Concatenar Data Graphs
    df_list = [];
    df_consol = pd.DataFrame()

    # Aplicar filtros
    socio_seleccionado = request.POST.getlist('valores');
    df_iterar = pd.DataFrame()
    df_iterar['socio_seleccionado'] = pd.Series(socio_seleccionado);

    df2 = pd.DataFrame(columns=['socio_seleccionado'])
    df2 = df2.append({'socio_seleccionado': '1=1'}, ignore_index=True)

    if df_iterar.empty:
        df_iterar = df2
    else:
        df_iterar = df_iterar

    linea_seleccionado = request.POST.getlist('linea')
    linea_fina_seleccionado = request.POST.getlist('linea_negocio')
    risk_seleccionado = request.POST.getlist('risk')
    canal_seleccionado = request.POST.getlist('canal')
    tipo_seleccionado = request.POST.getlist('tipo')

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

    if len(tipo_seleccionado) > 0:
        a = tuple(tipo_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        tipo_seleccionado = tuple(l)
        where2 = where2 + " AND TIPO IN " + str(tipo_seleccionado)

    # Query RT_OCURR_Q
    sql1 = """  SELECT CODPRODUCTO, RISK, LINEA, SOCIO, TIPO, PRODUCTO_FINANCIERO, CANAL,
                SUM(EP) AS EP, SUM(INCURRIDO) AS INCURRIDO,  
                SUM(PAGOS) AS PAGOS, SUM(VAR_RBNS) AS VAR_RBNS, SUM(VAR_IBNR) AS VAR_IBNR, 
                SUM(RBNS_EOP) AS RBNS_EOP, SUM(IBNR_EOP) AS IBNR_EOP, 
                SUM(EC) AS EC, SUM(PU_EOP) AS PU_EOP, SUM(E_IVAND) AS E_IVAND, 
                PERIODOTRUNC AS PERIODO, AÑO 
                FROM RT_RIESGO_OCURR 
    """ + where2 + """ AND AÑO >= 2015 
    GROUP BY SOCIO, RISK, LINEA, TIPO, PRODUCTO_FINANCIERO, CANAL, CODPRODUCTO, PERIODOTRUNC , AÑO 
    """;

    # Dataframe ejes_df
    ejes_df = pd.read_sql(sql1, cnxn);

    # Filters
    ejes_df = ejes_df[(ejes_df['PRODUCTO_FINANCIERO'].isin(
        ['N/A', 'NA', 'Giros', 'Microcredito', 'SOAT', 'Hipotecario', 'Vehiculos']) == False) &
                      (ejes_df['RISK'].isin(['AD', 'D', 'DD', 'IU', 'TD', 'TH', 'TPD'])) &
                      (ejes_df['SOCIO'].isin(
                          ['BANCO AV VILLAS', 'BANCO POPULAR', 'BANCO DE BOGOTA', 'BANCOLOMBIA', 'EXITO',
                           'BANCO DE OCCIDENTE']))]

    ejes_df['CODPRODUCTO'] = ejes_df["CODPRODUCTO"].astype(int)
    ejes_df['AÑO'] = ejes_df["AÑO"].astype(int)

    # UNICOS SELECT
    socios = list(ejes_df['SOCIO'].unique());
    socios.sort();

    linea = list(ejes_df['LINEA'].unique());
    linea.sort();

    linea_negocio = list(ejes_df['PRODUCTO_FINANCIERO'].unique())
    # linea_negocio.sort();

    risk = list(ejes_df['RISK'].unique());
    risk.sort();

    canal = list(ejes_df['CANAL'].unique());
    canal.sort();

    tipo = list(ejes_df['TIPO'].unique());
    # tipo.sort();

    del [ejes_df]

    #############################################################################################################
    ####################################FUNCION ITERAR SOCIOS####################################################
    #############################################################################################################

    def make_dataset(socio_iterar):

        media_ = 1

        # columna socio
        socio = socio_iterar
        socio_seleccionado = [socio_iterar]

        where22 = ' WHERE 1=1 '

        linea_seleccionado = request.POST.getlist('linea')
        linea_fina_seleccionado = request.POST.getlist('linea_negocio')
        risk_seleccionado = request.POST.getlist('risk')
        canal_seleccionado = request.POST.getlist('canal')
        tipo_seleccionado = request.POST.getlist('tipo')

        if len(socio_seleccionado) > 0:
            a = tuple(socio_seleccionado);
            b = '1=1'
            l = list(a);
            l.append(b)
            socio_seleccionado = tuple(l)
            where22 = where22 + " AND SOCIO IN " + str(socio_seleccionado)

        if len(linea_seleccionado) > 0:
            a = tuple(linea_seleccionado);
            b = '1=1'
            l = list(a);
            l.append(b)
            linea_seleccionado = tuple(l)
            where22 = where22 + " AND LINEA IN " + str(linea_seleccionado)

        if len(linea_fina_seleccionado) > 0:
            a = tuple(linea_fina_seleccionado);
            b = '1=1'
            l = list(a);
            l.append(b)
            linea_fina_seleccionado = tuple(l)
            where22 = where22 + " AND PRODUCTO_FINANCIERO IN " + str(linea_fina_seleccionado)

        if len(risk_seleccionado) > 0:
            a = tuple(risk_seleccionado);
            b = '1=1'
            l = list(a);
            l.append(b)
            risk_seleccionado = tuple(l)
            where22 = where22 + " AND RISK IN " + str(risk_seleccionado)

        if len(canal_seleccionado) > 0:
            a = tuple(canal_seleccionado);
            b = '1=1'
            l = list(a);
            l.append(b)
            canal_seleccionado = tuple(l)
            where22 = where22 + " AND CANAL IN " + str(canal_seleccionado)

        if len(tipo_seleccionado) > 0:
            a = tuple(tipo_seleccionado);
            b = '1=1'
            l = list(a);
            l.append(b)
            tipo_seleccionado = tuple(l)
            where22 = where22 + " AND TIPO IN " + str(tipo_seleccionado)

        #############################################################################################################

        # Consultar Base de Datos

        # Query RT_OCURR_Q
        sql11 = """  SELECT CODPRODUCTO, RISK, LINEA, SOCIO, TIPO, PRODUCTO_FINANCIERO, CANAL,
                    SUM(EP) AS EP, SUM(INCURRIDO) AS INCURRIDO,  
                    SUM(PAGOS) AS PAGOS, SUM(VAR_RBNS) AS VAR_RBNS, SUM(VAR_IBNR) AS VAR_IBNR, 
                    SUM(RBNS_EOP) AS RBNS_EOP, SUM(IBNR_EOP) AS IBNR_EOP, 
                    SUM(EC) AS EC, SUM(PU_EOP) AS PU_EOP, SUM(E_IVAND) AS E_IVAND, 
                    PERIODOTRUNC AS PERIODO, AÑO 
                    FROM RT_RIESGO_OCURR 
        """ + where22 + """ AND AÑO >= 2015 
        GROUP BY SOCIO, RISK, LINEA, TIPO, PRODUCTO_FINANCIERO, CANAL, CODPRODUCTO, PERIODOTRUNC , AÑO 
        """;

        # Dataframe ejes_df
        ejes_df = pd.read_sql(sql11, cnxn);

        ejes_df.PERIODO = pd.to_datetime(ejes_df.PERIODO, format='%d/%m/%y')

        # Filter
        ejes_df = ejes_df[(ejes_df['PRODUCTO_FINANCIERO'].isin(
            ['N/A', 'NA', 'Giros', 'Microcredito', 'SOAT', 'Hipotecario', 'Vehiculos']) == False) &
                          (ejes_df['RISK'].isin(['AD', 'D', 'DD', 'IU', 'TD', 'TH', 'TPD'])) &
                          (ejes_df['SOCIO'].isin(
                              ['BANCO AV VILLAS', 'BANCO POPULAR', 'BANCO DE BOGOTA', 'BANCOLOMBIA', 'EXITO',
                               'BANCO DE OCCIDENTE']))]

        ejes_df['CODPRODUCTO'] = ejes_df["CODPRODUCTO"].astype(int)
        ejes_df['AÑO'] = ejes_df["AÑO"].astype(int)

        # Filter Quarters
        file = 'static/expost/INPUT.xlsx'
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
        quarter_ocurr = pd.read_excel(file,
                                      sheetname='QUARTERS_OCURR')
        quarter_ocurr["QUARTER"] = quarter_ocurr['QUARTER'].astype(str).str[:4] + '-' + quarter_ocurr['QUARTER'].astype(
            str).str[-2:] + '-01'
        quarter_ocurr['QUARTER'] = pd.to_datetime(quarter_ocurr['QUARTER'])
        maximo = quarter_ocurr['QUARTER'].max()
        print('\n\n\n - maximo - \n\n\n')
        print(maximo)
        ejes_df = ejes_df[(ejes_df.PERIODO <= maximo)]

        if ((len(ejes_df) != 0)):

            #####################################################################################################################

            # drop columnas no necesarias
            selec_3 = ejes_df.drop(['CODPRODUCTO', 'RISK', 'LINEA', 'SOCIO', 'TIPO', 'PRODUCTO_FINANCIERO', 'CANAL'],
                                   axis=1)

            # Calculate SUM
            selec_3 = selec_3.groupby(['AÑO', 'PERIODO'])[
                'EP', 'INCURRIDO', 'PAGOS', 'RBNS_EOP', 'IBNR_EOP', 'EC', 'PU_EOP', 'E_IVAND'].sum().reset_index()

            # Aplicar Medias Móviles
            selec_3['PORC_INCU'] = (selec_3['INCURRIDO'].rolling(min_periods=1, window=media_).sum()) / (
                selec_3['EP'].rolling(min_periods=1, window=media_).sum())

            # Fill NA
            selec_3 = selec_3.replace(np.inf, np.nan).fillna(0)

            selec_4 = selec_3

            selec_4 = selec_4[['AÑO', 'PERIODO', 'PORC_INCU']]
            selec_4['SOCIO'] = socio

            selec_4['PERIODO'] = np.where((selec_4.PERIODO.astype(str).str[6:7]) == '1',
                                          selec_4['PERIODO'].astype(str).str[:4] + 'Q1',

                                          (np.where((selec_4.PERIODO.astype(str).str[6:7]) == '4',
                                                    selec_4['PERIODO'].astype(str).str[:4] + 'Q2',

                                                    (np.where((selec_4.PERIODO.astype(str).str[6:7]) == '7',
                                                              selec_4['PERIODO'].astype(str).str[:4] + 'Q3',

                                                              selec_4['PERIODO'].astype(str).str[:4] + 'Q4'

                                                              )))))

            return (selec_4)

        else:
            selec_4 = pd.DataFrame([[0, 0, 0, 0]], columns=['AÑO', 'PERIODO', 'PORC_INCU', 'SOCIO'])

    ########################################################################################################################################

    # Loop Informacion Productos Financieros
    def tipo_prod(socio_seleccionado):

        valor_ = make_dataset(socio_seleccionado)
        df_list.append(valor_)
        print("{}_done".format(socio_seleccionado))

    listas = list(df_iterar['socio_seleccionado'].unique())

    for lista in listas:
        tipo_prod(lista)

    # Concatenar All Socios
    df_consol = pd.concat(df_list, ignore_index=True)

    # Prepare Data
    df_consol = df_consol[(df_consol['AÑO'] != 0)]

    #Format Graph Amcharts (Multiplica * 100)
    df_consol['PORC_INCU'] = df_consol['PORC_INCU'] * 100

    # round 2 decimals
    decimals = 2
    df_consol['PORC_INCU'] = df_consol['PORC_INCU'].apply(lambda x: round(x, decimals))

    colorsList = {  # "BANCO AGRARIO": "#1f77b4",
        # "BANCO CORPBANCA": "#aec7e8",
        "BANCO DE BOGOTA": "#ff7f0e",
        "BANCO DE OCCIDENTE": "#F43009",
        "BANCO AV VILLAS": "#2ca02c",
        # "BANCO FALABELLA": "#98df8a",
        # "BANCO FINANDINA": "#d62728",
        # "BANCO PICHINCHA": "#ff9896",
        "BANCO POPULAR": "#9467bd",
        "BANCOLOMBIA": "#9edae5",
        # "CENCOSUD": "#e377c2",
        # "COOMEVA": "#17becf",
        "EXITO": "#dbdb8d",
        # "RIPLEY": "#8c564b"
    }

    def generate_tria(df):
        df = df[['PERIODO', 'PORC_INCU', 'SOCIO']]
        tria_ = pd.pivot_table(data=df, values='PORC_INCU', index=['PERIODO'], columns=['SOCIO'],
                               aggfunc=np.sum).reset_index()
        return tria_

    def generate_data(df):
        df = df[['PERIODO', 'PORC_INCU', 'SOCIO']]
        tria_ = pd.pivot_table(data=df, values='PORC_INCU', index=['PERIODO'], columns=['SOCIO'],
                               aggfunc=np.sum).reset_index()
        del (tria_['PERIODO'])
        columns = tria_.columns.values

        df_list = []
        for column in columns:
            df_list.append({
                "bullet": "bubble",
                "bulletBorderAlpha": 2,
                "bulletSize": 4,
                "lineThickness": 2,
                "bulletColor": colorsList[column],
                "bulletBorderThickness": 2,
                "type": "smoothedLine",
                "useLineColorForBulletBorder": "true",
                "fillAlphas": 0,
                "lineAlpha": 2,
                "title": column,
                "valueField": column,
                "lineColor": colorsList[column],
                "type": "smoothedLine",
                "balloonText": "[[title]]<br/><b style='font-size: 80%'>[[value]]%</b>"
            })
        return df_list

    # Data #1
    df_data1 = generate_tria(df_consol);
    df_data1 = df_data1.to_dict('records')

    # Data #2
    df_data2 = generate_data(df_consol)

    cnxn.close();

    return JsonResponse([socios, linea, linea_negocio, risk, canal, tipo, df_data1, df_data2], safe=False)




























