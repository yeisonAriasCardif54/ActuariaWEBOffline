import pandas as pd
from os.path import dirname, join
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import cx_Oracle
import configparser
import sqlite3


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
        "title": 'Edades',
        "area": 'ExPost',
        "herramienta": 'life_eg',
        "file": 'expost/life_eg.html',
    }
    return render(request, "principal/base.html", configurationView)


def selects(request):

    """
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
                             """
    cnxn = sqlite3.connect('actuariaDatabase')

    
    # Aplicar filtros
    socio_seleccionado = request.POST.getlist('socios')
    socio_seleccionado = [i for i in socio_seleccionado if i != '']
    socio_seleccionado = [sub_item for item in socio_seleccionado for sub_item in item.split(",")]
    
    canal_seleccionado = request.POST.getlist('canales')
    canal_seleccionado = [i for i in canal_seleccionado if i != '']
    canal_seleccionado = [sub_item for item in canal_seleccionado for sub_item in item.split(",")]
    
    tipo_seleccionado = request.POST.getlist('tipos')
    tipo_seleccionado = [i for i in tipo_seleccionado if i != '']
    tipo_seleccionado = [sub_item for item in tipo_seleccionado for sub_item in item.split(",")]
    
    linea_fina_seleccionado = request.POST.getlist('linea_fina')
    linea_fina_seleccionado = [i for i in linea_fina_seleccionado if i != '']
    linea_fina_seleccionado = [sub_item for item in linea_fina_seleccionado for sub_item in item.split(",")]  

    producto_seleccionado = request.POST.getlist('productos')
    producto_seleccionado = [i for i in producto_seleccionado if i != '']
    producto_seleccionado = [sub_item for item in producto_seleccionado for sub_item in item.split(",")]
    
    database_seleccionado = request.POST.getlist('database')
    database_seleccionado = [i for i in database_seleccionado if i != '']
    database_seleccionado = [sub_item for item in database_seleccionado for sub_item in item.split(",")]

    where2 = ' WHERE 1=1 '

    if len(socio_seleccionado) > 0:
        a = tuple(socio_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        socio_seleccionado = tuple(l)
        where2 = where2 + " AND SOCIO IN " + str(socio_seleccionado)
    
    if len(canal_seleccionado) > 0:
        a = tuple(canal_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        canal_seleccionado = tuple(l)
        where2 = where2 + " AND CANAL IN " + str(canal_seleccionado)    
        
    if len(tipo_seleccionado) > 0:
        a = tuple(tipo_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        tipo_seleccionado = tuple(l)
        where2 = where2 + " AND TIPO IN " + str(tipo_seleccionado)     
        
    if len(linea_fina_seleccionado) > 0:
        a = tuple(linea_fina_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        linea_fina_seleccionado = tuple(l)
        where2 = where2 + " AND LINEA_NEGOCIO IN " + str(linea_fina_seleccionado)      

    if len(producto_seleccionado) > 0:
        a = tuple(producto_seleccionado);
        b = 0
        l = list(a);
        l.append(b)
        producto_seleccionado = tuple(l)
        where2 = where2 + " AND PRODUCTO IN " + str(producto_seleccionado)
        
    if len(database_seleccionado) > 0:
        a = tuple(database_seleccionado);
        b = '1=1'
        l = list(a);
        l.append(b)
        database_seleccionado = tuple(l)
        where2 = where2 + " AND DATA IN " + str(database_seleccionado)   
        
    #print(where2)    

    #############################################################################################################

    # Consultar Base de Datos

    # Query Unicos Tabla Productos
    sql1 = """  SELECT DISTINCT PRODUCTO, SOCIO, CANAL, TIPO, LINEA_NEGOCIO, DATA_DATE, GENERO, AVG_GENERO, MEDIAN_GENERO, AVG_TOTAL, MEDIAN_TOTAL, DATA, RANGO 
                FROM DASH_LIFE_AGES   
                """ + where2 ;

    # Dataframe Data
    df_data = pd.read_sql(sql1, cnxn);
    df_data['PRODUCTO'] = df_data['PRODUCTO'].astype(int)
    #df_data.to_excel('C:/Users/b89591/Desktop/df_data.xlsx')
    lista = list(df_data['PRODUCTO'].unique())
    lista.insert(0, 0)
    #print('lista',lista)
        
    #Pivot Data
    df_data = df_data[(df_data['RANGO'].isin(['RANGO']))]
    df_avg =  pd.pivot_table(data=df_data, values=['AVG_GENERO','MEDIAN_GENERO'], columns=['GENERO'],
                           aggfunc=np.mean).reset_index()
    df_avg.rename(columns={'index':'Medidas'}, inplace=True)
    df_avg['Total'] =  df_avg.iloc[:, -2:].mean(axis=1)
    #df_avg.to_excel('C:/Users/b89591/Desktop/df_avg.xlsx')
 
    # Query Data
    sql2 = """  
            SELECT GENERO,CATEGORIA,TOTAL FROM DASH_LIFE_AGES WHERE PRODUCTO IN {0}
            """.format(tuple(lista));

    # Dataframe Edades
    df_tecn_orig = pd.read_sql(sql2, cnxn);
    print('\n\n\n - df_tecn_orig - \n\n\n')
    print(df_tecn_orig)
    #df_tecn_orig.to_excel('C:/Users/b89591/Desktop/df_tecn_orig.xlsx')
    df_tecn_orig = df_tecn_orig.fillna('No-Info')
    df_tecn_orig = df_tecn_orig[(df_tecn_orig['CATEGORIA'].isin(['Otros']) ==  False)]
    
    
    #Pivot Data
    tria_ = pd.pivot_table(data=df_tecn_orig, values='TOTAL', index=['CATEGORIA'], columns=['GENERO'],
                           aggfunc=np.sum).reset_index()
    #tria_.to_excel('C:/Users/b89591/Desktop/tria_.xlsx')
    
    
    tria_gra1 = tria_.copy()
       
    decimals = 2
    
    tria_gra1['Male_Perc'] = (tria_gra1['Male'] / tria_gra1['Male'].sum()) * 100
    tria_gra1['Male_Perc'] = tria_gra1['Male_Perc'].apply(lambda x: round(x, decimals))
    
    tria_gra1['Female_Perc'] = (tria_gra1['Female'] / tria_gra1['Female'].sum()) * 100
    tria_gra1['Female_Perc'] = tria_gra1['Female_Perc'].apply(lambda x: round(x, decimals))
    
    tria_gra1['Male']      = tria_gra1['Male'] * -1
    tria_gra1['Male_Perc'] = tria_gra1['Male_Perc'] * -1
    
    #Sort Column
    tria_gra1.sort_values(['CATEGORIA'], ascending=[False], inplace=True)

    #############################################################################################################################################################
    
    tria_gra1 = tria_gra1[(tria_gra1['CATEGORIA'].isin(['Otros']) ==  False)]
    #print(tria_gra1) 
    data_graph_a = []
    for i, row in tria_gra1.iterrows():

        data_graph_a.append({

            "CATEGORIA": str(row['CATEGORIA']),
            "Female": str(row['Female']),
            "Female_Perc": str(row['Female_Perc']),
            "Male": str(row['Male']),
            "Male_Perc": str(row['Male_Perc']),     
             
        })
       
    #############################################################################################################################################################
    tria_table = tria_.copy()
    tria_table = tria_table.reset_index(drop = True)
    tria_table['No-Info'] = 0
    
    #tria_table['Male'] = tria_table['Male'] * -1
    tria_table = tria_table.fillna(0)
    #tria_table['TOTAL'] = tria_table['Female'] + tria_table['Male'] + tria_table['No-Info']
    
    #print('longitud', tria_table.shape[1])
    
    if ( tria_table.shape[1] == 4):
        tria_table['TOTAL'] = tria_table.iloc[:, -3:].sum(axis=1)
    else:
        tria_table['TOTAL'] = tria_table.iloc[:, -2:].sum(axis=1)
        tria_table['No-Info'] = 0
    
    #tria_table.to_excel('C:/Users/b89591/Desktop/tria_table.xlsx')
    
    #df['Fruit Total']= df.iloc[:, -4:-1].sum(axis=1)
    
    tria_table['PORC'] = tria_table['TOTAL'] / tria_table['TOTAL'].sum()
 
    # Calcular row Totales
    tria_table.loc[len(tria_table), ['CATEGORIA', 'Female', 'Male', 'No-Info', 'TOTAL', 'PORC']] = ['Total',
                                                                                tria_table['Female'].sum(),
                                                                                 tria_table['Male'].sum(),
                                                                                 tria_table['No-Info'].sum(),
                                                                                tria_table['TOTAL'].sum(),
                                                                                tria_table['PORC'].sum()]
    tria_table = tria_table.fillna(0)    
    
    data_table_a = []
    for i, row in tria_table.iterrows():
        Female =  '{0:,.0f}'.format(row['Female'])
        Male =    '{0:,.0f}'.format(row['Male'])
        TOTAL =   '{0:,.0f}'.format(row['TOTAL'])
        PORC =    '{:.2%}'.format(row['PORC'])
        NO_INFO = '{0:,.0f}'.format(row['No-Info'])
        

        data_table_a.append({
            "CATEGORIA": str(row['CATEGORIA']),
            "Female": Female,
            "Male": Male,
            "TOTAL": TOTAL,
            "PORC": PORC,
            "No_Info": NO_INFO,
        })
    #print('AAA',data_table_a)

    #############################################################################################################################################################
    data_table_b = []
    for i, row in df_avg.iterrows():
        Female = '{0:,.0f}'.format(row['Female'])
        Male =   '{0:,.0f}'.format(row['Male'])
        Total =  '{0:,.0f}'.format(row['Total'])
        #PORC =   '{:.2%}'.format(row['PORC'])

        data_table_b.append({
            "Medidas": str(row['Medidas']),
            "Female": Female,
            "Male": Male,
            "Total": Total,
        })
    #print('BBB',data_table_b)
    # UNICOS SELECT
    socios = list(df_data['SOCIO'].unique());
    socios.sort();
    #print('socios',socios)
    
    canales = list(df_data['CANAL'].unique());
    canales.sort();
    
    tipos = list(df_data['TIPO'].unique());
    tipos.sort();
    
    prod_fina = list(df_data['LINEA_NEGOCIO'].unique());
    prod_fina.sort();

    productos = list(df_data['PRODUCTO'].astype(str).unique());
    productos.sort(key=int)
    #productos = ['601']
    #print('productos', productos)
    
    database = list(df_data['DATA'].unique());
    database.sort();
    #print(database)
    
    cnxn.close(); 
    #########################################################################################################################################################################

    
    return JsonResponse([socios, canales, tipos, prod_fina, productos, database, data_graph_a, data_table_a, data_table_b], safe=False)
     #                    graph_01, graph_02, graph_03, graph_04, graph_05, graph_06 ], safe=False)