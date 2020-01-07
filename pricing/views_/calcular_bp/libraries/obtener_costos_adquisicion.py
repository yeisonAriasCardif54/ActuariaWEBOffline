import cx_Oracle
import pandas as pd
import configparser
import numpy as np
import sqlite3


def obtener_costos_unitarios_adquisicion(Inputs):
    """
    # -- Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # -- Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    cnxn3 = sqlite3.connect('actuariaDatabase')

    # -- Consultar tabla de costo de adquisición -- #
    sql1 = """ SELECT * FROM PRICING_DATA_ACQUISITION_COSTS """
    costos = pd.read_sql(sql1, cnxn3)
    costos = costos.filter(['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE', 'UNIT_COST_IN_LC', 'PROD_GAINS', 'PROD_GAINS_NB', 'PROD_GAINS_START', 'INCIDENCE_RATE'])
    costos = costos.drop_duplicates()

    # -- hallar valores unitarios -- #
    Inputs['COUNTRY'] = 'COLOMBIA'
    # hallar Acquisition Fixed
    Inputs['DESTINATION'] = 'Acquisition'
    Inputs['COST_TYPE'] = 'Fixed'
    Inputs['unit_costs_Acquisition Fixed'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['Acquisition Fixed'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar Acquisition Variable
    Inputs['DESTINATION'] = 'Acquisition'
    Inputs['COST_TYPE'] = 'Variable'
    Inputs['unit_costs_Acquisition Variable'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['Acquisition Variable'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar Claims Variable
    Inputs['DESTINATION'] = 'Claims'
    Inputs['COST_TYPE'] = 'Variable'
    Inputs['unit_costs_Claims Variable'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['Claims Variable'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar Administration Fixed - Direct
    Inputs['DESTINATION'] = 'Administration'
    Inputs['COST_TYPE'] = 'Fixed - Direct'
    Inputs['unit_costs_Administration Fixed - Direct'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['Administration Fixed - Direct'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar Administration Fixed - Structure
    Inputs['DESTINATION'] = 'Administration'
    Inputs['COST_TYPE'] = 'Fixed - Structure'
    Inputs['unit_costs_Administration Fixed - Structure'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['Administration Fixed - Structure'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar Administration Variable
    Inputs['DESTINATION'] = 'Administration'
    Inputs['COST_TYPE'] = 'Variable'
    Inputs['unit_costs_Administration Variable'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['Administration Variable'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar FTS FTG
    Inputs['DESTINATION'] = 'FTS FTG'
    Inputs['COST_TYPE'] = 'FTS FTG'
    Inputs['unit_costs_FTS FTG'] = np.where(
        Inputs['business line'] == 'ASIGNAR MANUALMENTE',
        Inputs['FTS FTG'],
        pd.merge(Inputs, costos, left_on=['COUNTRY', 'business line', 'group of partners', 'DESTINATION', 'COST_TYPE'], right_on=['COUNTRY', 'BUSINESS_LINE', 'PARTNER_GROUP', 'DESTINATION', 'COST_TYPE'], how='left')['UNIT_COST_IN_LC']
    )
    # hallar Incidence rate
    Inputs['DESTINATION'] = 'Claims'
    Inputs['COST_TYPE'] = 'Variable'
    Inputs['unit_costs_Incidence rate'] = Inputs['Incidence rate']

    return Inputs


def obtener_costos_adquisicion(OutPut):
    OutPut['# In force policies'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['vigentes'],
        0
    )

    # Calcular inflación
    OutPut['Calc Inflation'] = (1 + OutPut['Inflation']) ** (np.ceil(OutPut['Mes'] / 12))

    # -- hallar Acquisition Fixed -- #
    OutPut['Acquisition Fixed Costs before adjustment'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['unit_costs_Acquisition Fixed'] * OutPut['# Agreements'],
        0
    )

    OutPut['Acquisition Fixed Costs before adjustment'] = OutPut['Acquisition Fixed Costs before adjustment'].astype(np.int)

    OutPut['Acquisition - Fixed'] = np.where(
        OutPut['Mes'] == 12,
        OutPut['Acquisition Fixed Costs before adjustment'] * OutPut['Calc Inflation'],
        0
    )
    # -- TODO: Aplicar % Stress -- #
    OutPut['Acquisition - Fixed'] = OutPut['Acquisition - Fixed'] * OutPut['Stress test Overheads increase']

    # -- hallar Acquisition - Variable -- #
    OutPut['Acquisition Variable Costs before adjustment'] = OutPut['unit_costs_Acquisition Variable'] * OutPut['nuevos']
    OutPut['Acquisition - Variable'] = OutPut['Acquisition Variable Costs before adjustment'] * OutPut['Calc Inflation']
    # -- TODO: Aplicar % Stress -- #
    OutPut['Acquisition - Variable'] = OutPut['Acquisition - Variable'] * OutPut['Stress test Overheads increase']

    # -- hallar Claims -- #
    OutPut['Claims Costs before adjustment'] = OutPut['unit_costs_Claims Variable'] * OutPut['vigentes'] * OutPut['unit_costs_Incidence rate']
    OutPut['Claims'] = OutPut['Claims Costs before adjustment'] * OutPut['Calc Inflation']
    # -- TODO: Aplicar % Stress -- #
    OutPut['Claims'] = OutPut['Claims'] * OutPut['Stress test Overheads increase']

    # -- hallar Administration Fixed - Direct -- #
    OutPut['Administration Fixed - Direct Costs before adjustment'] = np.where(
        OutPut['Mes'] % 12 == 0,
        np.where(
            OutPut['# In force policies'] > 0,
            OutPut['unit_costs_Administration Fixed - Direct'] * OutPut['# Agreements'],
            0
        ),
        0
    )
    OutPut['Administration Fixed - Direct'] = OutPut['Administration Fixed - Direct Costs before adjustment'] * OutPut['Calc Inflation']
    # -- TODO: Aplicar % Stress -- #
    OutPut['Administration Fixed - Direct'] = OutPut['Administration Fixed - Direct'] * OutPut['Stress test Overheads increase']

    # -- hallar Administration Variable -- #
    OutPut['Administration Variable Costs before adjustment'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['unit_costs_Administration Variable'] * OutPut['# In force policies'],
        0
    )
    OutPut['Administration Variable'] = OutPut['Administration Variable Costs before adjustment'] * OutPut['Calc Inflation']
    # -- TODO: Aplicar % Stress -- #
    OutPut['Administration Variable'] = OutPut['Administration Variable'] * OutPut['Stress test Overheads increase']

    # -- hallar Administration Fixed - Structure -- #
    OutPut['Administration Fixed - Structure Costs before adjustment'] = OutPut['unit_costs_Administration Fixed - Structure'] * (
            OutPut['Acquisition - Fixed'] +
            OutPut['Acquisition - Variable'] +
            OutPut['Claims'] +
            OutPut['Administration Fixed - Direct'] +
            OutPut['Administration Variable']
    )
    OutPut['Administration Fixed - Structure'] = OutPut['Administration Fixed - Structure Costs before adjustment']
    # -- TODO: Aplicar % Stress -- #
    OutPut['Administration Fixed - Structure'] = OutPut['Administration Fixed - Structure'] * OutPut['Stress test Overheads increase']

    # -- hallar FTS FTG -- 5#
    OutPut['FTS FTG Costs before adjustment'] = OutPut['unit_costs_FTS FTG'] * (
            OutPut['Acquisition - Fixed'] +
            OutPut['Acquisition - Variable'] +
            OutPut['Claims'] +
            OutPut['Administration Fixed - Direct'] +
            OutPut['Administration Variable'] +
            OutPut['Administration Fixed - Structure']
    )
    OutPut['FTS FTG'] = OutPut['FTS FTG Costs before adjustment']
    # -- TODO: Aplicar % Stress -- #
    OutPut['FTS FTG'] = OutPut['FTS FTG'] * OutPut['Stress test Overheads increase']
    # -- -- #

    OutPut['TOTAL ICA'] = OutPut['gwp'] * OutPut['Impuestos ICA']
    OutPut['TOTAL GMF'] = OutPut['gwpsc'] * OutPut['Impuestos GMF']
    OutPut['TOTAL ICA GMF'] = OutPut['TOTAL ICA'] + OutPut['TOTAL GMF']
    OutPut['TOTAL RECAUDO'] = OutPut['gwp'] * OutPut['Costo de Recaudo']

    OutPut['ASISTENCIA'] = OutPut['earnedP'] * OutPut['Costo Asistencia']
    # -- -- #
    OutPut['Costo Capacitación mes'] = np.where(
        OutPut['nuevos'] > 0,
        OutPut['Costo Capacitación'] / 12,
        0
    )
    OutPut['Publicidad mes'] = np.where(
        OutPut['nuevos'] > 0,
        OutPut['Publicidad'] / 12,
        0
    )
    OutPut['Bolsa Premios mes'] = np.where(
        OutPut['nuevos'] > 0,
        OutPut['Bolsa Premios'] / 12,
        0
    )
    OutPut['Costos Marketing'] = np.where(
        OutPut['nuevos'] > 0,
        OutPut['Costo Capacitación mes'] + OutPut['Publicidad mes'] + OutPut['Bolsa Premios mes'],
        0
    )
    OutPut['Gestores'] = np.where(
        OutPut['nuevos'] > 0,
        (OutPut['Número Gestores'] * OutPut['Costo Por Gestor']) * OutPut['Calc Inflation'],
        0
    )
    # -- -- #
    OutPut['Duración del seguro'] = 1 * (1 - (1 - OutPut['Caida']) ** OutPut['Duración del producto financiero']) / OutPut['Caida']
    OutPut['CalculoPeriodicidad'] = np.where(
        OutPut['Tipo de prima'] == 'Mensual',
        1,
        np.where(
            OutPut['Tipo de prima'] == 'Única',
            OutPut['Duración del producto financiero'],
            OutPut['Periodo de pago/CambioPrima']
        )
    )
    OutPut['Costo de Adquisicion Real'] = OutPut['Incentivo/Costo TMK']
    OutPut['Acquisition cost'] = OutPut['Costo de Adquisicion Real'] * OutPut['nuevos']

    OutPut['OVERHEADS'] = OutPut['Acquisition - Fixed'] + \
                          OutPut['Acquisition - Variable'] + \
                          OutPut['Claims'] + \
                          OutPut['Administration Fixed - Direct'] + \
                          OutPut['Administration Variable'] + \
                          OutPut['Administration Fixed - Structure'] + \
                          OutPut['FTS FTG'] + \
                          OutPut['TOTAL ICA GMF'] + \
                          OutPut['ASISTENCIA'] + \
                          OutPut['Costos Marketing'] + \
                          OutPut['Gestores'] + \
                          OutPut['Acquisition cost'] + \
                          OutPut['TOTAL RECAUDO']

    OutPut['Technical Result'] = OutPut['Total Earned Risk Premium'] - OutPut['Incurred Claims']
    OutPut['Technical Result with CoC'] = OutPut['Technical Result'] + OutPut['- Earned Insurer Capital Cost Loading'] - OutPut['earnedP'] * OutPut['Profit Share Retention'] + OutPut['- Insurer Written Acquisition Costs Loading'] + OutPut['- Insurer Earned Operating Expenses Loading'] - OutPut['OVERHEADS']
    OutPut['Pure Technical Loss Ratio'] = OutPut['Incurred Claims'] / OutPut['Total Earned Risk Premium']

    ''' CALCULO 1
    OutPut['Technical Result with CoC sum'] = (OutPut['Technical Result with CoC'] * OutPut['% PU']).cumsum()
    OutPut['Variable Commission'] = 0
    OutPut['Variable Commission'] = (OutPut['Technical Result with CoC sum'].shift(-1) - OutPut['Variable Commission']).cumsum()
    OutPut['Variable Commission'] = np.maximum(0, OutPut['Variable Commission'])
    '''

    ## CALCULO 2
    OutPut['Technical Result with CoC Xpu'] = OutPut['Technical Result with CoC'] * OutPut['% PU']
    OutPut['Technical Result with CoC sumXpu'] = (OutPut['Technical Result with CoC Xpu']).cumsum()
    OutPut['Technical Result with CoC sumXpu ANIO'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['Technical Result with CoC sumXpu'],
        0
    )
    OutPut['Technical Result with CoC sumXpu ANIO POS'] = np.where(
        OutPut['Technical Result with CoC sumXpu ANIO'] > 0,
        OutPut['Technical Result with CoC sumXpu ANIO'],
        0
    )
    OutPut['Variable Commission'] = 0
    OutPut['Variable Commission'] = np.where(
        OutPut['Mes'] == 12,
        OutPut['Technical Result with CoC sumXpu ANIO POS'],
        np.where(
            OutPut['Mes'] % 12 == 0,
            OutPut['Technical Result with CoC sumXpu ANIO POS'] - OutPut['Technical Result with CoC sumXpu ANIO POS'].shift(12),
            0
        )
    )

    #OutPut['RT - OVERHEADS'] = OutPut['earnedP'] - OutPut['- Earned Commission'] - OutPut['Incurred Claims'] - OutPut['Variable Commission'] - OutPut['Acquisition cost']
    # RT - OVERHEADS version 2:
    OutPut['RT - OVERHEADS'] = OutPut['- Insurer Written Acquisition Costs Loading'] + OutPut['- Insurer Earned Operating Expenses Loading'] + OutPut['- Earned Insurer Capital Cost Loading'] + OutPut['Technical Result']
    OutPut['NBI'] = OutPut['Financial Income on Reserves'] + OutPut['RT - OVERHEADS']
    OutPut['GOI'] = OutPut['NBI'] - OutPut['OVERHEADS']
    OutPut['TAX'] = OutPut['GOI'] * OutPut['Taxes']
    OutPut['NOI'] = OutPut['GOI'] - OutPut['TAX']

    OutPut['GWP net of IVA'] = OutPut['gwp'] + OutPut['gwpn']
    OutPut['Premium Life'] = OutPut['% Life'] * OutPut['GWP net of IVA']
    OutPut['Premium Non Life'] = OutPut['GWP net of IVA'] - OutPut['Premium Life']
    OutPut['Claim Life'] = OutPut['% Life'] * OutPut['Incurred Claims']
    OutPut['Claim non life'] = OutPut['Incurred Claims'] - OutPut['Claim Life']
    OutPut['Technical Reserves Life'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['% Life'] * OutPut['+ Change in Claim Reserve'] + OutPut['% Life'] * OutPut['upr'],
        0
    )

    # --  # in-force insured life -> vigentes del mes 12 de cada año
    OutPut['# in-force insured life'] = OutPut['# In force policies']
    OutPut['Capital (KCOP)'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['Valor Life'],
        0
    )
    OutPut['Sum at risk Life'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['Valor Life'] * OutPut['# in-force insured life'],
        0
    )
    OutPut['Solvency margin life'] = (OutPut['% technical reserves'] * OutPut['Technical Reserves Life']) + (OutPut['% Sum at risk'] * OutPut['Sum at risk Life'])
    OutPut['% Life Premium'] = OutPut['Solvency margin life'].div(OutPut['Premium Life'].where(OutPut['Premium Life'] != 0, 1))  # -- Se recalcula en obtener archivo
    OutPut['Component Claims PRE1'] = OutPut.groupby('Producto')['Claim non life'].apply(lambda x: x.rolling(center=False, min_periods=1, window=36).sum())
    OutPut['Component Claims PRE1'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['Component Claims PRE1'],
        0
    )

    OutPut['Year'] = (np.ceil(OutPut['Mes'] / 12))
    OutPut['Component Claims'] = np.where(
        OutPut['Mes'] % 12 == 0,
        (OutPut['Solvency margin % Claims'] * OutPut['Component Claims PRE1']) / np.minimum(OutPut['Year'], 3),
        0
    )
    OutPut['Component Premium'] = OutPut['Solvency margin % Premium'] * OutPut['Premium Non Life']
    OutPut['Component Premium'] = OutPut.groupby('Producto')['Component Premium'].apply(lambda x: x.rolling(center=False, min_periods=1, window=12).sum())
    OutPut['Component Premium'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['Component Premium'],
        0
    )
    OutPut['Solvency margin non life'] = np.maximum(OutPut['Component Claims'], OutPut['Component Premium'])  # -- Se recalcula en obtener archivo

    OutPut['Equity'] = OutPut['Solvency margin life'] + OutPut['Solvency margin non life']
    OutPut['Equity/Premium'] = OutPut['Equity'].div(OutPut['GWP net of IVA'].where(OutPut['GWP net of IVA'] != 0, 1))  # -- Se recalcula en obtener archivo
    OutPut['EquitySUM'] = OutPut.groupby('Producto')['Equity'].apply(lambda x: x.rolling(center=False, min_periods=1, window=12).sum())
    OutPut['EquitySUM'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['EquitySUM'],
        0
    )
    OutPut['Avg equity'] = np.where(
        OutPut['Mes'] == 12,
        OutPut['EquitySUM'] / 2,
        np.where(
            OutPut['Mes'] % 12 == 0,
            (OutPut['EquitySUM'] + OutPut['EquitySUM'].shift(12)) / 2,
            0
        )
    )

    OutPut['On Equity (Participate only in IROE calculations)'] = OutPut['Investment Rate anual'] * OutPut['Avg equity']
    OutPut['GOI con PF sobre equity'] = OutPut['GOI'] + OutPut['On Equity (Participate only in IROE calculations)']
    OutPut['TAX con PF sobre equity'] = OutPut['GOI con PF sobre equity'] * OutPut['Taxes']
    OutPut['NOI con PF sobre equity'] = OutPut['GOI con PF sobre equity'] - OutPut['TAX con PF sobre equity']
    OutPut['NOI con PF sobre equitySUM'] = OutPut.groupby('Producto')['NOI con PF sobre equity'].apply(lambda x: x.rolling(center=False, min_periods=1, window=12).sum())
    OutPut['NOI con PF sobre equitySUM'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['NOI con PF sobre equitySUM'],
        0
    )

    OutPut['IROE'] = OutPut['NOI'].div(OutPut['Avg equity'].where(OutPut['Avg equity'] != 0, 1))  # -- Se recalcula en obtener archivo

    OutPut['Cash-flow'] = np.where(
        OutPut['Mes'] == 1,
        OutPut['NOI con PF sobre equity'] - OutPut['Equity'],
        OutPut['NOI con PF sobre equity'] - (OutPut['Equity'] - OutPut['Equity'].shift(1))
    )
    OutPut['IRR'] = 0  # -- Se recalcula en obtener archivo

    OutPut['TMPYear'] = 1
    OutPut['Discount Rate'] = 1 / (1 + OutPut['Discount Rate annual']) ** OutPut['Year']  # -- Se recalcula en obtener archivo
    OutPut['Efficiency Ratio'] = OutPut['OVERHEADS'].div(OutPut['NBI'].where(OutPut['NBI'] != 0, 1))  # -- Se recalcula en obtener archivo
    OutPut['PV NOI con PF sobre equity'] = OutPut['NOI con PF sobre equitySUM'] * OutPut['Discount Rate']
    OutPut['PVFP'] = OutPut['PV NOI con PF sobre equity']  # -- Se recalcula en obtener archivo
    OutPut['PV Avg equity'] = OutPut['Avg equity'] * OutPut['Discount Rate']

    OutPut['(RC_(i-1)-RC_i)'] = np.where(
        OutPut['Mes'] == 12,
        OutPut['Equity'] * -1,
        np.where(
            OutPut['Mes'] % 12 == 0,
            OutPut['Equity'].shift(12) - OutPut['Equity'],
            0
        )
    )
    OutPut['NOI EQ + (RC_(i-1)-RC_i)'] = OutPut['NOI con PF sobre equitySUM'] + OutPut['(RC_(i-1)-RC_i)']
    OutPut['Value Creation'] = OutPut['NOI EQ + (RC_(i-1)-RC_i)'] * OutPut['Discount Rate']

    OutPut['Paid insurer underwriting'] = OutPut['Technical Result'] - OutPut['Variable Commission']
    OutPut['Fixed Costs'] = OutPut['Claims'] + \
                            OutPut['Administration Fixed - Direct'] + \
                            OutPut['Administration Variable'] + \
                            OutPut['Administration Fixed - Structure'] + \
                            OutPut['FTS FTG'] + \
                            OutPut['TOTAL ICA GMF'] + \
                            OutPut['ASISTENCIA'] + \
                            OutPut['Costos Marketing'] + \
                            OutPut['Gestores'] + \
                            OutPut['TOTAL RECAUDO']
    OutPut['Acquisition Costs'] = OutPut['Acquisition - Fixed'] + OutPut['Acquisition - Variable'] + OutPut['Acquisition cost']
    OutPut['Gross Operating Income (Including Financial Margin)'] = OutPut['GOI con PF sobre equity'] + OutPut['Financial Income on Reserves']
    #OutPut['Net Operating Income (Including Financial Margin)'] = OutPut['NOI con PF sobre equity'] + OutPut['Financial Income on Reserves']
    OutPut['Net Operating Income (Including Financial Margin)'] = OutPut['NOI con PF sobre equity']
    OutPut['Technical Loss Ratio'] = 0

    OutPut['Premium Collection Credit Risk'] = 0
    Maxgwpsc = pd.DataFrame({'value': OutPut.groupby(["Year"])['gwpsc'].max()}).reset_index()
    OutPut2 = pd.merge(OutPut.filter(['Year', 'Producto']), Maxgwpsc, on=['Year'])
    OutPut['Premium Collection Credit Risk'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut2['value'],
        0
    )
    OutPut['Claims Cash Advance Credit Risk'] = 0
    OutPut['Reinsurance Credit Risk'] = 0
    OutPut['PREcAL Surrender Credit Risk'] = np.where(
        OutPut['Mes'] == 0,
        0,
        np.maximum((OutPut['dac'].shift(1) * OutPut['Caida']), 0)
    )
    MaxPREcAL = pd.DataFrame({'value': OutPut.groupby(["Year"])['PREcAL Surrender Credit Risk'].max()}).reset_index()
    OutPut2 = pd.merge(OutPut.filter(['Year', 'Producto']), MaxPREcAL, on=['Year'])
    OutPut['Surrender Credit Risk'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut2['value'],
        0
    )
    OutPut['Total Credit Risk'] = OutPut['Premium Collection Credit Risk'] + OutPut['Claims Cash Advance Credit Risk'] + OutPut['Reinsurance Credit Risk'] + OutPut['Surrender Credit Risk']

    OutPut['vigentes'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['vigentes'],
        0
    )
    OutPut['gwp'] = OutPut['gwp'] + OutPut['- Premium Refund']

    return OutPut
