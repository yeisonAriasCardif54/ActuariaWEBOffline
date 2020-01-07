''' Obtener primas emitidas (GWP) '''

import pandas as pd
import numpy as np
from math import floor


# import time


def obtener_primas_emitidas(OutPut, meses, ipc, uprStock, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad):
    # start_time = time.time()

    # start_time1 = time.time()
    pd.options.mode.chained_assignment = None

    OutPut_tasa_caida_cancel['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']
    OutPut_tasa['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']

    # Calcular y
    OutPut['y'] = round((OutPut['TEMP_numeromes'] - 1) / 12, 1)
    OutPut['y'] = np.floor(OutPut['y'])
    y = round((meses - 1) / 12, 0)
    OutPut['x'] = 0

    # Crear Dataframe para guardar variables calculadas gwpnt_, gwpst_, uprt_
    OutPut_PRI = pd.DataFrame({});

    # Creacion de columnas gwpnt_0 a gwpnt_'meses' # Creacion de columnas gwpst_0 a gwpst_'meses' # Creacion de columnas uprt_0 a uprt_'meses'
    for i in range(0, meses + 1):
        OutPut_PRI['gwpnt_' + str(i)] = 0
        OutPut_PRI['gwpst_' + str(i)] = 0
        OutPut_PRI['uprt_' + str(i)] = 0
        OutPut_PRI['gwpt_' + str(i)] = 0

    # Nuevas variables
    OutPut['gwpn'] = 0.0
    OutPut['gwps'] = 0.0
    OutPut['gwp'] = 0.0
    OutPut['upr'] = 0.0
    OutPut['earnedP'] = 0.0

    # print("\n\n INICIO \n--- %s seconds ---" % (time.time() - start_time1))

    # Unificar informacion de Stock RRC (Vigentes)
    # start_time1 = time.time()
    OutPut_uprStock = pd.merge(OutPut.filter(['Id_Tool', 'TEMP_numeromes', 'Id_T.Prima']), uprStock, left_on='Id_Tool', right_on='Id_Tool', how='left')
    # print("\n\n Unificar informacion \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular primas emitidas con tipo de prima mensual (1)
    # start_time1 = time.time()
    OutPut = primas_emitidas_prima_mensual(OutPut, meses, y, ipc, OutPut_uprStock)
    # print("\n\n primas_emitidas_prima_mensual \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular primas emitidas con tipo de prima anual (2)
    # start_time1 = time.time()
    OutPut = primas_emitidas_prima_anual(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI)
    # print("\n\n primas_emitidas_prima_anual \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular primas emitidas con tipo de prima unica (3)
    # start_time1 = time.time()
    OutPut = primas_emitidas_prima_unica(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI)
    # print("\n\n primas_emitidas_prima_unica \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular primas emitidas con tipo de prima amortizada (4)
    # start_time1 = time.time()
    OutPut = primas_emitidas_prima_amortizada(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI)
    # print("\n\n primas_emitidas_prima_amortizada \n--- %s seconds ---" % (time.time() - start_time1))

    # Calcular primas emitidas con tipo de prima multiprima (5)
    # start_time1 = time.time()
    OutPut = primas_emitidas_prima_multiprima(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI)
    # print("\n\n primas_emitidas_prima_multiprima \n--- %s seconds ---" % (time.time() - start_time1))

    # Eliminar variables utilizadas  gwpnt_N, gwpst_N, uprt_N
    # OutPut = OutPut.drop(columns=OutPut.filter(regex=r'^gwpnt_[0-9]{1,2}$', axis=1))
    # OutPut = OutPut.drop(columns=OutPut.filter(regex=r'^gwpst_[0-9]{1,2}$', axis=1))
    # OutPut = OutPut.drop(columns=OutPut.filter(regex=r'^uprt_[0-9]{1,2}$', axis=1))

    # Cálculo de earnedP
    OutPut['earnedP'] = np.where(
        OutPut['Tipo Proyección'] != 'Stock_RRC',
        np.where(
            OutPut['TEMP_numeromes'] == 1,
            OutPut['gwp'] - OutPut['upr'],
            OutPut['gwp'] - OutPut['upr'] + OutPut['upr'].shift(1),
        ),
        ##### Stock_RRC #####
        np.where(
            OutPut['TEMP_numeromes'] == 1,
            OutPut['gwp'] - OutPut['upr'] + OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)),
            OutPut['gwp'] - OutPut['upr'] + OutPut['upr'].shift(1),
        ),
    )

    # print("\n\n obtener_primas_emitidas \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, OutPut_uprStock


