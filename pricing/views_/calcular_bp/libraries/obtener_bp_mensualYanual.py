''' Obtener los nuevos '''

import pandas as pd
import numpy as np


def obtener_bp_mensual(OutPut_imprimir, Inputs):
    OutPut_BP_mensual = pd.DataFrame()
    OutPut_BP_mensual['Producto'] = Inputs['Producto']

    list_columns = [
        'nuevos',
        'vigentes',
        'GWP',
        '- change in UPR net of DAC',
        '- Premium Refund',
        'Earned_Premium',
        '+ Technical Interest On Unearned Premium Reserve',
        '- Insurer Written Acquisition Costs Loading',
        '- Insurer Earned Operating Expenses Loading',
        '- Earned Commission',
        '- Earned Insurer Capital Cost Loading',
        'Total Earned Risk Premium',
        'Incurred Claims',
        'Paid Claims',
        '+ Change in Claim Reserve',
        'Technical Result',
        'Pure Technical Loss Ratio',
        'Variable Commission',
        '# In force policies',
        'Acquisition - Fixed',
        'Acquisition - Variable',
        'Claims',
        'Administration Fixed - Direct',
        'Administration Variable',
        'Administration Fixed - Structure',
        'FTS FTG',
        'TOTAL ICA GMF',
        'ASISTENCIA',
        'Costos Marketing',
        'Gestores',
        'Acquisition cost',
        'OVERHEADS',
        'RT - OVERHEADS',
        'Financial Income on Reserves',
        'NBI',
        'GOI',
        'TAX',
        'NOI',

        'GWP net of IVA',
        'Premium Life',
        'Premium Non Life',
        'Claim Life',
        'Claim non life',
        'Technical Reserves Life',

        '# in-force insured life',
        'Capital (KCOP)',
        'Sum at risk Life',
        'Solvency margin life',
        '% Life Premium',

        'Component Claims',
        'Component Premium',
        'Solvency margin non life',

        'Equity',
        'Equity/Premium',
        'Avg equity',
        'PV Avg equity',

        'On Equity (Participate only in IROE calculations)',
        'GOI con PF sobre equity',
        'TAX con PF sobre equity',
        'NOI con PF sobre equity',
        'PV NOI con PF sobre equity',

        'TMPYear',
        'Discount Rate annual',
        'Discount Rate',
        'IROE',
        'Cash-flow',
        'IRR',
        'PVFP',
        'Efficiency Ratio',

        '(RC_(i-1)-RC_i)',
        'NOI EQ + (RC_(i-1)-RC_i)',
        'Value Creation',

        'Exchange rate',
        'Paid insurer underwriting',
        'Fixed Costs',
        'Acquisition Costs',
        'Gross Operating Income (Including Financial Margin)',
        'Net Operating Income (Including Financial Margin)',
        'Technical Loss Ratio',
        'Written Commission Income',

        'Premium Collection Credit Risk',
        'Claims Cash Advance Credit Risk',
        'Reinsurance Credit Risk',
        'Surrender Credit Risk',
        'Total Credit Risk',
    ]

    for column in list_columns:
        OutPut_new = pd.pivot_table(OutPut_imprimir, index=['Producto'], columns=['Mes'], values=column)
        OutPut_new['item'] = column
        OutPut_new['Producto'] = OutPut_new.index
        OutPut_BP_mensual = pd.concat([OutPut_BP_mensual, OutPut_new], sort=False)

    cols = OutPut_BP_mensual.columns.tolist()
    column_to_move = "item"
    new_position = 1
    cols.insert(new_position, cols.pop(cols.index(column_to_move)))
    OutPut_BP_mensual = OutPut_BP_mensual[cols]
    for k in range(1, 121):
        year = np.ceil(int(k) / 12)
        year = int(year)
        OutPut_BP_mensual = OutPut_BP_mensual.rename(columns={OutPut_BP_mensual.columns[k + 1]: 'Mes ' + str(k) + ' (' + str(year) + ')'})

    OutPut_BP_mensual = OutPut_BP_mensual.sort_values(['Producto'])
    return OutPut_BP_mensual


def obtener_bp_anual(OutPut_BP_mensual):
    OutPut_BP_anual = pd.DataFrame()
    OutPut_BP_anual['Producto'] = OutPut_BP_mensual['Producto']
    OutPut_BP_anual['item'] = OutPut_BP_mensual['item']
    years = int(120 / 12)
    for k in range(1, years + 1):
        OutPut_BP_anual['Año ' + str(k)] = OutPut_BP_mensual.filter(like='(' + str(k) + ')').sum(axis=1)
    return OutPut_BP_anual
