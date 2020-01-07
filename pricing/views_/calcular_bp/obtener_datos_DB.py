import pandas as pd
import numpy as np
import cx_Oracle
import configparser


def obtener_datos_DB_DS(mes, anio, lista_prod_anuales):
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    mes = int(mes)
    anio = int(anio)

    mes_menos_dos = mes - 1
    if mes_menos_dos <= 0:
        mes_menos_dos = ((mes_menos_dos - 1) % 12) + 1
        anio = anio - 1
    mes_menos_dos = str(mes_menos_dos).zfill(2)

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    # Consultar vigentes del mes/anio seleccionados - MENSUALES
    sql1 = """select producto,fecha_inicio,sum(total_vigentes) as suma, sum(PRIMA_PERIODO) as primas
                from actuaria.cart_vigentes
                WHERE
                TO_CHAR(TO_DATE(fecha_inicio,'YYYY/MM'),'MM') = '""" + str(mes_menos_dos) + """'
                and TO_CHAR(TO_DATE(fecha_inicio,'YYYY/MM'),'YYYY') = '""" + str(anio) + """'
                and LENGTH(fecha_inicio) = 6
                group by producto,fecha_inicio
                order by producto,fecha_inicio"""

    vigentes_mensual = pd.read_sql(sql1, cnxn3)

    mes_mas_uno = mes + 1
    if mes_mas_uno > 12:
        mes_mas_uno = 1
        anio = anio + 1
    mes_mas_uno = str(mes_mas_uno).zfill(2)

    # Consultar proyección de vigentes ANUALES
    '''
    sql2 = """SELECT SUB2.PRODUCTO,SUB2.INICIO_CERTIFICADO,
                TO_CHAR(TO_DATE(INICIO_CERTIFICADO,'YYYY/MM'),'MM') mes, COUNT(SUB2.INICIO_CERTIFICADO) AS TOTAL FROM (
                SELECT SUB1.PRODUCTO,SUB1.CERTIFICADO,SUB1.CC,
                (TO_CHAR(EXTRACT(YEAR FROM SUB1.FECHAINICIO) || '' || SUBSTR(SUB1.FECHAINICIO,4,2))) AS INICIO_CERTIFICADO
                FROM(
                SELECT t1.PRODUCTO,t1.CC,t1.CERTIFICADO, 
                t1.FECHAINICIO,t1.TIPO_MOV 
                FROM ACTUARIA.RT_MOV_HIST_POLIZA t1 
                WHERE t1.CC NOT IN ('0',' ') AND t1.CERTIFICADO NOT LIKE '%Prov%' AND t1.CERTIFICADO NOT LIKE '%PROV%'
                AND t1.PRODUCTO
                IN (""" + lista_prod_anuales + """)
                ORDER BY T1.FECHAINICIO,T1.TIPO_MOV
                )SUB1 WHERE SUB1.FECHAINICIO BETWEEN TO_DATE('""" + str(anio - 1) + """-""" + str(mes_mas_uno) + """', 'YYYY-MM') AND TO_DATE('""" + str(anio) + """-""" + str(mes_mas_uno) + """', 'YYYY-MM')
                GROUP BY SUB1.PRODUCTO,SUB1.CERTIFICADO,SUB1.CC,SUB1.FECHAINICIO 
                HAVING SUM(SUB1.TIPO_MOV) = 0
                )SUB2 
                GROUP BY SUB2.PRODUCTO,SUB2.INICIO_CERTIFICADO
                """;
    
    '''
    sql2 = """SELECT * FROM 
                PROFITABILITY_PROYECCION 
                WHERE PRODUCTO
                IN (""" + lista_prod_anuales + """)
                AND TO_DATE(INICIO_CERTIFICADO, 'YYYY-MM') 
                BETWEEN TO_DATE('""" + str(anio - 1) + """-""" + str(mes_mas_uno) + """', 'YYYY-MM') 
                AND TO_DATE('""" + str(anio) + """-""" + str(mes) + """', 'YYYY-MM')
                    """

    vigentes_anuales = pd.read_sql(sql2, cnxn3)

    vigentes_anual_back = vigentes_anuales
    vigentes_anual_back['MES'] = vigentes_anual_back['MES'].astype(np.int32)

    # Mes siguiente
    vigentes_anual_back['MES'] = vigentes_anual_back['MES'] - mes - 1
    vigentes_anual_back['MES'] = (vigentes_anual_back['MES'] % 12) + 1

    vigentes_anuales_retorno = vigentes_anual_back.pivot_table(index=['PRODUCTO'],
                                                               columns='MES',
                                                               values='TOTAL',
                                                               fill_value=0) \
        .reset_index()

    return vigentes_mensual, vigentes_anuales_retorno


