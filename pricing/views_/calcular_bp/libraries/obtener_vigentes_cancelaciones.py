import numpy as np
import pandas as pd


def obtener_vigentes_y_cancelaciones(OutPut, OutPut_tasa, meses, caidaren):
    pd.options.mode.chained_assignment = None

    OutPut['vigentes'] = 0
    OutPut['cancelaciones'] = 0

    # -------------------------------------------------------------------------- #
    # ----------------------- INICIO Obtener vigentes -------------------------- #
    # -------------------------------------------------------------------------- #
    # -- Agrupar OutPut_tasa_agrupada -- #
    OutPut_tasa_agrupada = OutPut_tasa.groupby('Producto').sum()
    OutPut_tasa_agrupada['Producto'] = OutPut_tasa_agrupada.index
    OutPut_tasa_agrupada = pd.merge(OutPut.filter(['Producto']), OutPut_tasa_agrupada, left_on='Producto', right_on='Producto', how='left')

    # -- Obtener vigentes de Stock y Nuevos -- #
    OutPut['vigentes'] = OutPut_tasa_agrupada.lookup(OutPut_tasa_agrupada.index, 'tasa_caida_' + (OutPut['Mes']).astype(str))
    OutPut['vigentes'] = OutPut['vigentes'].fillna(0)
    # ----------------------------------------------------------------------- #
    # ----------------------- FIN Obtener vigentes -------------------------- #
    # ----------------------------------------------------------------------- #

    # ---------------------------------------------------------------------------------- #
    # -------------------------- Inicio Obtener Cancelaciones -------------------------- #
    # ---------------------------------------------------------------------------------- #
    # -- Creación de variable OutPut_tasa_caida_cancel -- #
    OutPut_tasa_caida_cancel = pd.DataFrame({})
    OutPut_tasa_caida_cancel['Producto'] = OutPut['Producto']
    OutPut_tasa_caida_cancel['Tipo de prima'] = OutPut['Tipo de prima']
    # -- Creación de columnas tasa_caida_cancel_-1 a tasa_caida_cancel_'meses' -- #
    for i in range(-1, meses + 1):
        OutPut_tasa_caida_cancel['tasa_caida_cancel_' + str(i)] = 0

    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_mensual(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_periodica(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, caidaren)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_unica(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)
    OutPut, OutPut_tasa_caida_cancel = vigentes_y_cancelaciones_prima_multiprima(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    # -- Agrupar OutPut_tasa_caida_cancel -- #
    OutPut_tasa_caida_agrupada = OutPut_tasa_caida_cancel.groupby('Producto').sum()
    OutPut_tasa_caida_agrupada['Producto'] = OutPut_tasa_caida_agrupada.index
    OutPut_tasa_caida_agrupada['Producto'] = OutPut_tasa_caida_agrupada['Producto'].astype(np.int32)
    OutPut_tasa_caida_agrupada = pd.merge(OutPut.filter(['Producto']), OutPut_tasa_caida_agrupada, left_on='Producto', right_on='Producto', how='left')
    # -- Obtener Cancelaciones -- #
    OutPut['cancelaciones'] = OutPut_tasa_caida_agrupada.lookup(OutPut_tasa_caida_agrupada.index, 'tasa_caida_cancel_' + (OutPut['Mes']).astype(str))

    # ----------------------------------------------------------------------------- #
    # ------------------------ Fin Obtener Cancelaciones -------------------------- #
    # ----------------------------------------------------------------------------- #

    return OutPut, OutPut_tasa_caida_cancel


def vigentes_y_cancelaciones_prima_mensual(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses):
    OutPut_tasa, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables('Mensual', OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    for i in range(meses + 1):
        # -- Condiciones y soluciones locales para optimización del código -- #
        cl1 = i >= OutPut['Mes']
        cl2 = ((i >= OutPut['Duración del producto financiero']) & (OutPut['Mes'] <= (i - OutPut['Duración del producto financiero'])) | (i == 1))
        cl3 = i == OutPut['Mes']
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
                        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
                        0,
                        rl1
                    ),
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


def vigentes_y_cancelaciones_prima_periodica(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses, caidaren):
    OutPut_tasa, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables('Periódica', OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    for i in range(meses + 1):
        # -- Condiciones y soluciones locales para optimización del código -- #
        cl1 = i >= OutPut['Mes']
        cl2 = ((i >= OutPut['Duración del producto financiero']) & (OutPut['Mes'] <= (i - OutPut['Duración del producto financiero'])) | (i == 1))
        cl3 = i == OutPut['Mes']
        cl4 = ((meses - OutPut['Mes']) % OutPut['Periodo de pago/CambioPrima']) == 0
        cl5 = (i <= (OutPut['Duración del producto financiero']))

        rl1 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * (OutPut['Caida'] + caidaren))
        rl2 = (OutPut_tasa['tasa_caida_' + str(i - 1)] * OutPut['Caida'])
        tasa = np.where(
            cl1,
            np.where(
                cl2,
                0,
                np.where(
                    cl3,
                    0,
                    np.where(
                        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
                        0,
                        np.where(
                            cl4,
                            rl1,
                            rl2
                        )
                    ),
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


def vigentes_y_cancelaciones_prima_unica(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses):
    OutPut_tasa, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables('Única', OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    tasa = 0
    for i in range(meses + 1):
        # -- Condiciones y soluciones locales para optimización del código -- #
        cl1 = (((i >= (OutPut['Duración del producto financiero'])) &
                (OutPut['Mes'] <= (i - (OutPut['Duración del producto financiero'])))) |
               (i == 1))
        cl2 = i >= OutPut['Mes']
        cl3 = i == OutPut['Mes']
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
                        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
                        0,
                        rl1
                    ),
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


def vigentes_y_cancelaciones_prima_multiprima(OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses):
    OutPut_tasa, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2 = preparar_variables('Multiprima', OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses)

    tasa = 0
    for i in range(meses + 1):
        # -- Condiciones y soluciones locales para optimización del código -- #
        cl1 = i >= OutPut['Mes']
        cl2 = (((i >= (OutPut['Duración del producto financiero'])) & (OutPut['Mes'] <= (i - (OutPut['Duración del producto financiero'])))) | (i == 1))
        cl3 = i == OutPut['Mes']
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
                        ((OutPut['Si run off ó cut off al fin de la producción'] == "Cut Off") & (OutPut['Mes'] >= OutPut['Duración del producto financiero'])),
                        0,
                        rl1
                    ),
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


def preparar_variables(Id_T_Prima, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa, meses):
    OutPut_tasa['Tipo de prima'] = OutPut['Tipo de prima']
    OutPut_tasa['Mes'] = OutPut['Mes']
    OutPut_tasa['nuevos'] = OutPut['nuevos']
    OutPut_tasa = OutPut_tasa[OutPut_tasa['Tipo de prima'] == Id_T_Prima]
    OutPut_tasa_caida_cancel['Tipo de prima'] = OutPut['Tipo de prima']
    OutPut_tasa_caida_cancel_NEW_2 = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Tipo de prima'] != Id_T_Prima]
    OutPut_tasa_caida_cancel = OutPut_tasa_caida_cancel[OutPut_tasa_caida_cancel['Tipo de prima'] == Id_T_Prima]
    OutPut_NEW_2 = OutPut[OutPut['Tipo de prima'] != Id_T_Prima]
    OutPut = OutPut[OutPut['Tipo de prima'] == Id_T_Prima]
    return OutPut_tasa, OutPut_NEW_2, OutPut, OutPut_tasa_caida_cancel, OutPut_tasa_caida_cancel_NEW_2
