''' Calculo de los ingresos financieros '''

import pandas as pd
import numpy as np
import time


def calcular_ingresos_financieros(OutPut, finanp, meses):
    # start_time = time.time()
    OutPut_TEMP = pd.DataFrame({});
    OutPut_TEMP['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    OutPut_TEMP['gwp'] = OutPut['gwp']
    OutPut_TEMP['incurC'] = OutPut['incurC']
    OutPut_TEMP['vigentes'] = OutPut['vigentes']
    OutPut_TEMP['Id_Tool'] = OutPut['Id_Tool']

    OutPut_TEMP['suminC'] = 0
    OutPut_TEMP['sumGwp'] = 0
    OutPut['reqcapy'] = 0
    OutPut['reqcap'] = 0
    OutPut['fincomer'] = 0
    OutPut['fincomec'] = 0

    OutPut_TEMP['suminC'] = OutPut_TEMP['suminC'].astype(np.float64)
    OutPut_TEMP['sumGwp'] = OutPut_TEMP['sumGwp'].astype(np.float64)
    OutPut['reqcap'] = OutPut['reqcap'].astype(np.float64)
    OutPut['fincomer'] = OutPut['fincomer'].astype(np.float64)
    OutPut['fincomec'] = OutPut['fincomec'].astype(np.float64)

    # Si el tipo de proyeccion es Stock, el DAC es igual a cero
    OutPut['dac'] = np.where(
        OutPut['Tipo Proyección'] == 'Stock',
        0,
        OutPut['dac']
    )

    # Ingresos financieros por reservas
    OutPut['fincomer'] = (OutPut['upr'] - OutPut['dac']) * (((finanp + 1) ** (1 / 12)) - 1)  # Ingreso financiero mensual

    # Determinar el acumulado de claims de los ùltimos 36 meses:
    OutPut_TEMP['TEMP_incurC-36'] = OutPut['incurC'].shift(36)

    # Determinar el acumulado de GWP de los ùltiumo 12 meses:
    OutPut_TEMP['TEMP_gwp-12'] = OutPut['gwp'].shift(12)

    # Verificar la existencia de vigentes para futuros calculos
    OutPut_TEMP['existen_vigentes'] = np.where(OutPut_TEMP['vigentes'] > 0, 1, 0)

    ########## Calcular suminC ##########
    # Calcular columna incurC/3 para el calculo de suminC
    OutPut_TEMP['incurC_recal'] = np.where(
        (OutPut_TEMP['TEMP_numeromes'] <= 36),
        (OutPut_TEMP['incurC'] / 3),
        ((OutPut_TEMP['incurC'] / 3) - (OutPut_TEMP['TEMP_incurC-36'] / 3))
    )
    mask = OutPut_TEMP.existen_vigentes == 1
    aux = OutPut_TEMP.incurC_recal[mask]  # Precalculamos la división entre 3 necesarias
    parts = OutPut_TEMP.Id_Tool[mask]
    OutPut_TEMP['suminC'] = aux.groupby(parts).cumsum()
    OutPut_TEMP['suminC'].fillna(0, inplace=True)

    ########## Calcular sumGwp ##########
    # Calcular columna gwp para el calculo de sumGwp
    OutPut_TEMP['gwp_recal'] = np.where(
        (OutPut_TEMP['TEMP_numeromes'] <= 12),
        (OutPut_TEMP['gwp']),
        ((OutPut_TEMP['gwp']) - OutPut_TEMP['TEMP_gwp-12'])
    )
    mask2 = OutPut_TEMP.existen_vigentes == 1
    aux2 = OutPut_TEMP.gwp_recal[mask2]
    parts2 = OutPut_TEMP.Id_Tool[mask2]
    OutPut_TEMP['sumGwp'] = aux2.groupby(parts2).cumsum()
    OutPut_TEMP['sumGwp'].fillna(0, inplace=True)

    OutPut['suminC'] = OutPut_TEMP['suminC']
    OutPut['sumGwp'] = OutPut_TEMP['sumGwp']

    # Ingresos financieros por capital
    OutPut['reqcap'] = np.where(
        (OutPut['sumGwp'] * 0.18) > (OutPut['suminC'] * 0.26),
        (OutPut['sumGwp'] * 0.18),
        (OutPut['suminC'] * 0.26)
    )  # Calculo de requerimiento de capital

    OutPut['fincomec'] = np.where(
        (OutPut['sumGwp'] * 0.18) > (OutPut['suminC'] * 0.26),
        (OutPut['sumGwp'] * 0.18) * (((finanp + 1) ** (1 / 12) - 1)),
        (OutPut['suminC'] * 0.26) * (((finanp + 1) ** (1 / 12) - 1))
    )

    OutPut['reqcapy'] = np.where((OutPut['TEMP_numeromes'] % 12) == 0, OutPut['reqcap'], OutPut['reqcapy'])

    OutPut['fincomer'] = np.where(OutPut['vigentes'] <= 0, 0, OutPut['fincomer'])
    OutPut['reqcap'] = np.where(OutPut['vigentes'] <= 0, 0, OutPut['reqcap'])
    OutPut['fincomec'] = np.where(OutPut['vigentes'] <= 0, 0, OutPut['fincomec'])
    OutPut['reqcapy'] = np.where(OutPut['vigentes'] <= 0, 0, OutPut['reqcapy'])
    OutPut['sumGwp'] = np.where(OutPut['vigentes'] <= 0, 0, OutPut['sumGwp'])
    OutPut['suminC'] = np.where(OutPut['vigentes'] <= 0, 0, OutPut['suminC'])

    OutPut['suminC'] = OutPut['suminC'].fillna(0)
    OutPut['sumGwp'] = OutPut['sumGwp'].fillna(0)

    return OutPut
