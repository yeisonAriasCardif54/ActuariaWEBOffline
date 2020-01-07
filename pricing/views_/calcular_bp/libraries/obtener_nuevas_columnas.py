import numpy as np


def obtener_nuevas_columnas_input(Inputs):
    """
    # -- Calculas los siguientes valores: -- #
    →→→ Claims rate ←←←
    →→→ Comisión Total ←←←
    →→→ Comisión Socio ←←←
    →→→ Comisión Broker ←←←
    →→→ IVA no descontable comisión ←←←
    →→→ % VAT ←←←
    →→→ % Costo de adquisición ←←←
    →→→ Persistencia ←←←
    →→→ Costo de adquisición ←←←
    →→→ Impuestos ←←←
    →→→ Costo Asistencia ←←←
    →→→ Overheads ←←←
    →→→ Costo de Capital ←←←
    →→→ % Costo Recaudo ←←←
    →→→ % Claims ←←←
    →→→ Investment Rate Mensual ←←←
    :param Inputs: Dataframe con los inputs originales.
    :return: Inputs (Dataframe agregando los nuevos valores).
    """

    # -- TODO: Aplicar % Stress -- #
    Inputs['Caida'] = Inputs['Caida'] * Inputs['Stress test Lapse increase']
    Inputs['Claims rate'] = Inputs['Prima de Riesgo'] / Inputs['Vlr prima']
    Inputs['Comisión Total'] = (Inputs['Comisión socio'] + Inputs['Comisión Broker'] + Inputs['Comisión Facilitador'] + Inputs['IVA no descontable comisión socio'] + Inputs['IVA no descontable comisión Broker']) / Inputs['Vlr prima']
    Inputs['Comisión Socio'] = Inputs['Comisión socio'] / (Inputs['Comisión socio'] + Inputs['Comisión Broker'] + Inputs['Comisión Facilitador'] + Inputs['IVA no descontable comisión socio'] + Inputs['IVA no descontable comisión Broker'])
    Inputs['Comisión Broker'] = (Inputs['Comisión Broker'] + Inputs['Comisión Facilitador']) / (Inputs['Comisión socio'] + Inputs['Comisión Broker'] + Inputs['Comisión Facilitador'] + Inputs['IVA no descontable comisión socio'] + Inputs['IVA no descontable comisión Broker'])
    Inputs['IVA no descontable comisión'] = Inputs['IVA no descontable comisión socio'] / Inputs['Vlr prima']
    Inputs['% VAT'] = Inputs['IVA no descontable comisión socio'] / Inputs['Comisión socio']
    Inputs['% Costo de adquisición'] = (Inputs['Costo incentivo/Costo TMKT'] + Inputs['IVA no descontable costo incentivo/TMKT'] + Inputs['Fee Incentivo']) / Inputs['Vlr prima']
    Inputs['Persistencia'] = (1 - (1 - Inputs['Caida']) ** (Inputs['Duración del producto financiero'])) / Inputs['Caida']
    Inputs['Costo de adquisición'] = (Inputs['Costo incentivo/Costo TMKT'] + Inputs['IVA no descontable costo incentivo/TMKT'] + Inputs['Fee Incentivo']) / Inputs['Persistencia']
    Inputs['Impuestos'] = (Inputs['ICA (1,104%)'] + Inputs['GMF']) / Inputs['Vlr prima']
    Inputs['Impuestos ICA'] = (Inputs['ICA (1,104%)']) / Inputs['Vlr prima']
    Inputs['Impuestos GMF'] = (Inputs['GMF']) / Inputs['Vlr prima']
    Inputs['Costo Asistencia'] = Inputs['Asistencia'] / Inputs['Vlr prima']
    Inputs['Costo de Recaudo'] = (Inputs['Costo de Recaudo']) / Inputs['Vlr prima']
    Inputs['Overheads'] = ((Inputs['Costo certificado'] + Inputs['Costo administrativos'] + Inputs['Otros gastos'] + Inputs['Gastos fijos']) /
                           Inputs['Vlr prima']) + \
                          Inputs['Impuestos'] + Inputs['Costo Asistencia'] + Inputs['Costo de Recaudo']
    Inputs['Costo de Capital'] = Inputs['Utilidad esperada'] / Inputs['Vlr prima']
    # Inputs['% Costo Recaudo'] = Inputs['Costo de Recaudo'] / Inputs['Vlr prima']
    Inputs['% Claims'] = Inputs['Prima de Riesgo'] / Inputs['Vlr prima']
    Inputs['Investment Rate mensual'] = ((1 + Inputs['Investment Rate anual']) ** (1 / 12)) - 1
    Inputs['Discount Rate mensual'] = Inputs['Discount Rate annual'] / 12

    return Inputs


