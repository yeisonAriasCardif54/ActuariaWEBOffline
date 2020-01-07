''' Obtener tasa de caida  VIG'''

import numpy as np
import pandas as pd

np.seterr(invalid='ignore')


# import time


def obtener_tasa(OutPut, meses, mesiniciost, desembolsos_st_TEMP, vigentesStock, vector):
    # start_time = time.time()
    # Unificar información de Stock RRC (Vigentes)
    vigentesStock = pd.merge(OutPut.filter(['Id_Tool']), vigentesStock, left_on='Id_Tool', right_on='Id_Tool', how='left')

    # Unificar información de vector con OutPut
    vector = pd.merge(OutPut.filter(['Id_Tool', 'TEMP_numeromes']), vector, left_on='TEMP_numeromes', right_on='Mes', how='left')
    vector['Id_T.Prima'] = OutPut['Id_T.Prima']

    # Anadir mes cero a OutPut
    OutPut['Id_Tool'] = OutPut['Id_Tool'].astype(np.int64)
    desembolsos_st_TEMP_ = desembolsos_st_TEMP.filter(['Id_Tool', 'Mes 0'])
    OutPut = pd.merge(OutPut, desembolsos_st_TEMP_, on='Id_Tool', how='left')
    OutPut['Mes 0'] = OutPut['Mes 0'].fillna(0)

    # Creacion de variable OutPut_tasa
    OutPut_tasa = pd.DataFrame({})
    # Agregamos variables requeridas a OutPut_tasa

    OutPut_tasa['Id_Tool'] = OutPut['Id_Tool']
    OutPut_tasa['Id_T.Prima'] = OutPut['Id_T.Prima']
    OutPut_tasa['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    OutPut_tasa['Duración'] = OutPut['Duración']
    OutPut_tasa['Meses garantía fabricante'] = OutPut['Meses garantía fabricante']
    OutPut_tasa['nuevos'] = OutPut['nuevos']
    OutPut_tasa['Caida'] = OutPut['Caida']
    OutPut_tasa['Mes 0'] = OutPut['Mes 0']
    OutPut_tasa['Tipo Proyección'] = OutPut['Tipo Proyección']

    OutPut_tasa['tasa_caida_-1'] = 0

    condlist = [(OutPut_tasa['Tipo Proyección'] == 'Nuevo'), (OutPut_tasa['Tipo Proyección'] == 'Stock'), (OutPut_tasa['Tipo Proyección'] == 'Stock_RRC')]

    # Definir condiciones repetidas en bucle para optimizar su velocidad
    cond1 = OutPut_tasa['Id_T.Prima'] == 1  # para mensual
    cond2 = OutPut_tasa['TEMP_numeromes'] == 1
    cond4 = OutPut_tasa['TEMP_numeromes'] <= mesiniciost

    def Tasa(OutPut_tasa, i, condlist, cond1, cond2, cond4, vigentesStock, vector):
        # Definir condiciones y respuestas repetidas en bucle para optimizar su velocidad
        cond3 = i == OutPut_tasa['TEMP_numeromes']
        choice1 = OutPut_tasa['nuevos']
        choice2 = OutPut_tasa['tasa_caida_' + str(i - 1)] * (1 - OutPut_tasa['Caida'])
        choicelist = [
            np.where(  # Nuevos
                (i < OutPut_tasa['TEMP_numeromes']) |
                (OutPut_tasa['TEMP_numeromes'] <= (i - (OutPut_tasa['Duración'] + OutPut_tasa['Meses garantía fabricante']))),
                0,
                np.where(
                    cond3,
                    choice1,
                    OutPut_tasa['tasa_caida_' + str(i - 1)] - (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut_tasa['Caida']),
                )
            ),
            np.where(  # Stock
                (cond4) |
                (
                        ((i > (OutPut_tasa['Duración']))) |
                        (OutPut_tasa['TEMP_numeromes'] <= ((i - OutPut_tasa['Duración'])))
                ),
                0,
                np.where(
                    cond3,
                    np.where(
                        cond1,
                        np.where(
                            cond2,
                            OutPut_tasa['Mes 0'] * (1 - OutPut_tasa['Caida']),
                            0
                        ),
                        choice1
                    ),
                    np.where(
                        cond1,
                        np.where(
                            cond2,
                            OutPut_tasa['tasa_caida_' + str(i - 1)] + choice1 - (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut_tasa['Caida']),
                            0
                        ),
                        choice2
                    )
                ),
            ),
            np.where(  # Stock_RRC
                OutPut['TEMP_numeromes'] == i,
                np.where(
                    (OutPut['TEMP_numeromes'] == 1),
                    vigentesStock.lookup(OutPut_tasa.index, 'vigentesStockRRC_Mes ' + (OutPut_tasa['TEMP_numeromes']).astype(str)),
                    np.where(
                        ((OutPut['TEMP_numeromes'] > 1) & (OutPut['TEMP_numeromes'] <= 5)),
                        vigentesStock.lookup(OutPut_tasa.index, 'vigentesStockRRC_Mes ' + (OutPut_tasa['TEMP_numeromes']).astype(str)) - (OutPut_tasa['tasa_caida_' + str(i - 1)].shift() * (OutPut_tasa['Caida'] * vector['Vector Control RRC'])),
                        np.maximum(
                            (vigentesStock.lookup(OutPut_tasa.index, 'vigentesStockRRC_Mes ' + (OutPut_tasa['TEMP_numeromes']).astype(str)) - (OutPut_tasa['tasa_caida_' + str(i - 1)].shift() * OutPut_tasa['Caida'])),
                            0
                        )
                    )
                ),
                0
            )
        ]
        return np.select(condlist, choicelist, default=0)

    for i in range(meses + 1):
        OutPut_tasa['tasa_caida_' + str(i)] = Tasa(OutPut_tasa, i, condlist, cond1, cond2, cond4, vigentesStock, vector)

    del (OutPut_tasa['TEMP_numeromes'])
    del (OutPut_tasa['Duración'])
    del (OutPut_tasa['Meses garantía fabricante'])
    del (OutPut_tasa['nuevos'])
    del (OutPut_tasa['Caida'])
    del (OutPut_tasa['Mes 0'])
    del (OutPut_tasa['Tipo Proyección'])

    # print("\n\n obtener_tasa \n--- %s seconds ---" % (time.time() - start_time))
    print('\n\n\n - OutPut_tasa - \n\n\n')
    print(OutPut_tasa)
    return OutPut, OutPut_tasa
