''' Obtener vigentes y cancelaciones '''

import numpy as np
import pandas as pd
#import time


def obtener_vigentes_y_cancelaciones(OutPut, OutPut_tasa, meses, caidaren, mesiniciost, vigentesStock, vector):
    # start_time = time.time()
    pd.options.mode.chained_assignment = None

    OutPut['vigentes'] = 0
    OutPut['cancelaciones'] = 0

    # Unificar información de Stock RRC (Vigentes)
    vigentesStock = pd.merge(OutPut.filter(['Id_Tool']), vigentesStock, left_on='Id_Tool', right_on='Id_Tool', how='left')

    # Unificar información de vector con OutPut
    vector = pd.merge(OutPut.filter(['Id_Tool', 'TEMP_numeromes']), vector, left_on='TEMP_numeromes', right_on='Mes', how='left')
    vector['Id_T.Prima'] = OutPut['Id_T.Prima']

    #############################################################################
    ########################## INICIO Obtener vigentes ##########################
    #############################################################################
    # Agrupar OutPut_tasa_agrupada
    OutPut_tasa_agrupada = OutPut_tasa.groupby('Id_Tool').sum()
    OutPut_tasa_agrupada['Id_Tool'] = OutPut_tasa_agrupada.index
    OutPut_tasa_agrupada['Id_Tool'] = OutPut_tasa_agrupada['Id_Tool'].astype(np.int32)
    OutPut_tasa_agrupada = pd.merge(OutPut.filter(['Id_Tool']), OutPut_tasa_agrupada, left_on='Id_Tool', right_on='Id_Tool', how='left')
    # Obtener vigentes de Stock y Nuevos
    OutPut['vigentes'] = OutPut_tasa_agrupada.lookup(OutPut_tasa_agrupada.index, 'tasa_caida_' + (OutPut['TEMP_numeromes']).astype(str))
    OutPut['vigentes'] = OutPut['vigentes'].fillna(0)
    ##########################################################################
    ########################## FIN Obtener vigentes ##########################
    ##########################################################################

    ##################################################################################
    ########################## Inicio Obtener Cancelaciones ##########################
    ##################################################################################
    # Creación de variable OutPut_tasa_caida_cancel
    OutPut_tasa_caida_cancel = pd.DataFrame({});
    OutPut_tasa_caida_cancel['Id_Tool'] = OutPut['Id_Tool']
    OutPut_tasa_caida_cancel['Id_T.Prima'] = OutPut['Id_T.Prima']
    # Creación de columnas tasa_caida_cancel_-1 a tasa_caida_cancel_'meses'
    for i in range(-1, meses + 1):
        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = 0
    # Calcular cancelaciones con tipo de prima mensual (1)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_mensual(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, vector)
    # Calcular cancelaciones con tipo de prima anual (2)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_anual(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, vigentesStock, meses, caidaren, mesiniciost, vector)
    # Calcular cancelaciones con tipo de prima unica (3)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_unica(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, vigentesStock, meses, vector)
    # Calcular cancelaciones con tipo de prima amortizada (4)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_amortizada(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)
    # Calcular cancelaciones con tipo de prima multiprima (5)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_multiprima(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)
    ### Agrupar OutPut_tasa_caida_cancel ###
    OutPut_tasa_caida_agrupada = OutPut_tasa_caida_cancel.groupby('Id_Tool').sum()
    OutPut_tasa_caida_agrupada['Id_Tool'] = OutPut_tasa_caida_agrupada.index
    OutPut_tasa_caida_agrupada['Id_Tool'] = OutPut_tasa_caida_agrupada['Id_Tool'].astype(np.int32)
    OutPut_tasa_caida_agrupada = pd.merge(OutPut.filter(['Id_Tool']), OutPut_tasa_caida_agrupada, left_on='Id_Tool', right_on='Id_Tool', how='left')
    ########### Obtener Cancelaciones
    OutPut['cancelaciones'] = np.where(
        OutPut['Tipo Proyección'] != 'Stock_RRC',
        OutPut_tasa_caida_agrupada.lookup(OutPut_tasa_caida_agrupada.index, 'tasa_caida_cancel_' + (OutPut['TEMP_numeromes']).astype(str)),
        OutPut['cancelaciones']
    )
    ###############################################################################
    ########################## Fin Obtener Cancelaciones ##########################
    ###############################################################################

    # print("\n\n obtener_vigentes_y_cancelaciones \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, OutPut_tasa_caida_cancel, vector


