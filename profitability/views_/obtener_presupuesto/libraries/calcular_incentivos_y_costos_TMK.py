''' Calculo de los incentivos y costos de TMK '''

import numpy as np
#import time


def calcular_incentivos_y_costos_TMK(OutPut, ipc, tipincent, piva, pica, pgmf, mesanual):
    # start_time = time.time()
    # IDs de tipos de oferta
    tiposDeOferta = [1, 5, 6, 8, 12, 13]

    # determinar cuantos años han transcurrido
    OutPut['yipc'] = np.where(
        np.isin(OutPut['Id_T.Oferta'], tiposDeOferta),  # Si el tipo de oferta es hall, o Garantìa extendida
        (OutPut['TEMP_numeromes'] - 1) / 12,
        0
    )
    OutPut['yipc'] = np.floor(OutPut['yipc'])
    OutPut['yipc'] = OutPut['yipc'].fillna(0)

    OutPut['incentp'] = np.where(
        np.isin(OutPut['Id_T.Oferta'], tiposDeOferta),  # Si el tipo de oferta es hall, o Garantìa extendida,
        np.where(
            OutPut['Id_T.Prima'] == 1,  # Pregunta el tipo de prima, si es mensual:
            np.where(
                OutPut['¿Aplica IPC?'] == 'Si',  # Afectar el valor de la prima promedio por el IPC
                OutPut['% incentivo'] * (OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['yipc'])) * OutPut['nuevos'],  # Incentivo pagado
                OutPut['% incentivo'] * OutPut['Vlr. Prima Prom'] * OutPut['nuevos']  # Incentivo pagado
            ),
            np.where(
                OutPut['Id_T.Prima'] == 2,  # Si es anual
                np.where(
                    OutPut['¿Aplica IPC?'] == 'Si',  # Afectar el valor de la prima promedio por el IPC
                    OutPut['% incentivo'] * ((OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['yipc'])) / 12) * OutPut['nuevos'],
                    OutPut['% incentivo'] * (OutPut['Vlr. Prima Prom'] / 12) * OutPut['nuevos']
                ),
                # Si es ùnica
                np.where(
                    OutPut['¿Aplica IPC?'] == 'Si',  # Afectar el valor de la prima promedio por el IPC
                    OutPut['% incentivo'] * ((OutPut['Vlr. Prima Prom'] * ((1 + ipc) ** OutPut['yipc'])) / OutPut['Duración']) * OutPut['nuevos'],
                    OutPut['% incentivo'] * (OutPut['Vlr. Prima Prom'] / OutPut['Duración']) * OutPut['nuevos']
                ),
            )
        ),
        0
    )
    OutPut['incentp'] = OutPut['incentp'].fillna(0)

    OutPut['ipctmk'] = np.where(
        np.isin(OutPut['Id_T.Oferta'], tiposDeOferta) == False,
        (OutPut['TEMP_numeromes'] + mesanual - 2) / 12,
        0
    )
    OutPut['ipctmk'] = np.floor(OutPut['ipctmk'])
    OutPut['ipctmk'] = OutPut['ipctmk'].fillna(0)

    OutPut['tmkCost'] = np.where(
        np.isin(OutPut['Id_T.Oferta'], tiposDeOferta) == False,
        (OutPut['C/U. Venta TMKT'] * ((1 + ipc) ** OutPut['ipctmk']) * OutPut['nuevos']),
        0
    )
    OutPut['tmkCost'] = OutPut['tmkCost'].fillna(0)

    # Incentivos amortizados
    # OutPut['TEMP_upr-1'] = np.where( (OutPut['TEMP_numeromes'] <= 12), 0, OutPut.groupby(['TEMP_key_numeromeses'])['upr'].sum()['(' + (OutPut['Id_Tool']).astype(str)  + ', ' + (OutPut['TEMP_numeromes']-1).astype(str) + ')'] )
    OutPut['TEMP_upr-1'] = OutPut['upr'].shift(1)
    # Solo aplica para Nuevos
    OutPut['incent'] = np.where(
        OutPut['Tipo Proyección'] == 'Nuevo',
        np.where(
            OutPut['TEMP_numeromes'] == 1,
            OutPut['incentp'] - (((OutPut['upr'] + OutPut['gwpn']) / OutPut['Duración']) * OutPut['% incentivo']),
            OutPut['incentp'] - (((OutPut['upr'] + OutPut['gwpn']) / OutPut['Duración']) * OutPut['% incentivo']) + (((OutPut['TEMP_upr-1'] + OutPut['gwpn']) / OutPut['Duración']) * OutPut['% incentivo'])
        ),
        0
    )
    OutPut['incent'] = OutPut['incent'].fillna(0)

    # VAT de incentivos y de costos de TMKT
    OutPut['vatincent'] = np.where(
        np.isin(OutPut['Id_T.Oferta'], tiposDeOferta),  # Si el tipo de oferta es hall, o Garantìa extendida
        np.where(
            tipincent == "Pagados",
            OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['incentp'] * piva,  # VAT pagado de incentivos
            OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['incent'] * piva  # VAT amortizado de incentivos
        ),
        0
    )
    OutPut['vatincent'] = OutPut['vatincent'].fillna(0)

    OutPut['vatmk'] = np.where(
        np.isin(OutPut['Id_T.Oferta'], tiposDeOferta) == False,
        OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['tmkCost'] * piva,
        0
    )
    OutPut['vatmk'] = OutPut['vatmk'].fillna(0)

    # Calculo de ica y 4x1000
    OutPut['ica'] = np.where(
        (OutPut['gwp'] * pica) > 0,
        OutPut['gwp'] * pica,
        0
    )
    OutPut['ica'] = OutPut['ica'].fillna(0)

    OutPut['gmf'] = np.where(
        (OutPut['gwp'] * pgmf) > 0,
        OutPut['gwp'] * pgmf,
        0
    )
    OutPut['gmf'] = OutPut['gmf'].fillna(0)

    #print("\n\n calcular_incentivos_y_costos_TMK \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut
