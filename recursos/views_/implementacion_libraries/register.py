import cx_Oracle
import pandas as pd
import configparser


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


def get_register_all(category):
    extra_where = ''
    #if category != 0:
    #    extra_where = ' AND PRICING_TARIFICADORES_TAGS.ID = ' + str(category)
    cnxn = conection()
    sql = """SELECT PRICING_TARIFICADORES.*, AUTH_USER.FIRST_NAME, AUTH_USER.LAST_NAME, PRICING_TARIFICADORES_TAGS.NOMBRE, PRICING_TARIFICADORES_TAGS.COLOR
                FROM  PRICING_TARIFICADORES
                JOIN AUTH_USER ON AUTH_USER.ID = PRICING_TARIFICADORES.USER_ID
                LEFT JOIN PRICING_TARIFICADORES_TAGS ON PRICING_TARIFICADORES.TAG = PRICING_TARIFICADORES_TAGS.ID
                WHERE
                STATUS = 1
                AND PRICING_TARIFICADORES_TAGS.NOMBRE = 'Publicado'
                ORDER BY PRICING_TARIFICADORES.ID DESC
                """
    registers = pd.read_sql(sql, cnxn)
    return registers

def get_register_byId(id):
    extra_where = ''
    #if category != 0:
    #    extra_where = ' AND PRICING_TARIFICADORES_TAGS.ID = ' + str(category)
    cnxn = conection()
    sql = """SELECT PRICING_TARIFICADORES.*, AUTH_USER.FIRST_NAME, AUTH_USER.LAST_NAME, PRICING_TARIFICADORES_TAGS.NOMBRE, PRICING_TARIFICADORES_TAGS.COLOR
                FROM  PRICING_TARIFICADORES
                JOIN AUTH_USER ON AUTH_USER.ID = PRICING_TARIFICADORES.USER_ID
                LEFT JOIN PRICING_TARIFICADORES_TAGS ON PRICING_TARIFICADORES.TAG = PRICING_TARIFICADORES_TAGS.ID
                WHERE
                STATUS = 1
                AND PRICING_TARIFICADORES.ID = """ + str(id) + """
                ORDER BY PRICING_TARIFICADORES.ID DESC
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_all_coberturas():
    cnxn = conection()
    sql = """SELECT PRICING_TAN_COBERTURAS.*,
                PRICING_TAN_COBERTURAS.ID || '-' || PRICING_TAN_COBERTURAS.COBERTURA AS "FULLCOBERTURA"
                FROM  PRICING_TAN_COBERTURAS
                """
    registers = pd.read_sql(sql, cnxn)
    return registers