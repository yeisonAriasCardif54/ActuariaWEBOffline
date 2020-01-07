# -- Obtener vlrprimac y vlrprimad para posterior cálculos de primas -- #

import pandas as pd
import numpy as np


def obtener_vlrprima_c_d(OutPut, meses):
    pd.options.mode.chained_assignment = None

    # -- Creación de variable OutPut_vlrprimac y OutPut_vlrprimad -- #
    OutPut_vlrprimac = pd.DataFrame()
    OutPut_vlrprimad = pd.DataFrame()
    OutPut_vlrprimac['Producto'] = OutPut['Producto']
    OutPut_vlrprimad['Producto'] = OutPut['Producto']
    OutPut_vlrprimac['Mes'] = OutPut['Mes']
    OutPut_vlrprimad['Mes'] = OutPut['Mes']
    OutPut_vlrprimac['Tipo de prima'] = OutPut['Tipo de prima']
    OutPut_vlrprimad['Tipo de prima'] = OutPut['Tipo de prima']

    # -- Determinar el mes maximo en columna Amortización/CambioPrima -- #
    for i in range(-(max(OutPut['Periodo de pago/CambioPrima']) + 12) - 1, meses + 1):
        OutPut_vlrprimac['vlrprimac_' + str(i)] = 0.0
        OutPut_vlrprimad['vlrprimad_' + str(i)] = 0.0

    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_periodica(OutPut, meses, OutPut_vlrprimac, OutPut_vlrprimad)
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_unica(OutPut, meses, OutPut_vlrprimac, OutPut_vlrprimad)
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_multiprima(OutPut, meses, OutPut_vlrprimac, OutPut_vlrprimad)

    return OutPut, OutPut_vlrprimac, OutPut_vlrprimad


def vlrprima_c_d_prima_periodica(OutPut, meses, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Periódica']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Periódica']
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] != 'Periódica']
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] == 'Periódica']
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] != 'Periódica']
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] == 'Periódica']

    yvlrp = OutPut['Mes'] % OutPut['Periodo de pago/CambioPrima']
    # -- Condiciones y soluciones globales para optimización del código -- #
    cg1 = OutPut['Mes'] == 1
    cg3 = yvlrp == 1

    for i in range(1, meses + 1):
        # -- Condiciones y soluciones locales para optimización del código -- #
        cl1 = i < (OutPut['Periodo de pago/CambioPrima']+1)
        cl2 = OutPut['Mes'] <= i

        vlrprimac = np.where(
            cl1,
            np.where(  # Columnas de vlrprimac_1 a vlrprimac_OutPut['Periodo de pago/CambioPrima']
                cg1,
                OutPut['Vlr prima'] * ((OutPut['Periodo de pago/CambioPrima'] - i) / OutPut['Periodo de pago/CambioPrima']),
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
            ),
            np.where(  # Columnas de vlrprimac_1 a vlrprimac_meses+1
                cl2,
                np.where(
                    cg1,
                    OutPut_vlrprimac.lookup(OutPut.index, 'vlrprimac_' + (i - OutPut['Periodo de pago/CambioPrima']).astype(str)),
                    OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
                ),
                OutPut_vlrprimac['vlrprimac_' + str(i)]
            )
        )

        vlrprimad = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr prima'] * ((OutPut['Periodo de pago/CambioPrima'] - i + 0.5) / OutPut['Periodo de pago/CambioPrima']),
                OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
            ),
            np.where(
                cl2,
                np.where(
                    cg1,
                    OutPut_vlrprimad.lookup(OutPut.index, 'vlrprimad_' + (i - OutPut['Periodo de pago/CambioPrima']).astype(str)),
                    OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
                ),
                OutPut_vlrprimad['vlrprimad_' + str(i)]
            )
        )

        OutPut_vlrprimac['vlrprimac_' + str(i)] = vlrprimac
        OutPut_vlrprimac['vlrprimac_' + str(i)] = OutPut_vlrprimac['vlrprimac_' + str(i)].astype(np.float64)

        OutPut_vlrprimad['vlrprimad_' + str(i)] = vlrprimad
        OutPut_vlrprimad['vlrprimad_' + str(i)] = OutPut_vlrprimad['vlrprimad_' + str(i)].astype(np.float64)

    OutPut_vlrprimad = pd.concat([OutPut_vlrprimad, OutPut_vlrprimad_NEW_2], sort=False)
    OutPut_vlrprimad = OutPut_vlrprimad.sort_index()
    OutPut_vlrprimac = pd.concat([OutPut_vlrprimac, OutPut_vlrprimac_NEW_2], sort=False)
    OutPut_vlrprimac = OutPut_vlrprimac.sort_index()
    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    return OutPut, OutPut_vlrprimac, OutPut_vlrprimad


