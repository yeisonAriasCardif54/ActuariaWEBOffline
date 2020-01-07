import numpy as np
import pandas as pd
from openpyxl import load_workbook
import time
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_datos_DB_DS
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_datos_DB_RRC
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_prima_promedio
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_tabla_productos
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_socios
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_pricing
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_rt_riesgo
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_grupos_pu
from profitability.views_.calcular_rrc.obtener_datos_DB import obtener_ofertas
import os
import xlsxwriter

import pandas.io.formats.excel

pandas.io.formats.excel.header_style = None


def get_data(file, mes, anio, meses):
    # sys.path.insert(0, "Q:\Profitability\Proyecto Automatizacion\Budget\Py\\presupuesto_data_inicial")

    start_time_GLOBAL = time.time()

    mes = mes
    anio = int(anio)
    meses_proyeccion = int(meses)

    ##########
    # PASO 1) CARGAMOS LOS PARÁMETROS DEL STOCK
    ##########

    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../' + file)

    xlsxFile = pd.ExcelFile(path)
    ParametrosSt = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='ParametrosSt'))
    ParametrosSt.rename(
        columns={
            'Id_T.Prima': 'Id_TPrima',
            'Cod. Producto': 'Cod Producto',
            'Tipo Proyección': 'Tipo_Proyeccion',
            'Pent. Inicial Año 2 ': 'Pent. Inicial Año 2',
            'Pent. Final Año 2 ': 'Pent. Final Año 2',
            'Pent. Inicial Año 3 ': 'Pent. Inicial Año 3',
            'Unnamed: 41': ''
        }, inplace=True)
    xlsxFile.close()

    ##########
    # PASO 2) VALIDACIONES
    ##########

    ############################################################
    ### INICIO VALIDAR TIPOS DE PRIMA PARA TODOS LOS PRODUCTOS
    ############################################################
    # CONSULTAR TABLA DE PRODUCTOS
    Tabla_Productos = obtener_tabla_productos()
    DesembolsosSt = pd.merge(ParametrosSt, Tabla_Productos.filter(['COD_PROD', 'PERIODO']), left_on='Cod Producto', right_on='COD_PROD', how='left')
    validacion = ''
    validacion_mensaje = ''
    for ind in DesembolsosSt.index:
        if DesembolsosSt['Id_TPrima'][ind] == 2 and DesembolsosSt['PERIODO'][ind] != 'Anual':
            validacion = validacion + ', ' + str(DesembolsosSt['Cod Producto'][ind])
            validacion_mensaje = validacion_mensaje + ', ' + str(DesembolsosSt['PERIODO'][ind])
        elif DesembolsosSt['Id_TPrima'][ind] == 1 and DesembolsosSt['PERIODO'][ind] != 'Mensual':
            validacion = validacion + ', ' + str(DesembolsosSt['Cod Producto'][ind])
            validacion_mensaje = validacion_mensaje + ', ' + str(DesembolsosSt['PERIODO'][ind])
        elif DesembolsosSt['Id_TPrima'][ind] == 3 and DesembolsosSt['PERIODO'][ind] != 'Unica':
            validacion = validacion + ', ' + str(DesembolsosSt['Cod Producto'][ind])
            validacion_mensaje = validacion_mensaje + ', ' + str(DesembolsosSt['PERIODO'][ind])
    if validacion != '':
        raise ValueError("Error al validar los tipos de primas: el(los) producto(s) ID " + str(validacion) + " debe ser de tipo(en su orden): " + validacion_mensaje)
    ############################################################
    ### FIN VALIDAR TIPOS DE PRIMA PARA TODOS LOS PRODUCTOS
    ############################################################

    ############################################################
    ### INICIO VALIDAR PRODUCTOS NUEVOS NO CONTEMPLADOS
    ############################################################
    PRODUCTOS_VIGENTES = obtener_prima_promedio()
    PRODUCTOS_VIGENTES['PRODUCTO'] = PRODUCTOS_VIGENTES['PRODUCTO'].astype(np.int64)
    PRODUCTOS_VIGENTES['PRODUCTO_'] = PRODUCTOS_VIGENTES['PRODUCTO'].astype(np.int64)
    ParametrosSt['Cod Producto_'] = ParametrosSt['Cod Producto'].astype(np.int64)
    PRODUCTOS_FALTANTES = PRODUCTOS_VIGENTES.merge(ParametrosSt.drop_duplicates(), left_on='PRODUCTO_', right_on='Cod Producto_', how='left', indicator=True)
    PRODUCTOS_FALTANTES = PRODUCTOS_FALTANTES.filter(['PRODUCTO_', '_merge'])
    PRODUCTOS_FALTANTES_TOTAL = PRODUCTOS_FALTANTES.query('_merge == "left_only"')
    PRODUCTOS_FALTANTES_LISTADO = PRODUCTOS_FALTANTES.query('_merge == "left_only"')['PRODUCTO_'].values.tolist()
    del (PRODUCTOS_VIGENTES['PRODUCTO_'])

    if len(PRODUCTOS_FALTANTES_TOTAL) > 0:
        # raise ValueError("Error: Se encontraron " + str(len(PRODUCTOS_FALTANTES_TOTAL)) +  " productos no contemplados en 'ParametrosSt': " + str(PRODUCTOS_FALTANTES_LISTADO))
        # Obtener información para agregarlo al Stock
        Socios = obtener_socios()
        Pricing = obtener_pricing()
        RT_riesgo = obtener_rt_riesgo()
        Grupos_PU = obtener_grupos_pu()
        Ofertas = obtener_ofertas()
        RT_riesgo['CODPRODUCTO'] = RT_riesgo['CODPRODUCTO'].astype(np.int)

        parametro_actual = len(ParametrosSt)
        for cod_producto in PRODUCTOS_FALTANTES_LISTADO:
            parametro_actual = parametro_actual + 1
            data_nuevo_producto = {}
            data_nuevo_producto['Id_Tool'] = parametro_actual

            ###### Hallar socio ######
            try:
                Socio = Tabla_Productos.query('COD_PROD == ' + str(cod_producto))['NOM_SOCIO'].item()
            except:
                raise ValueError("Error: No se encontró socio en TABLA_PRODUCTOS para el código: " + str(cod_producto))
            try:
                Socio_id = Socios.query('NOMBRE == "' + str(Socio) + '"')['ID'].item()
            except:
                raise ValueError("Error: No se encontró id_socio en PRF_SOCIOS para el socio: " + str(Socio))
            data_nuevo_producto['Id_Socio'] = Socio_id

            ###### Hallar Id_T.Oferta ######
            try:
                CHANNEL = Pricing.query('CODE == ' + str(cod_producto))['CHANNEL'].item()
            except:
                raise ValueError("Error: No se encontró CHANNEL en PRICING para el código: " + str(cod_producto))
            try:
                ID_OFERTA = Ofertas.query('NOMBRE_VERSION_PRICING == "' + str(CHANNEL) + '"')['ID'].item()
            except:
                raise ValueError("Error: No se encontró NOMBRE_VERSION_PRICING en PRF_OFERTAS para el CHANNEL: " + str(CHANNEL) + ', código: ' + str(cod_producto))
            data_nuevo_producto['Id_T.Oferta'] = ID_OFERTA

            ###### Hallar Duración ######
            try:
                DURACION_CREDITO = Pricing.query('CODE == ' + str(cod_producto))['DURACION_CREDITO'].item()
            except:
                raise ValueError("Error: No se encontró DURACION_CREDITO en PRICING para el código: " + str(cod_producto))
            data_nuevo_producto['Duración'] = DURACION_CREDITO

            ###### Hallar Id_TPrima ######
            try:
                Periodo = Tabla_Productos.query('COD_PROD == ' + str(cod_producto))['PERIODO'].item()
                if Periodo == 'Mensual':
                    data_nuevo_producto['Id_TPrima'] = int(1)
                elif Periodo == 'Anual':
                    data_nuevo_producto['Id_TPrima'] = int(2)
                elif Periodo == 'Unica':
                    data_nuevo_producto['Id_TPrima'] = int(3)
                else:
                    raise ValueError()
            except:
                raise ValueError("Error: No se encontró periodo en TABLA_PRODUCTOS ó No se encontró Id_TPrima para el código: " + str(cod_producto))

            ###### Hallar Vlr. Prima Prom ######
            ###### Hallar Vlr. Prima Prom para mensual
            try:
                Promedio_prima = PRODUCTOS_VIGENTES.query('PRODUCTO == ' + str(cod_producto))['VALOR'].item()
            except:
                raise ValueError("Error: No se encontró VALOR en PRODUCTOS_VIGENTES para el código: " + str(cod_producto))
            ###### Hallar Vlr. Prima Prom para única y anual
            try:
                MONTHLY_PREMIUM = Pricing.query('CODE == ' + str(cod_producto))['MONTHLY_PREMIUM'].item()
                DURACION_CREDITO = Pricing.query('CODE == ' + str(cod_producto))['DURACION_CREDITO'].item()
            except:
                raise ValueError("Error: No se encontró MONTHLY_PREMIUM,DURACION_CREDITO en PRICING para el código: " + str(cod_producto))

            if data_nuevo_producto['Id_TPrima'] == 1:
                data_nuevo_producto['Vlr. Prima Prom'] = Promedio_prima
            elif data_nuevo_producto['Id_TPrima'] == 2:
                data_nuevo_producto['Vlr. Prima Prom'] = MONTHLY_PREMIUM * 12
            elif data_nuevo_producto['Id_TPrima'] == 3:
                data_nuevo_producto['Vlr. Prima Prom'] = MONTHLY_PREMIUM * DURACION_CREDITO
            else:
                raise ValueError("Error: En clasificación de tipo de prima para el código: " + str(cod_producto))

            data_nuevo_producto['Mes Inicio'] = 1

            ###### Hallar Caida ######
            try:
                Caida = Pricing.query('CODE == ' + str(cod_producto))['LAPSES_RATES_YEARLY'].item()
                PARTNER_COMMISSIONS = Pricing.query('CODE == ' + str(cod_producto))['PARTNER_COMMISSIONS'].item()
                BROKER_COMMISSIONS = Pricing.query('CODE == ' + str(cod_producto))['BROKER_COMMISSIONS'].item()
                INTERMEDIARY_COMMISSIONS = Pricing.query('CODE == ' + str(cod_producto))['INTERMEDIARY_COMMISSIONS'].item()
                CLAIMS_RATIO = Pricing.query('CODE == ' + str(cod_producto))['CLAIMS_RATIO'].item()
                LIFE = Pricing.query('CODE == ' + str(cod_producto))['LIFE'].item()
                COMMISSIONS_NONINT = Pricing.query('CODE == ' + str(cod_producto))['COMMISSIONS_NONINT'].item()
                PRODUCT_NAME = Pricing.query('CODE == ' + str(cod_producto))['PRODUCT_NAME'].item()

                data_nuevo_producto['Caida'] = 1 - (1 - Caida) ** (1 / 12)
                data_nuevo_producto['Frecuencia'] = 0
                data_nuevo_producto['Comisión'] = PARTNER_COMMISSIONS + BROKER_COMMISSIONS + INTERMEDIARY_COMMISSIONS
                data_nuevo_producto['ClaimsRate_Y1'] = CLAIMS_RATIO
                data_nuevo_producto['ClaimsRate_Y3'] = CLAIMS_RATIO
                data_nuevo_producto['ClaimsRate_Y5'] = CLAIMS_RATIO
                data_nuevo_producto['% VAT'] = LIFE
                data_nuevo_producto['% Com Non'] = COMMISSIONS_NONINT
                data_nuevo_producto['% incentivo'] = 0
                data_nuevo_producto['C/U. Venta TMKT'] = ''
                data_nuevo_producto['Cod Producto'] = cod_producto
                data_nuevo_producto['Tipo_Proyeccion'] = 'Stock'
                data_nuevo_producto['Pent. Q1'] = 1
                data_nuevo_producto['Pent. Q2'] = ''
                data_nuevo_producto['Pent. Q3'] = ''
                data_nuevo_producto['Pent. Q4'] = ''
                data_nuevo_producto['Pent. Inicial Año 2'] = ''
                data_nuevo_producto['Pent. Final Año 2'] = ''
                data_nuevo_producto['Plazo Año 2'] = ''
                data_nuevo_producto['Pent. Inicial Año 3'] = ''
                data_nuevo_producto['Pent. Final Año 3'] = ''
                data_nuevo_producto['Plazo Año 3'] = ''
                data_nuevo_producto['Oferta CJ'] = 'No'
                data_nuevo_producto['Nombre Producto'] = PRODUCT_NAME
                data_nuevo_producto['¿Aplica IPC?'] = 'No'
                data_nuevo_producto['Overheads'] = 0.12
                data_nuevo_producto['Meses garantía fabricante'] = ''
                data_nuevo_producto['t CutOff'] = ''
                data_nuevo_producto['%Part.Broker'] = ''
                data_nuevo_producto['Amortizacion'] = 'Natural'
                data_nuevo_producto['% Asistencia'] = ''
                data_nuevo_producto['Claims cn Asistencia'] = ''
            except:
                raise ValueError("Error: No se encontraron DATA en PRICING de código: " + str(cod_producto))

            ###### Hallar Capa ######
            try:
                Capa = Tabla_Productos.query('COD_PROD == ' + str(cod_producto))['TIPO'].item()
            except:
                raise ValueError("Error: No se encontró TIPO en TABLA_PRODUCTOS para el código: " + str(cod_producto))
            data_nuevo_producto['Capa'] = Capa
            ###### Hallar Linea Negocio Socio ######
            try:
                Linea = Tabla_Productos.query('COD_PROD == ' + str(cod_producto))['LINEA_NEGOCIO'].item()
            except:
                raise ValueError("Error: No se encontró LINEA_NEGOCIO en TABLA_PRODUCTOS para el código: " + str(cod_producto))
            data_nuevo_producto['Linea Negocio Socio'] = Linea
            ###### Hallar Id_ Grupo_PU ######
            try:
                GRUPOPU = RT_riesgo.query('CODPRODUCTO == ' + str(cod_producto))['GRUPOPU'].item()
                if GRUPOPU == None:
                    GRUPOPU = 'Vacio'
                Grupo_PU = Grupos_PU.query('NOMBRE == "' + str(GRUPOPU) + '"')['ID'].item()
            except:
                raise ValueError("Error: No se encontró CODPRODUCTO en RT_RIESGO ó NOMBRE en Grupos_PU para el código: " + str(cod_producto))
            data_nuevo_producto['Id_ Grupo_PU'] = Grupo_PU

            # Imprimir Stock
            ParametrosSt = ParametrosSt.append(data_nuevo_producto, ignore_index=True)

            # Imprimir Stock RRC
            data_nuevo_producto['Tipo_Proyeccion'] = 'Stock_RRC'
            data_nuevo_producto['Vlr. Prima Prom'] = ''
            parametro_actual = parametro_actual + 1
            data_nuevo_producto['Id_Tool'] = parametro_actual
            ParametrosSt = ParametrosSt.append(data_nuevo_producto, ignore_index=True)

    del (ParametrosSt['Cod Producto_'])

    ############################################################
    ### FIN VALIDAR PRODUCTOS NUEVOS NO CONTEMPLADOS
    ############################################################

    ##########
    # PASO 3) CALCULAR DesembolsosSt
    ##########

    # Creación de DataFrame DesembolsosSt
    DesembolsosSt = pd.DataFrame({})
    DesembolsosSt['Id_Tool'] = ParametrosSt['Id_Tool']
    DesembolsosSt['Id_TPrima'] = ParametrosSt['Id_TPrima']
    DesembolsosSt['Id_Socio'] = ParametrosSt['Id_Socio']
    DesembolsosSt['Cod Producto'] = ParametrosSt['Cod Producto']
    DesembolsosSt['Tipo_Proyeccion'] = ParametrosSt['Tipo_Proyeccion']
    # DesembolsosSt['PERIODO'] = ParametrosSt['PERIODO']

    # Creamos los meses

    # Cargamos los vigentes de la base de datos
    lista_prod_anuales = DesembolsosSt.query("Id_TPrima == 2")['Cod Producto'].values.tolist()
    lista_prod_anuales = str(lista_prod_anuales)[1:-1]
    vigentes_mensual, vigentes_anuales = obtener_datos_DB_DS(mes, anio, lista_prod_anuales)

    ########################################################################
    ## Unificamos información con vigentes
    DesembolsosSt = pd.merge(DesembolsosSt, vigentes_mensual.filter(['PRODUCTO', 'SUMA']), left_on='Cod Producto', right_on='PRODUCTO', how='left')
    del (DesembolsosSt['PRODUCTO'])
    vigentes_anuales['PRODUCTO'] = vigentes_anuales['PRODUCTO'].astype(np.int64)
    DesembolsosSt = pd.merge(DesembolsosSt, vigentes_anuales, left_on='Cod Producto', right_on='PRODUCTO', how='left')
    del (DesembolsosSt['PRODUCTO'])

    DesembolsosSt = DesembolsosSt.fillna(0)
    DesembolsosSt[0] = 0

    def getMes(DesembolsosSt, i):
        try:
            return np.where(
                DesembolsosSt['Tipo_Proyeccion'] == 'Stock',
                np.where(
                    DesembolsosSt['Id_TPrima'] == 1,  # Mensual
                    np.where(
                        i == 0,  # Mes cero
                        DesembolsosSt['SUMA'],
                        0
                    ),
                    np.where(
                        DesembolsosSt['Id_TPrima'] == 2,  # Anual
                        np.where(
                            (i > 0) & (i <= 12),
                            DesembolsosSt[i],
                            0
                        ),
                        0
                    )
                ),
                0
            )
        except KeyError:
            return 0

    for i in range(0, meses_proyeccion + 1):
        DesembolsosSt['Mes ' + str(i)] = getMes(DesembolsosSt, i)

    ########################################################################
    ## CALCULAR ULTIMO MES PRODUCTOS GRUPO AVAL PRIMA ANUAL (IDs 2-4-5-7)
    socios = [2, 4, 5, 7]
    columns_sum = ['Mes 1', 'Mes 2', 'Mes 3', 'Mes 4', 'Mes 5', 'Mes 6', 'Mes 7', 'Mes 8', 'Mes 9', 'Mes 10', 'Mes 11']
    DesembolsosSt['Mes 12_recalculo'] = (DesembolsosSt.filter(columns_sum).sum(axis=1) / 11)
    DesembolsosSt['Mes 12'] = np.where(
        (np.isin(DesembolsosSt['Id_Socio'], socios)) & (DesembolsosSt['Id_TPrima'] == 2),
        DesembolsosSt['Mes 12_recalculo'].astype(np.int64),
        DesembolsosSt['Mes 12']
    )

    del (DesembolsosSt['SUMA'])
    del (DesembolsosSt['Mes 12_recalculo'])
    # Eliminar columnas de vigentes_anuales
    DesembolsosSt.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], axis=1, inplace=True)

    ##########
    # PASO 4) CALCULAR RRC
    ##########

    # Filtrar productos stock_rrc
    ParametrosSt_RRC = ParametrosSt.query("Tipo_Proyeccion == 'Stock_RRC'")

    RRC = pd.DataFrame({})
    RRC['Id_Tool'] = ParametrosSt_RRC['Id_Tool']
    RRC['Id_TPrima'] = ParametrosSt_RRC['Id_TPrima']
    RRC['Cod_Producto'] = ParametrosSt_RRC['Cod Producto']

    # Consultar RRC Y DAC en base de datos
    CART_RRC, CART_RRC_DAC = obtener_datos_DB_RRC(mes)
    # Renombramos las columnas en RRC
    CART_RRC = CART_RRC.rename(columns={CART_RRC.columns[0]: 'RRC'})
    for i in range(1, meses_proyeccion + 1):
        try:
            CART_RRC = CART_RRC.rename(columns={CART_RRC.columns[i]: 'Mes ' + str(i)})
        except:
            raise ValueError("Error: No se encontró Mes en CART_RRC para el mes: " + str(i))

    CART_RRC['PRODUCTO'] = CART_RRC.index
    RRC = pd.merge(RRC, CART_RRC, left_on='Cod_Producto', right_on='PRODUCTO', how='left')
    del (RRC['PRODUCTO'])

    RRC['ESPACIO1'] = ''
    RRC['ESPACIO1_2'] = ''
    RRC['Cod Producto2'] = ParametrosSt_RRC['Cod Producto']

    # Renombramos las columnas en DAC
    CART_RRC_DAC = CART_RRC_DAC.rename(columns={CART_RRC_DAC.columns[0]: 'DAC_Proy'})
    for i in range(1, meses_proyeccion + 1):
        CART_RRC_DAC = CART_RRC_DAC.rename(columns={CART_RRC_DAC.columns[i]: 'DACMes ' + str(i)})
    CART_RRC_DAC['PRODUCTO'] = CART_RRC_DAC.index
    RRC = pd.merge(RRC, CART_RRC_DAC, left_on='Cod_Producto', right_on='PRODUCTO', how='left')
    del (RRC['PRODUCTO'])

    # Consultar prima promedio
    PRIMAS_PROMEDIO = PRODUCTOS_VIGENTES

    RRC = pd.merge(RRC, PRIMAS_PROMEDIO, left_on='Cod_Producto', right_on='PRODUCTO', how='left')
    del (RRC['PRODUCTO'])

    # Calcular vigentes
    RRC['ESPACIO2'] = ''
    RRC['ESPACIO2_2'] = ''
    RRC['Cod Producto3'] = ParametrosSt_RRC['Cod Producto']

    RRC['VlrPrima Prom.'] = RRC['VALOR']
    del (RRC['VALOR'])
    RRC['Vigentes'] = np.maximum(RRC['RRC'] / RRC['VlrPrima Prom.'], 0)
    for i in range(1, meses_proyeccion + 1):
        RRC['VigMes ' + str(i)] = np.maximum(RRC['Mes ' + str(i)] / RRC['VlrPrima Prom.'], 0)
        # Renombrar columnas de meses
        RRC.rename(columns={'VigMes ' + str(i): 'Mes ' + str(i)}, inplace=True)
        RRC.rename(columns={'DACMes ' + str(i): 'Mes ' + str(i)}, inplace=True)

    # Renombrar columnas de espacios y códigos de productos
    RRC.rename(columns={'ESPACIO1': ''}, inplace=True)
    RRC.rename(columns={'ESPACIO1_2': ''}, inplace=True)
    RRC.rename(columns={'ESPACIO2': ''}, inplace=True)
    RRC.rename(columns={'ESPACIO2_2': ''}, inplace=True)
    RRC.rename(columns={'Cod Producto2': 'Cod_Producto'}, inplace=True)
    RRC.rename(columns={'Cod Producto3': 'Cod_Producto'}, inplace=True)
    ##########
    # PASO 5) Imprimir resultados
    ##########

    ParametrosSt.rename(
        columns={
            'Id_TPrima': 'Id_T.Prima',
            'Cod Producto': 'Cod. Producto',
            'Tipo_Proyeccion': 'Tipo Proyección',
        }, inplace=True)

    path2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../static/profitability/updaterrc/Plantilla_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.xlsx')
    writer = pd.ExcelWriter(path2, engine='xlsxwriter')

    ###################################################################################################################

    ParametrosSt.to_excel(writer, sheet_name='ParametrosSt', index=None, float_format='%.5f', startrow=0, header=True)
    ##################################
    ###### FORMATO ParametrosSt ######
    ##################################
    workbook = writer.book
    worksheet = writer.sheets['ParametrosSt']
    # ANCHO DE COLUMNA #
    for col_num, value in enumerate(ParametrosSt.columns.values):
        column_len = ParametrosSt[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    # FORMATO DE HEADER #
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    # FORMATO POR COLUMNA #
    format2 = workbook.add_format()
    format2.set_align('center')
    format2.set_font_size(10)
    worksheet.set_column('A:AR', 15, format2)
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
    worksheet.set_column('F:F', 15, format3)
    format4 = workbook.add_format()
    format4.set_font_size(9)
    format4.set_num_format('0.0%')
    worksheet.set_column('H:Q', 15, format4)
    worksheet.set_column('T:AC', 15, format4)
    worksheet.set_column('AI:AI', 15, format4)
    worksheet.set_column('AQ:AR', 15, format4)

    ####################################################################################################################

    del (DesembolsosSt['Id_TPrima'])
    del (DesembolsosSt['Id_Socio'])
    del (DesembolsosSt['Cod Producto'])
    del (DesembolsosSt['Tipo_Proyeccion'])
    DesembolsosSt['Espacio1'] = ' '
    DesembolsosSt['Id_Socio'] = ParametrosSt['Id_Socio']
    DesembolsosSt['Id_T.Oferta'] = ParametrosSt['Id_T.Oferta']
    DesembolsosSt['Id_T.Prima'] = ParametrosSt['Id_T.Prima']
    DesembolsosSt['Cod. Producto'] = ParametrosSt['Cod. Producto']
    DesembolsosSt['Tipo Proyección'] = ParametrosSt['Tipo Proyección']
    DesembolsosSt.rename(columns={'Espacio1': ''}, inplace=True)
    DesembolsosSt.to_excel(writer, 'DesembolsosSt', index=False, float_format='%.5f')
    ###################################
    ###### FORMATO DesembolsosSt ######
    ###################################
    workbook = writer.book
    worksheet = writer.sheets['DesembolsosSt']
    for col_num, value in enumerate(DesembolsosSt.columns.values):
        column_len = DesembolsosSt[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    # FORMATO DE HEADER #
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    # FORMATO POR COLUMNA #
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)')
    worksheet.set_column('B:YY', 15, format3)

    ###################################################################################################################

    del (RRC['Id_TPrima'])
    RRC.to_excel(writer, 'RRC', index=False)
    #########################
    ###### FORMATO RRC ######
    #########################
    workbook = writer.book
    worksheet = writer.sheets['RRC']

    # FORMATO DE HEADER #
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    # FORMATO POR COLUMNA #
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
    worksheet.set_column('C:YY', 15, format3)

    writer.save()
    total_time = (time.time() - start_time_GLOBAL)
    total_time = format(total_time, '.2f')
    return 'Se genero con éxito el archivo en ' + str(total_time) + ' segundos.', path2