def obtener_datos_DB_RRC(mes):
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    # Consultar vigentes del mes/anio seleccionados - MENSUALES
    sql1 = """select CART_RRC.*, TO_CHAR(TO_DATE(FEC_LIBERACION,'YYYY/MM'),'YYMM') mes from ACTUARIA.CART_RRC ORDER BY FEC_LIBERACION """

    RRC_ = pd.read_sql(sql1, cnxn3)

    RRC_['MES'] = RRC_['MES'].astype(np.int32)
    RRC = RRC_.pivot_table(index=['PRODUCTO'],
                           columns='MES',
                           values='DEVENGO_RESE_PRIMA',
                           fill_value=0) \

    DAC = RRC_.pivot_table(index=['PRODUCTO'],
                           columns='MES',
                           values='COM_SOCIO',
                           fill_value=0) \

    return RRC, DAC


def obtener_prima_promedio():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    ## PROMEDIO DE PRIMAS DE LOS ÚLTIMOS 6 MESES
    # RT_MOV_HIST_POLIZA
    '''
    sql1 = """ select PRODUCTO, AVG(PRIMANETA) VALOR
                from ACTUARIA.RT_MOV_HIST_POLIZA
                WHERE
                TIPO_MOV = 0
                AND FECHAFIN >= (SYSDATE)
                AND CERTIFICADO NOT LIKE '%Prov%' AND CERTIFICADO NOT LIKE '%PROV%'
                GROUP BY PRODUCTO
                 """
    '''
    sql1 = """ SELECT PRODUCTO, VALOR FROM PROFITABILITY_PRIMA_PROMEDIO
                WHERE PRODUCTO NOT IN (
                    6311,
                    6310,
                    6306,
                    6305,
                    6304,
                    6303,
                    6302,
                    6301,
                    1845
                )
                """
    
    # AND TO_DATE(FECHACONTABLE, 'YYYY-MM') BETWEEN (SYSDATE-365) AND SYSDATE

    PRIMAS_PROMEDIO = pd.read_sql(sql1, cnxn3)
    return PRIMAS_PROMEDIO


def obtener_tabla_productos():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    sql1 = """ SELECT * FROM ACTUARIA.TABLA_PRODUCTOS """

    TABLA_PRODUCTOS = pd.read_sql(sql1, cnxn3)
    return TABLA_PRODUCTOS


def obtener_socios():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    sql1 = """ SELECT * FROM ACTUARIA.PRF_SOCIOS """

    TABLA_PRODUCTOS = pd.read_sql(sql1, cnxn3)
    return TABLA_PRODUCTOS


def obtener_pricing():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    sql1 = """ SELECT * FROM ACTUARIA.PRICING """

    PRICING = pd.read_sql(sql1, cnxn3)
    return PRICING


def obtener_rt_riesgo():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    sql1 = """ SELECT CODPRODUCTO, GRUPOPU, SUM(CODPRODUCTO) FROM ACTUARIA.RT_RIESGO GROUP BY CODPRODUCTO, GRUPOPU """

    RT_RIESGO = pd.read_sql(sql1, cnxn3)
    return RT_RIESGO


def obtener_grupos_pu():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    sql1 = """ SELECT * FROM ACTUARIA.PRF_GRUPOS_PU """

    GRUPOSPU = pd.read_sql(sql1, cnxn3)
    return GRUPOSPU


def obtener_ofertas():
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)

    sql1 = """ SELECT * FROM ACTUARIA.PRF_OFERTAS """

    OFERTAS = pd.read_sql(sql1, cnxn3)
    return OFERTAS