def vlrprima_c_d_prima_unica(OutPut, meses, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Única']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Única']
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] != 'Única']
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] == 'Única']
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] != 'Única']
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] == 'Única']

    yvlrp = OutPut['Mes'] % 12

    # -- Condiciones y soluciones globales para optimización del código -- #
    cg1 = OutPut['Mes'] == 1
    cg2 = ((OutPut['Mes'] > 1) & (yvlrp == 1))

    # -- Calcular meses de 1 a 'meses' -- #
    for i in range(1, meses + 1):
        vlrprimac = np.where(
            cg1,
            OutPut['Vlr prima'] * ((OutPut['Duración del producto financiero'] - i) / OutPut['Duración del producto financiero']),
            np.where(
                cg2,
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1),
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
            )
        )

        vlrprimad = np.where(
            cg1,
            OutPut['Vlr prima'] * ((OutPut['Duración del producto financiero'] - i + 0.5) / OutPut['Duración del producto financiero']),
            np.where(
                cg2,
                OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1),
                OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
            )
        )
        OutPut_vlrprimac['vlrprimac_' + str(i)] = vlrprimac
        OutPut_vlrprimac['vlrprimac_' + str(i)] = OutPut_vlrprimac['vlrprimac_' + str(i)].astype(np.float64)

        OutPut_vlrprimad['vlrprimad_' + str(i)] = vlrprimad
        OutPut_vlrprimad['vlrprimad_' + str(i)] = OutPut_vlrprimad['vlrprimad_' + str(i)].astype(np.float64)

    OutPut_vlrprimad = pd.concat([OutPut_vlrprimad, OutPut_vlrprimad_NEW_2], sort=False)
    OutPut_vlrprimad = OutPut_vlrprimad.sort_index()
    OutPut_vlrprimac = pd.concat([OutPut_vlrprimac, OutPut_vlrprimac_NEW_2], sort=False)
    OutPut_vlrprimac = OutPut_vlrprimac.sort_index()
    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    return OutPut, OutPut_vlrprimac, OutPut_vlrprimad


def vlrprima_c_d_prima_multiprima(OutPut, meses, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Multiprima']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Multiprima']
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] != 'Multiprima']
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] == 'Multiprima']
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] != 'Multiprima']
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] == 'Multiprima']

    # -- Condiciones y soluciones globales para optimización del código -- #Ø
    cg1 = OutPut['Mes'] == 1

    for i in range(1, meses + 1):
        # -- Condiciones y soluciones locales para optimización del código -- #
        cl1 = (OutPut['Periodo de pago/CambioPrima'] + OutPut['Duración de producción en meses']) >= i  # Determinar si el mes es menor a Periodo de pago/CambioPrima

        vlrprimac = np.where(
            cl1,
            np.where(
                cg1,
                np.where(
                    (OutPut['Vlr prima'] * ((OutPut['Periodo de pago/CambioPrima'] - i) / OutPut['Periodo de pago/CambioPrima'])) >= 0,
                    OutPut['Vlr prima'] * ((OutPut['Periodo de pago/CambioPrima'] - i) / OutPut['Periodo de pago/CambioPrima']),
                    0
                ),
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
            ),
            0
        )

        vlrprimad = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr prima'] * OutPut['Periodo de pago/CambioPrima'] * ((OutPut['Periodo de pago/CambioPrima'] - i + 0.5) / OutPut['Periodo de pago/CambioPrima']),
                OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
            ),
            0
        )

        OutPut_vlrprimac['vlrprimac_' + str(i)] = vlrprimac
        OutPut_vlrprimac['vlrprimac_' + str(i)] = OutPut_vlrprimac['vlrprimac_' + str(i)].astype(np.float64)

        OutPut_vlrprimad['vlrprimad_' + str(i)] = vlrprimad
        OutPut_vlrprimad['vlrprimad_' + str(i)] = OutPut_vlrprimad['vlrprimad_' + str(i)].astype(np.float64)

    OutPut_vlrprimad = pd.concat([OutPut_vlrprimad, OutPut_vlrprimad_NEW_2], sort=False)
    OutPut_vlrprimad = OutPut_vlrprimad.sort_index()
    OutPut_vlrprimac = pd.concat([OutPut_vlrprimac, OutPut_vlrprimac_NEW_2], sort=False)
    OutPut_vlrprimac = OutPut_vlrprimac.sort_index()
    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    return OutPut, OutPut_vlrprimac, OutPut_vlrprimad
