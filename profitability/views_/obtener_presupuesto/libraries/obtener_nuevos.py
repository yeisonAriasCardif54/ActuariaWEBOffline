''' Obtener los nuevos '''

import pandas as pd
import numpy as np


# import time


def obtener_nuevos(OutPut, meses, parametros_st, parametros_nv, desembolsos_st, desembolsos_nv, mesanual, mesiniciost, caidaren, ctmkac, ctmktc):
    # start_time = time.time()
    # *****Calculo de los nuevos clientes*****
    # Obtener columna de desembolsos
    OutPut = obtener_desembolso(OutPut, meses, parametros_st, parametros_nv, desembolsos_st, desembolsos_nv)
    OutPut['Desembolso'] = OutPut['Desembolso'].fillna(0)
    OutPut['Desembolso'] = OutPut['Desembolso'].astype(np.float64)
    # Obtener penetracion
    OutPut['penetracion'] = 0
    condlist = [
        ((OutPut['TEMP_numeromes'] + mesanual) <= 3 + OutPut['Mes Inicio']),
        ((OutPut['TEMP_numeromes'] + mesanual) <= 6 + OutPut['Mes Inicio']),
        ((OutPut['TEMP_numeromes'] + mesanual) <= 9 + OutPut['Mes Inicio'])
    ]
    choicelist = [
        OutPut['Pent. Q1'],
        OutPut['Pent. Q2'],
        OutPut['Pent. Q3']
    ]
    mesTEMP = OutPut['TEMP_numeromes'] - ((12 + 1) - mesanual)
    mesTEMP2 = OutPut['TEMP_numeromes'] - ((24 + 1) - mesanual)
    OutPut['penetracion'] = np.where(
        OutPut['Tipo Proyección'] == 'Nuevo',
        np.where(
            ((OutPut['TEMP_numeromes'] >= OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)) | (OutPut['TEMP_numeromes'] < OutPut['Mes Inicio']),
            0,
            np.where(
                (OutPut['TEMP_numeromes'] <= (12 + OutPut['Mes Inicio'] - mesanual)),
                np.select(condlist, choicelist, default=OutPut['Pent. Q4']),
                np.where(
                    (OutPut['TEMP_numeromes'] <= (24 + OutPut['Mes Inicio'] - mesanual)),
                    np.where(
                        (OutPut['TEMP_numeromes'] <= (12 + OutPut['Mes Inicio'] - mesanual) + OutPut['Plazo Año 2']),
                        np.where(
                            (OutPut['TEMP_numeromes'] == (12 + OutPut['Mes Inicio'] - mesanual) + 1),
                            OutPut['Pent. Inicial Año 2'],
                            OutPut['Pent. Inicial Año 2'] + ((OutPut['Pent. Final Año 2'] - OutPut['Pent. Inicial Año 2']) / (OutPut['Plazo Año 2'] - 1) * (mesTEMP - 1))
                        ),
                        OutPut['Pent. Final Año 2']
                    ),
                    np.where(
                        (OutPut['TEMP_numeromes'] <= (24 + (OutPut['Mes Inicio'] - mesanual) + OutPut['Plazo Año 3'])),
                        np.where(
                            (OutPut['TEMP_numeromes'] == (24 + OutPut['Mes Inicio'] - mesanual) + 1),
                            OutPut['Pent. Inicial Año 3'],
                            OutPut['Pent. Inicial Año 3'] + ((OutPut['Pent. Final Año 3'] - OutPut['Pent. Inicial Año 3']) / (OutPut['Plazo Año 3'] - 1) * (mesTEMP2 - 1))
                        ),
                        OutPut['Pent. Final Año 3']
                    )
                )
            )
        ),
        0
    )
    OutPut['penetracion'] = OutPut['penetracion'].astype(np.float64)
    # Obtener nuevos
    OutPut = calcular_nuevos(OutPut, mesiniciost, caidaren, desembolsos_st, ctmkac, ctmktc)
    # print("\n\n obtener_nuevos \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut


