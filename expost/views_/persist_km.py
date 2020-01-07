import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser
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
        "title": 'Persistencia K_M',
        "area": 'ExPost',
        "herramienta": 'persist_km',
        "file": 'expost/persist_km.html',
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

    linea_fina_seleccionado = request.POST.getlist('linea_negocio')
    linea_fina_seleccionado = [i for i in linea_fina_seleccionado if i != '']
    linea_fina_seleccionado = [sub_item for item in linea_fina_seleccionado for sub_item in item.split(",")]

    periodo_seleccionado = request.POST.getlist('periodo')
    periodo_seleccionado = [i for i in periodo_seleccionado if i != '']
    periodo_seleccionado = [sub_item for item in periodo_seleccionado for sub_item in item.split(",")]

    canal_seleccionado = request.POST.getlist('canal')
    canal_seleccionado = [i for i in canal_seleccionado if i != '']
    canal_seleccionado = [sub_item for item in canal_seleccionado for sub_item in item.split(",")]

    producto_seleccionado = request.POST.getlist('productos')
    producto_seleccionado = [i for i in producto_seleccionado if i != '']
    producto_seleccionado = [sub_item for item in producto_seleccionado for sub_item in item.split(",")]

    media_ = request.POST.get('media')
    media_ = int(media_)

    where2 = ' WHERE 1=1 '

    if len(socio_seleccionado) > 0:
        a = tuple(socio_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        socio_seleccionado = tuple(l)
        where2 = where2 + " AND NOM_SOCIO IN " + str(socio_seleccionado)

    if len(linea_fina_seleccionado) > 0:
        a = tuple(linea_fina_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        linea_fina_seleccionado = tuple(l)
        where2 = where2 + " AND LINEA_NEGOCIO IN " + str(linea_fina_seleccionado)

    if len(periodo_seleccionado) > 0:
        a = tuple(periodo_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        periodo_seleccionado = tuple(l)
        where2 = where2 + " AND PERIODO IN " + str(periodo_seleccionado)

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
        where2 = where2 + " AND COD_PROD IN " + str(producto_seleccionado)

    #############################################################################################################

    # Consultar Base de Datos

    # Query Unicos Tabla Productos
    sql1 = """  SELECT DISTINCT COD_PROD, PERIODO, LINEA_NEGOCIO, NOM_SOCIO, CANAL
                FROM TABLA_PRODUCTOS 
                """ + where2 + """ AND ESTADO != 'NO-DATA'  """;

    # Dataframe Unicos
    df_unicos = pd.read_sql(sql1, cnxn);
    print('01-OK', len(df_unicos))

    lista = list(df_unicos['COD_PROD'].unique())
    for i in range(len(lista)):
        lista[i] = int(lista[i])
    lista.insert(0, 0)

    #print(lista)

    # Query CART_VIGENTES_FACTOR
    '''
    sql2 = """  SELECT * FROM(
        SELECT CENSURADO, DURACION_FINAL,COUNT(CENSURADO) AS TOTAL_CENSU,COUNT(DURACION_FINAL) AS TOTAL_DURACION
        FROM ACTUARIA.CART_VIGENTES_FACTOR WHERE PRODUCTO IN {0}
        GROUP BY DURACION_FINAL , CENSURADO
        ORDER BY DURACION_FINAL , CENSURADO 
        )PIVOT ( SUM(TOTAL_CENSU) FOR CENSURADO IN (0,1) ) ORDER BY DURACION_FINAL 
            """.format(tuple(lista));
            
    sql2 = """  
        SELECT CENSURADO, DURACION_FINAL,COUNT(CENSURADO) AS TOTAL_CENSU,COUNT(DURACION_FINAL) AS TOTAL_DURACION
        FROM ACTUARIA.CART_VIGENTES_FACTOR WHERE PRODUCTO IN {0}
        GROUP BY DURACION_FINAL , CENSURADO
        --ORDER BY DURACION_FINAL , CENSURADO 
        """.format(tuple(lista));    
        
    # Query Vigentes x Generaciones
    sql3 = """SELECT (TO_CHAR(EXTRACT(YEAR FROM FECHA_INICIO_EMITE))) AS ANUAL
            ,COUNT(*) AS CONTEO
            FROM ACTUARIA.CART_VIGENTES_FACTOR 
            WHERE CENSURADO = 1 
            AND PRODUCTO IN {0}
            GROUP BY (TO_CHAR(EXTRACT(YEAR FROM FECHA_INICIO_EMITE))) ORDER BY (TO_CHAR(EXTRACT(YEAR FROM FECHA_INICIO_EMITE)))""".format(
        tuple(lista));        
    '''

    sql2 = """  
            SELECT CENSURADO, DURACION_FINAL,
            SUM(TOTAL_CENSU) AS TOTAL_CENSU ,
            SUM(TOTAL_DURACION) AS TOTAL_DURACION 
            FROM DASH_PERSIST_01 WHERE PRODUCTO IN {0}
            GROUP BY CENSURADO, DURACION_FINAL
            """.format(tuple(lista));

    # Query Vigentes x Generaciones
    sql3 = """
            SELECT  ANUAL, SUM(TOTAL_DURACION) AS CONTEO
            FROM DASH_PERSIST_01 
            WHERE CENSURADO = 1 AND PRODUCTO IN {0}
            GROUP BY ANUAL ORDER BY ANUAL
            """.format(tuple(lista));

    # Dataframe CART_VIGENTES_FACTOR
    selected = pd.read_sql(sql2, cnxn);

    selected = selected.replace(np.inf, np.nan).fillna(0)
    # PIVOTE DATA FRAMES#
    selected = pd.pivot_table(data=selected, values='TOTAL_CENSU', index=['DURACION_FINAL', 'TOTAL_DURACION'],
                              columns=['CENSURADO'],
                              aggfunc=np.sum, fill_value=0).reset_index()
    print('02-OK')

    selected.rename(columns={'DURACION_FINAL': 't', 0: 'd', 1: 'c'}, inplace=True)
    selected.fillna(0, inplace=True)

    selected['TOTAL_DURACION'] = selected['TOTAL_DURACION'].astype(int)
    selected['d'] = selected['d'].astype(int)
    selected['c'] = selected['c'].astype(int)

    # Calcular r first rwo
    r_first = selected['TOTAL_DURACION'].sum()

    # Agrupar y sumar
    selec_2 = selected.groupby(['t'])['d', 'c'].sum().reset_index()

    # Create Dataframe to merge 72 meses
    numbers = list(range(0, 73))
    df_table = pd.DataFrame({'t': list(numbers)})

    # merge 60 meses
    selec_3 = pd.merge(df_table, selec_2, how='left', on=['t'])
    selec_3.fillna(0, inplace=True)
    print('03-OK')

    # Calcular columna r
    selec_3.loc[0, 'r'] = r_first
    for i in range(1, len(selec_3)):
        selec_3.loc[i, 'r'] = selec_3.loc[i - 1, 'r'] - selec_3.loc[i - 1, 'd'] - selec_3.loc[i - 1, 'c']

    # reorder dataframe
    selec_3 = selec_3[['t', 'r', 'd', 'c']]
    print('04-OK')

    # Calcular Columna S(t)
    temp_sx = selec_3.iloc[0]

    selec_3.loc[0, 'S(t)'] = (1 - (temp_sx['d'] / temp_sx['r']))
    for j in range(1, len(selec_3)):
        selec_3.loc[j, 'S(t)'] = (selec_3.loc[j - 1, 'S(t)']) * (1 - ((selec_3.loc[j, 'd'] / selec_3.loc[j, 'r'])))
    selec_3.fillna(0, inplace=True)
    print('05-OK')

    # Calcular Lapse rate
    temp_lr = selec_3.iloc[0]
    selec_3.loc[0, 'Lapse_rate'] = (-np.log(temp_lr['S(t)'])) / (temp_lr['t'] + 1)
    for k in range(1, len(selec_3)):
        selec_3.loc[k, 'Lapse_rate'] = np.where(selec_3.loc[k, 'S(t)'] != 0,
                                                -np.log(selec_3.loc[k, 'S(t)']) / (selec_3.loc[k, 't'] + 1),
                                                selec_3.loc[k - 1, 'Lapse_rate'])
    print('06-OK')

    # CALCULO ANTERIOR A MODIFICAR
    # Promedio  Lapse rate
    selec_z = selec_3.copy()
    # selec_z = selec_z[1:]
    lapse_mean = selec_z['Lapse_rate'].mean()

    # Calcular Av.rate
    # selec_3.loc[0, 'Av_rate'] = 0
    for l in range(0, len(selec_3)):
        selec_3.loc[l, 'Av_rate'] = lapse_mean
    print('07-OK')

    # Calcular Columna K-M Estimator S(t)
    temp_st = selec_3.iloc[0]
    selec_3.loc[0, 'S_t_2'] = np.exp(-temp_st['Lapse_rate'] * (temp_st['t'] + 1))
    for m in range(1, len(selec_3)):
        selec_3.loc[m, 'S_t_2'] = np.where(selec_3.loc[m, 'Lapse_rate'] != 0,
                                           np.exp(-selec_3.loc[m, 'Lapse_rate'] * (selec_3.loc[m, 't'] + 1)),
                                           np.exp(-selec_3.loc[m - 1, 'Lapse_rate'] * (selec_3.loc[m, 't'])))
    print('08-OK')

    # *********************************************************************************************************************************************************#

    # Tabla 2
    input_table = selec_3.copy()
    input_table = input_table[['t', 'd', 'c', 'Lapse_rate', 'Av_rate', 'S_t_2']]

    # Calcular Duration (1)
    for n in range(0, len(input_table)):
        input_table.loc[n, 'Duration_1'] = (
                (1 - (np.exp(-input_table.loc[n, 'Lapse_rate'] * input_table.loc[n, 't']))) /
                (1 - (np.exp(-input_table.loc[n, 'Lapse_rate']))))

    # Calcular Duration (2)
    input_table['Duration_2'] = ((input_table['S_t_2'].rolling(min_periods=1, window=(media_ + 1)).sum()) + 1)
    print('09-OK')
    # input_table['FILTER'] = 'INPUT'

    '''
    # Consulta CENSURADOS VIGENTES
    cnxn3 = pyodbc.connect(connection_db)
    sql3 = """SELECT (TO_CHAR(EXTRACT(YEAR FROM FECHA_INICIO_EMITE))) AS ANUAL
           ,COUNT(*) AS CONTEO
           FROM ACTUARIA.CART_VIGENTES_FACTOR 
           WHERE CENSURADO = 1 
           AND PRODUCTO IN {0}
           GROUP BY (TO_CHAR(EXTRACT(YEAR FROM FECHA_INICIO_EMITE))) ORDER BY (TO_CHAR(EXTRACT(YEAR FROM FECHA_INICIO_EMITE)))""".format(
        tuple(lista));
    censu_ = pd.read_sql(sql3, cnxn3);
    cnxn3.close();
    censu_['ANUAL'] = censu_["ANUAL"].astype(int)
    censu_['CONTEO'] = censu_["CONTEO"].astype(int)
    # censu_.to_excel('Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v3/excel_dash/ANUALES.xlsx', sheet_name='ANUALES', index=None)
    censu_.to_csv(
        'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/ANUALES.csv',
        sep=',')

    # input_table.to_excel('Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v1/excel_dash/Input_table.xlsx', sheet_name='Input_table', index = None)
    archivo_reporte = (
        'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/Tables_K-M.xlsx')

    writer = pd.ExcelWriter(archivo_reporte, engine='xlsxwriter')
    selec_3.to_excel(writer, sheet_name='K-M_Estimator', index=None, float_format='%.3f')
    input_table.to_excel(writer, sheet_name='input', index=None)
    '''
    # writer.save()

    '''
    df_tecn_orig.PERIODO = pd.to_datetime(df_tecn_orig.PERIODO, format='%d/%m/%Y')
    df_tecn_orig['PERIODO'] = df_tecn_orig['PERIODO'].astype(str).str[:4] + df_tecn_orig['PERIODO'].astype(str).str[5:7]
    df_tecn_orig['PERIODO'] = df_tecn_orig['PERIODO'].astype(int)
    df_tecn_orig['PRODUCTO_FINANCIERO'] = df_tecn_orig['PRODUCTO_FINANCIERO'].fillna('NA')
    df_tecn_orig['TIPO'] = df_tecn_orig['TIPO'].fillna('NA')
    df_tecn_orig['CANAL'] = df_tecn_orig['CANAL'].fillna('NA')
    '''

    #####################################################################################################################
    '''
    selec_4['PERIODO'] = np.where((selec_4.PERIODO.astype(str).str[-1:]) == '1',
                                  selec_4['PERIODO'].astype(str).str[:4] + 'Q1',

                                  (np.where((selec_4.PERIODO.astype(str).str[-1:]) == '4',
                                            selec_4['PERIODO'].astype(str).str[:4] + 'Q2',

                                            (np.where((selec_4.PERIODO.astype(str).str[-1:]) == '7',
                                                      selec_4['PERIODO'].astype(str).str[:4] + 'Q3',

                                                      selec_4['PERIODO'].astype(str).str[:4] + 'Q4'

                                                      )))))
    '''

    #############################################################################################################################################################

    # Data Table 01
    table_data = input_table.copy()
    vig_actual = table_data['c'].sum()
    data_table_1 = table_data[(table_data['t'].isin([media_]))]
    data_table_1['VIGENTES'] = vig_actual

    decimals = 3
    data_table_1['Av_rate'] = data_table_1['Av_rate'].apply(lambda x: round(x, decimals))
    data_table_1['Lapse_rate'] = data_table_1['Lapse_rate'].apply(lambda x: round(x, decimals))
    data_table_1['Duration_2'] = data_table_1['Duration_2'].apply(lambda x: round(x, decimals))

    data_table_01 = []
    for i, row in data_table_1.iterrows():
        Av_rate = '{:.2%}'.format(row['Av_rate'])
        Lapse_rate = '{:.2%}'.format(row['Lapse_rate'])
        Duration_2 = '{0:,.1f}'.format(row['Duration_2'])

        data_table_01.append({
            "Av_rate": Av_rate,
            "Lapse_rate": Lapse_rate,
            "Duration_2": Duration_2,
            "VIGENTES": str(row['VIGENTES']),
        })
    # print('01', data_table_01)

    #############################################################################################################################################################
    # Data Table 02
    data_table_2 = table_data[(table_data['t'].isin([6, 12, 18, 24, 30, 36, 42, 48, 54, 60]))]

    decimals = 3
    data_table_1['S_t_2'] = data_table_1['S_t_2'].apply(lambda x: round(x, decimals))
    data_table_1['Lapse_rate'] = data_table_1['Lapse_rate'].apply(lambda x: round(x, decimals))

    data_table_02 = []
    for i, row in data_table_2.iterrows():
        t = '{0:,.0f}'.format(row['t'])
        S_t_2 = '{:.2%}'.format(row['S_t_2'])
        Lapse_rate = '{:.2%}'.format(row['Lapse_rate'])

        data_table_02.append({
            "t": t,
            "S_t_2": S_t_2,
            "Lapse_rate": Lapse_rate,
        })
    # print('02', data_table_02)

    #############################################################################################################################################################
    # Data Table 03

    data_table_3 = input_table.copy()
    data_table_3 = data_table_3[['t', 'd', 'c']]
    data_table_3['RANGE'] = np.where(
        ((data_table_3.t < 1)), "<1|0",
        (np.where((data_table_3.t >= 1) & (data_table_3.t <= 3), "[1,3]|1",
                  (np.where((data_table_3.t > 3) & (data_table_3.t <= 6), "(3,6]|2",
                            (np.where((data_table_3.t > 6) & (data_table_3.t <= 12), "(6,12]|3",
                                      (np.where((data_table_3.t > 12) & (data_table_3.t <= 24), "(12,24]|4",
                                                (np.where((data_table_3.t > 24) & (data_table_3.t <= 36), "(24,36]|5",
                                                          ">36|6")))))))))))

    # Agrupar y sumar
    data_table_3 = data_table_3.groupby(['RANGE'])['d', 'c'].sum().reset_index()
    # data_table_3.to_excel('Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/data_table_3.xlsx', sheet_name='data_table_3', index = None)

    sum_d = data_table_3['d'].sum()
    # sum_c = data_table_3['c'].sum()

    data_table_3['TOTAL'] = data_table_3['d'] + data_table_3['c']
    data_table_3['q_x'] = data_table_3['d'] / sum_d

    # Split order
    data_table_3[['RANGE', 'ORDER']] = data_table_3['RANGE'].str.split('|', expand=True)
    data_table_3['ORDER'] = data_table_3['ORDER'].astype(int)

    # Order Dataframe
    data_table_3.sort_values("ORDER", inplace=True)

    # Copy Graph 3
    graph_3 = data_table_3.copy()

    # Calcular row Totales
    data_table_3.loc[len(data_table_3), ['RANGE', 'd', 'c', 'TOTAL', 'q_x']] = ['Total',
                                                                                data_table_3['d'].sum(),
                                                                                data_table_3['c'].sum(),
                                                                                data_table_3['TOTAL'].sum(),
                                                                                data_table_3['q_x'].sum()]
    data_table_3['ORDER'] = data_table_3['ORDER'].fillna(value=7)
    # print('ORDER', data_table_3)
    # source_3.data = {'RANGE': data_table_3.RANGE, 'd': data_table_3.d, 'c' : data_table_3.c, 'TOTAL': data_table_3.TOTAL, 'q_x': data_table_3.q_x, 'ORDER': data_table_3.ORDER}
    # print('data_table_3', data_table_3)

    decimals = 3
    data_table_3['d'] = data_table_3['d'].apply(lambda x: round(x, decimals))
    data_table_3['c'] = data_table_3['c'].apply(lambda x: round(x, decimals))
    data_table_3['TOTAL'] = data_table_3['TOTAL'].apply(lambda x: round(x, decimals))
    data_table_3['q_x'] = data_table_3['q_x'].apply(lambda x: round(x, decimals))

    data_table_03 = []
    for i, row in data_table_3.iterrows():
        d = '{0:,.0f}'.format(row['d'])
        c = '{0:,.0f}'.format(row['c'])
        TOTAL = '{0:,.1f}'.format(row['TOTAL'])
        q_x = '{:.2%}'.format(row['q_x'])

        data_table_03.append({
            "RANGE": str(row['RANGE']),
            "d": d,
            "c": c,
            "TOTAL": TOTAL,
            "q_x": q_x,
            "ORDER": str(row['ORDER']),
        })

    # print('03', data_table_03)
    print('10-Tables-OK')
    # ***************************************************************************************************#
    # Data Graphs 1 y 2
    graphs_a = input_table.copy()
    graphs_a = graphs_a[['t', 'S_t_2', 'Lapse_rate', 'Av_rate']]
    graphs_a = graphs_a.loc[(graphs_a['t'] >= 1) & (graphs_a['t'] <= 60)]

    # Format Graph Amcharts (Multiplica * 100)
    graphs_a['S_t_2'] = graphs_a['S_t_2'] * 100
    graphs_a['Lapse_rate'] = graphs_a['Lapse_rate'] * 100
    graphs_a['Av_rate'] = graphs_a['Av_rate'] * 100

    decimals = 3
    graphs_a['S_t_2'] = graphs_a['S_t_2'].apply(lambda x: round(x, decimals))
    graphs_a['Lapse_rate'] = graphs_a['Lapse_rate'].apply(lambda x: round(x, decimals))
    graphs_a['Av_rate'] = graphs_a['Av_rate'].apply(lambda x: round(x, decimals))

    graphs_1_2 = []
    for i, row in graphs_a.iterrows():
        t = '{0:,.0f}'.format(row['t'])
        # c = '{0:,.0f}'.format(row['c'])
        # TOTAL = '{0:,.1f}'.format(row['TOTAL'])
        # _x = '{:.2%}'.format(row['q_x'])

        graphs_1_2.append({
            "t": t,
            "S_t_2": str(row['S_t_2']),
            "Lapse_rate": str(row['Lapse_rate']),
            "Av_rate": str(row['Av_rate'])
        })

    # print('graphs_1_2', graphs_1_2)

    # ***************************************************************************************************#
    # Data Graph 3

    graph_3 = graph_3[['RANGE', 'q_x']]

    # Format Graph AmCharts (Multiplica *100)
    graph_3['q_x'] = graph_3['q_x'] * 100

    decimals = 3
    graph_3['q_x'] = graph_3['q_x'].apply(lambda x: round(x, decimals))

    graphs_3 = []
    for i, row in graph_3.iterrows():
        graphs_3.append({
            "RANGE": str(row['RANGE']),
            "q_x": str(row['q_x'])
        })

    print('11-OK')

    # ***************************************************************************************************#
    # Data Graph 4

    # Dataframe Vigentes x Generaciones
    graph_4 = pd.read_sql(sql3, cnxn);
    print('12-last-query-OK')

    decimals = 1
    graph_4['CONTEO'] = graph_4['CONTEO'].apply(lambda x: round(x, decimals))
    # graph_4['ANUAL'] = graph_4["ANUAL"].astype(int)
    # graph_4['CONTEO'] = graph_4["CONTEO"].astype(int)

    graphs_4 = []
    for i, row in graph_4.iterrows():
        # CONTEO = '{0:,.0f}'.format(row['CONTEO'])
        graphs_4.append({
            "ANUAL": str(row['ANUAL']),
            "CONTEO": str(row['CONTEO']),
        })

    # UNICOS SELECT
    socios = list(df_unicos['NOM_SOCIO'].unique());
    socios.sort();
    # print('socios', socios)

    # linea = list(df_unicos['LINEA'].unique());
    # linea.sort();

    linea_negocio = list(df_unicos['LINEA_NEGOCIO'].unique())
    # linea_negocio.sort();
    # print('linea_negocio', linea_negocio)

    periodo = list(df_unicos['PERIODO'].unique());
    periodo.sort();
    # print('periodo', periodo)

    canal = list(df_unicos['CANAL'].unique());
    canal.sort();
    # print('canal', canal)

    df_unicos['COD_PROD'] = df_unicos['COD_PROD'].astype(str)
    productos = list(df_unicos['COD_PROD'].unique());
    productos.sort(key=int)
    # print('productos', productos)

    # tipo = list(df_unicos['TIPO'].unique());
    # tipo.sort();

    cnxn.close();

    return JsonResponse(
        [socios, linea_negocio, periodo, canal, productos, data_table_01, data_table_02, data_table_03, graphs_1_2,
         graphs_3, graphs_4], safe=False)