def primas_emitidas_prima_mensual(OutPut, meses, y, ipc, OutPut_uprStock):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 1]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 1]
    OutPut_uprStock = OutPut_uprStock[OutPut_uprStock['Id_T.Prima'] == 1]

    sg1 = OutPut['vigentes'] * OutPut['Vlr. Prima Prom']
    cg1 = OutPut['Tipo Proyección'] != 'Stock_RRC'
    OutPut['gwp'] = np.where(
        cg1,
        np.where(
            OutPut['¿Aplica IPC?'] == "Si",  # Pregunta si le aplica o no el IPC
            np.where(
                ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                'ERR',
                sg1 * ((1 + ipc) ** OutPut['y'])
            ),
            sg1
        ),
        ##### Stock_RRC #####
        sg1
    )
    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    # Cálculo de la reserva requerida mensual, UPR_eop
    OutPut['upr'] = np.where(
        OutPut['Id_T.Prima'] == 1,
        np.where(
            cg1,
            np.where(
                OutPut['Id_T.Oferta'] == 3,
                0,
                OutPut['gwp'] * 0.5
            ),
            ##### Stock_RRC #####
            np.where(
                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                0,
                (OutPut['gwp'] * 0.5) + OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes']).astype(str))
            ),
        ),
        OutPut['upr']
    )

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut


