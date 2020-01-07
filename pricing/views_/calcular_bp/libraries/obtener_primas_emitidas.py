import pandas as pd
import numpy as np
from math import floor


def obtener_primas_emitidas(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad):
    pd.options.mode.chained_assignment = None

    OutPut_tasa_caida_cancel['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']
    OutPut_tasa['TEMP_key_numeromeses'] = OutPut['TEMP_key_numeromeses']

    # -- Calcular y -- #
    OutPut['y'] = round((OutPut['Mes'] - 1) / 12, 1)
    OutPut['y'] = np.floor(OutPut['y'])
    y = round((meses - 1) / 12, 0)
    OutPut['x'] = 0

    # -- Crear Dataframe para guardar variables calculadas gwpnt_, gwpst_, uprt_ -- #
    OutPut_PRI = pd.DataFrame()

    # -- Creación de columnas gwpnt_0 a gwpnt_'meses' # Creación de columnas gwpst_0 a gwpst_'meses' # Creación de columnas uprt_0 a uprt_'meses' -- #
    for i in range(0, meses + 1):
        OutPut_PRI['gwpnt_' + str(i)] = 0
        OutPut_PRI['gwpst_' + str(i)] = 0
        OutPut_PRI['uprt_' + str(i)] = 0
        OutPut_PRI['vig_' + str(i)] = 0

    # -- Nuevas variables -- #
    OutPut['gwpn'] = 0.0
    OutPut['gwps'] = 0.0
    OutPut['gwp'] = 0.0
    OutPut['upr'] = 0.0
    OutPut['earnedP'] = 0.0

    OutPut = primas_emitidas_prima_mensual(OutPut, meses)
    OutPut, OutPut_PRI_temp = primas_emitidas_prima_periodica(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI)
    OutPut = primas_emitidas_prima_unica(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI)
    OutPut = primas_emitidas_prima_multiprima(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI)

    OutPut['gwpsc'] = OutPut['gwp'] + OutPut['gwpn']

    # -- Cálculo de earnedP -- #
    OutPut['earnedP'] = np.where(
        OutPut['Tipo de prima'] == 'Mensual',
        OutPut['Vlr prima'] * OutPut['vigentes'],
        np.where(
            OutPut['Tipo de prima'] == 'Periódica',
            (OutPut['Vlr prima'] / OutPut['Periodo de pago/CambioPrima']) * OutPut['vigentes'],
            np.where(
                OutPut['Tipo de prima'] == 'Única',
                (OutPut['Vlr prima'] / OutPut['Duración del producto financiero']) * OutPut['vigentes'],
                (OutPut['Vlr prima'] / OutPut['Periodo de pago/CambioPrima']) * OutPut['vigentes']
            )
        )
    )

    # PAGOS 1ER DIA
    OutPut['upr'] = (OutPut['gwp'] - OutPut['earnedP']).cumsum()

    ''' 
    # NORMAL
    OutPut['upr-.5'] = OutPut['earnedP'] * 0.5
    OutPut['upr'] = np.where(
        OutPut['Mes'] == 1,
        (OutPut['gwp'] - (OutPut['earnedP'] * 0.5)),
        ((OutPut['gwp'] - (OutPut['earnedP'] * 0.5)) - OutPut['upr-.5'].shift(1))
    ).cumsum()
    '''
    '''
    # Cálculo de earnedP
    OutPut['earnedP'] = np.where(
        OutPut['Mes'] == 1,
        OutPut['gwp'] - OutPut['upr'],
        OutPut['gwp'] - OutPut['upr'] + OutPut['upr'].shift(1),
    )
    '''

    return OutPut, OutPut_PRI_temp


def primas_emitidas_prima_mensual(OutPut, meses):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Mensual']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Mensual']

    OutPut['gwp'] = OutPut['vigentes'] * OutPut['Vlr prima']
    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    # -- Cálculo de la reserva requerida mensual, UPR_eop -- #
    OutPut['upr'] = np.where(
        OutPut['Tipo de prima'] == 'Mensual',
        np.where(
            OutPut['Canal'] == 'Compulsory',
            0,
            OutPut['gwp'] * 0.5
        ),
        OutPut['upr']
    )

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut


