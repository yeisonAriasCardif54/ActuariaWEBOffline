import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser
import os
from functools import reduce


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
        "title": 'Frecuencia Socios',
        "area": 'ExPost',
        "herramienta": 'frecuencia_qx',
        "file": 'expost/frecuencia_qx.html',
    }
    return render(request, "principal/base.html", configurationView)


def selects(request):
    global cnxn

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
        where2 = where2 + " AND LINEA_NEGOCIO IN " + str(linea_fina_seleccionado)

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

    # Consultar Base de Datos
    sql1 = """ SELECT * FROM ACTUARIA.DASH_FREQ_01 
       """ + where2 + """
       """;

    # Dataframe ejes_df
    ejes_df = pd.read_sql(sql1, cnxn);

    # Filters
    ejes_df = ejes_df[(ejes_df['LINEA_NEGOCIO'].isin(
        ['N/A', 'NA', 'Giros', 'Microcredito', 'SOAT', 'Hipotecario', 'Vehiculos']) == False) &
                      (ejes_df['RISK'].isin(['AD', 'D', 'DD', 'IU', 'TD', 'TH', 'TPD'])) &
                      (ejes_df['SOCIO'].isin(
                          ['BANCO AV VILLAS', 'BANCO POPULAR', 'BANCO DE BOGOTA', 'BANCOLOMBIA', 'EXITO',
                           'BANCO DE OCCIDENTE']))]

    # UNICOS SELECT
    socios = list(ejes_df['SOCIO'].unique());
    socios.sort();

    linea = list(ejes_df['LINEA'].unique());
    linea.sort();

    linea_negocio = list(ejes_df['LINEA_NEGOCIO'].unique())
    linea_negocio.sort();

    risk = list(ejes_df['RISK'].unique());
    risk.sort();

    canal = list(ejes_df['CANAL'].unique());
    canal.sort();

    tipo = list(ejes_df['TIPO'].unique());
    tipo.sort();

    del [ejes_df]

    #############################################################################################################
    ####################################FUNCION ITERAR SOCIOS####################################################
    #############################################################################################################

    def make_dataset(socio_iterar):

        media_ = 1

        # Quarters MOVIMIENTO
        file = 'static/expost/INPUT.xlsx'
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
        quarters_mov = pd.read_excel(file,
                                     sheetname='QUARTERS_MOV')
        quarters_mov.rename(columns={'QUARTER': 'FECHA_OCURRENCIA'}, inplace=True)
        quarters_mov['FECHA_MOVIMIENTO'] = quarters_mov['FECHA_OCURRENCIA']

        # columna socio
        socio = socio_iterar
        socio_seleccionado = [socio_iterar]

        where11 = ' WHERE 1=1 '
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
            where22 = where22 + " AND LINEA_NEGOCIO IN " + str(linea_fina_seleccionado)

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

        where22 = where22 + " AND LINEA_NEGOCIO NOT IN ('N/A','NA','Giros','Microcredito','SOAT','Hipotecario','Vehiculos') AND RISK NOT IN ('ADA', 'AST', 'ATPD', 'ELF', 'EMBD', 'FU', 'GAP', 'H', 'LP', 'TPL') "

        #############################################################################################################

        # Consultar Base de Datos

        # Query FREQ 01 - EJES DF
        sql1 = """ SELECT * FROM ACTUARIA.DASH_FREQ_01 
            """ + where22 + """
            """;

        # Query FREQ 02 - CONTEO IU
        sql2 = """ SELECT * FROM ACTUARIA.DASH_FREQ_02 
            """ + where22 + """
            """;

        # Query FREQ 03 - INCURRIDO IU
        sql3 = """ SELECT * FROM ACTUARIA.DASH_FREQ_03 
            """ + where22 + """
            """;

        # Query Expuestos
        sql4 = """ SELECT * FROM ACTUARIA.DASH_FREQ_04 
            """ + where11 + """
            """;

        # Dataframe ejes_df
        ejes_df = pd.read_sql(sql1, cnxn);

        # Dataframe conteo
        conteo = pd.read_sql(sql2, cnxn);

        # Dataframe incurrido
        incurrido = pd.read_sql(sql3, cnxn);

        # Dataframe expuesto
        expuesto_IU = pd.read_sql(sql4, cnxn);

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

            conteo_end = conteo.drop(['PRODUCTO', 'SOCIO', 'RISK', 'LINEA', 'LINEA_NEGOCIO', 'CANAL', 'TIPO'], axis=1)
            conteo_end = conteo_end.groupby(["FECHA_OCURRENCIA", "FECHA_MOVIMIENTO"]).sum().reset_index()
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

            #####################################################################################################################

            # Data Triangulo Incurrido

            incurrido_pre_1 = incurrido.drop(
                ['PRODUCTO', 'SOCIO', 'RISK', 'LINEA', 'LINEA_NEGOCIO', 'PAGOS', 'RBNS', 'CANAL', 'TIPO'],
                axis=1)
            incurrido_end = incurrido_pre_1.groupby(["FECHA_OCURRENCIA", "FECHA_MOVIMIENTO"]).sum().reset_index()

            incurrido_end['CONTEO'] = incurrido_end['INCURRIDO']
            incurrido_end = incurrido_end.drop(['INCURRIDO'], axis=1)
            incurrido_end['FECHA_OCURRENCIA'] = incurrido_end['FECHA_OCURRENCIA'].astype(np.int64)
            incurrido_end['FECHA_MOVIMIENTO'] = incurrido_end['FECHA_MOVIMIENTO'].astype(np.int64)
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

            expuesto_end = pd.merge(quarters_mov, expuesto_copy, how='outer',
                                    on=['FECHA_OCURRENCIA', 'FECHA_MOVIMIENTO'])

            expuesto_end = expuesto_end.fillna(0);

            unique_exp_IU = pd.DataFrame(expuesto_end.FECHA_MOVIMIENTO.unique())
            unique_exp_IU.columns = ['QUARTER']
            unique_exp_IU = unique_exp_IU

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

            # CREATE DATAFRAME TRIANGULO INCURRIDO
            def tipo_incurr(QUARTER):
                value_unique_incurr = triangulos(QUARTER, incurrido_end)
                list_unique_incurr.append(value_unique_incurr)
                # print("{}_done".format(QUARTER))

            unique_incurrido_IU.apply(lambda row: tipo_incurr(row['QUARTER']), axis=1)
            frame_incu = pd.concat(list_unique_incurr)
            frame_incu['FECHA_MOVIMIENTO'] = frame_incu["FECHA_MOVIMIENTO"].astype(int)
            frame_incu['Q_OCURR'] = frame_incu["Q_OCURR"].astype(int)

            frame_incu = frame_incu[frame_incu.Q_OCURR != 0];

            # CREATE DATAFRAME TRIANGULO EXPUESTO
            def tipo_expuesto(QUARTER):
                value_expuesto = triangulos(QUARTER, expuesto_end)
                list_unique_expuesto.append(value_expuesto)

            unique_exp_IU.apply(lambda row: tipo_expuesto(row['QUARTER']), axis=1)
            frame_expuesto = pd.concat(list_unique_expuesto)

            frame_expuesto['FECHA_MOVIMIENTO'] = frame_expuesto["FECHA_MOVIMIENTO"].astype(int)
            frame_expuesto['Q_OCURR'] = frame_expuesto["Q_OCURR"].astype(
                int)

            frame_expuesto = frame_expuesto[frame_expuesto.Q_OCURR != 0];

            del [conteo_end, incurrido_end]

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
                frame.drop(['FECHA_OCURRENCIA', 'QUARTER_YEAR', 'QUARTER_MONTH', 'Q_OCURR_YEAR', 'Q_OCURR_MONTH'],
                           axis=1,
                           inplace=True)
                frame = frame.loc[frame['LAG'] >= 0]
                return (frame)

            lag_frame_u = lag_calcu(frame_u);
            lag_frame_incu = lag_calcu(frame_incu)
            lag_frame_expuesto = lag_calcu(frame_expuesto)

            #####################################################################################################################

            # PIVOTE DATA FRAMES#
            tria_count = pd.pivot_table(data=lag_frame_u, values='ACUMULADO', index=['Q_OCURR'], columns=['LAG'],
                                        aggfunc=np.sum)

            tria_incurr = pd.pivot_table(data=lag_frame_incu, values='ACUMULADO', index=['Q_OCURR'], columns=['LAG'],
                                         aggfunc=np.sum)

            tria_expue = pd.pivot_table(data=lag_frame_expuesto, values='ACUMULADO', index=['Q_OCURR'], columns=['LAG'],
                                        aggfunc=np.sum)

            #####################################################################################################################

            copy_incu = tria_incurr.copy();
            copy_count = tria_count.copy();
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

            # FREQUENCIAS
            ultim_freq = opera_triangulo(copy_count, copy_expu)
            ultim_freq['FREQUENCY'] = ultim_freq.iloc[:, -1]
            ultim_freq['FREQUENCY'] = np.where(ultim_freq.FREQUENCY >= 0, ultim_freq.FREQUENCY, 0);
            #####################################################################################################################

            # Preparar Data - Tabla Final

            expuesto_df_pre = expuesto_end.copy()
            expuesto_df = expuesto_df_pre.drop(['FECHA_MOVIMIENTO'], axis=1)

            ultim_coste_01 = pd.DataFrame(ultim_coste)
            ultim_coste_01['Q_OCURR2'] = ultim_coste_01.index
            ultim_coste_df = ultim_coste_01[['Q_OCURR2', 'SEVERITY']]
            ultim_coste_df.rename(columns={'Q_OCURR2': 'FECHA_OCURRENCIA'}, inplace=True)
            ultim_coste_df['FECHA_OCURRENCIA'] = ultim_coste_df["FECHA_OCURRENCIA"].astype(int)

            ultim_freq_01 = pd.DataFrame(ultim_freq)
            ultim_freq_01['Q_OCURR2'] = ultim_freq_01.index
            ultim_freq_df = ultim_freq_01[['Q_OCURR2', 'FREQUENCY']]
            ultim_freq_df.rename(columns={'Q_OCURR2': 'FECHA_OCURRENCIA'}, inplace=True)
            ultim_freq_df['FECHA_OCURRENCIA'] = ultim_freq_df["FECHA_OCURRENCIA"].astype(int)

            ejes_df_pre = ejes_df.copy()

            ejes_df_pre_2 = ejes_df_pre.drop(['PRODUCTO', 'RISK', 'SOCIO', 'LINEA', 'LINEA_NEGOCIO'], axis=1)
            ejes_df_table = ejes_df_pre_2.groupby(['FECHA_OCURRENCIA'])['ERP', 'EP'].sum().reset_index()
            ejes_df_table['FECHA_OCURRENCIA'] = ejes_df_table['FECHA_OCURRENCIA'].astype(int)

            table_01 = [ultim_coste_df, ejes_df_table, expuesto_df, ultim_freq_df]

            # if you want to fill the values that don't exist in the lines of merged dataframe simply fill with required strings as
            table_02 = reduce(lambda left, right: pd.merge(left, right, on=['FECHA_OCURRENCIA'], how='left'),
                              table_01).fillna('0')
            table_02.rename(columns={'CONTEO': 'EXPUESTO'}, inplace=True);

            del [table_01, ultim_coste_df, ejes_df_table, expuesto_df, ultim_freq_df]

            # Column Pricing Risk Premium - severity*exposure
            table_02['PRIC_RISK_PREMIUM'] = table_02['ERP'] / table_02['EXPUESTO']
            table_02['PRIC_RISK_PREMIUM'] = np.where(table_02.PRIC_RISK_PREMIUM >= 0, table_02.PRIC_RISK_PREMIUM, 0)

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
            table_02['OCURRENCIA'] = table_02['FECHA_OCURRENCIA'].astype(str).str[:4] + 'Q' + table_02['MONTH2'].astype(
                str)

            final_table = table_02[
                ['ANUAL', 'FECHA_OCURRENCIA', 'OCURRENCIA', 'FEC_DATE', 'EXPUESTO', 'ERP', 'EP', 'INSURED_VALUE',
                 'FREQUENCY', 'SEVERITY', 'RISK_PREMIUM', 'PRIC_RISK_PREMIUM',
                 'ULTIMATE_LOSS', 'LR', 'LR_ACUM', 'PTLR', 'PTLR_ACUM', 'QX', 'QX_ACUM', 'QX_MAX', 'QX_MIN']]

            del [table_02]

            final_table = final_table.fillna(0);

            final_table2 = final_table[['FEC_DATE', 'FECHA_OCURRENCIA', 'OCURRENCIA', 'QX_ACUM']]
            final_table2['SOCIO'] = socio

            # Filter Quarters
            file = 'static/expost/INPUT.xlsx'
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
            quarter_ocurr = pd.read_excel(file,
                                          sheetname='QUARTERS_OCURR')
            quarter_ocurr["QUARTER"] = quarter_ocurr['QUARTER'].astype(str).str[:4] + '-' + quarter_ocurr[
                                                                                                'QUARTER'].astype(
                str).str[-2:] + '-01'
            quarter_ocurr['QUARTER'] = pd.to_datetime(quarter_ocurr['QUARTER'])
            maximo = quarter_ocurr['QUARTER'].max()
            final_table2 = final_table2[(final_table2.FEC_DATE <= maximo)]
        else:
            final_table2 = pd.DataFrame([[0, 0, 0, 0, 0]],
                                        columns=['FEC_DATE', 'FECHA_OCURRENCIA', 'OCURRENCIA', 'QX_ACUM', 'SOCIO'])

        return final_table2

    ########################################################################################################################################

    # Loop Informacion Productos Financieros
    def tipo_prod(socio_seleccionado):

        valor_ = make_dataset(socio_seleccionado)
        df_list.append(valor_)
        print("{}_done".format(socio_seleccionado))

    listas = list(df_iterar['socio_seleccionado'].unique())

    for lista in listas:
        tipo_prod(lista)

    df_consol = pd.concat(df_list, ignore_index=True)

    # Prepare Data
    df_consol = df_consol.loc[df_consol['FECHA_OCURRENCIA'].astype(int) >= 201501]

    #Format Graph AmCharts (Multiplica *100)
    df_consol['QX_ACUM'] = df_consol['QX_ACUM'] * 100

    # round 2 decimals
    decimals = 2
    df_consol['QX_ACUM'] = df_consol['QX_ACUM'].apply(lambda x: round(x, decimals))

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
        df = df[['OCURRENCIA', 'QX_ACUM', 'SOCIO']]
        tria_ = pd.pivot_table(data=df, values='QX_ACUM', index=['OCURRENCIA'], columns=['SOCIO'],
                               aggfunc=np.sum).reset_index()
        return tria_

    def generate_data(df):
        df = df[['OCURRENCIA', 'QX_ACUM', 'SOCIO']]
        tria_ = pd.pivot_table(data=df, values='QX_ACUM', index=['OCURRENCIA'], columns=['SOCIO'],
                               aggfunc=np.sum).reset_index()
        del (tria_['OCURRENCIA'])
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




























