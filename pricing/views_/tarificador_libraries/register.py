import cx_Oracle
import pandas as pd
import configparser
import sqlite3


def conection():
    """
    # Cargar archivo de configuración principal
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    return cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    cnxn3 = sqlite3.connect('actuariaDatabase')


def create_register(request, filename):
    cnxn = conection()
    cur = cnxn.cursor()
    # out = En esta variable se guardara el # ID del insert
    out = cur.var(cx_Oracle.STRING)
    row = {'user_id': request.user.id, 'filename': filename, "u": out}
    cur.execute("INSERT INTO PRICING_TARIFICADORES (USER_ID, FILE_INPUT) VALUES (:user_id,:filename) returning ID into :u", row)
    cnxn.commit()
    # Recuperamos el numero de filas insertadas
    rowcount = cur.rowcount
    # Recuperamos el ID del registro insertado
    insert_id = out.getvalue()[0]
    return rowcount, insert_id


def create_register_tag(nombre, color):
    cnxn = conection()
    cur = cnxn.cursor()
    # out = En esta variable se guardara el # ID del insert
    out = cur.var(cx_Oracle.STRING)
    row = {'nombre': nombre, 'color': color, "u": out}
    cur.execute("INSERT INTO PRICING_TARIFICADORES_TAGS (NOMBRE, COLOR) VALUES (:nombre,:color) returning ID into :u", row)
    cnxn.commit()
    # Recuperamos el numero de filas insertadas
    rowcount = cur.rowcount
    # Recuperamos el ID del registro insertado
    insert_id = out.getvalue()[0]
    return rowcount, insert_id


def update_register(insert_id, file_output, success, total_time, error=''):
    cnxn = conection()
    cur = cnxn.cursor()
    row_update = {'user_id': insert_id, 'file_output': file_output, "success": success, "total_time": total_time, "error": error}
    cur.execute("UPDATE PRICING_TARIFICADORES SET FILE_OUTPUT_TAN = :file_output, SUCCESS_TAN = :success, TOTAL_TIME_TAN = :total_time, ERROR_TAN = :error WHERE ID=:user_id", row_update)
    cnxn.commit()
    # Recuperamos el numero de filas actualizadas
    rowcount = cur.rowcount
    assert isinstance(rowcount, object)
    return rowcount


def update_register_tag(nombre, color, tag):
    cnxn = conection()
    cur = cnxn.cursor()
    row_update = {'nombre': nombre, 'color': color, "tag": tag}
    cur.execute("UPDATE PRICING_TARIFICADORES_TAGS SET COLOR = :color, NOMBRE = :nombre WHERE ID=:tag", row_update)
    cnxn.commit()
    # Recuperamos el numero de filas actualizadas
    rowcount = cur.rowcount
    assert isinstance(rowcount, object)
    return rowcount


def get_register_byID(user_id):
    cnxn = conection()
    sql = """SELECT *
                FROM  PRICING_TARIFICADORES
                WHERE
                USER_ID = '""" + str(user_id) + """'
                AND STATUS = 1
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_tag_byId(id):
    cnxn = conection()
    sql = """SELECT *
                FROM  PRICING_TARIFICADORES_TAGS
                WHERE
                ID = '""" + str(id) + """'
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_register_byListIDs(ids_users):
    cnxn = conection()
    sql = """SELECT PRICING_TARIFICADORES.*, AUTH_USER.FIRST_NAME, AUTH_USER.LAST_NAME
                FROM  PRICING_TARIFICADORES
                JOIN AUTH_USER ON AUTH_USER.ID = PRICING_TARIFICADORES.USER_ID
                WHERE
                PRICING_TARIFICADORES.USER_ID IN """ + str(ids_users) + """
                AND STATUS = 1 AND FAVORITE = 1 AND IS_UNION = 0
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_count_registers():
    cnxn = conection()
    sql = """SELECT COUNT(PRICING_TARIFICADORES.ID) AS TOTAL
                FROM  PRICING_TARIFICADORES
                JOIN AUTH_USER ON AUTH_USER.ID = PRICING_TARIFICADORES.USER_ID
                LEFT JOIN PRICING_TARIFICADORES_TAGS ON PRICING_TARIFICADORES.TAG = PRICING_TARIFICADORES_TAGS.ID
                WHERE
                STATUS = 1
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_register_all(category):
    extra_where = ''
    if category != 0:
        extra_where = ' AND PRICING_TARIFICADORES_TAGS.ID = ' + str(category)
    cnxn = conection()
    sql = """SELECT PRICING_TARIFICADORES.*, AUTH_USER.FIRST_NAME, AUTH_USER.LAST_NAME, PRICING_TARIFICADORES_TAGS.NOMBRE, PRICING_TARIFICADORES_TAGS.COLOR
                FROM  PRICING_TARIFICADORES
                JOIN AUTH_USER ON AUTH_USER.ID = PRICING_TARIFICADORES.USER_ID
                LEFT JOIN PRICING_TARIFICADORES_TAGS ON PRICING_TARIFICADORES.TAG = PRICING_TARIFICADORES_TAGS.ID
                WHERE
                STATUS = 1
                """ + extra_where + """
                ORDER BY PRICING_TARIFICADORES.ID DESC
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_categories():
    cnxn = conection()
    sql = """SELECT 
                PRICING_TARIFICADORES_TAGS.ID, 
                PRICING_TARIFICADORES_TAGS.NOMBRE, 
                PRICING_TARIFICADORES_TAGS.COLOR,
                (
                SELECT COUNT(PRICING_TARIFICADORES.ID) AS TOTAL
                FROM  PRICING_TARIFICADORES
                JOIN AUTH_USER ON AUTH_USER.ID = PRICING_TARIFICADORES.USER_ID
                LEFT JOIN PRICING_TARIFICADORES_TAGS ON PRICING_TARIFICADORES.TAG = PRICING_TARIFICADORES_TAGS.ID
                WHERE
                PRICING_TARIFICADORES.TAG = PRICING_TARIFICADORES_TAGS.ID
                AND STATUS = 1
                ) AS TOTAL
                FROM PRICING_TARIFICADORES_TAGS
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def update_favorite(id, idcategory):
    cnxn = conection()
    cur = cnxn.cursor()
    row_update = {'id': id, 'value': idcategory}
    cur.execute("UPDATE PRICING_TARIFICADORES SET TAG = :value WHERE ID=:id", row_update)
    cnxn.commit()
    # Recuperamos el numero de filas actualizadas
    rowcount = cur.rowcount
    return rowcount


def change_state(id, value):
    cnxn = conection()
    cur = cnxn.cursor()
    row_update = {'id': id, 'value': value}
    cur.execute("UPDATE PRICING_TARIFICADORES SET STATUS = :value WHERE ID=:id", row_update)
    cnxn.commit()
    # Recuperamos el numero de filas actualizadas
    rowcount = cur.rowcount
    return rowcount


def get_id_group(user_id):
    cnxn = conection()
    sql = """SELECT UG.GROUP_ID FROM
                AUTH_USER U
                JOIN AUTH_USER_GROUPS UG ON U.ID = UG.USER_ID
                WHERE U.ID = '""" + str(user_id) + """'
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_id_users_by_idGroup(id_group):
    cnxn = conection()
    sql = """SELECT UG.* FROM 
            AUTH_USER U
            INNER JOIN AUTH_USER_GROUPS UG ON UG.USER_ID = U.ID
            WHERE UG.GROUP_ID = '""" + str(id_group) + """'
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def update_pricing_acquisitionCost(newData):
    cnxn = conection()
    newData['UNIT_COST_IN_LC'] = newData.apply(lambda x: "{:.7f}".format(x['UNIT_COST_IN_LC']), axis=1)
    cur = cnxn.cursor()
    cur.execute('truncate table "PRICING_DATA_ACQUISITION_COSTS" drop storage')
    cnxn.commit()
    for i, row in newData.iterrows():
        cur = cnxn.cursor()
        row = {
            'COUNTRY': row['COUNTRY'],
            'BUSINESS_LINE': row['BUSINESS_LINE'],
            'PARTNER_GROUP': row['PARTNER_GROUP'],
            'DESTINATION': row['DESTINATION'],
            'COST_TYPE': row['COST_TYPE'],
            'UNIT_COST_IN_LC': row['UNIT_COST_IN_LC']
        }
        cur.execute("INSERT INTO ARIASYE.PRICING_DATA_ACQUISITION_COSTS (COUNTRY,BUSINESS_LINE,PARTNER_GROUP,DESTINATION,COST_TYPE,UNIT_COST_IN_LC) VALUES (:COUNTRY,:BUSINESS_LINE,:PARTNER_GROUP,:DESTINATION,:COST_TYPE,:UNIT_COST_IN_LC)", row)
        cnxn.commit()
    return 1
