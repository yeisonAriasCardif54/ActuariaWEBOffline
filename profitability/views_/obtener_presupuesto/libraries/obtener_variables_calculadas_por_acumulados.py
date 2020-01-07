''' Después de las primera impresión sigue la de variables calculadas por acumulados '''

import pandas as pd
import numpy as np


# import time


def obtener_variables_calculadas_por_acumulados(OutPut, taxr, meses, nproduct, Up):
    # start_time = time.time()
    meses = meses + 1

    OutPut_newOutPut = pd.DataFrame()
    OutPut_newOutPut['taxreal'] = [0 for i in [0] * len(OutPut)]
    OutPut_newOutPut['taxreal'] = OutPut_newOutPut['taxreal'].astype(np.float64)

    OutPut_newOutPut['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    OutPut_newOutPut['gross2'] = OutPut['gross2']

    newUp = pd.DataFrame()
    newUp['tax'] = [0 for i in [0] * meses]
    newUp['Acumtax'] = [0 for i in [0] * meses]
    newUp['taxrealm'] = [0 for i in [0] * meses]
    newUp['Acumtaxrealm'] = [0 for i in [0] * meses]

    # Cálculo de los impuesto
    newUp['tax'] = Up['gross2m'] * taxr  # Tax nominal

    for index, row in newUp.iterrows():
        if index == 0:
            newUp['Acumtax'][index] = newUp['tax'][index]
            newUp['taxrealm'][index] = 0
            newUp['Acumtaxrealm'][index] = newUp['taxrealm'][index]
        else:
            newUp['Acumtax'][index] = newUp['Acumtax'][index - 1] + newUp['tax'][index]

            if (newUp['Acumtax'][index] > 0) & (newUp['Acumtax'][index - 1] > 0):
                if (newUp['Acumtax'][index] - newUp['Acumtaxrealm'][index - 1]) > 0:
                    newUp['taxrealm'][index] = newUp['Acumtax'][index] - newUp['Acumtaxrealm'][index - 1]
                else:
                    0
            else:
                if newUp['Acumtax'][index] > 0:
                    newUp['taxrealm'][index] = newUp['Acumtax'][index]
                else:
                    0

            newUp['Acumtaxrealm'][index] = newUp['Acumtaxrealm'][index - 1] + newUp['taxrealm'][index]

    newUp['taxrealm'] = newUp['taxrealm'].fillna(0)
    newUp['taxrealm'] = newUp['taxrealm'].astype(np.float64)

    # Unificar OutPut_newOutPut con newUp
    newUp['TEMP_numeromes'] = newUp.index
    OutPut_newOutPut = pd.merge(OutPut_newOutPut, newUp, on=['TEMP_numeromes'], how='left')

    # Unificar OutPut_newOutPut con Up
    Up['TEMP_numeromes'] = Up.index
    OutPut_newOutPut = pd.merge(OutPut_newOutPut, Up, on=['TEMP_numeromes'], how='left')

    OutPut_newOutPut['taxreal'] = np.where(
        OutPut_newOutPut['gross2'] > 0,
        OutPut_newOutPut['taxrealm'] * (OutPut_newOutPut['gross2'] / OutPut_newOutPut['Acumgross2']),
        0
    )

    OutPut['taxreal'] = OutPut_newOutPut['taxreal'].fillna(0)
    OutPut['taxreal'] = OutPut['taxreal'].astype(np.float64)

    Up['tax'] = newUp['tax'].fillna(0)
    Up['Acumtax'] = newUp['Acumtax'].fillna(0)
    Up['taxrealm'] = newUp['taxrealm'].fillna(0)
    Up['Acumtaxrealm'] = newUp['Acumtaxrealm'].fillna(0)

    # print("\n\n obtener_variables_calculadas_por_acumulados \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, Up
