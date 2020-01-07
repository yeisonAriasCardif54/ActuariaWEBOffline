''' Obtener primas emitidas (GWP) '''

import pandas as pd
import numpy as np
from math import floor
import time


def obtener_primas_emitidas_v2(OutPut, meses, ipc, uprStock, OutPut_tasa_caida_cancel, OutPut_tasa, vector, OutPut_vlrprimac, OutPut_vlrprimad):
    start_time = time.time()
    pd.options.mode.chained_assignment = None

    OutPut_tasa_caida_cancel['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']
    OutPut_tasa['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']

    # Crear Dataframe para guardar variables calculadas gwpnt_, gwpst_, uprt_
    OutPut_PRI = pd.DataFrame({});
    OutPut_PRI['Id_Tool'] = OutPut['Id_Tool']

    # Creacion de columnas gwpnt_0 a gwpnt_'meses' # Creacion de columnas gwpst_0 a gwpst_'meses' # Creacion de columnas uprt_0 a uprt_'meses'
    for i in range(0, meses + 1):
        OutPut_PRI['gwpnt_' + str(i)] = 0
        OutPut_PRI['gwpst_' + str(i)] = 0
        OutPut_PRI['uprt_' + str(i)] = 0
    
    # Nuevas variables
    OutPut['gwpn'] = 0.0
    OutPut['gwps'] = 0.0
    OutPut['gwp'] = 0.0
    OutPut['upr'] = 0.0
    OutPut['earnedP'] = 0.0

    # Unificar informacion de Stock RRC (Vigentes)
    OutPut_uprStock = pd.merge(OutPut.filter(['Id_Tool', 'TEMP_numeromes', 'Id_T.Prima']), uprStock, left_on='Id_Tool', right_on='Id_Tool', how='left')

    ######################################################################################################################
    ######################################################################################################################
    ######################################################################################################################
    ## Condiciones globales
    # prima_mensual
    cg1 = OutPut['Id_T.Prima'] == 1
    # prima_anual
    cg2 = OutPut['Id_T.Prima'] == 2
    # prima_unica
    cg3 = OutPut['Id_T.Prima'] == 3
    # prima_amortizada
    cg4 = OutPut['Id_T.Prima'] == 4
    # prima_multiprima
    cg5 = OutPut['Id_T.Prima'] == 5
    
    
    ##### Calcular y
    condicionesY = [
                        cg2,
                        cg3,
                        cg4,
                        cg5
                     ]
    solucionesY = [
                    # prima_anual
                    round((OutPut['TEMP_numeromes'] - 1) / 12, 1),
                    # prima_unica
                    (OutPut['TEMP_numeromes'] - OutPut['Mes Inicio']) / 12,
                    # prima_amortizada
                    round((OutPut['TEMP_numeromes'] - 1) / 12, 1),
                    # prima_multiprima
                    round((OutPut['TEMP_numeromes'] - 1) / 12, 1)
                   ]
    OutPut['y'] = np.select(condicionesY, solucionesY, default=0)
    OutPut['y'] = OutPut['y'].astype(np.float64)
    OutPut['y'] = round(OutPut['y'], 1)
    OutPut['y'] = np.floor(OutPut['y'])
    
    
    ##### Calcular x
    condicionesX = [
                        cg2,
                        cg3,
                        cg4,
                        cg5
                     ]
    solucionesX = [
                    # prima_anual
                    np.where(
                                OutPut['¿Aplica IPC?'] == "Si", #¿Aplica IPC?'
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y']),
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom']
                            ),
                    # prima_unica
                    np.where(
                                OutPut['¿Aplica IPC?'] == "Si", #¿Aplica IPC?'
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y']),
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom']
                            ),
                    # prima_amortizada
                    np.where(
                                OutPut['¿Aplica IPC?'] == "Si",
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
                            ),
                    # prima_multiprima
                    np.where(
                                OutPut['¿Aplica IPC?'] == "Si",
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
                                OutPut['nuevos'] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
                            )
                   ]
    OutPut['x'] = np.select(condicionesX, solucionesX, default=0)
    OutPut['x'] = OutPut['x'].fillna(0)

    
    
    for i in range(meses + 1):
        ########## Calcular gwpnt ##########
        condicionesGWPNT = [
                                cg2,
                                cg3,
                                cg4,
                                cg5
                           ]
        solucionesGWPNT = [
                            # prima_anual
                             np.where(
                                        (OutPut['Tipo Proyección'] != 'Stock_RRC') | (OutPut['TEMP_numeromes'] <= 12),
                                        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)],
                                        0
                                    ),
                            # prima_unica
                            np.where(
                                        ((i - OutPut['TEMP_numeromes']) < OutPut['Meses garantía fabricante']),
                                        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut['Vlr. Prima Prom'],
                                        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]
                                    ),
                            # prima_amortizada
                            np.where(
                                        (((i - OutPut['TEMP_numeromes']) % OutPut['Amortizacion/CambioPrima']) == 0),
                                        np.where(
                                            OutPut['¿Aplica IPC?'] == "Si",
                                            OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima'] * ((1 + ipc) ** OutPut['y']),
                                            OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut['Vlr. Prima Prom'] * OutPut['Amortizacion/CambioPrima']
                                        ),
                                        0
                                    ),
                            # prima_multiprima
                            OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]
                          ]
        OutPut_PRI['gwpnt_' + str(i)] = np.select(condicionesGWPNT, solucionesGWPNT, default=0)
        
        
        ########## Calcular gwpst ##########
        condicionesGWPST = [
                                cg2,
                                cg4
                           ]
        solucionesGWPST = [
                            # prima_anual
                             np.where(
                                        (OutPut['Tipo Proyección'] != 'Stock_RRC') & ((i > 12) & (i > OutPut['TEMP_numeromes'])) & ((((i - OutPut['TEMP_numeromes']) % 12) == 0) & (i > OutPut['Mes Inicio'])),
                                        np.where(
                                            OutPut['¿Aplica IPC?'] == "Si", #¿Aplica IPC?'
                                            np.where(
                                                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                                0,
                                                OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** floor((i - 1) / 12))
                                            ),
                                            np.where(
                                                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                                0,
                                                OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom']
                                            )
                                        ),
                                        0
                                    ),
                            # prima_amortizada
                            np.where(
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
                          ]
        OutPut_PRI['gwpst_' + str(i)] = np.select(condicionesGWPST, solucionesGWPST, default=0)
        
        
        
        ########## Calcular uprt ##########
        condicionesUPRT = [
                            cg2,
                            cg3,
                            cg4,
                            cg5
                          ]
        solucionesUPRT = [
                            # prima_anual
                            np.where(
                                OutPut['Tipo Proyección'] != 'Stock_RRC',
                                OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
                                ##### Stock_RRC #####
                                np.where(
                                    OutPut['TEMP_numeromes'] <= 12,
                                    OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
                                    0  # Siempre será cero pórque no habrá renovaciones
                                )
                            ),
                            # prima_unica
                            np.where(
                                        ((i - OutPut['TEMP_numeromes']) < OutPut['Meses garantía fabricante']),
                                        OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr. Prima Prom'],
                                        OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)]
                                    ),
                            # prima_amortizada
                            OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
                            # prima_multiprima
                            OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)]
                          ]
        OutPut_PRI['uprt_' + str(i)] = np.select(condicionesUPRT, solucionesUPRT, default=0)
        
        
        
        ########## Calcular gwpn ##########
        condicionesGWPN = [
                            cg2,
                            cg3,
                            cg4
                          ]
        solucionesGWPN = [
                            # prima_anual
                            np.where(
                                        OutPut['TEMP_numeromes'] <= 5,
                                        np.where(
                                                    OutPut['TEMP_numeromes'] == 1,
                                                    OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes']-1).astype(str)) * (OutPut['Caida'] * vector['Vector Control RRC']),
                                                    OutPut['upr'].shift(1) * (OutPut['Caida'] * vector['Vector Control RRC'])
                                                ),
                                        np.where(
                                                    OutPut['TEMP_numeromes'] <= 12,
                                                    OutPut['upr'].shift(1) * OutPut['Caida'],
                                                    0
                                                )
                                    ),
                            # prima_unica
                            np.where(
                                        (i == OutPut['TEMP_numeromes']),
                                        np.where(
                                            OutPut['Tipo Proyección'] != 'Stock_RRC',
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
                                    ),
                            # prima_amortizada
                            np.where(
                                        (i == OutPut['TEMP_numeromes']),
                                        OutPut_PRI.groupby(['Id_Tool'])['gwpnt_' + str(i)].sum()[OutPut['Id_Tool']],
                                        OutPut['gwpn']
                                    )
                          ]
        OutPut['gwpn'] =  np.select(condicionesGWPN, solucionesGWPN, default=0)

        
        
        ########### Cálculo de la reserva requerida mensual, UPR_eop ##########
        condicionesUPR = [
                            cg2,
                            cg3,
                            cg4,
                            cg5
                          ]
        solucionesUPR = [
                            # prima_anual
                            np.where(
                                        OutPut['TEMP_numeromes'] <= 12,
                                        np.where(
                                            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff']>0)),
                                            0,
                                            OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes']).astype(str)) - OutPut['gwpn']
                                        ),
                                        0
                                    ),
                            # prima_unica
                            np.where(
                                        (i == OutPut['TEMP_numeromes']),
                                        np.where(
                                            OutPut['Tipo Proyección'] != 'Stock_RRC',
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
                                    ),
                            # prima_amortizada
                            np.where(
                                        (i == OutPut['TEMP_numeromes']),
                                        np.where(
                                            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                            0,
                                            OutPut_PRI.groupby(['Id_Tool'])['uprt_' + str(i)].sum()[OutPut['Id_Tool']]
                                        ),
                                        OutPut['upr']
                                    ),
                            # prima_multiprima
                            np.where(
                                        (i == OutPut['TEMP_numeromes']),
                                        np.where(
                                            (OutPut['TEMP_numeromes'] > OutPut['Amortizacion/CambioPrima']),
                                            np.where(
                                                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                                0,
                                                np.where(
                                                    OutPut['Id_T.Oferta'] == 3,
                                                    0,
                                                    # Calculo igual al calculo de gwp en esta instancia (es igual a gwp(k) * 0.5)
                                                    np.where(
                                                        OutPut['¿Aplica IPC?'] == "Si",
                                                        (OutPut['vigentes'] * (OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y']))) * 0.5,
                                                        (OutPut['vigentes'] * OutPut['Vlr. Prima Prom']) * 0.5
                                                    )
                                                )
                                            ),
                                            np.where(
                                                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                                0,
                                                OutPut_PRI.groupby(['Id_Tool'])['uprt_' + str(i)].sum()[OutPut['Id_Tool']]
                                            ),
                                        ),
                                        OutPut['upr']
                                    )
                          ]
        OutPut['upr']  = np.select(condicionesUPR, solucionesUPR, default=0)

        
        ########### ENDFOR
        
    # Agrupar OutPut_PRI
    # Calcular gwps
    OutPut_PRI_agrupada = OutPut_PRI.groupby('Id_Tool').sum()
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada.index
    OutPut_PRI_agrupada['Id_Tool'] = OutPut_PRI_agrupada['Id_Tool'].astype(np.int32)
    OutPut_PRI_agrupada = pd.merge(OutPut.filter(['Id_Tool']), OutPut_PRI_agrupada, left_on='Id_Tool', right_on='Id_Tool', how='left')
    
    
    ##### gwps
    condicionesGWPS = [
                        cg2,
                        cg4,
                        cg5
                     ]
    solucionesGWPS = [
                    # prima_anual
                    OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpst_' + (OutPut['TEMP_numeromes']).astype(str)),
                    # prima_amortizada
                    OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpst_' + (OutPut['TEMP_numeromes']).astype(str)),
                    # prima_multiprima
                    OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpst_' + (OutPut['TEMP_numeromes']).astype(str))
                   ]
    OutPut['gwps'] = np.select(condicionesGWPS, solucionesGWPS, default=0)
    
    
    ##### gwpn
    condicionesGWPN = [
                        cg2
                     ]
    solucionesGWPN = [
                    # prima_anual
                    np.where(
                                OutPut['Tipo Proyección'] != 'Stock_RRC',
                                OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['TEMP_numeromes']).astype(str)),
                                OutPut['gwpn']
                            )
                   ]
    OutPut['gwpn'] = np.select(condicionesGWPN, solucionesGWPN, default=0)
    
    ##### gwp
    condicionesGWP = [
                        cg1,
                        cg2,
                        cg3,
                        cg4,
                        cg5
                     ]
    solucionesGWP = [
                    # prima_mensual
                    np.where(
                                OutPut['Tipo Proyección'] != 'Stock_RRC',
                                np.where(
                                    OutPut['¿Aplica IPC?'] == "Si",  # Pregunta si le aplica o no el IPC
                                    np.where(
                                        ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                        'ERR',
                                        OutPut['vigentes'] * OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['y'])
                                    ),
                                    OutPut['vigentes'] * OutPut['Vlr. Prima Prom']
                                ),
                                ##### Stock_RRC #####
                                OutPut['vigentes'] * OutPut['Vlr. Prima Prom']
                            )
                    ,
                    # prima_anual
                    np.where(
                                OutPut['Tipo Proyección'] != 'Stock_RRC',
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
                            ),
                    # prima_unica
                    np.where(
                            OutPut['Tipo Proyección'] != 'Stock_RRC',
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
                        ),
                    # prima_amortizada
                    np.where(
                                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                OutPut['gwp'].shift(1),
                                OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
                            ),
                    # prima_multiprima
                    np.where(
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
                   ]
    OutPut['gwp'] = np.select(condicionesGWP, solucionesGWP, default=0)
    OutPut['gwp'] = OutPut['gwp'].fillna(0).astype(np.float64)
    
    ##### upr
    condicionesUPR = [
                        cg1,
                        cg2
                     ]
    solucionesUPR = [
                    # prima_mensual
                    np.where(
                        OutPut['Tipo Proyección'] != 'Stock_RRC',
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
                    )
                    ,
                    # prima_anual
                    np.where(
                            OutPut['Tipo Proyección'] != 'Stock_RRC',
                            np.where(
                                ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                                0,
                                #OutPut_PRI.groupby(['Id_Tool'])['uprt_' + str(i)].sum()[OutPut['Id_Tool']]
                                OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'uprt_' + (OutPut['TEMP_numeromes']).astype(str)),
                            ),
                            OutPut['upr']
                        )
                    
                   ]
    OutPut['upr'] = np.select(condicionesUPR, solucionesUPR, default=0)
    
    
    ##### Variable temporal upr-1
    OutPut['TEMP_earnedP_upr-1'] = OutPut['upr'].shift(1)
    OutPut['TEMP_earnedP_upr-1'] = OutPut['TEMP_earnedP_upr-1'].fillna(0)
    
    
    ##### earnedP
    condicionesEarnedP = [
                            cg1,
                            cg2,
                            cg3,
                            cg4,
                            cg5
                         ]
    solucionesEarnedP = [
                        # prima_mensual
                        np.where(
                                    OutPut['Tipo Proyección'] != 'Stock_RRC',
                                    np.where(
                                        OutPut['TEMP_numeromes'] == 1,
                                        OutPut['gwp'] - OutPut['upr'],
                                        OutPut['gwp'] - OutPut['upr'] + OutPut['TEMP_earnedP_upr-1'],
                                    ),
                                    ##### Stock_RRC #####
                                    np.where(
                                        OutPut['TEMP_numeromes'] == 1,
                                        OutPut['gwp'] - OutPut['upr'] + OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)),
                                        OutPut['gwp'] - OutPut['upr'] + OutPut['TEMP_earnedP_upr-1'],
                                    ),
                                ),
                        # prima_anual
                        np.where(
                                    OutPut['Tipo Proyección'] != 'Stock_RRC',
                                    np.where(
                                        OutPut['TEMP_numeromes'] == 1,
                                        OutPut['gwp'] - OutPut['upr'],
                                        OutPut['gwp'] - OutPut['upr'] + OutPut['TEMP_earnedP_upr-1'],
                                    ),
                                    ##### Stock_RRC #####
                                    np.where(
                                        OutPut['TEMP_numeromes'] == 1,
                                        OutPut['gwp'] - OutPut['upr'] + OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)),
                                        OutPut['gwp'] - OutPut['upr'] + OutPut['upr'].shift(1)
                                    )
                                ),
                        # prima_unica
                        np.where(
                                    OutPut['Tipo Proyección'] != 'Stock_RRC',
                                    np.where(
                                        OutPut['TEMP_numeromes'] == 1,
                                        OutPut['gwp'] - OutPut['upr'],
                                        OutPut['gwp'] - OutPut['upr'] + OutPut['TEMP_earnedP_upr-1'],
                                    ),
                                    ##### Stock_RRC #####
                                    np.where(
                                        OutPut['TEMP_numeromes'] == 1,
                                        OutPut['gwp'] - OutPut['upr'] + OutPut_uprStock.lookup(OutPut.index, 'uprStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)),
                                        OutPut['gwp'] - OutPut['upr'] + OutPut['upr'].shift(1)
                                    )
                                ),
                        # prima_amortizada
                        np.where(
                                    OutPut['TEMP_numeromes'] == 1,
                                    OutPut['gwp'] - OutPut['upr'],
                                    OutPut['gwp'] - OutPut['upr'] + OutPut['TEMP_earnedP_upr-1'],
                                ),
                        # prima_multiprima
                        np.where(
                                    OutPut['TEMP_numeromes'] == 1,
                                    OutPut['gwp'] - OutPut['upr'],
                                    OutPut['gwp'] - OutPut['upr'] + OutPut['TEMP_earnedP_upr-1'],
                                )
                       ]
    OutPut['earnedP'] = np.select(condicionesEarnedP, solucionesEarnedP, default=0)
    
    
    
    ######################################################################################################################
    ######################################################################################################################
    ######################################################################################################################

    OutPut['gwpn'] = OutPut['gwpn'].fillna(0).astype(np.float64)
    OutPut['gwps'] = OutPut['gwps'].fillna(0).astype(np.float64)
    
    OutPut['upr'] = OutPut['upr'].fillna(0).astype(np.float64)
    OutPut['earnedP'] = OutPut['earnedP'].fillna(0).astype(np.float64)
    #print("\n\n obtener_primas_emitidas \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, OutPut_uprStock