def obtener_nuevas_columnas_output(OutPut):
    """
    # -- Calculas los siguientes valores: -- #
    →→→ - change in UPR net of DAC ←←←
    →→→ - Premium Refund ←←←
    →→→ + Technical Interest On Unearned Premium Reserve ←←←
    →→→ - Insurer Written Acquisition Costs Loading ←←←
    →→→ - Insurer Earned Operating Expenses Loading ←←←
    →→→ - Earned Commission ←←←
    →→→ - Earned Insurer Capital Cost Loading ←←←
    →→→ Total Earned Risk Premium ←←←
    →→→ Incurred Claims ←←←
    →→→ Paid Claims ←←←
    →→→ + Change in Claim Reserve ←←←
    →→→ Technical Result ←←←
    →→→ Pure Technical Loss Ratio ←←←
    →→→ Variable Commission ←←←
    :param OutPut: Dataframe con los OutPuts originales.
    :return: OutPut (Dataframe agregando los nuevos valores).
    """

    OutPut['+ Technical Interest On Unearned Premium Reserve'] = 0
    # OutPut['- Insurer Written Acquisition Costs Loading'] = OutPut['% Costo de adquisición'] * OutPut['earnedP']
    OutPut['- Insurer Written Acquisition Costs Loading'] = OutPut['gwp'] * (OutPut['% Costo de adquisición'])
    OutPut['- Insurer Earned Acquisition Costs Loading'] = OutPut['earnedP'] * (OutPut['% Costo de adquisición'])
    OutPut['- Insurer Earned Operating Expenses Loading'] = (OutPut['Overheads']) * OutPut['earnedP']
    OutPut['- Earned Commission'] = OutPut['earnedC']
    OutPut['- Earned Insurer Capital Cost Loading'] = OutPut['Costo de Capital'] * OutPut['earnedP']

    OutPut['- Insurer Unearned Acquisition Costs Loading'] = OutPut['upr'] * (OutPut['% Costo de adquisición'])
    OutPut['- change in UPR net of DAC'] = OutPut['upr'] - OutPut['dac'] - OutPut['- Insurer Unearned Acquisition Costs Loading']
    OutPut['- change in UPR net of DAC'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['- change in UPR net of DAC'],
        0
    )
    # OutPut['- Insurer Writing Acquisition Costs Loading'] = OutPut['gwp'] * (OutPut['Costo incentivo/Costo TMKT'] + OutPut['IVA no descontable costo incentivo/TMKT'])
    # OutPut['- Premium Refund'] = OutPut['gwpn']
    OutPut['- Premium Refund'] = np.where(
        OutPut['Mes'] == 1,
        0,
        (OutPut['upr'].shift(1) - OutPut['dac'].shift(1) - OutPut['- Insurer Unearned Acquisition Costs Loading'].shift(1)) * OutPut['Caida']
    )

    OutPut['Total Earned Risk Premium'] = OutPut['earnedP'] - OutPut['- Insurer Earned Acquisition Costs Loading'] - OutPut['- Insurer Earned Operating Expenses Loading'] - OutPut['- Earned Commission'] - OutPut['- Earned Insurer Capital Cost Loading']
    OutPut['Incurred Claims'] = OutPut['earnedP'] * OutPut['% Claims']
    # -- TODO: Aplicar % Stress -- #
    OutPut['Incurred Claims'] = OutPut['Incurred Claims'] * OutPut['Stress test Claims increase']
    OutPut['+ Change in Claim Reserve'] = np.where(
        OutPut['Incurred Claims'] > 0,
        OutPut['Incurred Claims'] - OutPut['Incurred Claims'] * (OutPut['% Claim Reserves/Paid Claims']),
        0
    )
    OutPut['Claim Reserves'] = OutPut['+ Change in Claim Reserve']
    OutPut['Paid Claims'] = np.where(
        OutPut['Mes'] == 1,
        0,
        np.where(
            OutPut['Mes'] == 2,
            OutPut['Incurred Claims'].shift(1) * (OutPut['% Claim Reserves/Paid Claims']),
            np.where(
                OutPut['Mes'] == 3,
                OutPut['Incurred Claims'].shift(1) * (OutPut['% Claim Reserves/Paid Claims']) + OutPut['+ Change in Claim Reserve'].shift(2) * (OutPut['% Claim Reserves/Paid Claims']),
                np.where(
                    OutPut['Mes'] == 4,
                    OutPut['Incurred Claims'].shift(1) * (OutPut['% Claim Reserves/Paid Claims']) + OutPut['+ Change in Claim Reserve'].shift(2) * (OutPut['% Claim Reserves/Paid Claims']) + OutPut['+ Change in Claim Reserve'].shift(3) * (OutPut['% Claim Reserves/Paid Claims']) * (1 - (OutPut['% Claim Reserves/Paid Claims'])),
                    OutPut['Incurred Claims'].shift(1) * (OutPut['% Claim Reserves/Paid Claims']) + OutPut['+ Change in Claim Reserve'].shift(2) * (OutPut['% Claim Reserves/Paid Claims']) + OutPut['+ Change in Claim Reserve'].shift(3) * (OutPut['% Claim Reserves/Paid Claims']) * (1 - (OutPut['% Claim Reserves/Paid Claims'])) + OutPut['+ Change in Claim Reserve'].shift(4) * (OutPut['% Claim Reserves/Paid Claims']) * (1 - (OutPut['% Claim Reserves/Paid Claims'])) * (1 - (OutPut['% Claim Reserves/Paid Claims']))
                )
            )
        )
    )

    OutPut['+ Change in Claim Reserve'] = OutPut.groupby('Producto')['+ Change in Claim Reserve'].apply(lambda x: x.rolling(center=False, min_periods=1, window=12).sum())
    OutPut['+ Change in Claim Reserve'] = np.where(
        OutPut['Mes'] % 12 == 0,
        OutPut['+ Change in Claim Reserve'],
        0
    )

    OutPut['PREFinancial Income on Reserves'] = np.where(
        (OutPut['Si run off ó cut off al fin de la producción'] == 'Cut Off') & ((OutPut['Mes'] + 12) > OutPut['Duración de producción en meses']),
        0,
        1
    )
    OutPut['Financial Income on Reserves'] = np.where(
        OutPut['Mes'] == 12,
        OutPut['Investment Rate anual'] * (
                (OutPut['- change in UPR net of DAC']) *
                OutPut['PREFinancial Income on Reserves'] + 0.5 * (OutPut['Claim Reserves'])
        ) / 2,
        np.where(
            OutPut['Mes'] % 12 == 0,
            OutPut['Investment Rate anual'] * (
                    (OutPut['- change in UPR net of DAC'] + OutPut['- change in UPR net of DAC'].shift(12)) *
                    OutPut['PREFinancial Income on Reserves'] + 0.5 * (OutPut['Claim Reserves'] + OutPut['Claim Reserves'].shift(12))
            ) / 2,
            0
        )
    )

    OutPut['Written Commission Income'] = OutPut['gwp'] * OutPut['Comisión Total']

    return OutPut
