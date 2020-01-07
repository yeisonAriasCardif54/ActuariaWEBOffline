import re
import time
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None
import os

''' *****Librerías del proyecto***** '''
# Librerías generales
from profitability.views_.obtener_presupuesto.libraries.general.obtener_output_inicial import obtener_output_inicial
from profitability.views_.obtener_presupuesto.libraries.general.obtener_archivo_reporte import obtener_archivo_reporte
from profitability.views_.obtener_presupuesto.libraries.base_de_datos.obtener_datos_estaticos_DB import obtener_datos_estaticos_DB
# Librerías para calcular columnas
from profitability.views_.obtener_presupuesto.libraries.obtener_nuevos import obtener_nuevos
from profitability.views_.obtener_presupuesto.libraries.obtener_tasa_caida import obtener_tasa
from profitability.views_.obtener_presupuesto.libraries.obtener_vigentes_cancelaciones import obtener_vigentes_y_cancelaciones
from profitability.views_.obtener_presupuesto.libraries.obtener_siniestros import obtener_siniestros
from profitability.views_.obtener_presupuesto.libraries.obtener_vlrprima_c_d import obtener_vlrprima_c_d
from profitability.views_.obtener_presupuesto.libraries.obtener_primas_emitidas import obtener_primas_emitidas
# from libraries.obtener_primas_emitidas_v2 import obtener_primas_emitidas_v2
from profitability.views_.obtener_presupuesto.libraries.obtener_comisiones import obtener_comisiones
from profitability.views_.obtener_presupuesto.libraries.obtener_incurred_claims import obtener_incurred_claims
from profitability.views_.obtener_presupuesto.libraries.calcular_ingresos_financieros import calcular_ingresos_financieros
from profitability.views_.obtener_presupuesto.libraries.calcular_incentivos_y_costos_TMK import calcular_incentivos_y_costos_TMK
from profitability.views_.obtener_presupuesto.libraries.obtener_variables_agrupamiento_PU import obtener_variables_agrupamiento_PU
from profitability.views_.obtener_presupuesto.libraries.obtener_PU import obtener_PU
from profitability.views_.obtener_presupuesto.libraries.obtener_resultado_tecnico import obtener_resultado_tecnico
from profitability.views_.obtener_presupuesto.libraries.obtener_utilidad_preliminar import obtener_utilidad_preliminar
from profitability.views_.obtener_presupuesto.libraries.distribuir_PU import distribuir_PU
from profitability.views_.obtener_presupuesto.libraries.obtener_variables_calculadas_por_acumulados import obtener_variables_calculadas_por_acumulados
from profitability.views_.obtener_presupuesto.libraries.obtener_variables_ajustes_pgv import obtener_variables_ajustes_pgv