def primas_emitidas_prima_anual(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 2]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 2]
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Id_T.Prima'] == 2]
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Id_T.Prima'] == 2]
    vector = vector[vector['Id_T.Prima'] == 2]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 2]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 2]
    OutPut_uprStock = OutPut_uprStock[OutPut_uprStock['Id_T.Prima'] == 2]

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Id_Tool'] = OutPut['Id_Tool']

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = OutPut['Tipo Proyección'] != 'Stock_RRC'
    cg2 = OutPut['¿Aplica IPC?'] == "Si"
    cg3 = ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))

    for i in range(meses + 1):
        # Calcular gwpnt
        OutPut_PRI['gwpnt_' + str(i)] = np.where(
            (cg1) | (OutPut['TEMP_numeromes'] <= 12),
            OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)],
            0
        )

        # Calcular gwpst
        OutPut_PRI['gwpst_' + str(i)] = np.where(
            (cg1) & ((i > 12) & (i > OutPut['TEMP_numeromes'])) & ((((i - OutPut['TEMP_numeromes']) % 12) == 0) & (i > OutPut['Mes Inicio'])),
            np.where(
                cg2,  # ¿Aplica IPC?'
                np.where(
                    cg3,
                    0,
                    OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** floor((i - 1) / 12))
                ),
                np.where(
                    cg3,
                    0,
                    OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom']
                )
            ),
            0
        )

        # Calcular uprt
        OutPut_PRI['uprt_' + str(i)] = np.where(
            OutPut['Id_T.Prima'] == 2,
            np.where(
                cg1,
                OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
                ##### Stock_RRC #####
                np.where(
                    OutPut['TEMP_numeromes'] <= 12,
                    OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
                    0  # Siempre será cero pórque no habrá renovaciones
                )
            ),
            OutPut_PRI['uprt_' + str(i)]
        )

        # Calcular gwpn
        OutPut['gwpn'] = np.where(
            OutPut['TEMP_numeromes'] <= 5,
            np.where(
                OutPut['TEMP_numeromes'] == 1,
                OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)) * (OutPut['Caida'] * vector['Vector Control RRC']),
                OutPut['upr'].shift(1) * (OutPut['Caida'] * vector['Vector Control RRC'])
            ),
            np.where(
                OutPut['TEMP_numeromes'] <= 12,
                OutPut['upr'].shift(1) * OutPut['Caida'],
                0
            )
        )

        # Cálculo de la reserva requerida mensual, UPR_eop
        OutPut['upr'] = np.where(
            OutPut['TEMP_numeromes'] <= 12,
            np.where(
                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                0,
                OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes']).astype(str)) - OutPut['gwpn']
            ),
            0
        )

    # Agrupar OutPut_PRI
    # Calcular gwps
    OutPut_PRI_agrupada = OutPut_PRI.groupby('Id_Tool').sum()
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada.index
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada['Id_Tool'].astype(np.int32)
    OutPut_PRI_agrupada = pd.merge(OutPut.filter(['Id_Tool']), OutPut_PRI_agrupada, left_on='Id_Tool', right_on='Id_Tool', how='left')

    # Optener vigentes de Stock y Nuevos
    OutPut['gwps'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpst_' + (OutPut['TEMP_numeromes']).astype(str))

    # Calcular gwpn

    OutPut['gwpn'] = np.where(
        cg1,
        OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['TEMP_numeromes']).astype(str)),
        OutPut['gwpn']
    )

    # Cálculo de la reserva requerida mensual, UPR_eop
    OutPut['upr'] = np.where(
        cg1,
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
            0,
            # OutPut_PRI.groupby(['Id_Tool'])['uprt_' + str(i)].sum()[OutPut['Id_Tool']]
            OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'uprt_' + (OutPut['TEMP_numeromes']).astype(str)),
        ),
        OutPut['upr']
    )

    # Calcular y
    OutPut['y'] = round((OutPut['TEMP_numeromes'] - 1) / 12, 1)
    OutPut['y'] = np.floor(OutPut['y'])

    # Calcular x
    OutPut['x'] = np.where(
        cg2,  # ¿Aplica IPC?'
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y']),
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom']
    )
    OutPut['x'] = OutPut['x'].fillna(0)

    # Calcular gwp
    OutPut['gwp'] = np.where(
        cg1,
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
            OutPut['gwp'].shift(1),
            OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
        ),
        ##### Stock_RRC #####
        np.where(
            OutPut['TEMP_numeromes'] <= 12,
            np.where(
                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                -OutPut['upr'].shift(1),
                OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
            ),
            np.where(
                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                -OutPut['upr'].shift(1),
                OutPut['gwps'] - OutPut['gwpn']
            ),
        )
    )

    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut


