import numpy as np


def calcular_incentivos_y_costos_TMK(OutPut):
    OutPut['tipincent'] = 'Pagados'  # --  Cálculo RT con Incentivos -- #
    OutPut['pica'] = 0.01104  # -- % ICA -- #
    OutPut['pgmf'] = 0.004  # -- GMF -- #
    OutPut['mesanual'] = 1  # -- Mes del año proyección -- #

    # -- IDs de tipos de oferta -- #
    # -- 1 = Hall -- #
    # -- 5 = Autos -- #
    # -- 6 = Hogar -- #
    # -- 8 = Digital Nuevo -- #
    # -- 12 = Garantía Extendida -- #
    # -- 13 = Digital Stock -- #
    tiposDeOferta = ['Hall', 'Autos', 'Hogar', 'Digital Nuevo', 'Garantía Extendida', 'Digital Stock']

    # -- determinar cuantos años han transcurrido -- #
    OutPut['yipc'] = np.where(
        np.isin(OutPut['Canal'], tiposDeOferta),  # -- Si el tipo de oferta es hall, o Garantía extendida -- #
        (OutPut['Mes'] - 1) / 12,
        0
    )
    OutPut['yipc'] = np.floor(OutPut['yipc'])
    OutPut['yipc'] = OutPut['yipc'].fillna(0)

    OutPut['incentp'] = np.where(
        np.isin(OutPut['Canal'], tiposDeOferta),  # -- Si el tipo de oferta es hall, o Garantía extendida, -- #
        np.where(
            OutPut['Tipo de prima'] == 'Mensual',  # -- Pregunta el tipo de prima, si es mensual: -- #
            OutPut['% Incentivo'] * OutPut['Vlr prima'] * OutPut['nuevos'],  # -- Incentivo pagado -- #,
            np.where(
                OutPut['Tipo de prima'] == 'Anual',  # -- Si es anual -- #
                OutPut['% Incentivo'] * (OutPut['Vlr prima'] / 12) * OutPut['nuevos'],
                # -- Si es única -- #
                OutPut['% Incentivo'] * (OutPut['Vlr prima'] / OutPut['Duración del producto financiero']) * OutPut['nuevos'],
            )
        ),
        0
    )
    OutPut['incentp'] = OutPut['incentp'].fillna(0)

    OutPut['ipctmk'] = np.where(
        np.isin(OutPut['Canal'], tiposDeOferta) == False,
        (OutPut['Mes'] + OutPut['mesanual'] - 2) / 12,
        0
    )
    OutPut['ipctmk'] = np.floor(OutPut['ipctmk'])
    OutPut['ipctmk'] = OutPut['ipctmk'].fillna(0)

    OutPut['tmkCost'] = np.where(
        np.isin(OutPut['Canal'], tiposDeOferta) == False,
        (OutPut['c/u TMK'] * ((1 + OutPut['% Incremento  IPC']) ** OutPut['ipctmk']) * OutPut['nuevos']),
        0
    )
    OutPut['tmkCost'] = OutPut['tmkCost'].fillna(0)

    # -- Incentivos amortizados -- #
    # -- OutPut['TEMP_upr-1'] = np.where( (OutPut['Mes'] <= 12), 0, OutPut.groupby(['TEMP_key_numeromeses'])['upr'].sum()['(' + (OutPut['Id_Tool']).astype(str)  + ', ' + (OutPut['Mes']-1).astype(str) + ')'] )  -- #
    OutPut['TEMP_upr-1'] = OutPut['upr'].shift(1)
    # -- Solo aplica para Nuevos -- #
    OutPut['incent'] = np.where(
        OutPut['Mes'] == 1,
        OutPut['incentp'] - (((OutPut['upr'] + OutPut['gwpn']) / OutPut['Duración del producto financiero']) * OutPut['% Incentivo']),
        OutPut['incentp'] - (((OutPut['upr'] + OutPut['gwpn']) / OutPut['Duración del producto financiero']) * OutPut['% Incentivo']) + (((OutPut['TEMP_upr-1'] + OutPut['gwpn']) / OutPut['Duración del producto financiero']) * OutPut['% Incentivo'])
    )
    OutPut['incent'] = OutPut['incent'].fillna(0)

    # -- VAT de incentivos y de costos de TMKT -- #
    OutPut['vatincent'] = np.where(
        np.isin(OutPut['Canal'], tiposDeOferta),  # -- Si el tipo de oferta es hall, o Garantía extendida -- #
        np.where(
            OutPut['tipincent'] == "Pagados",
            OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['incentp'] * OutPut['IVA'],  # -- VAT pagado de incentivos -- #
            OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['incent'] * OutPut['IVA']  # -- VAT amortizado de incentivos -- #
        ),
        0
    )
    OutPut['vatincent'] = OutPut['vatincent'].fillna(0)

    OutPut['vatmk'] = np.where(
        np.isin(OutPut['Canal'], tiposDeOferta) == False,
        OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['tmkCost'] * OutPut['IVA'],
        0
    )
    OutPut['vatmk'] = OutPut['vatmk'].fillna(0)

    # -- Calculo de ica y 4x1000 -- #
    OutPut['ica'] = np.where(
        (OutPut['gwp'] * OutPut['pica']) > 0,
        OutPut['gwp'] * OutPut['pica'],
        0
    )
    OutPut['ica'] = OutPut['ica'].fillna(0)

    OutPut['gmf'] = np.where(
        (OutPut['gwp'] * OutPut['pgmf']) > 0,
        OutPut['gwp'] * OutPut['pgmf'],
        0
    )
    OutPut['gmf'] = OutPut['gmf'].fillna(0)

    return OutPut