def calcular_nuevos(OutPut, mesiniciost, caidaren, desembolsos_st, ctmkac, ctmktc):
    OutPut['nuevos'] = np.where(
        OutPut['Tipo Proyección'] == 'Nuevo',
        np.where(
            np.isin(OutPut['Id_T.Oferta'], [9, 10]) == True,
            np.where(
                OutPut['Linea Negocio Socio'] == "Cuentas",
                OutPut['penetracion'] * OutPut['Desembolso'] * (1 - ctmkac),
                np.where(
                    OutPut['Linea Negocio Socio'] == "Tarjetas",
                    OutPut['penetracion'] * OutPut['Desembolso'] * (1 - ctmktc),
                    OutPut['penetracion'] * OutPut['Desembolso']
                )
            ),
            OutPut['penetracion'] * OutPut['Desembolso']
        ),
        np.where(
            OutPut['Tipo Proyección'] == 'Stock',
            np.where(
                OutPut['TEMP_numeromes'] > mesiniciost,
                np.where(
                    OutPut['Id_T.Prima'] == 2,  # Stock - Anual
                    np.where(
                        (OutPut['TEMP_numeromes'] <= OutPut['Duración']) |
                        ((OutPut['TEMP_numeromes'] < OutPut['t CutOff']) & (OutPut['t CutOff'] > 0)),
                        OutPut['Pent. Q1'] * OutPut['Desembolso'] * ((1 - OutPut['Caida']) ** OutPut['TEMP_numeromes']) * (1 - caidaren),
                        0
                    ),
                    np.where(
                        OutPut['Id_T.Prima'] == 1,  # Stock - Mensual
                        0,
                        0  # Stock - Unica + posibles otras
                    )
                ),
                0
            ),
            0  # Stock RRC
        )
    )
    # Eliminar variables que posteriormente no se van a utilizar
    del (OutPut['Pent. Q1'])
    del (OutPut['Pent. Q2'])
    del (OutPut['Pent. Q3'])
    del (OutPut['Pent. Q4'])
    del (OutPut['Plazo Año 2'])
    del (OutPut['Plazo Año 3'])
    del (OutPut['Pent. Inicial Año 2'])
    del (OutPut['Pent. Inicial Año 3'])
    del (OutPut['penetracion'])
    del (OutPut['Desembolso'])
    return OutPut


def obtener_desembolso(OutPut, meses, parametros_st, parametros_nv, desembolsos_st, desembolsos_nv):
    try:
        del desembolsos_st['Mes 0']
        del desembolsos_nv['Mes 0']
    except KeyError:
        pass

    # Cambiar nombres de columnas desembolsos_st y limitar columnas a No. de meses
    total_no_colum_st = len(desembolsos_st.columns)
    nuevas_colum_st = list(range(0, total_no_colum_st, 1))
    desembolsos_st.columns = nuevas_colum_st
    filtro_colum = list(range(0, meses + 1, 1))
    desembolsos_st = desembolsos_st.filter(filtro_colum)
    desembolsos_st.rename(columns={0: 'Id_Tool'}, inplace=True)

    # Cambiar nombres de columnas desembolsos_nv y limitar columnas a No. de meses
    total_no_colum_nv = len(desembolsos_nv.columns)
    nuevas_colum_nv = list(range(0, total_no_colum_nv, 1))
    desembolsos_nv.columns = nuevas_colum_nv
    filtro_colum = list(range(0, meses + 1, 1))
    desembolsos_nv = desembolsos_nv.filter(filtro_colum)
    desembolsos_nv.rename(columns={0: 'Id_Tool'}, inplace=True)

    # Generar DataFrame con desembolsos por cada producto-mes
    filtro_colum[0] = 'Id_Tool'
    productos_desembolso = pd.concat([parametros_st.filter(['Id_Tool']), parametros_nv.filter(['Id_Tool'])])
    productos_desembolso = pd.DataFrame(data=productos_desembolso, columns=filtro_colum)
    productos_desembolso.loc[productos_desembolso.Id_Tool.isin(desembolsos_st.Id_Tool), filtro_colum] = desembolsos_st[filtro_colum].values
    productos_desembolso.loc[productos_desembolso.Id_Tool.isin(desembolsos_nv.Id_Tool), filtro_colum] = desembolsos_nv[filtro_colum].values
    productos_desembolso.Id_Tool = productos_desembolso.Id_Tool.astype(np.int)
    productos_desembolso.set_index(['Id_Tool'], inplace=True)
    productos_desembolso = productos_desembolso.fillna(0)
    productos_desembolso = productos_desembolso.stack()
    productos_desembolso = pd.DataFrame({'TEMP_key_numeromeses': productos_desembolso.index, 'Desembolso': productos_desembolso.values})

    # Volver las llaves a tipo String
    OutPut.TEMP_key_numeromeses = OutPut.TEMP_key_numeromeses.astype(str)
    productos_desembolso.TEMP_key_numeromeses = productos_desembolso.TEMP_key_numeromeses.astype(str)

    resultado = pd.merge(OutPut, productos_desembolso, on='TEMP_key_numeromeses', how='left')
    # Agregar columna de desembolso a OutPut
    return resultado
