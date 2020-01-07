import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser
from functools import reduce
from natsort import natsorted
from pandas.tseries import offsets
import os
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
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'title': 'Frecuencia General',
        'area': 'ExPost',
        'herramienta': 'frecuencia',
        'file': 'expost/frecuencia.html',
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

    # Quarters MOVIMIENTO
    file = 'static/expost/INPUT.xlsx'
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
    quarters_mov = pd.read_excel(path, sheetname='QUARTERS_MOV')
    quarters_mov.rename(columns={'QUARTER': 'FECHA_OCURRENCIA'}, inplace=True)
    quarters_mov['FECHA_MOVIMIENTO'] = quarters_mov['FECHA_OCURRENCIA']
    quarters_mov['FECHA_MOVIMIENTO'] = quarters_mov['FECHA_MOVIMIENTO'].astype(np.int64)
    quarters_mov['FECHA_OCURRENCIA'] = quarters_mov['FECHA_OCURRENCIA'].astype(np.int64)

    tria_count_l = []
    tria_incu_l  = []
    tria_expu_l = []
    tria_count_df = pd.DataFrame()
    tria_incu_df = pd.DataFrame()
    tria_expu_df = pd.DataFrame()


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

    whereb = ' WHERE 1=1 '
    wherea = ' WHERE 1=1 '

    if len(socio_seleccionado) > 0:
        a = tuple(socio_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        socio_seleccionado = tuple(l)
        whereb = whereb + " AND SOCIO IN " + str(socio_seleccionado)

    if len(linea_seleccionado) > 0:
        a = tuple(linea_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        linea_seleccionado = tuple(l)
        whereb = whereb + " AND LINEA IN " + str(linea_seleccionado)

    if len(linea_fina_seleccionado) > 0:
        a = tuple(linea_fina_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        linea_fina_seleccionado = tuple(l)
        whereb = whereb + " AND LINEA_NEGOCIO IN " + str(linea_fina_seleccionado)

    if len(risk_seleccionado) > 0:
        a = tuple(risk_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        risk_seleccionado = tuple(l)
        whereb = whereb + " AND RISK IN " + str(risk_seleccionado)

    if len(canal_seleccionado) > 0:
        a = tuple(canal_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        canal_seleccionado = tuple(l)
        whereb = whereb + " AND CANAL IN " + str(canal_seleccionado)

    if len(producto_seleccionado) > 0:
        a = tuple(producto_seleccionado);
        b = 0
        l = list(a);
        l.append(b)
        producto_seleccionado = tuple(l)
        whereb = whereb + " AND PRODUCTO IN " + str(producto_seleccionado)
        wherea = wherea + " AND PRODUCTO IN " + str(producto_seleccionado)

    if len(tipo_seleccionado) > 0:
        a = tuple(tipo_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        tipo_seleccionado = tuple(l)
        whereb = whereb + " AND TIPO IN " + str(tipo_seleccionado)

    #############################################################################################################

    # Consultar Base de Datos

    # Query FREQ 01 - EJES DF
    sql1 = """ SELECT * FROM DASH_FREQ_01 
    """ + whereb + """
    """;

    # Query FREQ 02 - CONTEO IU
    sql2 = """ SELECT * FROM DASH_FREQ_02 
    """ + whereb + """
    """;

    # Query FREQ 03 - INCURRIDO IU
    sql3 = """ SELECT * FROM DASH_FREQ_03 
    """ + whereb + """
    """;

    # Query Expuestos
    sql4 = """ SELECT * FROM DASH_FREQ_04 
    """ + wherea + """
    """;

    # Dataframe ejes_df
    ejes_df = pd.read_sql(sql1, cnxn);

    # Dataframe conteo
    conteo = pd.read_sql(sql2, cnxn);

    # Dataframe incurrido
    incurrido = pd.read_sql(sql3, cnxn);

    # Dataframe expuesto
    expuesto_IU = pd.read_sql(sql4, cnxn);

    cnxn.close();
    # print('A')

    if ((len(conteo) != 0) & (len(incurrido) != 0)):

        #####################################################################################################################

        # Function Simetría

        def simetria(df_simet):

            month_join = pd.DataFrame(df_simet.FECHA_MOVIMIENTO.unique());
            month_join.columns = ['FECHA_MOVIMIENTO']
            month_join['FECHA_OCURRENCIA'] = month_join['FECHA_MOVIMIENTO']

            # sort values
            month_join.sort_values(['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO'], inplace=True)

            list_end = [];
            frame_2 = pd.DataFrame()

            n = 0
            for i in range(0, len(month_join)):
                list_mer = list(np.arange(n, len(month_join), 1))
                zmonth_join2 = month_join.iloc[list_mer]
                maximo = zmonth_join2['FECHA_MOVIMIENTO'].min()
                zmonth_join2['FECHA_OCURRENCIA'] = maximo
                result = zmonth_join2
                list_end.append(result)
                n += 1
            frame_2 = pd.concat(list_end)

            # Merge Simetria
            df_end = pd.merge(frame_2, df_simet, how='left', on=['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO'])
            df_end = df_end.replace(np.inf, np.nan).fillna(0)
            return df_end

        #####################################################################################################################

        # Data Triangulo Conteo

        conteo_pre_1 = conteo.drop(['PRODUCTO', 'SOCIO', 'RISK', 'LINEA', 'LINEA_NEGOCIO', 'CANAL', 'TIPO'], axis=1)
        conteo_end = conteo_pre_1.groupby(["FECHA_OCURRENCIA", "FECHA_MOVIMIENTO"]).sum().reset_index()
        conteo_end['FECHA_OCURRENCIA'] = conteo_end['FECHA_OCURRENCIA'].astype(np.int64)
        conteo_end['FECHA_MOVIMIENTO'] = conteo_end['FECHA_MOVIMIENTO'].astype(np.int64)

        conteo_end = pd.merge(quarters_mov, conteo_end, how='outer',
                              on=['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO']).fillna(0)

        # sort values
        conteo_end.sort_values(['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO'], inplace=True)
        conteo_end['FECHA_OCURRENCIA'] = conteo_end['FECHA_OCURRENCIA'].astype(int)
        conteo_end['FECHA_MOVIMIENTO'] = conteo_end['FECHA_MOVIMIENTO'].astype(int)

        conteo_end = simetria(conteo_end);

        unique_conteo_IU = pd.DataFrame(conteo_end.FECHA_MOVIMIENTO.unique())
        unique_conteo_IU.columns = ['QUARTER']
        unique_conteo_IU = unique_conteo_IU
        quarters_q = unique_conteo_IU.copy()
        quarters_q.rename(columns={'QUARTER': 'FECHA_MOVIMIENTO'}, inplace=True)
        # print('B')
        #####################################################################################################################

        # Data Triangulo Incurrido

        incurrido_pre_1 = incurrido.drop(
            ['PRODUCTO', 'SOCIO', 'RISK', 'LINEA', 'LINEA_NEGOCIO', 'PAGOS', 'RBNS', 'CANAL', 'TIPO'],
            axis=1)
        incurrido_end = incurrido_pre_1.groupby(["FECHA_OCURRENCIA", "FECHA_MOVIMIENTO"]).sum().reset_index()

        incurrido_end['CONTEO'] = incurrido_end['INCURRIDO']
        incurrido_end = incurrido_end.drop(['INCURRIDO'], axis=1)
        incurrido_end['FECHA_OCURRENCIA'] = incurrido_end['FECHA_OCURRENCIA'].astype(int)
        incurrido_end['FECHA_MOVIMIENTO'] = incurrido_end['FECHA_MOVIMIENTO'].astype(int)

        incurrido_end = pd.merge(quarters_mov, incurrido_end, how='outer',
                                 on=['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO']).fillna(0)

        # sort values
        incurrido_end.sort_values(['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO'], inplace=True)
        incurrido_end['FECHA_OCURRENCIA'] = incurrido_end['FECHA_OCURRENCIA'].astype(int)
        incurrido_end['FECHA_MOVIMIENTO'] = incurrido_end['FECHA_MOVIMIENTO'].astype(int)

        incurrido_end = simetria(incurrido_end);

        unique_incurrido_IU = pd.DataFrame(incurrido_end.FECHA_MOVIMIENTO.unique())
        unique_incurrido_IU.columns = ['QUARTER']
        unique_incurrido_IU = unique_incurrido_IU
        # print('C')

        #####################################################################################################################
        # Data Triangulo Expuesto

        expuesto_copy_a = expuesto_IU.copy();
        selected_exp = ejes_df.copy()

        expuesto_copy_a['PRODUCTO'] = expuesto_copy_a["PRODUCTO"].astype(int)
        expuesto_copy_a['FECHA_OCURRENCIA'] = expuesto_copy_a["FECHA_OCURRENCIA"].astype(int)

        selected_exp = selected_exp.drop(['RISK', 'SOCIO', 'ERP', 'EP', 'LINEA', 'LINEA_NEGOCIO', 'CANAL', 'TIPO'],
                                         axis=1).fillna(0)
        selected_exp = selected_exp.drop_duplicates(['PRODUCTO', 'FECHA_OCURRENCIA'])
        selected_exp['PRODUCTO'] = selected_exp["PRODUCTO"].astype(int)
        selected_exp['FECHA_OCURRENCIA'] = selected_exp["FECHA_OCURRENCIA"].astype(int)

        # Merge expuestos - selected
        expuesto_copy = pd.merge(selected_exp, expuesto_copy_a, how='left',
                                 on=['FECHA_OCURRENCIA', 'PRODUCTO']).dropna()
        expuesto_copy = expuesto_copy.drop(['PRODUCTO'], axis=1)
        expuesto_copy = expuesto_copy.groupby(["FECHA_OCURRENCIA", "FECHA_MOVIMIENTO"]).sum().reset_index()

        expuesto_end = pd.merge(quarters_mov, expuesto_copy, how='outer', on=['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO'])
        expuesto_end = expuesto_end.fillna(0);

        unique_exp_IU = pd.DataFrame(expuesto_end.FECHA_MOVIMIENTO.unique())
        unique_exp_IU.columns = ['QUARTER']
        unique_exp_IU = unique_exp_IU
        # print('D')

        #####################################################################################################################
        # Función Triángulos

        # listas and dataframes
        list_unique_count = [];
        list_unique_incurr = [];
        list_unique_expuesto = []
        frame_u = pd.DataFrame();
        frame_incu = pd.DataFrame();
        frame_expuesto = pd.DataFrame()

        def triangulos(QUARTER, data_IU):

            # Filtro INPUT
            matrix_conteo = data_IU[(data_IU.FECHA_OCURRENCIA == QUARTER)]
            matrix_conteo = matrix_conteo[['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO', 'CONTEO']]

            # Merge 2 Dataframes
            df_uniq = pd.merge(quarters_q, matrix_conteo, how='left', on='FECHA_MOVIMIENTO').fillna(0)

            # Max Q_Ocurr
            df_uniq['Q_OCURR'] = df_uniq['FECHA_OCURRENCIA'].max()

            # Calcular Columna ACUMULADO
            df_uniq['ACUMULADO'] = df_uniq['CONTEO'].cumsum()

            return (df_uniq)

        # CREATE DATAFRAME TRIANGULO CONTEO
        def tipo_unique(QUARTER):
            value_unique_cont = triangulos(QUARTER, conteo_end)
            list_unique_count.append(value_unique_cont)

        unique_conteo_IU.apply(lambda row: tipo_unique(row['QUARTER']), axis=1)

        frame_u = pd.concat(list_unique_count)
        frame_u['FECHA_MOVIMIENTO'] = frame_u["FECHA_MOVIMIENTO"].astype(int)
        frame_u['Q_OCURR'] = frame_u["Q_OCURR"].astype(int)

        frame_u = frame_u[frame_u.Q_OCURR != 0];

        # print('E')

        # CREATE DATAFRAME TRIANGULO INCURRIDO
        def tipo_incurr(QUARTER):
            value_unique_incurr = triangulos(QUARTER, incurrido_end)
            list_unique_incurr.append(value_unique_incurr)

        unique_incurrido_IU.apply(lambda row: tipo_incurr(row['QUARTER']), axis=1)
        frame_incu = pd.concat(list_unique_incurr)
        frame_incu['FECHA_MOVIMIENTO'] = frame_incu["FECHA_MOVIMIENTO"].astype(int)
        frame_incu['Q_OCURR'] = frame_incu["Q_OCURR"].astype(int)

        frame_incu = frame_incu[frame_incu.Q_OCURR != 0];

        # print('F')

        # CREATE DATAFRAME TRIANGULO EXPUESTO
        def tipo_expuesto(QUARTER):
            value_expuesto = triangulos(QUARTER, expuesto_end)
            list_unique_expuesto.append(value_expuesto)

        unique_exp_IU.apply(lambda row: tipo_expuesto(row['QUARTER']), axis=1)
        frame_expuesto = pd.concat(list_unique_expuesto)

        frame_expuesto['FECHA_MOVIMIENTO'] = frame_expuesto["FECHA_MOVIMIENTO"].astype(int)
        frame_expuesto['Q_OCURR'] = frame_expuesto["Q_OCURR"].astype(int)

        frame_expuesto = frame_expuesto[frame_expuesto.Q_OCURR != 0];

        # print('G')

        #####################################################################################################################

        # Función Cálculo Lag
        def lag_calcu(frame):

            frame['FECHA_MOVIMIENTO'] = frame['FECHA_MOVIMIENTO'].astype(str)
            frame['QUARTER_YEAR'] = frame['FECHA_MOVIMIENTO'].str[:4]
            frame['QUARTER_MONTH'] = frame['FECHA_MOVIMIENTO'].str[4:]

            frame['Q_OCURR'] = frame['Q_OCURR'].astype(str)
            frame['Q_OCURR_YEAR'] = frame['Q_OCURR'].str[:4]
            frame['Q_OCURR_MONTH'] = frame['Q_OCURR'].str[4:6]

            # Calculo LAG = ((dt_two.year - dt_one.year)*12 + (dt_two.month - dt_one.month))/3.0
            frame['LAG'] = ((frame['QUARTER_YEAR'].astype(int) - frame['Q_OCURR_YEAR'].astype(int)) * 12 + (
                    frame['QUARTER_MONTH'].astype(int) - frame['Q_OCURR_MONTH'].astype(int))) / 3
            frame.drop(['FECHA_OCURRENCIA', 'QUARTER_YEAR', 'QUARTER_MONTH', 'Q_OCURR_YEAR', 'Q_OCURR_MONTH'], axis=1,
                       inplace=True)
            frame = frame.loc[frame['LAG'] >= 0]
            return (frame)

        lag_frame_u = lag_calcu(frame_u)
        lag_frame_incu = lag_calcu(frame_incu)
        lag_frame_expuesto = lag_calcu(frame_expuesto)
        # print('H')

        #####################################################################################################################

        # PIVOTE DATA FRAMES#
        tria_count = pd.pivot_table(data=lag_frame_u, values='ACUMULADO', index=['Q_OCURR'], columns=['LAG'],
                                    aggfunc=np.sum)

        '''tria_count.to_excel(
            'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/tria_count.xlsx',
            sheet_name='tria_count')
        '''
        tria_incurr = pd.pivot_table(data=lag_frame_incu, values='ACUMULADO', index=['Q_OCURR'], columns=['LAG'],
                                     aggfunc=np.sum)
        '''tria_incurr.to_excel(
            'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/tria_incurr.xlsx',
            sheet_name='tria_incurr')
        '''
        tria_expue = pd.pivot_table(data=lag_frame_expuesto, values='ACUMULADO', index=['Q_OCURR'], columns=['LAG'],
                                    aggfunc=np.sum)
        '''tria_expue.to_excel(
            'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/tria_expue.xlsx',
            sheet_name='tria_expue')
        '''
        # print('I')

        #####################################################################################################################
        copy_count = tria_count.copy();
        copy_incu = tria_incurr.copy();
        copy_expu = tria_expue.copy()

        def opera_triangulo(tria_a, tria_b):

            def isnumpy(item):
                return 'numpy' in str(type(item))

            def Lapply(_list, fun, **kwargs):
                iSize = _list.__len__()
                out = list()
                for index in range(0, iSize):
                    out.append(fun(_list[index], **kwargs))
                if isnumpy(_list):
                    out = np.array(out)
                return out

            def GetFactor(index, mTri):
                colSum = mTri[:np.negative(index + 1), index:(index + 2)].sum(0)
                colSum2 = colSum[1] / colSum[0]
                col_mean = np.nan_to_num(colSum2)
                if (col_mean == 0):
                    col_mean = col_mean + 1
                else:
                    col_mean
                return col_mean

            def GetChainSquare(mClaimTri):
                iSize = mClaimTri.shape[1]
                dFactors = Lapply(np.arange(iSize - 1), GetFactor, mTri=mClaimTri)
                dAntiDiag = mClaimTri[:, ::-1].diagonal()[1:]
                for index in range(dAntiDiag.size):
                    mClaimTri[index + 1, np.negative(index + 1):] = dAntiDiag[index] * dFactors[np.negative(
                        index + 1):].cumprod()
                return mClaimTri

            dff_ = tria_a / tria_b
            dff_1 = dff_.replace(np.inf, np.nan).fillna(0)
            dff_2 = dff_1.values
            factor_ = GetChainSquare(dff_2)
            factor2_a = pd.DataFrame(factor_)
            factor2 = factor2_a.replace(np.inf, np.nan).fillna(0)

            factor2 = pd.concat([quarters_q, factor2], axis=1)
            factor2.rename(columns={'FECHA_MOVIMIENTO': 'Q_OCURR'}, inplace=True)
            factor2.set_index('Q_OCURR', inplace=True)

            return (factor2)

        if copy_incu.empty:
            print('DataFrame Incurrido vacío')

        if copy_count.empty:
            print('DataFrame Conteo vacío')

        if copy_expu.empty:
            print('DataFrame Expuestos vacío')

        # COSTE MEDIO
        ultim_coste = opera_triangulo(copy_incu, copy_count)
        ultim_coste['SEVERITY'] = ultim_coste.iloc[:, -1]
        ultim_coste['SEVERITY'] = np.where(ultim_coste.SEVERITY >= 0, ultim_coste.SEVERITY, 0);
        '''ultim_coste.to_excel(
            'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/ultim_coste.xlsx',
            sheet_name='ultim_coste')
        '''
        # print('J')

        # FREQUENCIAS
        ultim_freq = opera_triangulo(copy_count, copy_expu)
        ultim_freq['FREQUENCY'] = ultim_freq.iloc[:, -1]
        ultim_freq['FREQUENCY'] = np.where(ultim_freq.FREQUENCY >= 0, ultim_freq.FREQUENCY, 0);
        '''ultim_freq.to_excel(
            'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/ultim_freq.xlsx',
            sheet_name='ultim_freq')
        '''

        # print('K')
        # *****************************************************************************************************************************#
        # *********************************************** BLOQUE GENERAR CONTEO COMPLETO **********************************************#
        # *****************************************************************************************************************************#

        count_fill = tria_count.copy()
        expu_fill = tria_expue.copy()

        freq_fill = ultim_freq.copy()
        freq_fill = freq_fill.drop(['FREQUENCY'], axis=1)

        CountTri = count_fill.values
        ExpuTri = expu_fill.values
        FreqTri = freq_fill.values

        CountDiag = CountTri[:, ::-1].diagonal()[1:]
        ExpuDiag = ExpuTri[:, ::-1].diagonal()[1:]

        for index in range(CountDiag.size):
            # code works
            CountTri[index + 1, np.negative(index + 1):] = ExpuDiag[index] * FreqTri[index + 1, np.negative(index + 1):]

        CountTri_end = pd.DataFrame(CountTri)

        '''CountTri_end.to_excel(
            'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/tria_count_completo.xlsx',
            sheet_name='tria_count_completo')
        '''
        # print('L')

        # *****************************************************************************************************************************#
        # ******************************************************END CONTEO COMPLETO****************************************************#
        # *****************************************************************************************************************************#

        # Preparar Data - Tabla Final

        expuesto_df_pre = expuesto_end.copy()
        expuesto_df = expuesto_df_pre.drop(['FECHA_MOVIMIENTO'], axis=1)

        ultim_coste_01 = pd.DataFrame(ultim_coste)
        ultim_coste_01['Q_OCURR2'] = ultim_coste_01.index
        ultim_coste_df = ultim_coste_01[['Q_OCURR2', 'SEVERITY']]
        ultim_coste_df.rename(columns={'Q_OCURR2': 'FECHA_OCURRENCIA'}, inplace=True)
        ultim_coste_df['FECHA_OCURRENCIA'] = ultim_coste_df["FECHA_OCURRENCIA"].astype(int)
        # print('M')

        ultim_freq_01 = pd.DataFrame(ultim_freq)
        ultim_freq_01['Q_OCURR2'] = ultim_freq_01.index
        ultim_freq_df = ultim_freq_01[['Q_OCURR2', 'FREQUENCY']]
        ultim_freq_df.rename(columns={'Q_OCURR2': 'FECHA_OCURRENCIA'}, inplace=True)
        ultim_freq_df['FECHA_OCURRENCIA'] = ultim_freq_df["FECHA_OCURRENCIA"].astype(int)
        # print('N')

        ejes_df_pre = ejes_df.copy()

        ejes_df_pre_2 = ejes_df_pre.drop(['PRODUCTO', 'RISK', 'SOCIO', 'LINEA', 'LINEA_NEGOCIO'], axis=1)
        ejes_df_table = ejes_df_pre_2.groupby(['FECHA_OCURRENCIA'])['ERP', 'EP'].sum().reset_index()
        ejes_df_table['FECHA_OCURRENCIA'] = ejes_df_table['FECHA_OCURRENCIA'].astype(int)

        table_01 = [ultim_coste_df, ejes_df_table, expuesto_df, ultim_freq_df]

        # if you want to fill the values that don't exist in the lines of merged dataframe simply fill with required strings as
        table_02 = reduce(lambda left, right: pd.merge(left, right, on=['FECHA_OCURRENCIA'], how='left'),
                          table_01).fillna('0')
        table_02.rename(columns={'CONTEO': 'EXPUESTO'}, inplace=True);

        # print('O')

        # Column Pricing Risk Premium - severity*exposure
        table_02['PRIC_RISK_PREMIUM'] = table_02['ERP'] / table_02['EXPUESTO']
        table_02['PRIC_RISK_PREMIUM'] = np.where(table_02.PRIC_RISK_PREMIUM >= 0, table_02.PRIC_RISK_PREMIUM, 0)
        # print('P')

        # Column Insured Value - severity*exposure
        table_02['INSURED_VALUE'] = table_02['SEVERITY'] * table_02['EXPUESTO']
        table_02['INSURED_VALUE'] = np.where(table_02.INSURED_VALUE >= 0, table_02.INSURED_VALUE, 0)

        # Column Risk Premium - frequency*severity
        table_02['RISK_PREMIUM'] = table_02['FREQUENCY'] * table_02['SEVERITY']
        table_02['RISK_PREMIUM'] = np.where(table_02.RISK_PREMIUM >= 0, table_02.RISK_PREMIUM, 0)

        # Column Ultimate Loss - RISK_PREMIUM*exposure
        table_02['ULTIMATE_LOSS'] = table_02['RISK_PREMIUM'] * table_02['EXPUESTO']
        table_02['ULTIMATE_LOSS'] = np.where(table_02.ULTIMATE_LOSS >= 0, table_02.ULTIMATE_LOSS, 0)

        # Column LR - ULTIMATE_LOSS/EP
        table_02['LR'] = table_02['ULTIMATE_LOSS'] / table_02['EP']
        table_02['LR'] = np.where(table_02.LR >= 0, table_02.LR, 0)
        # print('Q')

        # Column LR_ACUM
        table_02['LR_ACUM'] = (table_02['ULTIMATE_LOSS'].rolling(min_periods=1, window=media_).sum()) / (
            table_02['EP'].rolling(min_periods=1, window=media_).sum())
        table_02['LR_ACUM'] = np.where(table_02.LR_ACUM >= 0, table_02.LR_ACUM, 0)

        # Column PTLR - ULTIMATE_LOSS/ERP
        table_02['PTLR'] = table_02['ULTIMATE_LOSS'] / table_02['ERP']

        # Column PTLR_ACUM
        table_02['PTLR_ACUM'] = (table_02['ULTIMATE_LOSS'].rolling(min_periods=1, window=media_).sum()) / (
            table_02['ERP'].rolling(min_periods=1, window=media_).sum())
        table_02['PTLR_ACUM'] = np.where(table_02.PTLR_ACUM >= 0, table_02.PTLR_ACUM, 0)

        # Column qx
        table_02['QX'] = table_02['ULTIMATE_LOSS'] / table_02['INSURED_VALUE']

        # Column qx_ACUM
        table_02['QX_ACUM'] = (table_02['ULTIMATE_LOSS'].rolling(min_periods=1, window=media_).sum()) / (
            table_02['INSURED_VALUE'].rolling(min_periods=1, window=media_).sum())
        table_02['QX_ACUM'] = np.where(table_02.QX_ACUM >= 0, table_02.QX_ACUM, 0)

        # Fill NA - INF
        table_02 = table_02.replace(np.inf, np.nan).fillna(0)

        Min_Max = table_02.loc[(table_02['FECHA_OCURRENCIA'] >= 201601)]
        Max_qx = Min_Max['QX_ACUM'].max()
        Min_qx = Min_Max['QX_ACUM'].min()

        table_02['QX_MAX'] = Max_qx
        table_02['QX_MIN'] = Min_qx

        table_02['ANUAL'] = table_02['FECHA_OCURRENCIA'].astype(str).str[:4]
        table_02['MONTH'] = table_02['FECHA_OCURRENCIA'].astype(str).str[-2:]
        table_02["FEC_DATE"] = table_02["ANUAL"] + '-' + table_02["MONTH"] + '-01'
        table_02['FEC_DATE'] = pd.to_datetime(table_02['FEC_DATE'])

        table_02['MONTH2'] = ((table_02['MONTH'].astype(int) / 3).round() + 1).astype(int)
        table_02['OCURRENCIA'] = table_02['FECHA_OCURRENCIA'].astype(str).str[:4] + 'Q' + table_02['MONTH2'].astype(str)

        final_table = table_02[
            ['ANUAL', 'FECHA_OCURRENCIA', 'OCURRENCIA', 'FEC_DATE', 'EXPUESTO', 'ERP', 'EP', 'INSURED_VALUE',
             'FREQUENCY', 'SEVERITY', 'RISK_PREMIUM', 'PRIC_RISK_PREMIUM',
             'ULTIMATE_LOSS', 'LR', 'LR_ACUM', 'PTLR', 'PTLR_ACUM', 'QX', 'QX_ACUM', 'QX_MAX', 'QX_MIN']]

        final_table['FILTER'] = 'QUARTERS'
        final_table = final_table.fillna(0);

        # *********Acumulados Anuales************

        df_tot = final_table[['ANUAL', 'FECHA_OCURRENCIA', 'OCURRENCIA', 'FEC_DATE', 'ULTIMATE_LOSS', 'INSURED_VALUE']]

        media_anual = 4  # Quarters

        df_tot['EXPUESTO'] = 0
        df_tot['ERP'] = 0
        df_tot['EP'] = 0

        df_tot['INSURED_VALUE2'] = df_tot.groupby('ANUAL')['INSURED_VALUE'].apply(
            lambda x: x.rolling(center=False, window=media_anual).sum())
        df_tot['FREQUENCY'] = 0.0
        df_tot['SEVERITY'] = 0
        df_tot['RISK_PREMIUM'] = 0
        df_tot['PRIC_RISK_PREMIUM'] = 0

        df_tot['ULTIMATE_LOSS2'] = df_tot.groupby('ANUAL')['ULTIMATE_LOSS'].apply(
            lambda x: x.rolling(center=False, window=media_anual).sum())
        df_tot['LR'] = 0.0
        df_tot['LR_ACUM'] = 0.0
        df_tot['PTLR'] = 0.0
        df_tot['PTLR_ACUM'] = 0.0
        df_tot['QX'] = 0.0

        # qx ANUAL
        df_tot['QX_ACUM'] = df_tot['ULTIMATE_LOSS2'] / df_tot['INSURED_VALUE2']
        df_tot['QX_MAX'] = 0.0
        df_tot['QX_MIN'] = 0.0

        df_tot = df_tot.drop(['ULTIMATE_LOSS', 'INSURED_VALUE'], axis=1)
        df_tot['INSURED_VALUE2'] = 0
        df_tot['ULTIMATE_LOSS2'] = 0

        max_row = df_tot.loc[df_tot.reset_index().groupby(['ANUAL'])['FECHA_OCURRENCIA'].idxmax()]
        max_row = max_row.sort_index()
        max_row = max_row.reset_index(drop=True)
        max_row['FILTER'] = 'ANUALES'
        max_row = max_row.fillna(0)

        # Concatenar Data Final Gráficos
        df_tot_last = final_table[
            ['ANUAL', 'FECHA_OCURRENCIA', 'OCURRENCIA', 'FEC_DATE', 'EXPUESTO', 'ERP', 'EP', 'INSURED_VALUE',
             'FREQUENCY', 'SEVERITY', 'RISK_PREMIUM', 'PRIC_RISK_PREMIUM',
             'ULTIMATE_LOSS', 'LR', 'LR_ACUM', 'PTLR', 'PTLR_ACUM', 'QX', 'QX_ACUM', 'QX_MAX', 'QX_MIN', 'FILTER']]
        new_cols = {x: y for x, y in zip(max_row.columns, df_tot_last.columns)}
        final_table2 = df_tot_last.append(max_row.rename(columns=new_cols))
    else:
        file = 'static/expost/template.xlsx'
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
        final_table2 = pd.read_excel(path, sheetname='template')
        final_table2['ANUAL'] = final_table2['ANUAL'].astype(str)

    '''final_table2.to_excel(
        'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Frecuenciav2/bokeh_app_asegur/excel_dash/final_table2.xlsx',
        sheet_name='final_table2')
    '''
    #############################################################################################################################################################
    # Data Table
    data_table_1 = final_table2[((final_table2.FILTER == 'QUARTERS') & (final_table2.ANUAL >= '2015'))]
    data_table_1 = data_table_1[
        ['ANUAL', 'OCURRENCIA', 'FEC_DATE', 'EXPUESTO', 'EP', 'SEVERITY', 'RISK_PREMIUM', 'PRIC_RISK_PREMIUM',
         'ULTIMATE_LOSS', 'LR_ACUM', 'QX_ACUM']]

    # round 2 decimals
    decimals = 2
    data_table_1['EXPUESTO'] = data_table_1['EXPUESTO'].apply(lambda x: round(x, decimals))
    data_table_1['EP'] = data_table_1['EP'].apply(lambda x: round(x, decimals))
    data_table_1['SEVERITY'] = data_table_1['SEVERITY'].apply(lambda x: round(x, decimals))
    data_table_1['RISK_PREMIUM'] = data_table_1['RISK_PREMIUM'].apply(lambda x: round(x, decimals))
    data_table_1['PRIC_RISK_PREMIUM'] = data_table_1['PRIC_RISK_PREMIUM'].apply(lambda x: round(x, decimals))
    data_table_1['ULTIMATE_LOSS'] = data_table_1['ULTIMATE_LOSS'].apply(lambda x: round(x, decimals))

    # delimitar Data
    data_table_1 = data_table_1[:len(data_table_1) - 1]

    data_table = []
    for i, row in data_table_1.iterrows():
        EXPUESTO = '{0:,.2f}'.format(row['EXPUESTO'])
        LR_ACUM = '{:.2%}'.format(row['LR_ACUM'])
        QX_ACUM = '{:.3%}'.format(row['QX_ACUM'])
        data_table.append({
            "ANUAL": str(row['ANUAL']),
            "OCURRENCIA": str(row['OCURRENCIA']),
            "FEC_DATE": row['FEC_DATE'],
            "EXPUESTO": row['EXPUESTO'],
            "EP": row['EP'],
            "SEVERITY": row['SEVERITY'],
            "RISK_PREMIUM": row['RISK_PREMIUM'],
            "PRIC_RISK_PREM": row['PRIC_RISK_PREMIUM'],
            "ULTIMATE LOSS": row['ULTIMATE_LOSS'],
            "LR_ACUM": LR_ACUM,
            "QX_ACUM": QX_ACUM
        })

    #############################################################################################################################################################
    # Data Graph 1
    '''
    data_graph_1 = final_table2[(final_table2.FILTER == 'ANUALES')]
    data_graph_1 = data_graph_1.loc[data_graph_1['ANUAL'].astype(int) >= 2014]
    data_graph_1 = data_graph_1[['ANUAL', 'FEC_DATE', 'QX_ACUM']]
    # Sum a month
    data_graph_1['FEC_DATE'] = data_graph_1['FEC_DATE'] + pd.DateOffset(months=1)
    # Beggining of the Year
    data_graph_1['FEC_DATE'] = data_graph_1.apply(lambda x: x['FEC_DATE'] - offsets.YearBegin(), axis=1)
    data_graph_1['ANUAL'] = data_graph_1['ANUAL'].astype(str)

    data_graph_a = []
    for i, row in data_graph_1.iterrows():
        # QX_ACUM  = '{:.3%}'.format(row['QX_ACUM'])
        data_graph_a.append({
            "ANUAL": str(row['ANUAL']),
            "QX_ACUM": row['QX_ACUM'],

        })
    '''
    #############################################################################################################################################################
    # Data Graph 2 y 3

    data_graph_3 = final_table2[((final_table2.FILTER == 'QUARTERS') & (final_table2.ANUAL >= '2015'))]
    data_graph_3 = data_graph_3[['OCURRENCIA', 'FEC_DATE', 'SEVERITY', 'EXPUESTO', 'LR_ACUM', 'QX_ACUM']]

    # Formato Graph AmCharts (Multiplica * 100)
    data_graph_3['QX_ACUM'] = data_graph_3['QX_ACUM'] * 100
    data_graph_3['LR_ACUM'] = data_graph_3['LR_ACUM'] * 100

    # round 2 decimals
    decimals = 2
    data_graph_3['SEVERITY'] = data_graph_3['SEVERITY'].apply(lambda x: round(x, decimals))
    data_graph_3['EXPUESTO'] = data_graph_3['EXPUESTO'].apply(lambda x: round(x, decimals))

    # delimitar Data
    data_graph_3 = data_graph_3[:len(data_graph_3) - 1]

    data_graph_c = []
    for i, row in data_graph_3.iterrows():
        # QX_ACUM  = '{:.3%}'.format(row['QX_ACUM'])
        # PROFIT_MARGIN_LABEL = '{:.2f}'.format(row['QX_ACUM']) + ' %'
        data_graph_c.append({
            "OCURRENCIA": row['OCURRENCIA'],
            "FEC_DATE": row['FEC_DATE'],
            "SEVERITY": row['SEVERITY'],
            "EXPUESTO": row['EXPUESTO'],
            "LR_ACUM": row['LR_ACUM'],
            "QX_ACUM": row['QX_ACUM'],

        })

    # UNICOS SELECT
    socios = list(ejes_df['SOCIO'].unique());
    socios.sort();

    linea = list(ejes_df['LINEA'].unique());
    linea.sort();

    linea_negocio = list(ejes_df['LINEA_NEGOCIO'].unique());
    linea_negocio.sort();

    risk = list(ejes_df['RISK'].unique());
    risk.sort();

    canal = list(ejes_df['CANAL'].unique());
    canal.sort();

    productos = list(ejes_df['PRODUCTO'].unique());
    productos.sort(key=int)

    tipo = list(ejes_df['TIPO'].unique());
    tipo.sort();


    # Export Triángulo Conteo
    copy_count = copy_count.reset_index() ;     copy_count = copy_count.replace(np.inf, np.nan).fillna(0)
    tria_count_l.append(copy_count) ;    tria_count_df = pd.concat(tria_count_l)
    #tria_count_df = tria_count_df.to_dict('records')
    tria_count_df = tria_count_df.to_html(classes='table table-sm table-responsive table_count', border=0 ,float_format='%10.2f')

    # Export Triángulo Incurrido
    copy_incu = copy_incu.reset_index();     copy_incu = copy_incu.replace(np.inf, np.nan).fillna(0)
    tria_incu_l.append(copy_incu);     tria_incu_df = pd.concat(tria_incu_l)
    tria_incu_df = tria_incu_df.to_html(classes='table table-sm table-responsive table_incu', border=0, float_format='%10.2f')

    # Export Triángulo Expuesto
    copy_expu = copy_expu.reset_index();     copy_expu = copy_expu.replace(np.inf, np.nan).fillna(0)
    tria_expu_l.append(copy_expu);     tria_expu_df = pd.concat(tria_expu_l)
    tria_expu_df = tria_expu_df.to_html(classes='table table-sm table-responsive table_expu', border=0,float_format='%10.2f')

    #{0:, .2f}

    return JsonResponse(
        [socios, linea, linea_negocio, risk, canal, productos, tipo, data_table, data_graph_c, tria_count_df, tria_incu_df, tria_expu_df],
        safe=False)



