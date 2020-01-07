import cx_Oracle
import pandas as pd
import configparser
import sqlite3


def conection():
    # Cargar archivo de configuración principal
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    return cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    return sqlite3.connect('actuariaDatabase')

def create_register(request, filename, is_union=0):
    cnxn = conection()
    cur = cnxn.cursor()
    # out = En esta variable se guardara el # ID del insert
    out = cur.var(cx_Oracle.STRING)
    row = {'user_id': request.user.id, 'filename': filename, 'is_union': is_union, "u": out}
    cur.execute("INSERT INTO PROFITABILITY_PRESUPUESTO (USER_ID, FILE_INPUT, IS_UNION) VALUES (:user_id,:filename,:is_union) returning ID into :u", row)
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
    cur.execute("UPDATE PROFITABILITY_PRESUPUESTO SET FILE_OUTPUT = :file_output, SUCCESS = :success, TOTAL_TIME = :total_time, ERROR = :error WHERE ID=:user_id", row_update)
    cnxn.commit()
    # Recuperamos el numero de filas actualizadas
    rowcount = cur.rowcount
    assert isinstance(rowcount, object)
    return rowcount


def get_register_byID(user_id):
    cnxn = conection()
    sql = """SELECT *
                FROM  PROFITABILITY_PRESUPUESTO
                WHERE
                USER_ID = '""" + str(user_id) + """'
                AND STATUS = 1
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_register_byListIDs(ids_users):
    cnxn = conection()
    sql = """SELECT PROFITABILITY_PRESUPUESTO.*, AUTH_USER.FIRST_NAME, AUTH_USER.LAST_NAME
                FROM  PROFITABILITY_PRESUPUESTO
                JOIN AUTH_USER ON AUTH_USER.ID = PROFITABILITY_PRESUPUESTO.USER_ID
                WHERE
                PROFITABILITY_PRESUPUESTO.USER_ID IN """ + str(ids_users) + """
                AND STATUS = 1 AND FAVORITE = 1 AND IS_UNION = 0
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def get_register_all():
    cnxn = conection()
    sql = """SELECT PROFITABILITY_PRESUPUESTO.*, AUTH_USER.FIRST_NAME, AUTH_USER.LAST_NAME
                FROM  PROFITABILITY_PRESUPUESTO
                JOIN AUTH_USER ON AUTH_USER.ID = PROFITABILITY_PRESUPUESTO.USER_ID
                WHERE
                STATUS = 1
                """
    registers = pd.read_sql(sql, cnxn)
    return registers


def update_favorite(id, value, user_id):
    cnxn = conection()
    cur = cnxn.cursor()

    if value == '0':
        value_ = 1
        # -- Validar que no exista otro registro favorito del mismo usuario -- #
        sql = """SELECT * FROM
                        PROFITABILITY_PRESUPUESTO 
                        WHERE USER_ID = '""" + str(user_id) + """'
                        AND FAVORITE = 1
                        AND STATUS = 1
                        """
        user_register = pd.read_sql(sql, cnxn)
        if len(user_register > 1):
            return 0

    else:
        value_ = 0
    row_update = {'id': id, 'value': value_}
    cur.execute("UPDATE PROFITABILITY_PRESUPUESTO SET FAVORITE = :value WHERE ID=:id", row_update)
    cnxn.commit()
    # Recuperamos el numero de filas actualizadas
    rowcount = cur.rowcount
    return rowcount


def change_state(id, value):
    cnxn = conection()
    cur = cnxn.cursor()
    row_update = {'id': id, 'value': value}
    cur.execute("UPDATE PROFITABILITY_PRESUPUESTO SET STATUS = :value WHERE ID=:id", row_update)
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