def primas_emitidas_prima_periodica(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Periódica']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Periódica']
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Tipo de prima'] == 'Periódica']
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Tipo de prima'] == 'Periódica']
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] == 'Periódica']
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] == 'Periódica']

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Producto'] = OutPut['Producto']

    # -- Condiciones y soluciones globales para optimización del código -- #
    cg3 = ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero']))

    for i in range(meses + 1):
        # -- Calcular gwpnt -- #
        OutPut_PRI['gwpnt_' + str(i)] = OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]

        # -- Calcular gwpst -- #
        OutPut_PRI['gwpst_' + str(i)] = np.where(
            ((i > OutPut['Periodo de pago/CambioPrima']) & (i > OutPut['Mes']) & (((i - OutPut['Mes']) % OutPut['Periodo de pago/CambioPrima']) == 0)),
            np.where(
                cg3,
                0,
                OutPut_tasa['tasa_caida_' + str(i)] * OutPut['Vlr prima']
            ),
            0
        )

        # --  Calcular uprt -- #
        OutPut_PRI['uprt_' + str(i)] = np.where(
            OutPut['Tipo de prima'] == 'Periódica',
            OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)],
            OutPut_PRI['uprt_' + str(i)]
        )

        # -- Calcular gwpn -- #
        OutPut['gwpn'] = np.where(
            OutPut['Mes'] <= 5,
            np.where(
                OutPut['Mes'] == 1,
                OutPut['Caida'],
                OutPut['upr'].shift(1) * OutPut['Caida']
            ),
            np.where(
                OutPut['Mes'] <= OutPut['Periodo de pago/CambioPrima'],
                OutPut['upr'].shift(1) * OutPut['Caida'],
                0
            )
        )

        # -- Cálculo de la reserva requerida mensual, UPR_eop -- #
        OutPut['upr'] = np.where(
            OutPut['Mes'] <= OutPut['Periodo de pago/CambioPrima'],
            np.where(
                ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
                0,
                OutPut['gwpn']
            ),
            0
        )

    # -- Agrupar OutPut_PRI -- #
    # -- Calcular gwps -- #
    OutPut_PRI_agrupada = OutPut_PRI.groupby('Producto').sum()
    OutPut_PRI_agrupada['Producto'] = OutPut_PRI_agrupada.index
    OutPut_PRI_agrupada['Producto'] = OutPut_PRI_agrupada['Producto'].astype(np.int32)
    OutPut_PRI_agrupada = pd.merge(OutPut.filter(['Producto']), OutPut_PRI_agrupada, left_on='Producto', right_on='Producto', how='left')

    # -- Obtener vigentes de Stock y Nuevos -- #
    OutPut['gwps'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpst_' + (OutPut['Mes']).astype(str))

    # --Calcular gwpn -- #
    OutPut['gwpn'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['Mes']).astype(str))

    # -- Cálculo de la reserva requerida mensual, UPR_eop -- #
    OutPut['upr'] = np.where(
        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
        0,
        OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'uprt_' + (OutPut['Mes']).astype(str)),
    )

    # -- Calcular y -- #
    OutPut['y'] = (OutPut['Mes'] - 1) / 12
    OutPut['y'] = np.floor(OutPut['y'])

    # -- Calcular x -- #
    OutPut['x'] = OutPut['nuevos'] * OutPut['Vlr prima']
    OutPut['x'] = OutPut['x'].fillna(0)

    # -- Calcular gwp -- #
    OutPut['gwp'] = np.where(
        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
        OutPut['gwp'].shift(1),
        OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
    )

    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()

    return OutPut, OutPut_PRI


def primas_emitidas_prima_unica(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Única']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Única']
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Tipo de prima'] == 'Única']
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Tipo de prima'] == 'Única']
    OutPut_vlrprimac = OutPut_vlrprimac[OutPut_vlrprimac['Tipo de prima'] == 'Única']
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] == 'Única']

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Producto'] = OutPut['Producto']

    for i in range(meses + 1):
        # -- Calcular gwpnt -- #
        OutPut_PRI['gwpnt_' + str(i)] = OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]

        # -- Calcular gwpn -- #
        OutPut['gwpn'] = np.where(
            (i == OutPut['Mes']),
            OutPut_PRI.groupby(['Producto'])['gwpnt_' + str(i)].sum()[OutPut['Producto']],
            OutPut['gwpn']
        )

        # -- Calcular gwpst -- #
        OutPut_PRI['gwpst_' + str(i)] = 0

        # -- Calcular gwps -- #
        OutPut['gwps'] = 0

        # -- Calcular uprt -- #
        uprt = OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)]

        OutPut_PRI['uprt_' + str(i)] = np.where(
            (OutPut['Tipo de prima'] == 'Única'),
            uprt,
            OutPut_PRI['uprt_' + str(i)]
        )

        # -- Calcular upr -- #
        OutPut['upr'] = np.where(
            (i == OutPut['Mes']),
            np.where(
                ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
                0,
                OutPut_PRI.groupby(['Producto'])['uprt_' + str(i)].sum()[OutPut['Producto']]
            ),
            OutPut['upr']
        )

    # -- Calcular y -- #
    OutPut['y'] = (OutPut['Mes']) / 12
    OutPut['y'] = OutPut['y'].astype(np.float64)
    OutPut['y'] = round(OutPut['y'], 1)
    OutPut['y'] = np.floor(OutPut['y'])

    # -- Calcular x -- #
    OutPut['x'] = OutPut['nuevos'] * OutPut['Vlr prima']
    OutPut['x'] = OutPut['x'].fillna(0)

    # -- Calcular gwp -- #
    OutPut['gwp'] = np.where(
        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
        OutPut['upr'].shift(1) * -1,
        OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
    )

    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut


