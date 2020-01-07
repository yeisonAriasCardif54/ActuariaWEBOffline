''' Obtener tasa de caida  VIG'''
import numpy as np
import pandas as pd

# import time

def obtener_tasa(OutPut, meses, mesiniciost):

    # -- Creación de variable OutPut_tasa -- #
    OutPut_tasa = pd.DataFrame({})
    # -- Agregamos variables requeridas a OutPut_tasa -- #

    OutPut_tasa['Producto'] = OutPut['Producto']
    OutPut_tasa['Id_T.Prima'] = OutPut['Tipo de prima']
    OutPut_tasa['Mes'] = OutPut['Mes']
    OutPut_tasa['Duración del producto financiero'] = OutPut['Duración del producto financiero']
    OutPut_tasa['nuevos'] = OutPut['nuevos']
    OutPut_tasa['Caida'] = OutPut['Caida']
    OutPut_tasa['Mes 0'] = (OutPut['Clientes potenciales/mes'] * OutPut['penetración'] * (1 + OutPut['Tasa crecimiento mensual'] * (OutPut['Mes'] - 1))) + OutPut['Stock inicial']
    OutPut_tasa['Tipo Proyección'] = 'Nuevo'

    OutPut_tasa['tasa_caida_-1'] = 0

    condlist = [(OutPut_tasa['Tipo Proyección'] == 'Nuevo')]

    def Tasa(OutPut_tasa, i, condlist):
        # -- Definir condiciones y respuestas repetidas en bucle para optimizar su velocidad -- #
        cond3 = i == OutPut_tasa['Mes']
        choice1 = OutPut_tasa['nuevos']
        choicelist = [
            np.where(
                (i < OutPut_tasa['Mes']) |
                (OutPut_tasa['Mes'] <= (i - (OutPut_tasa['Duración del producto financiero']))),
                0,
                np.where(
                    cond3,
                    choice1,
                    OutPut_tasa['tasa_caida_' + str(i - 1)] - (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut_tasa['Caida']),
                )
            )
        ]
        return np.select(condlist, choicelist, default=0)

    for i in range(meses + 1):
        OutPut_tasa['tasa_caida_' + str(i)] = Tasa(OutPut_tasa, i, condlist)

    return OutPut, OutPut_tasa
