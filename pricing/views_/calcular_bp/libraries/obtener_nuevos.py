# -- Obtener los nuevos -- #

import pandas as pd
import numpy as np


def obtener_nuevos(Inputs):
    """
    Función cuyo objetivo principal es el calculo de los nuevos
    para todos los tipos de prima.

    :param Inputs: dataframe con la información de los Input cargados
    :return: OutPut con valores iniciales de:
    →→→ Mes
    →→→ fecha
    →→→ TEMP_key_numeromeses = (concatenación entre el productoID y el mes, en formato (productoID, Mes))
    →→→ porcentaje_penetración
    →→→ penetración
    →→→ nuevos
    """

    OutPut = Inputs
    # -- Obtener filas con fechas para cada uno de los productos -- #
    fechas = pd.date_range(start='01/03/2019', periods=120, freq='MS')
    fechas = fechas.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    fechas = pd.DataFrame({'fecha': fechas})
    fechas['Mes'] = fechas.index + 1

    OutPut['tmp'] = 1
    fechas['tmp'] = 1
    OutPut = pd.merge(OutPut, fechas, on=['tmp'])
    OutPut['fecha'] = pd.to_datetime(OutPut['fecha'], format='%Y-%m-%d').dt.date

    OutPut['TEMP_key_numeromeses'] = '(' + OutPut['Producto'].astype(str) + ', ' + OutPut['Mes'].astype(str) + ')'

    # -- Obtener penetración -- #
    OutPut['porcentaje_penetración'] = np.where(
        OutPut['Mes'] < OutPut['Se alcanza la penetración en No. Meses'],
        OutPut['Mes'] / OutPut['Se alcanza la penetración en No. Meses'],
        1
    )
    OutPut['penetración'] = OutPut['Penetración'] * OutPut['porcentaje_penetración']
    # -- TODO: Aplicar % Stress -- #
    OutPut['penetración'] = OutPut['penetración'] * OutPut['Stress test Penetration decrease']

    # -- Obtener nuevos -- #
    OutPut['nuevos'] = np.where(
        OutPut['Mes'] <= OutPut['Duración de producción en meses'],
        np.where(
            ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
            0,
            (OutPut['Clientes potenciales/mes'] * OutPut['penetración'] * ((1 + OutPut['Tasa crecimiento mensual']) ** (OutPut['Mes'] - 1)))
        ),
        0
    )

    return OutPut