def primas_emitidas_prima_unica(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 3]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 3]
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Id_T.Prima'] == 3]
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Id_T.Prima'] == 3]
    vector = vector[vector['Id_T.Prima'] == 3]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 3]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 3]
    OutPut_uprStock = OutPut_uprStock[OutPut_uprStock['Id_T.Prima'] == 3]

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Id_Tool'] = OutPut['Id_Tool']

    OutPut['Meses garantía fabricante'] = OutPut['Meses garantía fabricante'].astype(np.int32)

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = OutPut['Tipo Proyección'] != 'Stock_RRC'

    for i in range(meses + 1):
        # Calcular gwpnt
        OutPut_PRI['gwpnt_' + str(i)] = np.where(
            ((i - OutPut['TEMP_numeromes']) < OutPut['Meses garantía fabricante']),
            OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut['Vlr. Prima Prom'],
            OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]
        )

        # Calcular gwpn
        OutPut['gwpn'] = np.where(
            (i == OutPut['TEMP_numeromes']),
            np.where(
                cg1,
                OutPut_PRI.groupby(['Id_Tool'])['gwpnt_' + str(i)].sum()[OutPut['Id_Tool']],
                ##### Stock_RRC #####
                np.where(
                    OutPut['TEMP_numeromes'] <= 5,
                    np.where(
                        OutPut['TEMP_numeromes'] == 1,
                        OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)) * (OutPut['Caida'] * vector['Vector Control RRC']),
                        OutPut['upr'].shift(1) * (OutPut['Caida'] * vector['Vector Control RRC'])
                    ),
                    OutPut['upr'].shift(1) * OutPut['Caida']
                )
            ),
            OutPut['gwpn']
        )

        # Calcular gwpst
        OutPut_PRI['gwpst_' + str(i)] = 0

        # Calcular gwps
        OutPut['gwps'] = 0

        # Calcular uprt
        uprt = np.where(
            ((i - OutPut['TEMP_numeromes']) < OutPut['Meses garantía fabricante']),
            OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom'],
            OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)]
        )
        OutPut_PRI['uprt_' + str(i)] = np.where((OutPut['Id_T.Prima'] == 3), uprt, OutPut_PRI['uprt_' + str(i)])

        # Calcular upr
        OutPut['upr'] = np.where(
            (i == OutPut['TEMP_numeromes']),
            np.where(
                cg1,
                np.where(
                    ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                    0,
                    OutPut_PRI.groupby(['Id_Tool'])['uprt_' + str(i)].sum()[OutPut['Id_Tool']]
                ),
                ##### Stock_RRC #####
                np.where(
                    ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                    0,
                    np.where(
                        ((OutPut['TEMP_numeromes'] - 1) < OutPut['Meses garantía fabricante']),
                        np.where(
                            OutPut['TEMP_numeromes'] == 1,
                            OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)) - OutPut['gwpn'],
                            OutPut['upr'].shift(1) - OutPut['gwpn']
                        ),
                        OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes']).astype(str)) - OutPut['gwpn']
                    )
                ),
            ),
            OutPut['upr']
        )

    # Calcular y
    OutPut['y'] = (OutPut['TEMP_numeromes'] - OutPut['Mes Inicio']) / 12
    OutPut['y'] = OutPut['y'].astype(np.float64)
    OutPut['y'] = round(OutPut['y'], 1)
    OutPut['y'] = np.floor(OutPut['y'])

    # Calcular x
    OutPut['x'] = np.where(
        OutPut['¿Aplica IPC?'] == "Si",
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y']),
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom']
    )
    OutPut['x'] = OutPut['x'].fillna(0)

    # Calcular gwp
    OutPut['gwp'] = np.where(
        cg1,
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
            OutPut['upr'].shift(1) * -1,
            OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
        ),
        ##### Stock_RRC #####
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
            OutPut['upr'].shift(1) * -1,
            OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
        )
    )
    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut


def primas_emitidas_prima_amortizada(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 4]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 4]
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Id_T.Prima'] == 4]
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Id_T.Prima'] == 4]
    vector = vector[vector['Id_T.Prima'] == 4]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 4]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 4]
    OutPut_uprStock = OutPut_uprStock[OutPut_uprStock['Id_T.Prima'] == 4]

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Id_Tool'] = OutPut['Id_Tool']

    # Calcular y
    OutPut['y'] = round((OutPut['TEMP_numeromes'] - 1) / 12, 1)
    OutPut['y'] = np.floor(OutPut['y'])

    for i in range(meses + 1):
        # Calcular gwpnt
        OutPut_PRI['gwpnt_' + str(i)] = np.where(
            (((i - OutPut['TEMP_numeromes']) % OutPut['Amortizacion/CambioPrima']) == 0),
            np.where(
                OutPut['¿Aplica IPC?'] == "Si",
                OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
                OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
            ),
            0
        )

        # Calcular gwpst
        OutPut_PRI['gwpst_' + str(i)] = np.where(
            ((i > OutPut['Amortizacion/CambioPrima']) & (i > OutPut['TEMP_numeromes'])),
            np.where(
                (((i - OutPut['TEMP_numeromes']) % OutPut['Amortizacion/CambioPrima']) == 0) & (i > OutPut['Mes Inicio']),
                np.where(
                    OutPut['¿Aplica IPC?'] == "Si",
                    np.where(
                        ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                        0,
                        np.where(
                            (((i - OutPut['TEMP_numeromes']) % OutPut['Amortizacion/CambioPrima']) == 0),
                            OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
                            0
                        )
                    ),
                    np.where(
                        ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                        0,
                        OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
                    )
                ),
                0
            ),
            0
        )

        # Calcular uprt
        OutPut_PRI['uprt_' + str(i)] = OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)]

    # Agrupar OutPut_PRI
    OutPut_PRI_agrupada = OutPut_PRI.groupby('Id_Tool').sum()
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada.index
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada['Id_Tool'].astype(np.int32)
    OutPut_PRI_agrupada = pd.merge(OutPut.filter(['Id_Tool']), OutPut_PRI_agrupada, left_on='Id_Tool', right_on='Id_Tool', how='left')

    # Calcular gwpn
    OutPut['gwpn'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['TEMP_numeromes']).astype(str))

    # Calcular gwps
    OutPut['gwps'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpst_' + (OutPut['TEMP_numeromes']).astype(str))

    # Cálculo de la reserva requerida mensual, UPR_eop
    OutPut['upr'] = np.where(
        ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
        0,
        OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'uprt_' + (OutPut['TEMP_numeromes']).astype(str))
    )

    # Calcular x
    OutPut['x'] = np.where(
        OutPut['¿Aplica IPC?'] == "Si",
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
    )

    # Calcular gwp
    OutPut['gwp'] = np.where(
        ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
        OutPut['gwp'].shift(1),
        OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
    )

    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut


