''' Obtener comisiones '''

import numpy as np
import time


def obtener_comisiones(OutPut, meses):
    # start_time = time.time()
    # Obtiene las comisiones diferidas
    OutPut['dac'] = OutPut['upr'] * OutPut['Comisión']

    # Definir condiciones repetidas en bucle para optimizar su velocidad
    cg1 = OutPut['Tipo Proyección'] != 'Stock_RRC'
    cg2 = ((meses >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0))

    sg1 = OutPut['gwp'] * OutPut['Comisión']

    OutPut['commin'] = np.where(
        cg1,
        np.where(
            cg2,
            OutPut['dac'].shift(1) * -1,
            sg1
        ),
        ##### Stock_RRC #####
        np.where(
            OutPut['Id_T.Prima'] == 2,  # UNICA
            np.where(
                OutPut['TEMP_numeromes'] > 12,
                0,
                np.where(
                    cg2,
                    OutPut['dac'].shift(1) * -1,
                    sg1
                )
            ),
            np.where(
                cg2,
                OutPut['dac'].shift(1) * -1,
                sg1
            )
        )
    )

    OutPut['commins'] = OutPut['commin'] * OutPut['%Part.Socio']
    OutPut['commins'] = OutPut['commins'].fillna(0)

    OutPut['cominb'] = OutPut['commin'] * OutPut['%Part.Broker']
    OutPut['cominb'] = OutPut['cominb'].fillna(0)

    # Obtiene las comisiones devengadas
    ##Variable temporal dac-1
    OutPut['TEMP_dac-1'] = 0
    OutPut['TEMP_dac-1'] = np.where(
        OutPut['TEMP_dac-1'] == 0,
        OutPut['dac'].shift(1),
        0
    )

    OutPut['earnedC'] = np.where(
        cg1,
        np.where(
            OutPut['TEMP_numeromes'] == 1,
            OutPut['commin'] - OutPut['dac'],
            OutPut['commin'] - OutPut['dac'] + OutPut['TEMP_dac-1'],
        ),
        ##### Stock_RRC #####
        np.where(
            (OutPut['Id_T.Prima'] == 1) | (OutPut['Id_T.Prima'] == 3),  # PRIMA MENSUAL && UNICA
            np.where(
                OutPut['TEMP_numeromes'] == 1,
                OutPut['earnedP'] * OutPut['Comisión'],
                OutPut['commin'] - OutPut['dac'] + OutPut['TEMP_dac-1']
            ),
            np.where(  # PRIMA ANUAL
                OutPut['TEMP_numeromes'] > 12,
                0,
                np.where(
                    OutPut['TEMP_numeromes'] == 1,
                    OutPut['earnedP'] * OutPut['Comisión'],
                    OutPut['commin'] - OutPut['dac'] + OutPut['TEMP_dac-1']
                )

            )
        )
    )

    OutPut['ecs'] = OutPut['earnedC'] * OutPut['%Part.Socio']
    OutPut['ecs'] = OutPut['ecs'].fillna(0)

    OutPut['ecb'] = OutPut['earnedC'] * OutPut['%Part.Broker']
    OutPut['ecb'] = OutPut['ecb'].fillna(0)

    return OutPut
