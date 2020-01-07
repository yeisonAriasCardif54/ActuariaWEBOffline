''' Obtener vlrprimac y vlrprimad para posteriuor calculos de primas '''

import pandas as pd
import numpy as np


# import time


def obtener_vlrprima_c_d(OutPut, meses, ipc):
    # start_time = time.time()
    pd.options.mode.chained_assignment = None

    # Creacion de variable OutPut_vlrprimac y OutPut_vlrprimad
    OutPut_vlrprimac = pd.DataFrame({});
    OutPut_vlrprimad = pd.DataFrame({});
    OutPut_vlrprimac['Id_Tool'] = OutPut['Id_Tool']
    OutPut_vlrprimad['Id_Tool'] = OutPut['Id_Tool']
    OutPut_vlrprimac['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']
    OutPut_vlrprimad['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']
    OutPut_vlrprimac['Id_T.Prima'] = OutPut['Id_T.Prima']
    OutPut_vlrprimad['Id_T.Prima'] = OutPut['Id_T.Prima']

    ## Determinar el mes maximo en columna Amortizacion/CambioPrima
    for i in range(-(max(OutPut['Amortizacion/CambioPrima']) + 12) - 1, meses + 1):
        OutPut_vlrprimac['vlrprimac_' + str(i)] = 0.0
        OutPut_vlrprimad['vlrprimad_' + str(i)] = 0.0

    # Calcular vlrprima c Y d con tipo de prima anual (2)
    # start_time1 = time.time()
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_anual(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad)
    # print("\n\n ------vlrprima_c_d_prima_anual \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular vlrprima c Y d con tipo de prima unica (3)
    # start_time1 = time.time()
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_unica(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad)
    # print("\n\n ------vlrprima_c_d_prima_unica \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular vlrprima c Y d con tipo de prima amortizada (4)
    # start_time1 = time.time()
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_amortizada(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad)
    # print("\n\n ------vlrprima_c_d_prima_amortizada \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular vlrprima c Y d con tipo de prima multiprima (5)
    # start_time1 = time.time()
    OutPut, OutPut_vlrprimac, OutPut_vlrprimad = vlrprima_c_d_prima_multiprima(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad)
    # print("\n\n ------vlrprima_c_d_prima_multiprima \n--- %s seconds ---" % (time.time() - start_time1))

    # print("\n\n obtener_vlrprima_c_d \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, OutPut_vlrprimac, OutPut_vlrprimad


def vlrprima_c_d_prima_anual(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 2]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 2]
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] != 2]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 2]
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] != 2]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 2]

    yvlrp = OutPut['TEMP_numeromes'] % 12
    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = OutPut['TEMP_numeromes'] == 1
    cg2 = OutPut['¿Aplica IPC?'] == "Si"
    cg3 = yvlrp == 1

    for i in range(1, meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = i < 13
        cl2 = OutPut['TEMP_numeromes'] <= i

        vlrprimac = np.where(
            cl1,
            np.where(  # Columnas de vlrprimac_1 a vlrprimac_12
                cg1,
                OutPut['Vlr. Prima Prom'] * ((12 - i) / 12),
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
            ),
            np.where(  # Columnas de vlrprimac_1 a vlrprimac_meses+1
                cl2,
                np.where(
                    cg1,
                    np.where(
                        cg2,
                        OutPut_vlrprimac['vlrprimac_' + str(i - 12)] * (1 + ipc),
                        OutPut_vlrprimac['vlrprimac_' + str(i - 12)]
                    ),
                    np.where(
                        cg3,
                        np.where(
                            cg2,
                            OutPut_vlrprimac['vlrprimac_' + str(i - 12)].shift(12) * (1 + ipc),
                            OutPut_vlrprimac['vlrprimac_' + str(i - 12)].shift(12)
                        ),
                        OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
                    )
                ),
                OutPut_vlrprimac['vlrprimac_' + str(i)]
            )
        )

        vlrprimad = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr. Prima Prom'] * ((12 - i + 0.5) / 12),
                OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
            ),
            np.where(
                cl2,
                np.where(
                    cg1,
                    np.where(
                        cg2,
                        OutPut_vlrprimad['vlrprimad_' + str(i - 12)] * (1 + ipc),
                        OutPut_vlrprimad['vlrprimad_' + str(i - 12)]
                    ),
                    np.where(
                        cg3,
                        np.where(
                            cg2,
                            OutPut_vlrprimad['vlrprimad_' + str(i - 12)].shift(12) * (1 + ipc),
                            OutPut_vlrprimad['vlrprimad_' + str(i - 12)].shift(12)
                        ),
                        OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
                    )
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


def vlrprima_c_d_prima_unica(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 3]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 3]
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] != 3]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 3]
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] != 3]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 3]

    yvlrp = OutPut['TEMP_numeromes'] % 12

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = OutPut['TEMP_numeromes'] == 1
    cg2 = ((OutPut['TEMP_numeromes'] > 1) & (yvlrp == 1))
    cg4 = OutPut['¿Aplica IPC?'] == "Si"

    # Calcular meses de 1 a 'meses'
    for i in range(1, meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = OutPut['Meses garantía fabricante'] < i

        vlrprimac = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr. Prima Prom'] * ((OutPut['Duración'] - i + OutPut['Meses garantía fabricante']) / OutPut['Duración']),
                np.where(
                    cg2,
                    np.where(
                        cg4,
                        OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1) * (1 + ipc),
                        OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
                    ),
                    OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
                )
            ),
            0
        )

        vlrprimad = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr. Prima Prom'] * ((OutPut['Duración'] - i + OutPut['Meses garantía fabricante'] + 0.5) / OutPut['Duración']),
                np.where(
                    cg2,
                    np.where(
                        cg4,
                        OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1) * (1 + ipc),
                        OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
                    ),
                    OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
                )
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