def vigentes_y_cancelaciones_prima_mensual(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, vector):
    OutPut_tasa, vector, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables(1, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, vector)

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))
    cg2 = OutPut['Tipo Proyección'] == 'Nuevo'  ##### Nuevo #####
    cg3 = OutPut['Tipo Proyección'] == 'Stock'  ##### Stock #####
    rg1 = (OutPut['Mes 0'] * OutPut['Caida'])

    for i in range(meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = i >= OutPut['TEMP_numeromes']
        cl2 = ((i >= OutPut['Duración']) & (OutPut['TEMP_numeromes'] <= (i - OutPut['Duración'] - 1)) | (i == 1))  # Confirmar la duración (NO SE TIENE EN CUENTA MES DE GARANTIA DEL FABRICANTE)
        cl3 = i == OutPut['TEMP_numeromes']
        cl4 = (OutPut['TEMP_numeromes'] <= OutPut['Duración'] + 1) & (i <= OutPut['Duración'] + 1)  # Si es antes de la duración
        rl1 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida'])

        tasa = np.where(
            cg2,
            np.where(
                cl1,
                np.where(
                    cl2,
                    0,
                    np.where(
                        cl3,
                        0,
                        np.where(
                            cg1,
                            0,
                            rl1
                        )
                    )
                ),
                0
            ),
            np.where(
                cg3,
                np.where(
                    cl1,
                    np.where(
                        cl4,
                        np.where(
                            cl2,
                            rg1,
                            np.where(
                                cl3,
                                0,
                                np.where(
                                    cg1,
                                    0,
                                    rl1
                                )
                            )
                        ),
                        0
                    ),
                    0
                ),
                0
            )
        )

        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = tasa

    OutPut['cancelaciones'] = np.where(
        OutPut['Tipo Proyección'] == 'Stock_RRC',
        np.where(
            OutPut['TEMP_numeromes'] <= 5,  # Condicional par determinar si se le asigna el vector de comportamiento de la caida o no
            np.where(
                (OutPut['TEMP_numeromes'] == 1) | cg1,
                0,
                OutPut['vigentes'].shift(1) * (OutPut['Caida'] * vector['Vector Control RRC'])
            ),
            np.where(
                cg1,
                0,
                (OutPut['vigentes'].shift(1) * (OutPut['Caida']))
            )
        ),
        OutPut['cancelaciones']
    )

    OutPut['cancelaciones'] = OutPut['cancelaciones']

    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    OutPut_tasa_caida_cancel = pd.concat([OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2], sort=False)
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel.sort_index()
    return OutPut, OutPut_tasa_caida_cancel


def vigentes_y_cancelaciones_prima_anual(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, vigentesStock, meses, caidaren, mesiniciost, vector):
    OutPut_tasa, vector, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables(2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, vector)

    tasa = 0

    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = OutPut['Tipo Proyección'] == 'Nuevo'  ##### Nuevo #####
    cg2 = OutPut['Tipo Proyección'] == 'Stock'  ##### Stock #####
    cg3 = ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))

    for i in range(meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = i >= OutPut['TEMP_numeromes']
        cl2 = ((i >= OutPut['Duración']) & (OutPut['TEMP_numeromes'] <= (i - OutPut['Duración'] - 1)) | (i == 1))  # Confirmar la duración (NO SE TIENE EN CUENTA MES DE GARANTIA DEL FABRICANTE)
        cl3 = i == OutPut['TEMP_numeromes']
        cl4 = ((meses - OutPut['TEMP_numeromes']) % 12) == 0  # Caida adicional generada por las renovaciones
        cl5 = (i <= (OutPut['Duración']))

        rl1 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * (OutPut['Caida'] + caidaren))  # Tendrá en cuenta la caida normal del mes, más la caida adicional de las renovaciones
        rl2 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida'])
        tasa = np.where(
            cg1,
            np.where(
                cl1,
                np.where(
                    cl2,
                    0,
                    np.where(
                        cl3,
                        0,
                        np.where(
                            cg3,
                            0,
                            np.where(
                                cl4,
                                rl1,
                                rl2
                            )
                        )
                    )
                ),
                0
            ),
            np.where(
                cg2,
                np.where(
                    cl5,
                    np.where(
                        cl1,
                        np.where(
                            cl2,
                            0,
                            np.where(
                                cl3,
                                0,
                                np.where(
                                    cg3,
                                    0,
                                    np.where(
                                        cl4,
                                        rl1,
                                        rl2
                                    )
                                )
                            )
                        ),
                        0
                    ),
                    0
                ),
                ##### Stock RRC #####
                0
            )
        )
        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = tasa

    OutPut['cancelaciones'] = np.where(
        OutPut['TEMP_numeromes'] <= 5,  # Condicional par determinar si se le asigna el vector de comportamiento de la caida o no
        np.where(
            OutPut['TEMP_numeromes'] == 1,
            vigentesStock.lookup(OutPut.index, 'vigentesStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)) * (OutPut['Caida'] * vector['Vector Control RRC']),
            np.where(
                ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                0,
                (OutPut['vigentes'].shift(1) * (OutPut['Caida'] * vector['Vector Control RRC']))
            )
        ),
        (OutPut['vigentes'].shift(1) * OutPut['Caida'])
    )

    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    OutPut_tasa_caida_cancel = pd.concat([OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2], sort=False)
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel.sort_index()
    return OutPut, OutPut_tasa_caida_cancel


def vigentes_y_cancelaciones_prima_unica(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, vigentesStock, meses, vector):
    OutPut_tasa, vector, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables(3, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, vector)

    tasa = 0
    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))

    for i in range(meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = (((i >= (OutPut['Duración'] + OutPut['Meses garantía fabricante'])) &
                (OutPut['TEMP_numeromes'] <= (i - (OutPut['Duración'] + OutPut['Meses garantía fabricante'])))) |
               (i == 1))  # Confirmar la duración + mese de garantia del fabricante
        cl2 = i >= OutPut['TEMP_numeromes']
        cl3 = i == OutPut['TEMP_numeromes']
        rl1 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida'])
        tasa = np.where(
            cl2,
            np.where(
                cl1,
                0,
                np.where(
                    cl3,
                    0,
                    np.where(
                        cg1,
                        0,
                        rl1
                    )
                )
            ),
            0
        )
        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = tasa

    OutPut['cancelaciones'] = np.where(
        OutPut['TEMP_numeromes'] <= 5,  # Condicional par determinar si se le asigna el vector de comportamiento de la caida o no
        np.where(
            OutPut['TEMP_numeromes'] == 1,
            vigentesStock.lookup(OutPut.index, 'vigentesStockRRC_Mes ' + (OutPut['TEMP_numeromes'] - 1).astype(str)) * (OutPut['Caida']),
            np.where(
                cg1,
                0,
                (OutPut['vigentes'].shift(1) * (OutPut['Caida'] * vector['Vector Control RRC']))
            )
        ),
        np.where(
            cg1,
            0,
            (OutPut['vigentes'].shift(1) * (OutPut['Caida']))
        )
    )

    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    OutPut_tasa_caida_cancel = pd.concat([OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2], sort=False)
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel.sort_index()
    return OutPut, OutPut_tasa_caida_cancel


def vigentes_y_cancelaciones_prima_amortizada(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses):
    OutPut_tasa, vector, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables(4, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    tasa = 0
    # Condiciones y soluciones globales para optimización del código
    cg1 = ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))

    for i in range(meses + 1):
        # Condiciones y soluciones locales para optimización del código
        cl1 = i > OutPut['TEMP_numeromes']
        cl2 = (OutPut['TEMP_numeromes'] > (i + OutPut['Duración']))  # Confirmar la duración + mese de garantía del fabricante
        cl3 = i == OutPut['TEMP_numeromes']
        cl4 = ((((i - OutPut['TEMP_numeromes']) % OutPut['Amortizacion/CambioPrima']) == 1) & ((i - OutPut['TEMP_numeromes']) >= 1))
        rl1 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida'])
        rl2 = (tasa + (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida']))
        tasa = np.where(
            cl1,
            np.where(
                cl2,
                0,
                np.where(
                    cl3,
                    0,
                    np.where(
                        cg1,
                        0,
                        np.where(
                            cl4,
                            rl1,
                            rl2
                        )
                    )
                )
            ),
            0
        )
        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = tasa

        # Recalculo de Tasa caida para tipo de prima amortizada
        # cond3 = i == OutPut_tasa['TEMP_numeromes']
        # choice1 = OutPut_tasa['nuevos']
        tasa1 = np.where(
            cl1,
            np.where(
                cl2,
                0,
                np.where(
                    cl3,
                    OutPut_tasa['nuevos'],
                    1
                )
            ),
            0
        )
        # OutPut_tasa['tasa_caida_' + str(i)] = tasa1

    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    OutPut_tasa_caida_cancel = pd.concat([OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2], sort=False)
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel.sort_index()
    return OutPut, OutPut_tasa_caida_cancel


def vigentes_y_cancelaciones_prima_multiprima(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses):
    OutPut_tasa, vector, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables(5, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    tasa = 0
    # Condiciones y soluciones globales para optimizacion del codigo
    cg1 = ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))

    for i in range(meses + 1):
        # Condiciones y soluciones locales para optimizacion del codigo
        cl1 = i >= OutPut['TEMP_numeromes']
        cl2 = (((i >= (OutPut['Duración'])) & (OutPut['TEMP_numeromes'] <= (i - (OutPut['Duración'])))) | (i == 1))  # Confirmar la duración + mese de garantia del fabricante
        cl3 = i == OutPut['TEMP_numeromes']
        rl1 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida'])

        tasa = np.where(
            cl1,
            np.where(
                cl2,
                0,
                np.where(
                    cl3,
                    0,
                    np.where(
                        cg1,
                        0,
                        rl1
                    )
                )
            ),
            0
        )

        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = tasa

    OutPut = pd.concat([OutPut, OutPut_NEW_2], sort=False)
    OutPut = OutPut.sort_index()
    OutPut_tasa_caida_cancel = pd.concat([OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2], sort=False)
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel.sort_index()
    return OutPut, OutPut_tasa_caida_cancel


def preparar_variables(Id_T_Prima, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, vector=[]):
    OutPut_tasa['Id_T.Prima'] = OutPut['Id_T.Prima']
    OutPut_tasa['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    OutPut_tasa['Duración'] = OutPut['Duración']
    OutPut_tasa['Meses garantía fabricante'] = OutPut['Meses garantía fabricante']
    OutPut_tasa['nuevos'] = OutPut['nuevos']
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Id_T.Prima'] == Id_T_Prima]

    OutPut_tasa_caida_cancel['Id_T.Prima'] = OutPut['Id_T.Prima']

    OutPut_tasa_caida_cancel_NEW_2 = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Id_T.Prima'] != Id_T_Prima]
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Id_T.Prima'] == Id_T_Prima]

    if len(vector) > 0:
        vector['Id_T.Prima'] = OutPut['Id_T.Prima']
        vector = vector[vector['Id_T.Prima'] == Id_T_Prima]

    OutPut_NEW_2 = OutPut[OutPut['Id_T.Prima'] != Id_T_Prima]
    OutPut = OutPut[OutPut['Id_T.Prima'] == Id_T_Prima]

    return OutPut_tasa, vector, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2