def get_data(file, parametrosNvUnificados=[], desembolsosNvUnificados=[]):
    start_time_GLOBAL = time.time()
    start_time = time.time()

    ''' *********************************************************** Extraer inputs *********************************************************** '''
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../' + file)
    xlsx_inputs = pd.ExcelFile(path)

    ''' Inputs - Configuración '''
    configuracion = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='Consola', skiprows=3))
    configuracion = configuracion.fillna(0)
    configuracion1 = configuracion.filter(['Unnamed: 1', 'Unnamed: 2'])
    configuracion1.rename(columns={'Unnamed: 1': 'Variable', 'Unnamed: 2': 'Valor'}, inplace=True)
    configuracion1.set_index(['Variable'], inplace=True)
    configuracion2 = configuracion.loc[0:2].filter(['Unnamed: 4', 'Unnamed: 6'])
    configuracion2.rename(columns={'Unnamed: 4': 'Variable', 'Unnamed: 6': 'Valor'}, inplace=True)
    configuracion2.set_index(['Variable'], inplace=True)
    configuracion3 = configuracion.loc[5:10].filter(['Unnamed: 4', 'Unnamed: 5'])
    configuracion3.rename(columns={'Unnamed: 4': 'Variable', 'Unnamed: 5': 'Valor'}, inplace=True)
    configuracion3.set_index(['Variable'], inplace=True)
    configuracion = pd.concat([configuracion1, configuracion2, configuracion3])

    ''' Inputs - Productos Stock '''
    parametros_st = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='ParametrosSt'))
    parametros_st = parametros_st.fillna(0)
    desembolsos_st = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='DesembolsosSt'))
    desembolsos_st = desembolsos_st.fillna(0)
    desembolsos_st_TEMP = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='DesembolsosSt'))

    ''' Inputs - Productos Nuevos '''
    # Validar si los parametros y desembolsos llegan unificados
    if len(parametrosNvUnificados) > 0 and len(desembolsosNvUnificados) > 0:
        parametros_nv = parametrosNvUnificados
        desembolsos_nv = desembolsosNvUnificados
    else:
        parametros_nv = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='ParametrosNv'))
        parametros_nv = parametros_nv.dropna(subset=['Id_Tool'])  # Eliminar registros cuyo Id_Tool sea nulo
        desembolsos_nv = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='DesembolsosNv'))
        desembolsos_nv = desembolsos_nv.dropna(subset=['Id_Tool'])  # Eliminar registros cuyo Id_Tool sea nulo
        desembolsos_nv = desembolsos_nv.fillna(0)

    ''' Inputs - RRC '''
    rrc = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='RRC'))
    rrc = rrc.fillna(0)
    ''' Extraer información - RRC '''
    uprStock = rrc.filter(regex=r'^Id_Tool$|RRC|^Mes [0-9]{1,3}$', axis=1)
    uprStock.rename(columns={'RRC': 'Mes 0'}, inplace=True)
    uprStock.columns = [re.sub('^Mes', 'uprStockRRC_Mes', c) for c in uprStock.columns]
    dacStock = rrc.filter(regex=r'^Id_Tool$|DAC_Proy|^Mes [0-9]{1,3}\.1$', axis=1)
    dacStock.rename(columns={'DAC_Proy': 'Mes 0.1'}, inplace=True)
    dacStock.columns = [re.sub('^Mes (\d+).1$', r'dacStockRRC_Mes \1', c) for c in dacStock.columns]
    vigentesStock = rrc.filter(regex=r'^Id_Tool$|Vigentes|^Mes [0-9]{1,3}\.2$', axis=1)
    vigentesStock.rename(columns={'Vigentes': 'Mes 0.2'}, inplace=True)
    vigentesStock.columns = [re.sub('^Mes (\d+).2$', r'vigentesStockRRC_Mes \1', c) for c in vigentesStock.columns]

    ''' ********************************** Extraer datos estáticos ********************************** '''
    data_fromDB = obtener_datos_estaticos_DB()
    data_socios = data_fromDB['socios']
    data_ofertas = data_fromDB['ofertas']
    data_t_primas = data_fromDB['tipos_prima']
    data_grupos_pu = data_fromDB['grupos_pu']

    data_grupos_pu['Id_Grupo'] = data_grupos_pu['Id_Grupo'].astype(np.int64)
    """
    data_grupos_pu['CapitalCost'] = data_grupos_pu['CapitalCost'].str.replace(',','.').astype(np.float32)
    data_grupos_pu['Share_PU'] = data_grupos_pu['Share_PU'].str.replace(',','.').astype(np.float32)
    data_grupos_pu['Paid/Liberación'] = data_grupos_pu['Paid/Liberación'].str.replace(',','.').astype(np.float32)
    data_grupos_pu['Claims Result to Share'] = data_grupos_pu['Claims Result to Share'].str.replace(',','.').astype(np.float32)
    data_grupos_pu['% Overhead_Grupal'] = data_grupos_pu['% Overhead_Grupal'].str.replace(',','.').astype(np.float32)
    data_grupos_pu = data_grupos_pu.fillna(0)
    """
    print('\n\n\n - data_grupos_pu - \n\n\n')
    print(data_grupos_pu.to_string())
    print(data_grupos_pu.info())
    ''' *************************************************** Lectura de parámetros generales *************************************************** '''
    try:
        finanp = configuracion[configuracion.index == 'Finan. Income (Anual)'].Valor.item()  # Tasa de costo de oportunidad
        meses = configuracion[configuracion.index == 'Meses a proyectar'].Valor.item()  # Meses a proyectar
        mesiniciost = configuracion[configuracion.index == 'Mes Inicia Stock:'].Valor.item()  #
        mesinicio = configuracion[configuracion.index == 'Imprimir desde mes:'].Valor.item()  # Mes de arranque de proyección
        mesesimprime = 601  # Meses maximo a imprimir. Se espera que sean 121 (10 años+mes cero)
        mesanual = configuracion[configuracion.index == 'Mes del año proyección'].Valor.item()  # Meses transcurridos desde enero del año de la proyección
        ipc = configuracion[configuracion.index == '% Incremento  IPC'].Valor.item()  # Ipc del año
        caidaren = configuracion[configuracion.index == 'Caida en Renovación'].Valor.item()  # Caida general de las renovaciones
        msipc = configuracion[configuracion.index == 'Meses Stcok Mensual'].Valor.item()  # Supuesto de meses que tienen en promedio los clientes del stock mensual
        piva = configuracion[configuracion.index == '% De IVA Vigente'].Valor.item()  # '% de IVA
        pica = configuracion[configuracion.index == '% ICA'].Valor.item()  # % de ICA
        pgmf = configuracion[configuracion.index == 'GMF'].Valor.item()  # % de ICA
        taxr = configuracion[configuracion.index == 'Income Tax Rate'].Valor.item()  # Tasa de impuesto
        tipincent = configuracion[configuracion.index == '      Cálculo RT con Incentivos'].Valor.item()  # Tipo de pago de incentivos
        mesunoproyeccion = configuracion[configuracion.index == 'Mes Uno Proyección'].Valor.item()  # Mes Uno Proyección
        imprimirBaseReal = configuracion[configuracion.index == 'Imprimir Base Real'].Valor.item()  # Imprimir Base Real
        try:
            MesesVectorAjusteSKB = configuracion[configuracion.index == 'Meses Vector ajuste SKB'].Valor.item()  # Imprimir Base Real
        except:
            MesesVectorAjusteSKB = 0
        vector = pd.DataFrame(data={  # Vector del manejo de RRC
            'Mes': [1, 2, 3, 4, 5],
            'Vector Control RRC': [
                0.75, 0.80, 0.80, 0.85, 0.9
            ]
        })
        """
        'Vector Control RRC': [
                configuracion[configuracion.index == 1].Valor.item(),
                configuracion[configuracion.index == 2].Valor.item(),
                configuracion[configuracion.index == 3].Valor.item(),
                configuracion[configuracion.index == 4].Valor.item(),
                configuracion[configuracion.index == 5].Valor.item()
            ]
        """
    except:
        finanp, meses, mesiniciost, mesinicio, mesesimprime, mesanual, ipc, caidaren, msipc, piva, pica, pgmf, taxr, tipincent, mesunoproyeccion, vector = 0
        print("Error al extraer los valores de configuración, por favor cerciórese que los títulos no hayan sido alterados y los valores se encuentren diligenciados correctamente.")
        exit(0)
    ''' *************************************************** Lectura de parámetros generales para PGV *************************************************** '''
    try:
        dataExtraPGV = 1
        tasadesemen = configuracion[configuracion.index == 'Discount Rate (Monthly Rate)'].Valor.item()  # Tasa de Descuento Mensual
        tasadeseanu = configuracion[configuracion.index == 'Discount Rate (yearthly Rate)'].Valor.item()  # Tasa de Descuento EA
        ctmktc = configuracion[configuracion.index == 'Caida TMK Tarjetas'].Valor.item()  # Caida TMK Tarjetas
        ctmkac = configuracion[configuracion.index == 'Caida TMK Cuentas'].Valor.item()  # Caida TMK Cuentas
    except:
        dataExtraPGV = 0
        tasadesemen = 0  # Tasa de Descuento Mensual
        tasadeseanu = 0  # Tasa de Descuento EA
        ctmktc = 0  # Caida TMK Tarjetas
        ctmkac = 0  # Caida TMK Cuentas

    ''' *************************************************** Lectura de parametros de la data *************************************************** '''
    sproduct = len(parametros_st[pd.notnull(parametros_st['Id_Tool'])])  # Determinar no. productos stoc
    nproduct = len(parametros_nv[pd.notnull(parametros_nv['Id_Tool'])])  # Determinar no. productos nuevos
    totalproduct = sproduct + nproduct  # Totaliza el número de productos de stock y nuevos
    nparametros = len(parametros_st.columns) - 9  # Numero de parametros
    ngrupos = len(data_grupos_pu)  # Numero de grupos
    nstocks = len(rrc[pd.notnull(rrc['Id_Tool'])])  # Numero de productos que tendrán stocks de RRC
    nsocios = len(data_socios)  # Numero de socios
    nofertas = len(data_ofertas)  # Numero de ofertas
    ntipos = len(data_t_primas)  # Numero de tipos
    ngrupos = len(data_grupos_pu)  # Numero de grupos de PU

    print('\n\n Total tiempo lectura: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Generar DataFrame con output y elementos iniciales: '''
    OutPut = obtener_output_inicial(parametros_st, parametros_nv, mesunoproyeccion, meses, data_socios, data_ofertas, data_t_primas)
    print('\n\n Total obtener_output_inicial: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener los nuevos '''
    OutPut = obtener_nuevos(OutPut, meses, parametros_st, parametros_nv, desembolsos_st, desembolsos_nv, mesanual, mesiniciost, caidaren, ctmkac, ctmktc)
    print('\n\n Total obtener_nuevos: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener tasa de caída '''
    OutPut, OutPut_tasa = obtener_tasa(OutPut, meses, mesiniciost, desembolsos_st_TEMP, vigentesStock, vector)
    print('\n\n Total obtener_tasa: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener vigentes y cancelaciones '''
    OutPut, OutPut_tasa_caida_cancel, vector = obtener_vigentes_y_cancelaciones(OutPut, OutPut_tasa, meses, caidaren, mesiniciost, vigentesStock, vector)
    print('\n\n Total obtener_vigentes_y_cancelaciones: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener siniestros '''
    OutPut = obtener_siniestros(OutPut)
    print('\n\n Total obtener_siniestros: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener vlrprimac y vlrprimad para posterior cálculos de primas '''
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = obtener_vlrprima_c_d(OutPut, meses, ipc)
    print('\n\n Total obtener_vlrprima_c_d: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener primas emitidas (GWP) '''
    OutPut, OutPut_uprStock = obtener_primas_emitidas(OutPut, meses, ipc, uprStock, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad)
    print('\n\n Total obtener_primas_emitidas: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener comisiones '''
    OutPut = obtener_comisiones(OutPut, meses)
    print('\n\n Total obtener_comisiones: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener incurred claims '''
    OutPut = obtener_incurred_claims(OutPut, piva)
    print('\n\n Total obtener_incurred_claims: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Calculo de los ingresos financieros '''
    OutPut = calcular_ingresos_financieros(OutPut, finanp, meses)
    print('\n\n Total calcular_ingresos_financieros: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Calculo de los incentivos y costos de TMK '''
    OutPut = calcular_incentivos_y_costos_TMK(OutPut, ipc, tipincent, piva, pica, pgmf, mesanual)
    print('\n\n Total calcular_incentivos_y_costos_TMK: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Variables para el agrupamiento por PU '''
    Pu = obtener_variables_agrupamiento_PU(tipincent, ngrupos, meses, mesiniciost, OutPut, data_grupos_pu)
    print('\n\n Total obtener_variables_agrupamiento_PU: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    print('\n\n\n - Pu - \n\n\n')
    print(Pu)

    ''' Calculo de la PU por grupo de PU '''
    Pu = obtener_PU(OutPut, ngrupos, meses, data_grupos_pu, Pu)
    print('\n\n Total obtener_PU: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Obtener Resultado Técnico '''
    Return, Pu = obtener_resultado_tecnico(OutPut, Pu, ngrupos, meses)
    print('\n\n Total obtener_resultado_tecnico: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Utilidad preliminar '''
    OutPut_data_grupos_pu = pd.merge(OutPut.filter(['Id_Tool', 'Id_ Grupo_PU']), data_grupos_pu, left_on='Id_ Grupo_PU', right_on='Id_Grupo', how='left')
    OutPut, Up = obtener_utilidad_preliminar(OutPut, tipincent, ngrupos, data_grupos_pu, nproduct, meses, OutPut_data_grupos_pu)
    print('\n\n Total obtener_utilidad_preliminar: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    # -- AJUSTE SKB -- #
    try:
        OutPut['upr'] = np.where(
            ((OutPut['Vector ajuste SKB'] == 'Si') & (OutPut['TEMP_numeromes'] > MesesVectorAjusteSKB)),
            0,
            OutPut['upr']
        )
        OutPut['earnedP'] = np.where(
            ((OutPut['Vector ajuste SKB'] == 'Si') & (OutPut['TEMP_numeromes'] > MesesVectorAjusteSKB)),
            0,
            OutPut['earnedP']
        )
        OutPut['earnedC'] = np.where(
            ((OutPut['Vector ajuste SKB'] == 'Si') & (OutPut['TEMP_numeromes'] > MesesVectorAjusteSKB)),
            0,
            OutPut['earnedC']
        )
        OutPut['dac'] = np.where(
            ((OutPut['Vector ajuste SKB'] == 'Si') & (OutPut['TEMP_numeromes'] > MesesVectorAjusteSKB)),
            0,
            OutPut['dac']
        )
        OutPut['vata'] = np.where(
            ((OutPut['Vector ajuste SKB'] == 'Si') & (OutPut['TEMP_numeromes'] > MesesVectorAjusteSKB)),
            0,
            OutPut['vata']
        )
    except:
        OutPut['upr'] = OutPut['upr']
    # -- FIN AJUSTE SKB -- #
    print('\n\n Total AJUSTE SKB: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Distribuir la PU para cada uno de los productos que tiene resultado técnico positivo '''
    OutPut, Up = distribuir_PU(OutPut, ngrupos, Pu, nproduct, meses, Up)
    print('\n\n Total distribuir_PU: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' variables calculadas por acumulados '''
    OutPut, Up = obtener_variables_calculadas_por_acumulados(OutPut, taxr, meses, nproduct, Up)
    print('\n\n Total obtener_variables_calculadas_por_acumulados: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ''' Exportar el resultado '''
    start_time_2 = time.time()
    OutPut_imprimir = pd.DataFrame(
        {
            'Id_Tool': OutPut['Id_Tool'],
            'Socio': OutPut['Socio'],
            'Producto': OutPut['Cod. Producto'],
            'Tipo Oferta': OutPut['Oferta'],
            'Tipo de Prima': OutPut['Tipo Prima'],
            'Tipo_Proyección': OutPut['Tipo Proyección'],
            'Id_Escen/ Grupo': OutPut['Id_ Grupo_PU'],
            'Fecha': OutPut['fecha'],
            'Nuevos': OutPut['nuevos'],
            'Vigentes': OutPut['vigentes'],
            'Cancelaciones': OutPut['cancelaciones'],
            'Siniestros': OutPut['siniestros'],
            'GWP neto': OutPut['gwp'],
            'GWP Cancelaciones': OutPut['gwpn'],
            'UPR_eop': OutPut['upr'],
            'Earned_Premium': OutPut['earnedP'],
            'Total Commissions': OutPut['commin'],
            'Partner Commissions': OutPut['commins'],
            'Broker Commissions': OutPut['cominb'],
            'DAC': OutPut['dac'],
            'Total Earned_Commissions': OutPut['earnedC'],
            'Partner Earned_Commissions': OutPut['ecs'],
            'Broker Earned_Commissions': OutPut['ecb'],
            'Incurred_Claims': OutPut['incurC'],
            'Profit Share Reserve END': OutPut['pureal'],
            'PU_Incurrida ': OutPut['puincur'],
            'Resultado_Tec': OutPut['ResulTec'],
            'VAT Paid': OutPut['vatp'],
            'VAT incurred': OutPut['vata'],
            'Incentivos Diferidos': OutPut['incent'],
            'Incentivos Pagados': OutPut['incentp'],
            'TMKT Costo': OutPut['tmkCost'],
            'ICA': OutPut['ica'],
            'GMF': OutPut['gmf'],
            'VAT Incentives': OutPut['vatincent'],
            'VAT TMKT Cost': OutPut['vatmk'],
            'NBI': OutPut['gross2'] + OutPut['gastos'] - (OutPut['fincomec'] + OutPut['fincomer']),
            'Overheads': (OutPut['Overheads'] * OutPut['earnedP']),
            'GOI': OutPut['gross2'],
            'TAX': OutPut['taxreal'],
            'Linea Negocio Socio': OutPut['Linea Negocio Socio'],
            'Oferta CJ': OutPut['Oferta CJ'],
            'Capa': OutPut['Capa'],
            'Nombre Producto': OutPut['Nombre Producto'],
            'Mes': OutPut['TEMP_numeromes'],
            'Año': np.ceil(OutPut['TEMP_numeromes'] / 12),
            'Grupo_PU': OutPut_data_grupos_pu['Grupo_PU'],
            'Capital Requirement': OutPut['reqcap'],
            'Capital Req. Anual': OutPut['reqcapy'],
            'Financial Incomes': (OutPut['fincomec'] + OutPut['fincomer']),
            'TNBI': OutPut['TNBI'],
            'Ecosistema': OutPut['Ecosistema'],
            # 'ClaimsRate_Y1': OutPut['ClaimsRate_Y1'],
            # 'ClaimsRate_Y1_BACKUP': OutPut['ClaimsRate_Y1_BACKUP'],
            # 'Vector ajuste SKB': OutPut['Vector ajuste SKB'],
            # 'Resultado_TecV2': OutPut['ResulTecV2'],
        }
    )
    print('\n\n Total DATAFRAME: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    # -- Si es requerido, se adjunta base real -- #
    # start_timeBR = time.time()
    if imprimirBaseReal == 'Si':
        file = '/static/profitability/basereal/basereal.xlsx'
        file2 = '/static/profitability/basereal/basereal.csv'
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../' + file)
        path2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../' + file2)
        # print("\n\n LECTURA_ARCHIVO \n--- %s seconds ---" % (time.time() - start_timeBR))

        # start_timeBR0 = time.time()
        xlsx_baseReal = pd.ExcelFile(path)
        # print("\n\n LECTURA_ARCHIVO 1 \n--- %s seconds ---" % (time.time() - start_timeBR0))

        # start_timeBR1 = time.time()
        baseReal = pd.DataFrame(pd.read_excel(xlsx_baseReal, sheet_name='BaseReal'))
        # print("\n\n LECTURA_ARCHIVO 2 \n--- %s seconds ---" % (time.time() - start_timeBR1))

        # start_timeBR11 = time.time()
        # baseReal = pd.read_csv(path2, encoding='Latin-1', parse_dates=['Fecha'])
        baseReal = baseReal.fillna(0)
        # print("\n\n LECTURA_ARCHIVO 3 CSV \n--- %s seconds ---" % (time.time() - start_timeBR11))
        # print('\n\n\n - baseReal2 - \n\n\n')
        # print(baseReal)

        # start_timeBR2 = time.time()
        # -- Filtrar la baseReal solo con los socios del tipo de proyección 'Nuevos' -- #
        OutPut_imprimir_listaFiltro = OutPut_imprimir.groupby(['Socio']).mean().reset_index()
        OutPut_imprimir_listaFiltro = OutPut_imprimir_listaFiltro['Socio'].tolist()
        baseRealFiltrado = baseReal.loc[baseReal['Socio'].isin(OutPut_imprimir_listaFiltro)]
        OutPut_imprimir2 = pd.concat([OutPut_imprimir, baseRealFiltrado])
        # print("\n\n FILTRADO \n--- %s seconds ---" % (time.time() - start_timeBR2))

        # start_timeBR3 = time.time()
        # OutPut_imprimir2 = pd.concat([OutPut_imprimir, baseReal])
        OutPut_imprimir = OutPut_imprimir2.reindex(OutPut_imprimir.columns, axis="columns")
        # print("\n\n CAMBIAR VALOR DE OutPut_imprimir \n--- %s seconds ---" % (time.time() - start_timeBR3))
    # start_timeBRTOTAL = (time.time() - start_timeBR)
    # print("\n\n base real \n--- %s seconds ---" % start_timeBRTOTAL)
    # -- ajustes PGV --
    print('\n\n Total BASEREAL: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    try:
        if dataExtraPGV:
            OutPut = obtener_variables_ajustes_pgv(OutPut, tasadesemen, tasadeseanu, ctmktc, ctmkac)
            OutPut_imprimir['NOI'] = OutPut['NOI']
            OutPut_imprimir['PVFP'] = OutPut['PVFP']
            OutPut_imprimir['PVGWP'] = OutPut['PVGWP']
            OutPut_imprimir['PVEP'] = OutPut['PVEP']
            OutPut_imprimir['PVCOMMISION'] = OutPut['PVCOMMISION']
            OutPut_imprimir['PVCLAIMS'] = OutPut['PVCLAIMS']
            OutPut_imprimir['PV Cap Req'] = OutPut['PV Cap Req']
            OutPut_imprimir['Variacion Req Capital'] = OutPut['Variacion Req Capital']
            OutPut_imprimir['Value Creation'] = OutPut['Value Creation']
            OutPut_imprimir['Technical NOI'] = OutPut['Technical NOI']
            OutPut_imprimir['Technical PVFP'] = OutPut['Technical PVFP']
            OutPut_imprimir['Financial PVFP'] = OutPut['Financial PVFP']
            OutPut_imprimir['NBV'] = OutPut['NBV']
            OutPut_imprimir['PV NEP'] = OutPut['PV NEP']
            OutPut_imprimir['APE'] = OutPut['APE']
            OutPut_imprimir['Prima Media'] = OutPut['Prima Media']
            OutPut_imprimir['Duración'] = OutPut['Duración']
            OutPut_imprimir['Reservas fincome'] = OutPut['fincomer']
            OutPut_imprimir['Capital fincome'] = OutPut['fincomec']
    except:
        OutPut_imprimir = OutPut_imprimir

    print('\n\n Total dataExtraPGV: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    ###################################################################################################################
    ##############################
    ###### IMPRIMIR OUTPUT #######
    ##############################

    file_output = 'OutPut_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.csv'
    path2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../static/profitability/update_presupuesto/' + file_output)

    start_time_imprimir = time.time()
    # writer = obtener_archivo_reporte(path2, OutPut_imprimir)
    OutPut_imprimir.to_csv(path2, index=None, sep=',', encoding='utf-8-sig', float_format='%.5f', header=True, decimal=".")
    total_imprimir = (time.time() - start_time_imprimir)
    print('Total tiempo imprimir: ' + str(total_imprimir))

    print('\n\n Total imprimir: ' + str(time.time() - start_time_GLOBAL) + '\n\n')

    total_time = (time.time() - start_time_GLOBAL)
    total_time = format(total_time, '.2f')
    return str(total_time), file_output