def primas_emitidas_prima_multiprima(OutPut, meses, y, ipc, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_uprStock, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != 5]
    OutPut = OutPut[OutPut['Id_T.Prima'] == 5]
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Id_T.Prima'] == 5]
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Id_T.Prima'] == 5]
    vector = vector[vector['Id_T.Prima'] == 5]
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Id_T.Prima'] == 5]
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Id_T.Prima'] == 5]
    OutPut_uprStock = OutPut_uprStock[OutPut_uprStock['Id_T.Prima'] == 5]

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Id_Tool'] = OutPut['Id_Tool']

    # Calcular y
    OutPut['y'] = round((OutPut['TEMP_numeromes'] - 1) / 12, 1)
    OutPut['y'] = np.floor(OutPut['y'])

    # Calcular x
    OutPut['x'] = np.where(
        OutPut['¿Aplica IPC?'] == "Si",
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
        OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
    )

    # Calcular gwps
    OutPut['gwps'] = 0
    OutPut['Amortizacion/CambioPrima'] = OutPut['Amortizacion/CambioPrima'] + (OutPut['Mes Inicio'] - 1)

    for i in range(meses + 1):
        # Calcular gwpnt
        OutPut_PRI['gwpnt_' + str(i)] = OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]
        #OutPut_PRI['gwpnt_' + str(i)] = OutPut_vlrprimac['vlrprimac_' + str(i - 1)]

        # Calcular uprt
        OutPut_PRI['uprt_' + str(i)] = np.where(
            (i - OutPut['TEMP_numeromes']) < OutPut['Amortizacion/CambioPrima'],
            OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
            (OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom']) * 0.5
        )

        # Calcular gwpt_
        OutPut_PRI['gwpt_' + str(i)] = np.where(
            (OutPut['TEMP_numeromes'] <= i),
            np.where(
                (i - OutPut['TEMP_numeromes']) < OutPut['Amortizacion/CambioPrima'],
                np.where(
                    (i - OutPut['TEMP_numeromes']) == 0,
                    OutPut['gwps'] + OutPut['x'] - OutPut_PRI['gwpnt_' + str(i)],
                    OutPut['gwps'] - OutPut_PRI['gwpnt_' + str(i)]
                ),
                OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom']
            ),
            OutPut_PRI['gwpt_' + str(i)]
        )

    # print("\n\n----------------------------------\n\n")
    # print(OutPut_PRI.to_string())
    # print("\n\n----------------------------------\n\n")
    """
    OutPut_tasa_imprimir = OutPut_tasa.filter(regex='tasa_caida_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_tasa_imprimir.xlsx', engine='xlsxwriter')
    OutPut_tasa_imprimir.to_excel(writer, sheet_name='tasa_caida', index=None, float_format='%.8f')
    writer.save()
    OutPut_vlrprimac_imprimir = OutPut_vlrprimac.filter(regex='vlrprimac_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_vlrprimac_imprimir.xlsx', engine='xlsxwriter')
    OutPut_vlrprimac_imprimir.to_excel(writer, sheet_name='vlrprimac', index=None, float_format='%.8f')
    writer.save()
    OutPut_vlrprimad_imprimir = OutPut_vlrprimad.filter(regex='vlrprimad_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_vlrprimad_imprimir.xlsx', engine='xlsxwriter')
    OutPut_vlrprimad_imprimir.to_excel(writer, sheet_name='vlrprimad', index=None, float_format='%.8f')
    writer.save()
    OutPut_tasa_caida_cancel_imprimir = OutPut_tasa_caida_cancel.filter(regex='tasa_caida_cancel_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_tasa_caida_cancel_imprimir.xlsx', engine='xlsxwriter')
    OutPut_tasa_caida_cancel_imprimir.to_excel(writer, sheet_name='tasa_caida_cancel', index=None, float_format='%.8f')
    writer.save()

    OutPut_PRI_uprt_imprimir = OutPut_PRI.filter(regex='uprt_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_PRI_uprt_imprimir.xlsx', engine='xlsxwriter')
    OutPut_PRI_uprt_imprimir.to_excel(writer, sheet_name='OutPut_PRI_uprt_imprimir', index=None, float_format='%.8f')
    writer.save()

    
    

    OutPut_PRI_uprt_imprimir = OutPut_PRI.filter(regex='uprt_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_PRI_uprt_imprimir.xlsx', engine='xlsxwriter')
    OutPut_PRI_uprt_imprimir.to_excel(writer, sheet_name='OutPut_PRI_uprt_imprimir', index=None, float_format='%.8f')
    writer.save()

    OutPut_PRI_gwpt_imprimir = OutPut_PRI.filter(regex='gwpt_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_PRI_gwpt_imprimir.xlsx', engine='xlsxwriter')
    OutPut_PRI_gwpt_imprimir.to_excel(writer, sheet_name='OutPut_PRI_gwpt_imprimir', index=None, float_format='%.8f')
    writer.save()

    OutPut_PRI_imprimir = OutPut_PRI.filter(regex='gwpnt_', axis=1)  # VARIABLE PARA ENTORNO DE DESARROLLO
    writer = pd.ExcelWriter('Q:\\Profitability\\Proyecto Automatizacion\\Budget\\OutPut_PRI_imprimir.xlsx', engine='xlsxwriter')
    OutPut_PRI_imprimir.to_excel(writer, sheet_name='OutPut_PRI_imprimir', index=None, float_format='%.8f')
    writer.save()
    
    """
    




    # Agrupar OutPut_PRI
    OutPut_PRI_agrupada = OutPut_PRI.groupby('Id_Tool').sum()
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada.index
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada['Id_Tool'].astype(np.int32)
    OutPut_PRI_agrupada = pd.merge(OutPut.filter(['Id_Tool']), OutPut_PRI_agrupada, left_on='Id_Tool', right_on='Id_Tool', how='left')

    # Calcular gwpn
    OutPut['gwpn'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['TEMP_numeromes']).astype(str))
    # OutPut['gwpn'] = np.where(
    #    (OutPut['TEMP_numeromes'] <= OutPut['Amortizacion/CambioPrima']),
    #    OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['TEMP_numeromes']).astype(str)),
    #    0
    # )

    # Cálculo de la reserva requerida mensual, UPR_eop
    OutPut['upr'] = np.where(
        ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
        0,
        OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'uprt_' + (OutPut['TEMP_numeromes']).astype(str)),
    )

    # Calcular gwp
    """
    OutPut['gwp'] = np.where(
        (OutPut['TEMP_numeromes'] > OutPut['Amortizacion/CambioPrima']),
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
            OutPut['upr'].shift(1) * -1,
            np.where(
                OutPut['¿Aplica IPC?'] == "Si",
                OutPut['vigentes'] * (OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y'])),
                OutPut['vigentes'] * OutPut['Vlr. Prima Prom']
            )
        ),
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
            OutPut['gwp'].shift(1),
            OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
        )
    )
    """

    OutPut['gwp'] = np.where(
        ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
        OutPut['upr'].shift(1) * -1,
        OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpt_' + (OutPut['TEMP_numeromes']).astype(str))
    )

    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut
