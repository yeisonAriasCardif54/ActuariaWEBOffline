from django.shortcuts import render
import os
import pandas as pd
import numpy as np

# pd.options.display.float_format = '$ {:,.0f} M'.format
pd.options.display.float_format = '{:,.1f} M'.format


def index(request):
    # Obtener variables POST
    id_tab_content = request.POST.get('id_tab_content')
    filename, analizarPor = request.POST.get('file_summary'), request.POST.get('analizarPor')
    filtro0, filtro1, filtro2, filtro3, filtro4, filtro5, filtro6 = request.POST.getlist('filtro0'), request.POST.getlist('filtro1'), request.POST.getlist('filtro2'), request.POST.getlist('filtro3'), request.POST.getlist('filtro4'), request.POST.getlist('filtro5'), request.POST.getlist('filtro6')
    valores = request.POST.getlist('valores')

    # Validar datos iniciales
    if analizarPor == None:
        analizarPor = '0'
    if filtro0 == None:
        filtro0 = []
    if filtro1 == None:
        filtro1 = []
    if filtro2 == None:
        filtro2 = []
    if filtro3 == None:
        filtro3 = []
    if filtro4 == None:
        filtro4 = []
    if filtro5 == None:
        filtro5 = []
    if filtro6 == None:
        filtro6 = []
    if valores == []:
        # Por defecto: GWP neto y Total Commissions
        valores = ['GWP neto', 'Total Commissions']
    valor1 = valores[0]
    valor2 = valores[1]
    folder = 'static/profitability/update_presupuesto'
    file = folder + '/' + filename
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../' + file)
    # -- INICIO - Determinar la forma de lectura del archivo (dependiendo si es csv o xlsx)
    # -- Extraer extension
    file_ext = filename[-4:]
    if file_ext == 'xlsx':
        output = pd.DataFrame(pd.read_excel(path, sheet_name='OutPut'))
    else:
        output = pd.read_csv(path)
    # -- FIN- Determinar la forma de lectura del archivo (dependiendo si es csv o xlsx)
    # Agrupar información
    output = output.filter(['Socio', 'Linea Negocio Socio', 'Tipo Oferta', 'Producto', 'Capa', valor1, valor2, 'Año', 'Fecha', 'Tipo_Proyección','Oferta CJ'])
    output = output.fillna(0)

    output['Año'] = output['Año'].astype(int)
    output['Producto'] = output['Producto'].astype(str)

    # Datos de listas desplegables
    socios = output['Socio'].unique()
    lineas = output['Linea Negocio Socio'].unique()
    tipos_oferta = output['Tipo Oferta'].unique()
    productos = output['Producto'].unique()
    productos = productos.astype(str)
    capas = output['Capa'].unique()
    tipos_proyeccion = output['Tipo_Proyección'].unique()
    segmentos = output['Oferta CJ'].unique()
    # Aplicar filtros
    if len(filtro0) > 0:  # Socio
        output = output.loc[output['Socio'].isin(filtro0)]
    if len(filtro1) > 0:  # Linea de negocio
        output = output.loc[output['Linea Negocio Socio'].isin(filtro1)]
    if len(filtro2) > 0:  # Tipo Oferta
        output = output.loc[output['Tipo Oferta'].isin(filtro2)]
    if len(filtro3) > 0:  # Producto
        output = output.loc[output['Producto'].isin(filtro3)]
    if len(filtro4) > 0:  # Capa
        output = output.loc[output['Capa'].isin(filtro4)]
    if len(filtro5) > 0:  # Tipo_Proyección
        output = output.loc[output['Tipo_Proyección'].isin(filtro5)]
    if len(filtro6) > 0:  # Segmentos
        output = output.loc[output['Oferta CJ'].isin(filtro6)]
    # Convertir valores en millones

    output[valor1] = output[valor1] / 1000000
    output[valor1] = output[valor1].apply(lambda x: round(x, 2))
    output[valor2] = output[valor2] / 1000000
    output[valor2] = output[valor2].apply(lambda x: round(x, 2))

    # Convertir a fecha
    output['Fecha'] = pd.to_datetime(output['Fecha'], format='%Y-%m-%d')
    output['Fecha'] = output['Fecha'].dt.year
    output['Año'] = output['Fecha']

    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\outputResumen.xlsx', engine='xlsxwriter')
    output.to_excel(writer, sheet_name='Resumen', index=None, float_format='%.3f')
    writer.save()

    # Calculando resumen
    analizarPorNombre = ''
    if analizarPor == '0':  # Analizar por socios
        analizarPorNombre = 'Socio'
        output2 = pd.pivot_table(output, index=["Socio"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)
    if analizarPor == '1':  # Analizar por Linea Negocio Socio
        analizarPorNombre = 'Linea Negocio Socio'
        output2 = pd.pivot_table(output, index=["Linea Negocio Socio"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)
    if analizarPor == '2':  # Analizar por Tipo Oferta
        analizarPorNombre = 'Tipo Oferta'
        output2 = pd.pivot_table(output, index=["Tipo Oferta"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)
    if analizarPor == '3':  # Analizar por Producto
        analizarPorNombre = 'Producto'
        output2 = pd.pivot_table(output, index=["Producto"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)
    if analizarPor == '4':  # Analizar por Capa
        analizarPorNombre = 'Capa'
        output2 = pd.pivot_table(output, index=["Capa"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)
    if analizarPor == '5':  # Analizar por Tipo de proyección
        analizarPorNombre = 'Tipo_Proyección'
        output2 = pd.pivot_table(output, index=["Tipo_Proyección"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)
    if analizarPor == '6':  # Analizar por Segmento - Oferta CJ
        analizarPorNombre = 'Oferta CJ'
        output2 = pd.pivot_table(output, index=["Oferta CJ"], columns=['Año'], values=[valor1, valor2], aggfunc=np.sum)

    # -- Reemplazar valores NaN -- #ø
    where_are_NaNs = np.isnan(output2)
    output2[where_are_NaNs] = 0

    total = output2.apply(np.sum)

    # Extraer información requerida para DashBoard
    # Años
    años = output['Año'].tolist()
    años = np.unique(años)
    if int(len(años)) > 0:
        anchoChart = 24 / int(len(años))
    else:
        anchoChart = 12

    # Construir chart.data
    dataChart = {}
    dataChart_total = {}
    for año in años:
        colname = '%d' % año.astype(int)
        dataChart[colname] = []
        dataChart_total[colname] = []
        # Suma de 'valor1' y 'valor2'
        sumGWP = output.query('Año==' + str(año)).groupby(['Año', analizarPorNombre])[valor1, valor2].agg('sum')
        # Convertir a dataframe
        sumGWP = sumGWP.apply(list).apply(pd.Series)
        sumGWP = sumGWP.sort_values(by=valor1, ascending=False)
        # Suma de valor2
        for i, row in sumGWP.iterrows():
            dataChart[colname].append(
                {
                    "category": str(i[1]),
                    'valor1': str(row[valor1].round(2)),
                    'valor2': str(row[valor2].round(2))
                }
            )
        dataChart_total[colname].append(
            {
                "category": 'Total',
                'valor1': str(sumGWP[valor1].sum().round(2)),
                'valor2': str(sumGWP[valor2].sum().round(2))
            }
        )

    output2 = output2.append(pd.DataFrame(total.values, index=total.keys()).T, ignore_index=False)
    output2 = output2.rename(index={0: 'Total (M)'})
    output2 = output2.applymap("{:,.2f} M".format)
    table = output2.to_html(classes='table table-striped- table-bordered table-hover table-checkable table-resumen', border=0)

    # Mostrar total en miles de millones
    configurationView = {
        'dataChart': dataChart,
        'dataChart_total': dataChart_total,
        'anchoChart': int(anchoChart),
        'años': años,
        'id_tab_content': id_tab_content,
        'filename': filename,
        'analizarPor': analizarPor,
        'socios': socios,
        'lineas': lineas,
        'tipos_oferta': tipos_oferta,
        'productos': productos,
        'capas': capas,
        'tipos_proyeccion': tipos_proyeccion,
        'segmentos': segmentos,
        'filtro0': filtro0,
        'filtro1': filtro1,
        'filtro2': filtro2,
        'filtro3': filtro3,
        'filtro4': filtro4,
        'filtro5': filtro5,
        'valores': valores,
        'valor1': valor1,
        'valor2': valor2,
        'table': table,
    }
    return render(request, "profitability/presupuesto_resumen.html", configurationView)