def vlrprima_c_d_prima_amortizada(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 4]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 4]
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] != 4]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 4]
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] != 4]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 4]

    yvlrp = OutPut['TEMP_numeromes'] % 12

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = ((OutPut['TEMP_numeromes'] > 1) & (yvlrp == 1))
    cg2 = OutPut['TEMP_numeromes'] == 1
    cg3 = OutPut['¿Aplica IPC?'] == "Si"

    # Calcular meses de 1 a 'meses'
    for i in range(1, meses + 1):
        vlrprimac = np.where(
            OutPut['Amortizacion/CambioPrima'] >= i,  # Determinar si el mes es menor a Amortizacion/CambioPrima
            np.where(
                cg2,
                OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((OutPut['Amortizacion/CambioPrima'] - i) / OutPut['Amortizacion/CambioPrima']),
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
            ),
            np.where(
                i >= OutPut['TEMP_numeromes'],
                np.where(
                    cg2,
                    np.where(
                        cg3,
                        OutPut_vlrprimac.lookup(OutPut.index, 'vlrprimac_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str)) * (1 + ipc),
                        OutPut_vlrprimac.lookup(OutPut.index, 'vlrprimac_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str))
                    ),
                    np.where(
                        cg1,
                        np.where(
                            cg3,
                            OutPut_vlrprimac.shift(12).lookup(OutPut.index, 'vlrprimac_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str)) * (1 + ipc),
                            OutPut_vlrprimac.shift(12).lookup(OutPut.index, 'vlrprimac_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str))
                        ),
                        OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
                    )
                ),
                0
            )
        )

        vlrprimad = np.where(
            OutPut['Amortizacion/CambioPrima'] >= i,  # Determinar si el mes es menor a Amortizacion/CambioPrima
            np.where(
                cg2,
                OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((OutPut['Amortizacion/CambioPrima'] - i + 0.5) / OutPut['Amortizacion/CambioPrima']),
                OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
            ),
            np.where(
                i >= OutPut['TEMP_numeromes'],
                np.where(
                    cg2,
                    np.where(
                        cg3,
                        OutPut_vlrprimad.lookup(OutPut.index, 'vlrprimad_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str)) * (1 + ipc),
                        OutPut_vlrprimad.lookup(OutPut.index, 'vlrprimad_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str))
                    ),
                    np.where(
                        cg1,
                        np.where(
                            cg3,
                            OutPut_vlrprimad.shift(12).lookup(OutPut.index, 'vlrprimad_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str)) * (1 + ipc),
                            OutPut_vlrprimad.shift(12).lookup(OutPut.index, 'vlrprimad_' + (i - OutPut['Amortizacion/CambioPrima']).astype(str))
                        ),
                        OutPut_vlrprimad['vlrprimad_' + str(i - 1)].shift(1)
                    )
                ),
                0
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


def vlrprima_c_d_prima_multiprima(OutPut, meses, ipc, OutPut_vlrprimac, OutPut_vlrprimad):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 5]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 5]
    OutPut_vlrprimac_NEW_2 = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] != 5]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 5]
    OutPut_vlrprimad_NEW_2 = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] != 5]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 5]

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = OutPut['TEMP_numeromes'] == 1
    #OutPut['Amortizacion/CambioPrima'] = (OutPut['Amortizacion/CambioPrima'] + (OutPut['Mes Inicio'] - 1))

    for i in range(1, meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = (OutPut['TEMP_numeromes'] + OutPut['Amortizacion/CambioPrima'] + (OutPut['Mes Inicio'] - 1)) > i  # Determinar si el mes es menor a Amortizacion/CambioPrima

        vlrprimac = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((OutPut['Amortizacion/CambioPrima'] - i) / OutPut['Amortizacion/CambioPrima']),
                OutPut_vlrprimac['vlrprimac_' + str(i - 1)].shift(1)
            ),
            0
        )

        vlrprimad = np.where(
            cl1,
            np.where(
                cg1,
                OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((OutPut['Amortizacion/CambioPrima'] - i + 0.5) / OutPut['Amortizacion/CambioPrima']),
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
