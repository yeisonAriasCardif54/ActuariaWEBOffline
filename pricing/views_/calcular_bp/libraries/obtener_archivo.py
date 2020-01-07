import numpy as np
import pandas as pd
from datetime import datetime

n = datetime.now()
t = n.timetuple()
AnioActual = t[0]


def generateExcel(writer, ver_mas_detalles, OutPut_imprimir, OutPut_tasa, OutPut_tasa_caida_cancel, OutPut_productsBP_mensual, OutPut_productsBP_anual, OutPut_vlrprimac, OutPut_vlrprimad, OutPut_PRI_temp, Inputs):

    OrdenOutPut = [
        'New Production Volume',
        'Outstanding Production Volume',
        'Written Premium Net of Tax',
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

    # ----------------------------- #
    # ------ OutPut_BP_anual ------ #
    # ----------------------------- #
    OutPut_productsBP_anual_general = OutPut_productsBP_anual.groupby(['item'], as_index=False, sort=False).sum()
    OutPut_productsBP_anual_general.loc[OutPut_productsBP_anual_general['item'] == 'nuevos', ['item']] = 'New Production Volume'
    OutPut_productsBP_anual_general.loc[OutPut_productsBP_anual_general['item'] == 'vigentes', ['item']] = 'Outstanding Production Volume'
    OutPut_productsBP_anual_general.loc[OutPut_productsBP_anual_general['item'] == 'GWP', ['item']] = 'Written Premium Net of Tax'
    del (OutPut_productsBP_anual_general['Producto'])
    OutPut_productsBP_anual_general.index = OutPut_productsBP_anual_general['item']
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.reindex(OrdenOutPut)
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.replace([np.inf, -np.inf], np.nan).fillna(0)
    # Hallar el gran total -- #
    ColumnasYears = OutPut_productsBP_anual_general.filter(regex="Año")
    GranTotal = ColumnasYears.sum(axis=1)
    OutPut_productsBP_anual_general['Total'] = GranTotal
    # -- % -- #
    del (OutPut_productsBP_anual_general['item'])
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.astype(object).T
    OutPut_productsBP_anual_general['Pure Technical Loss Ratio'] = OutPut_productsBP_anual_general['Incurred Claims'].div(OutPut_productsBP_anual_general['Total Earned Risk Premium'].where(OutPut_productsBP_anual_general['Total Earned Risk Premium'] != 0, 1))
    OutPut_productsBP_anual_general['% Life Premium'] = OutPut_productsBP_anual_general['Solvency margin life'].div(OutPut_productsBP_anual_general['Premium Life'].where(OutPut_productsBP_anual_general['Premium Life'] != 0, 1))
    OutPut_productsBP_anual_general['Equity/Premium'] = OutPut_productsBP_anual_general['Equity'].div(OutPut_productsBP_anual_general['GWP net of IVA'].where(OutPut_productsBP_anual_general['GWP net of IVA'] != 0, 1))
    OutPut_productsBP_anual_general['IROE'] = OutPut_productsBP_anual_general['PV NOI con PF sobre equity'].div(OutPut_productsBP_anual_general['PV Avg equity'].where(OutPut_productsBP_anual_general['PV Avg equity'] != 0, 1))
        #OutPut_productsBP_anual_general['Discount Rate'] = 1 / (1 + OutPut_productsBP_anual_general['Discount Rate annual']) ** OutPut_productsBP_anual_general['TMPYear']
    OutPut_productsBP_anual_general['Efficiency Ratio'] = OutPut_productsBP_anual_general['OVERHEADS'].div(OutPut_productsBP_anual_general['NBI'].where(OutPut_productsBP_anual_general['NBI'] != 0, 1))
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.T
    OutPut_productsBP_anual_general.insert(0, "item", OutPut_productsBP_anual_general.index, True)
    # -- % -- #
    # -- Calcular IRR -- #
    ColumnasYears = OutPut_productsBP_anual_general.filter(regex="Año")
    Cash_flow_tir = np.irr(ColumnasYears.loc[ColumnasYears.index == 'Cash-flow'].values[0])
    OutPut_productsBP_anual_general['Total'][OutPut_productsBP_anual_general.index == 'IRR'] = Cash_flow_tir
    # -- Fin Calcular IRR -- #

    # -- Calcular MAX en columnas de Credit Risk -- #
    ColumnasYears = OutPut_productsBP_anual_general.filter(regex="Año")

    OutPut_productsBP_anual_general['Total'][OutPut_productsBP_anual_general.index == 'Premium Collection Credit Risk'] = ColumnasYears.loc[ColumnasYears.index == 'Premium Collection Credit Risk'].max(axis=1)
    OutPut_productsBP_anual_general['Total'][OutPut_productsBP_anual_general.index == 'Claims Cash Advance Credit Risk'] = ColumnasYears.loc[ColumnasYears.index == 'Claims Cash Advance Credit Risk'].max(axis=1)
    OutPut_productsBP_anual_general['Total'][OutPut_productsBP_anual_general.index == 'Reinsurance Credit Risk'] = ColumnasYears.loc[ColumnasYears.index == 'Reinsurance Credit Risk'].max(axis=1)
    OutPut_productsBP_anual_general['Total'][OutPut_productsBP_anual_general.index == 'Surrender Credit Risk'] = ColumnasYears.loc[ColumnasYears.index == 'Surrender Credit Risk'].max(axis=1)
    OutPut_productsBP_anual_general['Total'][OutPut_productsBP_anual_general.index == 'Total Credit Risk'] = ColumnasYears.loc[ColumnasYears.index == 'Total Credit Risk'].max(axis=1)

    # -- Preparar datos para informe -- #
    OutPut_productsBP_anualv2_general = OutPut_productsBP_anual_general.filter(regex="Total")
    OutPut_productsBP_anualTAN_general = OutPut_productsBP_anual_general

    # -- Eliminar datos para informe -- #
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.astype(object).T
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.drop(['TMPYear', 'Discount Rate annual', 'Discount Rate', 'IROE', 'Cash-flow', 'IRR', 'PVFP', 'Efficiency Ratio', 'Value Creation', 'Exchange rate'], axis=1)
    OutPut_productsBP_anual_general = OutPut_productsBP_anual_general.T

    # -- Imprimir -- #
    OutPut_productsBP_anual_general.to_excel(writer, sheet_name='BP Anual', index=None, float_format='%.15f', startrow=0, header=True)
    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['BP Anual']
    # -- ANCHO DE COLUMNA -- #
    for col_num, value in enumerate(OutPut_productsBP_anual_general.columns.values):
        column_len = OutPut_productsBP_anual_general[value].astype(str).str.len().max()
        column_len = max(column_len, len(value) - 5) + 0
        worksheet.set_column(col_num, col_num, column_len)
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
    worksheet.set_column('A:ZZ', 13, format3)
    format4 = workbook.add_format()
    format4.set_font_size(9)
    format4.set_num_format('0.0%')
    worksheet.set_row(17, 13, format4)
    worksheet.set_row(49, 13, format4)
    worksheet.set_row(54, 13, format4)
    worksheet.set_column('M:ZZ', 13, format4)

    # ----------------------------- #
    # ----- OutPut_BP_mensual ----- #
    # ----------------------------- #

    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual.groupby(['item'], as_index=False, sort=False).sum()
    OutPut_productsBP_mensual_general.loc[OutPut_productsBP_mensual_general['item'] == 'nuevos', ['item']] = 'New Production Volume'
    OutPut_productsBP_mensual_general.loc[OutPut_productsBP_mensual_general['item'] == 'vigentes', ['item']] = 'Outstanding Production Volume'
    OutPut_productsBP_mensual_general.loc[OutPut_productsBP_mensual_general['item'] == 'GWP', ['item']] = 'Written Premium Net of Tax'
    del (OutPut_productsBP_mensual_general['Producto'])
    OutPut_productsBP_mensual_general.index = OutPut_productsBP_mensual_general['item']
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.reindex(OrdenOutPut)
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.replace([np.inf, -np.inf], np.nan).fillna(0)
    # Hallar el gran total
    ColumnasYears = OutPut_productsBP_mensual_general.filter(regex="Mes")
    GranTotal = ColumnasYears.sum(axis=1)
    OutPut_productsBP_mensual_general['Total'] = GranTotal

    # -- % -- #
    del (OutPut_productsBP_mensual_general['item'])
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.astype(object).T
    OutPut_productsBP_mensual_general['Pure Technical Loss Ratio'] = OutPut_productsBP_mensual_general['Incurred Claims'].div(OutPut_productsBP_mensual_general['Total Earned Risk Premium'].where(OutPut_productsBP_mensual_general['Total Earned Risk Premium'] != 0, 1))
    OutPut_productsBP_mensual_general['% Life Premium'] = OutPut_productsBP_mensual_general['Solvency margin life'].div(OutPut_productsBP_mensual_general['Premium Life'].where(OutPut_productsBP_mensual_general['Premium Life'] != 0, 1))
    OutPut_productsBP_mensual_general['Equity/Premium'] = OutPut_productsBP_mensual_general['Equity'].div(OutPut_productsBP_mensual_general['GWP net of IVA'].where(OutPut_productsBP_mensual_general['GWP net of IVA'] != 0, 1))
    OutPut_productsBP_mensual_general['IROE'] = OutPut_productsBP_mensual_general['PV NOI con PF sobre equity'].div(OutPut_productsBP_mensual_general['PV Avg equity'].where(OutPut_productsBP_mensual_general['PV Avg equity'] != 0, 1))
    #OutPut_productsBP_mensual_general['Discount Rate'] = 1 / (1 + OutPut_productsBP_mensual_general['Discount Rate annual']) ** OutPut_productsBP_mensual_general['TMPYear']
    OutPut_productsBP_mensual_general['Efficiency Ratio'] = OutPut_productsBP_mensual_general['OVERHEADS'].div(OutPut_productsBP_mensual_general['NBI'].where(OutPut_productsBP_mensual_general['NBI'] != 0, 1))
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.T
    OutPut_productsBP_mensual_general.insert(0, "item", OutPut_productsBP_mensual_general.index, True)
    # -- % -- #

    # -- Eliminar datos para informe -- #
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.astype(object).T
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.drop(['TMPYear', 'Discount Rate annual', 'Discount Rate', 'IROE', 'Cash-flow', 'IRR', 'PVFP', 'Efficiency Ratio', 'Value Creation'], axis=1)
    OutPut_productsBP_mensual_general = OutPut_productsBP_mensual_general.T

    # -- Imprimir -- #
    OutPut_productsBP_mensual_general.to_excel(writer, sheet_name='BP Mensual', index=None, float_format='%.15f', startrow=0, header=True)
    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['BP Mensual']
    # -- ANCHO DE COLUMNA -- #
    for col_num, value in enumerate(OutPut_productsBP_mensual_general.columns.values):
        column_len = OutPut_productsBP_mensual_general[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
    worksheet.set_column('B:ZZ', 15, format3)

    # --------------------------------- #
    # ----- OutPut_BP_anual - TAN ----- #
    # --------------------------------- #
    OutPut_tan = [
        'New Production Volume',
        'Outstanding Production Volume',
        ' ',
        'Written Premium Net of Tax',
        '- change in UPR net of DAC',
        '- Premium Refund',
        '+ Technical Interest On Unearned Premium Reserve',
        '- Insurer Written Acquisition Costs Loading',
        '- Insurer Earned Operating Expenses Loading',
        'Written Commission Income',
        '- Written Commission',
        '- Earned Insurer Capital Cost Loading',
        'Total Earned Risk Premium',
        ' ',
        'Incurred Claims',
        'Paid Claims',
        '+ Change in Claim Reserve',
        '- Technical Interests On Claims Reserve',
        'Claims',
        ' ',
        'Pure Technical Loss Ratio',
        ' ',
        'Technical Result',
        ' ',
        'Paid partner variable commission',
        'Paid insurer underwriting',
        ' ',
        'Financial Income on Reserves',
        'On Equity (Participate only in IROE calculations)',
        ' ',
        'Insurer Net Banking Income',
        'Fixed Costs',
        'Acquisition Costs',
        'Total Overhead',
        'Gross Operating Income (Including Financial Margin)',
        'Net Operating Income (Including Financial Margin)',
        ' ',
        'Average Solvency 1 Required Capital',
        'Technical Loss Ratio',
        'Exchange rate',
        ' ',
        'Premium Collection Credit Risk',
        'Claims Cash Advance Credit Risk',
        'Reinsurance Credit Risk',
        'Surrender Credit Risk',
        'Total Credit Risk',
    ]
    # -- Definir columnas exentas de cambio a euro
    OutPut_noEuro = []


    OutPut_productsBP_anualTAN_general['item'][OutPut_productsBP_anualTAN_general['item'] == 'Variable Commission'] = 'Paid partner variable commission'
    OutPut_productsBP_anualTAN_general['item'][OutPut_productsBP_anualTAN_general['item'] == 'NBI'] = 'Insurer Net Banking Income'
    OutPut_productsBP_anualTAN_general['item'][OutPut_productsBP_anualTAN_general['item'] == 'OVERHEADS'] = 'Total Overhead'
    OutPut_productsBP_anualTAN_general['item'][OutPut_productsBP_anualTAN_general['item'] == 'Avg equity'] = 'Average Solvency 1 Required Capital'
    OutPut_productsBP_anualTAN_general['item'][OutPut_productsBP_anualTAN_general['item'] == 'Written Commission Income'] = '- Written Commission'
    OutPut_productsBP_anualTAN_general.index = OutPut_productsBP_anualTAN_general['item']
    OutPut_productsBP_anualTAN_general = OutPut_productsBP_anualTAN_general.astype(object).T
    OutPut_productsBP_anualTAN_general[' '] = ''
    OutPut_productsBP_anualTAN_general = OutPut_productsBP_anualTAN_general.filter(OutPut_tan)

    # -- Cambiar valores a Euros
    '''
    for col_num, value in enumerate(OutPut_productsBP_anualTAN_general.columns.values):
        if (value in OutPut_noEuro) == False:
            OutPut_productsBP_anualTAN_general[value] = OutPut_productsBP_anualTAN_general[value].astype(np.float)
            OutPut_productsBP_anualTAN_general[value] = OutPut_productsBP_anualTAN_general[value].mul(0.000289687137891078, fill_value=0)  # * OutPut_productsBP_anualTAN_general['Exchange rate']
    '''

    def mul(x, y):
        try:
            return pd.to_numeric(x) * y
        except:
            return x

    column_names = [
        'New Production Volume',
        'Outstanding Production Volume',
        'Net Operating Income (Including Financial Margin)',
        'Average Solvency 1 Required Capital'
    ]
    # OutPut_productsBP_anualTAN_general[OutPut_noEuro] = OutPut_productsBP_anualTAN_general[OutPut_noEuro].applymap(lambda x: mul(x, 0.000289687137891078))

    OutPut_productsBP_anualTAN_general = OutPut_productsBP_anualTAN_general.T
    OutPut_productsBP_anualTAN_general.rename(columns={'item': ''}, inplace=True)

    # -- Renombrar columnas de años -- #
    for i in range(0, 10):
        OutPut_productsBP_anualTAN_general.rename(columns={'Año ' + str(i + 1): AnioActual + (i)}, inplace=True)

    OutPut_productsBP_anualTAN_general.to_excel(writer, sheet_name='TAN Results', index=None, float_format='%.15f', startrow=0, header=True)
    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['TAN Results']

    format0 = workbook.add_format()
    format0.set_font_size(8)
    format0.set_font_name('Arial')
    format0.set_num_format('_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)')
    worksheet.set_column('B:Z', 15, format0)

    format1 = workbook.add_format()
    format1.set_font_size(9)
    format1.set_bold()
    format1.set_font_name('Arial')
    worksheet.set_column('A:A', 9, format1)

    format1_2 = workbook.add_format()
    format1_2.set_align('center')
    format1_2.set_font_size(9)
    format1_2.set_bold()
    format1_2.set_font_name('Arial')
    worksheet.set_row(0, 13, format1)

    # -- ANCHO DE COLUMNA AA -- #
    worksheet.set_column('A:A', 50)

    # format1 = workbook.add_format()
    # format1.set_align('center')
    # format1.set_bold()
    # format1.set_font_size(10)
    # format1.set_font_name('Arial')
    # worksheet.set_row(0, 10, format1)

    # ------------------------------------- #
    # ----- OutPut_BP_anual - INFORME ----- #
    # ------------------------------------- #
    OutPut_productsBP_anualv2_general = OutPut_productsBP_anualv2_general.loc[ColumnasYears.index.isin(['IROE', 'IRR', 'PVFP', 'Efficiency Ratio', 'Value Creation'])]
    OutPut_productsBP_anualv2_general.insert(0, "item", OutPut_productsBP_anualv2_general.index, True)
    OutPut_productsBP_anualv2_general['Total'][OutPut_productsBP_anualv2_general.index == 'Cash-flow'] = 0
    # -- cambiar nombre de Total en KCOP
    OutPut_productsBP_anualv2_general.to_excel(writer, sheet_name='BP Anual INFORME', index=None, float_format='%.15f', startrow=0, header=True)
    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['BP Anual INFORME']
    # -- ANCHO DE COLUMNA -- #
    for col_num, value in enumerate(OutPut_productsBP_anual_general.columns.values):
        column_len = OutPut_productsBP_anual_general[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    format1 = workbook.add_format()
    format1.set_bg_color('#212468')
    format1.set_font_color('white')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_color('yellow')
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    format3 = workbook.add_format()
    format3.set_font_size(9)
    format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
    worksheet.set_column('A:ZZ', 15, format3)
    format4 = workbook.add_format()
    format4.set_font_size(9)
    format4.set_num_format('0.0%')
    worksheet.set_row(1, 13, format4)
    worksheet.set_row(2, 13, format4)
    worksheet.set_row(4, 13, format4)

    if ver_mas_detalles == 'SI':
        # ----------------------------------------------------- #
        # ------ OutPut_BP_anual - Agrupado por producto ------ #
        # ----------------------------------------------------- #
        OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'] == 'nuevos', ['item']] = 'New Production Volume'
        OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'] == 'vigentes', ['item']] = 'Outstanding Production Volume'
        OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'] == 'GWP', ['item']] = 'Written Premium Net of Tax'
        # -- Reordenar columna items -- #
        sorterIndex = dict(zip(OrdenOutPut, range(len(OrdenOutPut))))
        OutPut_productsBP_anual['ORDEN'] = OutPut_productsBP_anual['item'].map(sorterIndex)
        OutPut_productsBP_anual = OutPut_productsBP_anual.sort_values(by=['Producto', 'ORDEN'], ascending=[True, True])
        del (OutPut_productsBP_anual['ORDEN'])

        # Hallar el gran total
        ColumnasYears = OutPut_productsBP_anual.filter(regex="Año")
        GranTotal = ColumnasYears.sum(axis=1)
        OutPut_productsBP_anual['Total'] = GranTotal

        OutPut_productsBP_anual.to_excel(writer, sheet_name='BP Anual (PorProducto)', index=None, float_format='%.15f', startrow=0, header=True)
        # ----- FORMATO ----- #
        workbook = writer.book
        worksheet = writer.sheets['BP Anual (PorProducto)']
        # -- ANCHO DE COLUMNA -- #
        for col_num, value in enumerate(OutPut_productsBP_anual.columns.values):
            column_len = OutPut_productsBP_anual[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 0
            worksheet.set_column(col_num, col_num, column_len)
        format1 = workbook.add_format()
        format1.set_bg_color('#212468')
        format1.set_font_color('white')
        format1.set_align('center')
        format1.set_bold()
        format1.set_font_size(10)
        format1.set_font_color('yellow')
        format1.set_font_name('Calibri')
        worksheet.set_row(0, 13, format1)
        format3 = workbook.add_format()
        format3.set_font_size(9)
        format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
        worksheet.set_column('B:ZZ', 15, format3)

        # ----------------------------------------------------- #
        # ----- OutPut_BP_mensual - Agrupado por producto ----- #
        # ----------------------------------------------------- #

        OutPut_productsBP_mensual.loc[OutPut_productsBP_mensual['item'] == 'nuevos', ['item']] = 'New Production Volume'
        OutPut_productsBP_mensual.loc[OutPut_productsBP_mensual['item'] == 'vigentes', ['item']] = 'Outstanding Production Volume'
        OutPut_productsBP_mensual.loc[OutPut_productsBP_mensual['item'] == 'GWP', ['item']] = 'Written Premium Net of Tax'
        # -- Reordenar columna items -- #
        sorterIndex = dict(zip(OrdenOutPut, range(len(OrdenOutPut))))
        OutPut_productsBP_mensual['ORDEN'] = OutPut_productsBP_mensual['item'].map(sorterIndex)
        OutPut_productsBP_mensual = OutPut_productsBP_mensual.sort_values(by=['Producto', 'ORDEN'], ascending=[True, True])
        del (OutPut_productsBP_mensual['ORDEN'])

        # Hallar el gran total
        ColumnasYears = OutPut_productsBP_mensual.filter(regex="Mes")
        GranTotal = ColumnasYears.sum(axis=1)
        OutPut_productsBP_mensual['Total'] = GranTotal

        OutPut_productsBP_mensual.to_excel(writer, sheet_name='BP Mensual (PorProducto)', index=None, float_format='%.15f', startrow=0, header=True)
        # ----- FORMATO ----- #
        workbook = writer.book
        worksheet = writer.sheets['BP Mensual (PorProducto)']
        # --- ANCHO DE COLUMNA --- #
        for col_num, value in enumerate(OutPut_productsBP_mensual.columns.values):
            column_len = OutPut_productsBP_mensual[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 0
            worksheet.set_column(col_num, col_num, column_len)
        format1 = workbook.add_format()
        format1.set_bg_color('#212468')
        format1.set_font_color('white')
        format1.set_align('center')
        format1.set_bold()
        format1.set_font_size(10)
        format1.set_font_color('yellow')
        format1.set_font_name('Calibri')
        worksheet.set_row(0, 13, format1)
        format3 = workbook.add_format()
        format3.set_font_size(9)
        format3.set_num_format('_($ * #,##0_);_($ * (#,##0);_($ * "-"??_);_(@_)')
        worksheet.set_column('B:ZZ', 15, format3)

        # ---------------------- #
        # ----- tasa_caida ----- #
        # ---------------------- #
        del (OutPut_tasa['tasa_caida_-1'])
        del (OutPut_tasa['tasa_caida_0'])
        del (OutPut_tasa['Tipo de prima'])
        del (OutPut_tasa['Mes'])
        del (OutPut_tasa['Duración del producto financiero'])
        del (OutPut_tasa['nuevos'])
        del (OutPut_tasa['Caida'])
        del (OutPut_tasa['TEMP_key_numeromeses'])
        del (OutPut_tasa['Tipo Proyección'])
        del (OutPut_tasa['Mes 0'])
        OutPut_tasa.to_excel(writer, sheet_name='▲Vigentes', index=None, float_format='%.15f', startrow=0, header=True)
        # ----- FORMATO ----- #
        worksheet = writer.sheets['▲Vigentes']
        # ----- ANCHO DE COLUMNA ----- #
        for col_num, value in enumerate(OutPut_tasa.columns.values):
            column_len = OutPut_tasa[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 0
            worksheet.set_column(col_num, col_num, column_len)
        format3 = workbook.add_format()
        format3.set_font_size(9)
        format3.set_num_format('_( * #,##0_);_($ * (#,##0);_( * "-"??_);_(@_)')
        worksheet.set_column('B:ZZ', 15, format3)

        # ----------------------------- #
        # ----- tasa_caida_cancel ----- #
        # ----------------------------- #
        del (OutPut_tasa_caida_cancel['tasa_caida_cancel_-1'])
        del (OutPut_tasa_caida_cancel['tasa_caida_cancel_0'])
        del (OutPut_tasa_caida_cancel['TEMP_key_numeromeses'])
        OutPut_tasa_caida_cancel.to_excel(writer, sheet_name='▲Cancelados', index=None, float_format='%.15f', startrow=0, header=True)
        # ----- FORMATO ----- #
        worksheet = writer.sheets['▲Cancelados']
        # ANCHO DE COLUMNA #
        for col_num, value in enumerate(OutPut_tasa_caida_cancel.columns.values):
            column_len = OutPut_tasa_caida_cancel[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 0
            worksheet.set_column(col_num, col_num, column_len)
        format3 = workbook.add_format()
        format3.set_font_size(9)
        format3.set_num_format('_( * #,##0_);_($ * (#,##0);_( * "-"??_);_(@_)')
        worksheet.set_column('B:ZZ', 15, format3)

        # ---------------------------------------------- #
        # ----- OutPut_vlrprimac, OutPut_vlrprimad ----- #
        # ---------------------------------------------- #
        OutPut_vlrprimac = OutPut_vlrprimac.drop([col for col in OutPut_vlrprimac.columns if '-' in col], axis=1)
        OutPut_vlrprimac.to_excel(writer, sheet_name='▲OutPut_vlrprimac', index=None, float_format='%.15f', startrow=0, header=True)
        OutPut_vlrprimad = OutPut_vlrprimad.drop([col for col in OutPut_vlrprimad.columns if '-' in col], axis=1)
        OutPut_vlrprimad.to_excel(writer, sheet_name='▲OutPut_vlrprimad', index=None, float_format='%.15f', startrow=0, header=True)

        # ---------------------------------------------- #
        # -------------- OutPut_PRI_temp --------------- #
        # ---------------------------------------------- #
        OutPut_PRI_temp_impri = OutPut_PRI_temp.filter(regex='gwpst_', axis=1)
        OutPut_PRI_temp_impri = OutPut_PRI_temp_impri.drop([col for col in OutPut_vlrprimac.columns if '-' in col], axis=1)
        OutPut_PRI_temp_impri.to_excel(writer, sheet_name='▲gwpst_ Periódica', index=None, float_format='%.15f', startrow=0, header=True)

        # ------------------ #
        # ------ Data ------ #
        # ------------------ #
        OutPut_imprimir.to_excel(writer, sheet_name='Data', index=None, float_format='%.15f', startrow=0, header=True)
        # -- FORMATO -- #
        workbook = writer.book
        worksheet = writer.sheets['Data']
        # -- ANCHO DE COLUMNA -- #
        for col_num, value in enumerate(OutPut_imprimir.columns.values):
            column_len = OutPut_imprimir[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 0
            worksheet.set_column(col_num, col_num, column_len)
        format1 = workbook.add_format()
        format1.set_bg_color('#212468')
        format1.set_font_color('white')
        format1.set_align('center')
        format1.set_bold()
        format1.set_font_size(10)
        format1.set_font_color('yellow')
        format1.set_font_name('Calibri')
        worksheet.set_row(0, 13, format1)

        # ------------------ #
        # ----- Inputs ----- #
        # ------------------ #
        del (Inputs['tmp'])
        Inputs.to_excel(writer, sheet_name='Inputs', index=None, float_format='%.15f', startrow=0, header=True)
        # -- FORMATO -- #
        workbook = writer.book
        worksheet = writer.sheets['Inputs']
        # -- ANCHO DE COLUMNA -- #
        for col_num, value in enumerate(Inputs.columns.values):
            column_len = Inputs[value].astype(str).str.len().max()
            column_len = max(column_len, len(value)) + 0
            worksheet.set_column(col_num, col_num, column_len)
        format1 = workbook.add_format()
        format1.set_bg_color('#212468')
        format1.set_font_color('white')
        format1.set_align('center')
        format1.set_bold()
        format1.set_font_size(10)
        format1.set_font_color('yellow')
        format1.set_font_name('Calibri')
        worksheet.set_row(0, 13, format1)

    return writer