def primas_emitidas_prima_multiprima(OutPut, meses, OutPut_tasa_caida_cancel, OutPut_tasa, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI):
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != 'Multiprima']
    OutPut = OutPut[OutPut['Tipo de prima'] == 'Multiprima']
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Tipo de prima'] == 'Multiprima']
    OutPut_vlrprimad = OutPut_vlrprimad[OutPut_vlrprimad['Tipo de prima'] == 'Multiprima']

    OutPut_PRI = OutPut_PRI[:-0]
    OutPut_PRI['Producto'] = OutPut['Producto']

    # -- Calcular y -- #
    OutPut['y'] = round((OutPut['Mes'] - 1) / 12, 1)
    OutPut['y'] = np.floor(OutPut['y'])

    for i in range(meses + 1):
        # -- Calcular gwpnt -- #
        OutPut_PRI['gwpnt_' + str(i)] = OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] * OutPut_vlrprimac['vlrprimac_' + str(i - 1)]

        # -- Calcular uprt -- #
        OutPut_PRI['uprt_' + str(i)] = OutPut_tasa['tasa_caida_' + str(i)] * OutPut_vlrprimad['vlrprimad_' + str(i)]

        # -- Triangulo vigentes para prima multiprima -- #
        '''
        OutPut_PRI['vig_' + str(i)] = np.where(
            (OutPut['Mes'] + OutPut['Periodo de pago/CambioPrima']) <= i,
            OutPut_tasa['tasa_caida_' + str(i)],
            OutPut_PRI['vig_' + str(i)]
        )
        '''

    # -- Calcular gwps -- #
    OutPut['gwps'] = 0

    # -- Agrupar OutPut_PRI -- #
    OutPut_PRI_agrupada = OutPut_PRI.groupby('Producto').sum()
    OutPut_PRI_agrupada['Producto'] = OutPut_PRI_agrupada.index
    OutPut_PRI_agrupada['Producto'] = OutPut_PRI_agrupada['Producto'].astype(np.int32)
    OutPut_PRI_agrupada = pd.merge(OutPut.filter(['Producto']), OutPut_PRI_agrupada, left_on='Producto', right_on='Producto', how='left')

    # -- Calcular gwpn -- #
    # OutPut['gwpn'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['Mes']).astype(str))
    '''
    OutPut['gwpn'] = np.where(
        (OutPut['Mes'] <= OutPut['Periodo de pago/CambioPrima']),
        OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['Mes']).astype(str)),
        0
    )
    '''
    OutPut['gwpn'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'gwpnt_' + (OutPut['Mes']).astype(str))
    OutPut['vig'] = OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'vig_' + (OutPut['Mes']).astype(str))

    # -- Cálculo de la reserva requerida mensual, UPR_eop -- #
    OutPut['upr'] = np.where(
        (OutPut['Mes'] > OutPut['Periodo de pago/CambioPrima']),
        np.where(
            ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
            0,
            np.where(
                OutPut['Canal'] == 'Compulsory',
                0,
                # -- Calculo igual al calculo de gwp en esta instancia (es igual a gwp(k) * 0.5) -- #
                (OutPut['vigentes'] * OutPut['Vlr prima']) * 0.5
            )
        ),
        np.where(
            ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
            0,
            OutPut_PRI_agrupada.lookup(OutPut_PRI_agrupada.index, 'uprt_' + (OutPut['Mes']).astype(str)),
        ),
    )

    # -- Calcular x -- #
    OutPut['x'] = OutPut['nuevos'] * OutPut['Vlr prima']

    # -- Calcular gwp -- #
    OutPut['gwp'] = np.where(
        (OutPut['Mes'] > OutPut['Periodo de pago/CambioPrima']),
        np.where(
            ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
            OutPut['upr'].shift(1) * -1,
            (((OutPut['vig'] * OutPut['Vlr prima']) / OutPut['Periodo de pago/CambioPrima']) + (OutPut['nuevos'] * OutPut['Vlr prima'])) - OutPut['gwpn']
        ),
        np.where(
            ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
            OutPut['gwp'].shift(1),
            OutPut['gwps'] + OutPut['x'] - OutPut['gwpn']
        )
    )

    OutPut['gwp'] = OutPut['gwp'].fillna(0)
    OutPut['gwp'] = OutPut['gwp'].astype(np.float64)

    OutPut = pd.concat([OutPut, OutPut_NEW_2])
    OutPut = OutPut.sort_index()
    return OutPut
