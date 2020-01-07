import cx_Oracle
import pandas as pd
import configparser
import sqlite3

def obtener_datos_estaticos_DB():
    # Cargar archivo de configuración principal
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Conexión
    ip = config.get('database', 'DATABASE_HOST')
    port = config.get('database', 'DATABASE_PORT')
    SID = config.get('database', 'DATABASE_NAME')  # Oracle System ID - Instancia
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)  # Realizar Data Source Name (Nombre de origen de datos)
    cnxn3 = cx_Oracle.connect(config.get('database', 'DATABASE_USER'), config.get('database', 'DATABASE_PASSWORD'), dsn_tns)
    """
    cnxn3 = sqlite3.connect('actuariaDatabase')
    
    # Consultar socios
    sql1 = """ SELECT * FROM PRF_SOCIOS """
    socios = pd.read_sql(sql1,cnxn3)
    socios.rename(columns={
            'ID':'Id_Socio',
            'NOMBRE':'Socio'
            }, inplace=True)
    
    
    # Consultar ofertas
    sql2 = """ SELECT * FROM PRF_OFERTAS """
    ofertas = pd.read_sql(sql2,cnxn3)
    ofertas.rename(columns={
            'ID':'Id_T.Oferta',
            'NOMBRE':'Oferta'
            }, inplace=True)
    
    
    # Consultar tipos de primas
    sql3 = """ SELECT * FROM PRF_TIPOS_PRIMA """
    tipos_prima = pd.read_sql(sql3,cnxn3)
    tipos_prima.rename(columns={
            'ID':'Id_T.Prima',
            'NOMBRE':'Tipo Prima'
            }, inplace=True)
    
    
    # Consultar grupos PU
    sql4 = """ SELECT * FROM PRF_GRUPOS_PU """
    grupos_pu = pd.read_sql(sql4,cnxn3)
    grupos_pu.rename(columns={
            'ID':'Id_Grupo',
            'NOMBRE':'Grupo_PU',
            'CAPITALCOST':'CapitalCost',
            'SHARE_PU':'Share_PU',
            'PAID_LIBERACION':'Paid/Liberación',
            'CLAIMS_RESULT_TO_SHARE':'Claims Result to Share',
            'PORC_OVERHEAD_GRUPAL':'% Overhead_Grupal'
            }, inplace=True)
    
    
    # Cerrar conexion
    cnxn3.close()
    
    
    return  { 
                'socios': socios,
                'ofertas': ofertas,
                'tipos_prima': tipos_prima,
                'grupos_pu': grupos_pu,
            }