import pandas as pd
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser


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
        "title": 'Persistencia Triang',
        "area": 'ExPost',
        "herramienta": 'persist_triang',
        "file": 'expost/persist_triang.html',
    }
    return render(request, "principal/base.html", configurationView)


def selects(request):
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

    where2 = ' WHERE 1=1 '

    list_2 = []

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
                FROM ACTUARIA.TABLA_PRODUCTOS 
                """ + where2 + """ AND ESTADO != 'NO-DATA'    """;

    # Dataframe Unicos
    df_unicos = pd.read_sql(sql1, cnxn);


    lista = list(df_unicos['COD_PROD'].unique())
    for i in range(len(lista)):
        lista[i] = int(lista[i])
    lista.insert(0, 0)

    # Query CART_VIGENTES_FACTOR
    sql2 = """  SELECT FECHA_INICIO_EMITE AS FECHA_EMISION, FECHA_INICIO AS FECHA_CORTE, SUM(TOTAL_VIGENTES) AS TOTAL_VIGENTES
        FROM ACTUARIA.CART_VIGENTES_TRIANG 
        WHERE PRODUCTO IN {0} 
        AND FECHA_INICIO_EMITE >= 201501       
        GROUP BY FECHA_INICIO_EMITE,FECHA_INICIO""".format(tuple(lista));

    # Dataframe VIGENTES_TRIANG
    frame_ = pd.read_sql(sql2, cnxn);
    print('01-OK', len(df_unicos))

    # sort values
    frame_.sort_values(['FECHA_EMISION', 'FECHA_CORTE'], inplace=True)

    # selected.fillna(0, inplace=True)
    frame_['FECHA_EMISION'] = frame_['FECHA_EMISION'].astype(int)
    frame_['FECHA_CORTE'] = frame_['FECHA_CORTE'].astype(int)
    frame_['TOTAL_VIGENTES'] = frame_['TOTAL_VIGENTES'].astype(int)

    if len(frame_) != 0:

        unique_month = pd.DataFrame(frame_.FECHA_CORTE.unique())
        unique_month.columns = ['MONTH']

        month_join = pd.DataFrame(frame_.FECHA_CORTE.unique())
        month_join.columns = ['FECHA_CORTE']
        month_join['FECHA_EMISION'] = month_join['FECHA_CORTE']

        list_end = []
        frame_2 = pd.DataFrame()

        n = 0
        for i in range(0, len(month_join)):
            list_mer = list(np.arange(n, len(month_join), 1))
            zmonth_join2 = month_join.iloc[list_mer]
            maximo = zmonth_join2['FECHA_CORTE'].min()
            zmonth_join2['FECHA_EMISION'] = maximo
            result = zmonth_join2
            list_end.append(result)
            n += 1
        frame_2 = pd.concat(list_end)

        # Merge Simetria
        frame = pd.merge(frame_2, frame_, how='left', on=['FECHA_EMISION', 'FECHA_CORTE'])
        frame = frame.replace(np.inf, np.nan).fillna(0)
        #frame.to_excel(
        #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/frame-simetria-merge.xlsx',
        #    sheet_name='frame-simetria')

        unique_sime = pd.DataFrame(frame.FECHA_CORTE.unique())
        unique_sime.columns = ['FECHA_CORTE']
        unique_sime = unique_sime[-3:]
        # unique_sime['FECHA_CORTE'] = unique_sime['FECHA_CORTE'].astype(int)

        unique_sime = list(unique_sime['FECHA_CORTE'])

        frame = frame[(frame['FECHA_CORTE'].isin(unique_sime) == False)]

        #frame.to_excel(
        #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/2-frame-simetria-merge.xlsx',
        #    sheet_name='frame-simetria')

        # delete temp dataframe
        del [[frame_, frame_2, month_join]]

        frame['FECHA_CORTE'] = frame['FECHA_CORTE'].astype(str)
        frame['QUARTER_YEAR'] = frame['FECHA_CORTE'].str[:4]
        frame['QUARTER_MONTH'] = frame['FECHA_CORTE'].str[4:]

        frame['FECHA_EMISION'] = frame['FECHA_EMISION'].astype(str)
        frame['Q_OCURR_YEAR'] = frame['FECHA_EMISION'].str[:4]
        frame['Q_OCURR_MONTH'] = frame['FECHA_EMISION'].str[4:6]

        # Calculo LAG = ((dt_two.year - dt_one.year)*12 + (dt_two.month - dt_one.month))/3.0
        frame['LAG'] = ((frame['QUARTER_YEAR'].astype(int) - frame['Q_OCURR_YEAR'].astype(int)) * 12 + (
                    frame['QUARTER_MONTH'].astype(int) - frame['Q_OCURR_MONTH'].astype(int)))  # / 3

        # PIVOTE DATA FRAMES
        tria_frame = pd.pivot_table(data=frame, values='TOTAL_VIGENTES', index=['FECHA_EMISION'], columns=['LAG'],
                                    aggfunc=np.sum)  # ;print(tria_count)
        #tria_frame.to_excel(
        #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/1-tria_frame.xlsx',
        #    sheet_name='tria_frame')

        #######################################################################################################################################################################################
        ################################################################################## Triangulo Polizas ##################################################################################
        #######################################################################################################################################################################################

        copy_frame = tria_frame.copy()

        def triangulo_factors(tria_a):

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
                print('dFactors:', dFactors)
                list_2.append(dFactors)
                dAntiDiag = mClaimTri[:, ::-1].diagonal()[1:]
                for index in range(dAntiDiag.size):
                    mClaimTri[index + 1, np.negative(index + 1):] = dAntiDiag[index] * dFactors[np.negative(
                        index + 1):].cumprod()
                return mClaimTri

            dff_2 = tria_a.values
            factor_ = GetChainSquare(dff_2)
            factor2_a = pd.DataFrame(factor_)
            factor2 = factor2_a.replace(np.inf, np.nan).fillna(0)

            return (factor2)

        # call function triangle
        ultim_polizas = triangulo_factors(copy_frame)
        ultim_polizas = pd.DataFrame(ultim_polizas)
        ultim_polizas = pd.concat([unique_month, ultim_polizas], axis=1)

        # concatenar lista & get last 3 factors
        frame_2 = pd.DataFrame(np.concatenate(list_2))
        frame_2.columns = ['FACTORS']
        frame_2 = frame_2[-3:].reset_index()
        frame_2 = frame_2.drop(['index'], axis=1)

        # Minimo 3 factores para Calcular

        if len(frame_2) == 3:

            # Calcular 60 factores
            factors_60 = frame_2.copy()
            for i in range(3, 63):
                factors_60.loc[i, 'FACTORS'] = np.minimum((((factors_60.loc[i - 1, 'FACTORS'] + factors_60.loc[
                    i - 2, 'FACTORS'] + factors_60.loc[i - 3, 'FACTORS']) / 3) + (
                                                               (factors_60.loc[i - 3:i - 1, 'FACTORS']).std(
                                                                   axis=0)) * 0.5), 1)
            # print('frame_3::', frame_3)
            #factors_60.to_excel(
            #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/factors_60.xlsx',
            #    sheet_name='factors_60')

            # separate last 60 factors
            factors_60 = factors_60[-60:].reset_index()
            factors_60 = factors_60.drop(['index'], axis=1)

            ############################# Proyectar a 60 meses ############################################################################

            months = range(1, 61)
            # name last column
            ultim_polizas['ep0'] = ultim_polizas.iloc[:, -1]
            j = 0
            for month in months:
                colname = 'ep%d' % month
                prev_colname = 'ep%d' % (month - 1)
                ultim_polizas[colname] = ultim_polizas[prev_colname] * factors_60.loc[j, 'FACTORS']
                j += 1

            ultim_polizas.drop('ep0', axis=1, inplace=True)
            #ultim_polizas.to_excel(
            #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/2-ultim_polizas.xlsx',
            #    sheet_name='ultim_polizas')

            # delete temp dataframe
            del [[frame, frame_2, tria_frame, unique_month, factors_60, copy_frame]]

            ################################################################################## End Triangulo Polizas ##############################################################################
            # %%

            #######################################################################################################################################################################################
            ################################################################################## Triangulo Porcentajes ##############################################################################
            #######################################################################################################################################################################################

            porcen_all = ultim_polizas.copy()

            # Rename Columns
            cols = porcen_all.columns.tolist()
            porcen_all.columns = cols[:1] + ['ep%i' % i for i in range(0, len(cols[2:]) + 1)]
            ultim_porc = porcen_all[['MONTH', 'ep0']]

            # limit of columns range
            number_cols = ultim_polizas.shape[1] - 1

            months = range(1, number_cols)
            k = 1
            for month in months:
                colname = 'ep%d' % month  # ;print('colname::',colname)
                prev_colname = 'ep%d' % (month - k)  # ;print('prev_colname::',prev_colname)
                ultim_porc[colname] = porcen_all[colname] / porcen_all[prev_colname]
                k += 1

            ultim_porc = ultim_porc.replace(np.inf, np.nan).fillna(0)
            #ultim_porc.to_excel(
            #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/3-ultim_porc.xlsx',
            #    sheet_name='ultim_porc')

            # delete temp dataframe
            del [[porcen_all]]

            #######################################################################################################################################################################################
            ################################################################################# % Persistencia mes a mes por año de venta############################################################
            #######################################################################################################################################################################################

            ultim_v_pre = pd.DataFrame((ultim_porc['MONTH'].astype(str).str[:4]).unique())
            ultim_v_pre.columns = ['MONTH']

            # limit of columns range
            number_cols2 = ultim_porc.shape[1] - 1

            months = range(1, number_cols2)
            k = 1

            for month in months:
                colname = 'ep%d' % month  # ;print('colname::',colname)
                prev_colname = 'ep%d' % (month - k)  # ;print('prev_colname::',prev_colname)
                colname2 = 'ep%d' % month  # ;print('colname2::',colname2)

                def my_func2(row2):
                    # Suma-Producto / Suma
                    d = ((row2[prev_colname] * row2[colname]).sum()) / np.maximum(((row2[prev_colname]).sum()),
                                                                                  0.00000000001)  # ;print('d:', d)
                    return pd.Series({colname2: d})

                result = ultim_porc.groupby((ultim_porc['MONTH'].astype(str).str[:4])).apply(my_func2).reset_index()
                ultim_persis = pd.merge(ultim_v_pre, result, how='left', on=['MONTH'])
                ultim_v_pre = ultim_persis
                k += 1

            ####################################################################################################
            # Calculate Column ep0
            def my_func0(row_0):
                colname = 'ep0'
                d = (row_0[colname].sum()) / np.maximum((row_0[colname].sum()), 0.00000000001)
                return pd.Series({colname: d})

            result_0 = ultim_porc.groupby((ultim_porc['MONTH'].astype(str).str[:4])).apply(my_func0).reset_index()
            ultim_persis = pd.merge(ultim_persis, result_0, how='left', on=['MONTH'])
            # Move position ep0
            ep0 = ultim_persis['ep0']
            ultim_persis.drop(labels=['ep0'], axis=1, inplace=True)
            ultim_persis.insert(1, 'ep0', ep0)
            ####################################################################################################

            ultim_persis.rename(columns={'MONTH': 'ANUAL'}, inplace=True)

            # mean column ep0
            mean_ep0 = ultim_persis['ep0'].mean()

            # Calcular Totals Persistencia mes a mes por año de venta
            ultim_persis.loc[len(ultim_persis)] = [
                ((ultim_porc['ep0'] * ultim_porc[col]).sum()) / ((ultim_porc['ep0']).sum()) for col in
                ultim_porc.columns]

            # Change values Total and ep0
            ultim_persis.at[ultim_persis.index[-1], ['ANUAL', 'ep0']] = ['Total', mean_ep0]

            #ultim_persis.to_excel(
            #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/4-ultim_persis.xlsx',
            #    sheet_name='ultim_persis')

            del [[ultim_polizas, ultim_v_pre, result]]

            #######################################################################################################################################################################################
            ################################################################################# Tasa de Caida Mensual############################################################
            #######################################################################################################################################################################################

            ultim_tasa = pd.DataFrame(ultim_persis['ANUAL'])

            # limit of columns range
            number_cols3 = ultim_persis.shape[1] - 1

            months = range(0, number_cols3)

            k = 1

            for month in months:
                colname = 'ep%d' % month  # ;print('columns:',colname)
                prev_colname = k - 1
                ultim_tasa[colname] = (-np.log(ultim_persis[colname]) / prev_colname)
                k += 1

            ultim_tasa = ultim_tasa.replace(np.inf, np.nan).fillna(0)
            #ultim_tasa.to_excel(
            #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/5-ultim_tasa.xlsx',
            #    sheet_name='ultim_tasa')

            del [[ultim_porc]]

            #######################################################################################################################################################################################
            ################################################################################# % Persistencia meses trimestrales por año de venta ############################################################
            #######################################################################################################################################################################################

            list_C = list(np.arange(1, len(ultim_persis), 1))
            list_C.insert(0, 0)

            list_Q = list(np.arange(1, 46, 3))
            list_Q.insert(0, 0)

            # Quarters
            ultim_persis_Q = ultim_persis.iloc[list_C, list_Q]

            ultim_persis_Q['Duration'] = ultim_persis.iloc[:, 1:62].sum(axis=1)

            # ultim_persis_Q['Duration']   = ultim_persis_Q['Duration'] / 100

            ultim_persis_Q['Lapse_rate'] = ultim_tasa.iloc[:, 2:62].mean(axis=1)

            #ultim_persis_Q.to_excel(
            #    'Q:/Transversal/Scripts-Outputs-IT/Bokeh_Projects/Dash_Persistencia/bokeh_app_v4/excel_dash/6-ultim_persis_Q.xlsx',
            #    sheet_name='ultim_persis_Q')

            resultado = ultim_persis_Q

            del [[ultim_tasa, ultim_persis]]


        else:
            resultado = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                     columns=['ANUAL', 'ep0', 'ep3', 'ep6', 'ep9', 'ep12', 'ep15', 'ep18', 'ep21',
                                              'ep24', 'ep27', 'ep30', 'ep33', 'ep36', 'ep39', 'ep42', 'Duration',
                                              'Lapse_rate'])


    else:
        resultado = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                 columns=['ANUAL', 'ep0', 'ep3', 'ep6', 'ep9', 'ep12', 'ep15', 'ep18', 'ep21', 'ep24',
                                          'ep27', 'ep30', 'ep33', 'ep36', 'ep39', 'ep42', 'Duration', 'Lapse_rate'])
    print('02-OK')
    #resultado.to_excel('C:/Users/b89591/Desktop/test01.xlsx', sheet_name='test01')

    #############################################################################################################################################################

    # Data Tables
    data_table_1 = resultado.copy()

    decimals = 4
    data_table_1['ep0'] = data_table_1['ep0'].apply(lambda x: round(x, decimals))
    data_table_1['ep3'] = data_table_1['ep3'].apply(lambda x: round(x, decimals))
    data_table_1['ep6'] = data_table_1['ep6'].apply(lambda x: round(x, decimals))
    data_table_1['ep9'] = data_table_1['ep9'].apply(lambda x: round(x, decimals))
    data_table_1['ep12'] = data_table_1['ep12'].apply(lambda x: round(x, decimals))
    data_table_1['ep15'] = data_table_1['ep15'].apply(lambda x: round(x, decimals))
    data_table_1['ep18'] = data_table_1['ep18'].apply(lambda x: round(x, decimals))
    data_table_1['ep21'] = data_table_1['ep21'].apply(lambda x: round(x, decimals))
    data_table_1['ep24'] = data_table_1['ep24'].apply(lambda x: round(x, decimals))
    data_table_1['ep27'] = data_table_1['ep27'].apply(lambda x: round(x, decimals))
    data_table_1['ep30'] = data_table_1['ep30'].apply(lambda x: round(x, decimals))
    data_table_1['ep33'] = data_table_1['ep33'].apply(lambda x: round(x, decimals))
    data_table_1['ep36'] = data_table_1['ep36'].apply(lambda x: round(x, decimals))
    data_table_1['Duration'] = data_table_1['Duration'].apply(lambda x: round(x, decimals))
    data_table_1['Lapse_rate'] = data_table_1['Lapse_rate'].apply(lambda x: round(x, decimals))

    data_table_01 = []
    for i, row in data_table_1.iterrows():
        ep0  = '{:.2%}'.format(row['ep0'])
        ep3  = '{:.2%}'.format(row['ep3'])
        ep6  = '{:.2%}'.format(row['ep6'])
        ep9  = '{:.2%}'.format(row['ep9'])
        ep12 = '{:.2%}'.format(row['ep12'])
        ep15 = '{:.2%}'.format(row['ep15'])
        ep18 = '{:.2%}'.format(row['ep18'])
        ep21 = '{:.2%}'.format(row['ep21'])
        ep24 = '{:.2%}'.format(row['ep24'])
        ep27 = '{:.2%}'.format(row['ep27'])
        ep30 = '{:.2%}'.format(row['ep30'])
        ep33 = '{:.2%}'.format(row['ep33'])
        ep36 = '{:.2%}'.format(row['ep36'])
        Lapse_rate = '{:.2%}'.format(row['Lapse_rate'])
        Duration = '{0:,.2f}'.format(row['Duration'])

        data_table_01.append({
            "ANUAL": str(row['ANUAL']),
            "ep0": ep0,
            "ep3": ep3,
            "ep6": ep6,
            "ep9": ep9,
            "ep12": ep12,
            "ep15": ep15,
            "ep18": ep18,
            "ep21": ep21,
            "ep24": ep24,
            "ep27": ep27,
            "ep30": ep30,
            "ep33": ep33,
            "ep36": ep36,
            "Duration": Duration,
            "Lapse_rate": Lapse_rate
        })

    # ***************************************************************************************************#
    # Data Graph 1
    graph_1 = resultado.copy()

    # traspuesta
    graph_1 = graph_1.set_index('ANUAL').T.reset_index()
    graph_1 = graph_1.drop(['index'], axis=1)

    if '2015' not in graph_1:
        graph_1['2015'] = 0

    if '2016' not in graph_1:
        graph_1['2016'] = 0

    if '2017' not in graph_1:
        graph_1['2017'] = 0

    if '2018' not in graph_1:
        graph_1['2018'] = 0

    graph_1['MONTH'] = graph_1.index
    graph_1['MONTH'] = graph_1['MONTH'] * 3
    # reorder
    graph_1 = graph_1[['MONTH', '2015', '2016', '2017', '2018', 'Total']]
    #print('data_trans01:', data_trans)
    graph_1.columns = graph_1.columns.astype(str).str.replace(r"[2]", "_2")
    # data_trans.rename(columns={'2015':'_2015', '2016':'_2016', '2017':'_2017', '2018':'_2018' }, inplace=True)
    list_C = list(np.arange(0, (len(graph_1) - 2), 1))
    list_Q = list(np.arange(0, (len(graph_1.columns))))
    # Quarters
    graph_1 = graph_1.iloc[list_C, list_Q]
    #graph_1.to_excel('C:/Users/b89591/Desktop/data_trans.xlsx', sheet_name='data_trans', index = None)

    # Format Graph AmCharts (Multiplica *100)
    graph_1['_2015'] = graph_1['_2015'] * 100
    graph_1['_2016'] = graph_1['_2016'] * 100
    graph_1['_2017'] = graph_1['_2017'] * 100
    graph_1['_2018'] = graph_1['_2018'] * 100
    graph_1['Total'] = graph_1['Total'] * 100

    #decimals = 3
    #graph_3['q_x'] = graph_3['q_x'].apply(lambda x: round(x, decimals))

    graphs_1 = []
    for i, row in graph_1.iterrows():
        MONTH = '{0:,.0f}'.format(row['MONTH'])
        graphs_1.append({
            "MONTH": MONTH,
            "2015": str(row['_2015']),
            "2016": str(row['_2016']),
            "2017": str(row['_2017']),
            "2018": str(row['_2018']),
            "Total": str(row['Total'])
        })

    ################################################################################################
    # Data Graph 2
    graph_2 = resultado.copy()
    graph_2 = graph_2[['ANUAL', 'Duration', 'Lapse_rate']]
    # data_rate = data_rate[1:(len(data_rate)-1)]
    graph_2 = graph_2[:-2]

    #Remove last column
    #graph_2 = graph_2.iloc[:, :-1]
    #graph_2['ANUAL'] = graph_2['ANUAL'].astype(int)
    #graph_2['ANUAL_STR'] = graph_2['ANUAL'].astype(str)

    # Format Graph AmCharts (Multiplica *100)
    graph_2['Lapse_rate'] = graph_2['Lapse_rate'] * 100

    # decimals = 3
    # graph_3['q_x'] = graph_3['q_x'].apply(lambda x: round(x, decimals))

    graphs_2 = []
    for i, row in graph_2.iterrows():
        Duration = '{0:,.1f}'.format(row['Duration'])
        graphs_2.append({
            "ANUAL": str(row['ANUAL']),
            "Duration": Duration,
            "Lapse_rate": str(row['Lapse_rate']),
        })

    #print(graphs_2)


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

    # tipo = list(df_unicos['TIPO'].unique());
    # tipo.sort();

    cnxn.close();

    return JsonResponse(
        [socios, linea_negocio, periodo, canal, productos, data_table_01, graphs_1,graphs_2 ], safe=False)
         #data_table_02, data_table_03, graphs_1_2,
         #graphs_3, graphs_4], safe=False)
