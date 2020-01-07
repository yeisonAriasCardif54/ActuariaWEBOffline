''' Generar DataFrame con OutPut y elementos iniciales: '''

import pandas as pd
import numpy as np

import time


def obtener_output_inicial(parametros_st, parametros_nv, mesunoproyeccion, meses, data_socios, data_ofertas, data_t_primas):
    # start_time = time.time()
    data_filter = [
        'Id_Tool',
        'Id_Socio',
        'Id_T.Oferta',
        'Duración',
        'Id_T.Prima',
        'Vlr. Prima Prom',
        'Mes Inicio',
        'Caida',
        'Frecuencia',
        'Comisión',
        'ClaimsRate_Y1',
        'ClaimsRate_Y2',
        'ClaimsRate_Y3+',
        '% VAT',
        '% Com Non',
        '% incentivo',
        'C/U. Venta TMKT',
        'Cod. Producto',
        'Tipo Proyección',
        'Pent. Q1',
        'Pent. Q2',
        'Pent. Q3',
        'Pent. Q4',
        'Pent. Inicial Año 2',
        'Pent. Final Año 2',
        'Plazo Año 2',
        'Pent. Inicial Año 3',
        'Pent. Final Año 3',
        'Plazo Año 3',
        'Oferta CJ',
        'Capa',
        'Nombre Producto',
        'Linea Negocio Socio',
        '¿Aplica IPC?',
        'Overheads',
        'Id_ Grupo_PU',
        'Meses garantía fabricante',
        't CutOff',
        '%Part.Socio',
        '%Part.Broker',
        'Amortizacion/CambioPrima',
        'Ecosistema',
        'Inicio mes ecosistema',
        'Vector ajuste SKB',
        'Factor siniestralidad año 1',
        'Factor siniestralidad año 2',
    ]

    OutPut = pd.concat([parametros_st.filter(data_filter), parametros_nv.filter(data_filter)], sort=False)

    # -- Eliminar registros con Id_Tool cero o vacio
    OutPut = OutPut.query('Id_Tool > 0')

    OutPut = OutPut.fillna(0)
    OutPut['Id_Tool'] = OutPut['Id_Tool'].astype(int)

    # -- Declarar Mes Inicio=1, siempre y cuando valga 0
    OutPut['Mes Inicio'] = np.where(
        OutPut['Mes Inicio'] < 1,
        1,
        OutPut['Mes Inicio']
    )
    # -- Declarar Id_ Grupo_PU=24, siempre y cuando valga 0
    OutPut['Id_ Grupo_PU'] = np.where(
        OutPut['Id_ Grupo_PU'] < 1,
        24,
        OutPut['Id_ Grupo_PU']
    )

    # Obtener filas con fechas para cada uno de los productos
    fechas = pd.date_range(start=mesunoproyeccion, periods=meses, freq='MS')
    fechas = fechas.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    fechas = pd.DataFrame({'fecha': fechas})
    fechas['TEMP_numeromes'] = fechas.index + 1
    OutPut['tmp'] = 1
    fechas['tmp'] = 1
    OutPut = pd.merge(OutPut, fechas, on=['tmp'])
    OutPut['fecha'] = pd.to_datetime(OutPut['fecha'], format='%Y-%m-%d').dt.date

    # Obtener Socio
    OutPut.Id_Socio = OutPut.Id_Socio.astype(np.int64)
    OutPut = pd.merge(OutPut, data_socios, on=['Id_Socio'], how='left')

    # Obtener Tipo Oferta
    OutPut['Id_T.Oferta'] = OutPut['Id_T.Oferta'].astype(np.int64)
    OutPut = pd.merge(OutPut, data_ofertas, on=['Id_T.Oferta'], how='left')

    # Obtener Tipo de Prima
    OutPut['Id_T.Prima'] = OutPut['Id_T.Prima'].astype(np.int64)
    OutPut = pd.merge(OutPut, data_t_primas, on=['Id_T.Prima'], how='left')

    # Variable temporal ( Id_Tool, mes) - Utilizada en metodo obtener_desembolso
    OutPut['TEMP_key_numeromeses'] = '(' + OutPut['Id_Tool'].astype(str) + ', ' + OutPut['TEMP_numeromes'].astype(str) + ')'

    # Conversion especial para algunas columnas
    OutPut['Id_Tool'] = OutPut['Id_Tool'].astype(np.int64)
    OutPut['Meses garantía fabricante'] = OutPut['Meses garantía fabricante'].astype(np.int32)
    OutPut['Id_ Grupo_PU'] = OutPut['Id_ Grupo_PU'].astype(np.int64)
    OutPut['Amortizacion/CambioPrima'] = OutPut['Amortizacion/CambioPrima'].astype(np.int64)

    # print("\n\n obtener_output_inicial \n--- %s seconds ---" % (time.time() - start_time))
    # Retornar Dataframe
    return OutPut
