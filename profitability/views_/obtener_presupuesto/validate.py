import cx_Oracle
import pandas as pd
import configparser
import os


def conection():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    return cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)


def validate(file):
    ### Cargamos el archivo
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../' + file)
    xlsx_inputs = pd.ExcelFile(path)

    # -------------------------------------------------- #
    # ------------- Inicio validar hojas --------------- #
    # -------------------------------------------------- #
    sheets = [
        'Consola',
        'ParametrosSt',
        'DesembolsosSt',
        'RRC',
        'ParametrosNv',
        'DesembolsosNv',
    ]
    sheets_excel = xlsx_inputs.sheet_names
    errorValidationSheet = 0
    errorValidationSheetList = []
    for row in sheets:
        if row not in sheets_excel:
            errorValidationSheet = 1
            errorValidationSheetList.append(row)
    if errorValidationSheet:
        return False, 'Asegurase de tener las siguientes hojas: ' + '<br>'.join(errorValidationSheetList)

    # ---------------------------------------------------- #
    # ------------- Inicio validar Consola --------------- #
    # ---------------------------------------------------- #
    '''
    configuracion = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='Consola', skiprows=3))
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
    configuracion_variables = [
        'Finan. Income (Anual)',
        'Meses a proyectar',
        'Mes Inicia Stock:',
        '% De IVA Vigente',
        'Imprimir desde mes:',
        '% Incremento  IPC',
        'Caida en Renovación',
        'Meses Stcok Mensual',
        'Imprimir Base Real',
        '% ICA',
        'GMF',
        'Income Tax Rate',
        'Mes Uno Proyección',
        'Mes del año proyección',
        '      Cálculo RT con Incentivos',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6'
    ]
    errorValidationConf = 0
    errorValidationConfList = []
    for row in configuracion_variables:
        if row not in configuracion.tolist():
            errorValidationConf = 1
            errorValidationConfList.append(row)
    if errorValidationConf:
        return False, 'Asegurase de tener las siguientes variables de configuración en la hoja "Consola": ' + '<br>'.join(errorValidationConfList)
    '''

    # ---------------------------------------------------------------------------- #
    # ------------- Inicio validar Meses a proyectar (Desembolsos) --------------- #
    # ---------------------------------------------------------------------------- #
    configuracion = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='Consola', skiprows=3))
    Meses_a_proyectar = configuracion.iloc[1]['Unnamed: 2']

    # -- DesembolsosSt -- #
    DesembolsosSt = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='DesembolsosSt'))
    DesembolsosSt = DesembolsosSt.T
    DesembolsosSt['Id_Tool'] = DesembolsosSt.index
    ElementosDesembolsosSt = DesembolsosSt.query('Id_Tool=="Mes ' + str(Meses_a_proyectar) + '"')['Id_Tool']
    if ElementosDesembolsosSt.empty:
        return False, 'Asegurase de tener hasta el "Mes ' + str(Meses_a_proyectar) + '" en la hoja "DesembolsosSt".'

    # -- DesembolsosNv -- #
    DesembolsosNv = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='DesembolsosNv'))
    DesembolsosNv = DesembolsosNv.T
    DesembolsosNv['Id_Tool'] = DesembolsosNv.index
    ElementosDesembolsosNv = DesembolsosNv.query('Id_Tool=="Mes ' + str(Meses_a_proyectar) + '"')['Id_Tool']
    if ElementosDesembolsosNv.empty:
        return False, 'Asegurase de tener hasta el "Mes ' + str(Meses_a_proyectar) + '" en la hoja "DesembolsosNv".'

    # -- RRC -- #
    RRC = pd.DataFrame(pd.read_excel(xlsx_inputs, sheet_name='RRC'))
    RRC = RRC.T
    RRC['Id_Tool'] = RRC.index
    ElementosRRC = RRC.query('Id_Tool.str.contains("Mes ' + str(Meses_a_proyectar) + '")')['Id_Tool']
    if ElementosRRC.count() < 3:  # -- Se validan que contenta 3 veces el mes, por RRC, DAC_Proy y Vigentes
        return False, 'Asegurase de tener hasta el "Mes ' + str(Meses_a_proyectar) + '" en la hoja "RRC" <br><small>(para los datos de RRC, DAC_Proy y Vigentes)</small>'

    return True, ''
