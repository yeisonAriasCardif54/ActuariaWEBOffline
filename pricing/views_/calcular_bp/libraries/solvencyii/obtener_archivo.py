import numpy as np
import pandas as pd
from datetime import datetime


#def generateExcelSolvencyII(writer, InputsSolvencia):
def generateExcelSolvencyII(writer, InputsSolvencia, Outputs_SII):
    """
    MK_Shocks.to_excel(writer, sheet_name='MK_Shocks', index=None, float_format='%.15f', startrow=0, header=True)
    workbook = writer.book
    worksheet = writer.sheets['MK_Shocks']
    for col_num, value in enumerate(MK_Shocks.columns.values):
        column_len = MK_Shocks[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)

    DataSolvencia.to_excel(writer, sheet_name='DataSolvencia', index=None, float_format='%.15f', startrow=0, header=True)
    workbook = writer.book
    worksheet = writer.sheets['DataSolvencia']
    for col_num, value in enumerate(DataSolvencia.columns.values):
        column_len = DataSolvencia[value].as
        (str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)

    InputsSolvencia = InputsSolvencia.T
    InputsSolvencia.to_excel(writer, sheet_name='InputsSolvencia', index=None, float_format='%.15f', startrow=0, header=True)

    """

    # ---------------------------------------------------------------------------------------------------- #
    # ------------------------------------------Imprimir Inputs
    # ---------------------------------------------------------------------------------------------------- #

    GlobalTable = InputsSolvencia['GlobalTable'].T
    ProductTable = InputsSolvencia['ProductTable'].T
    AssetByRatingTable = InputsSolvencia['AssetByRatingTable'].T
    RiskPremiumRepartition1Table = InputsSolvencia['RiskPremiumRepartition1Table'].T
    ExposedAmountTable = InputsSolvencia['ExposedAmountTable'].T
    LossRatiosPTLRTable = InputsSolvencia['LossRatiosPTLRTable'].T
    ClaimManagementOverheadsTable = InputsSolvencia['ClaimManagementOverheadsTable'].T
    RiskPremiumRepartitionTable = InputsSolvencia['RiskPremiumRepartitionTable'].T
    ExclusionPeriodTable = InputsSolvencia['ExclusionPeriodTable'].T
    TopKapiTable = InputsSolvencia['TopKapiTable'].T
    HealtTable = InputsSolvencia['HealtTable'].T
    ProductionYProductTable = InputsSolvencia['ProductionYProductTable'].T
    PremiumDataTable = InputsSolvencia['PremiumDataTable'].T

    InputsSolvenciaUnion = pd.concat([GlobalTable,
                                      ProductTable,
                                      AssetByRatingTable,
                                      RiskPremiumRepartition1Table,
                                      ExposedAmountTable,
                                      LossRatiosPTLRTable,
                                      ClaimManagementOverheadsTable,
                                      RiskPremiumRepartitionTable,
                                      ExclusionPeriodTable,
                                      TopKapiTable,
                                      HealtTable,
                                      ProductionYProductTable,
                                      PremiumDataTable,
                                      ])

    InputsSolvenciaUnion['Title'] = InputsSolvenciaUnion.index
    InputsSolvenciaUnion['Style'] = ''
    for index, row in InputsSolvenciaUnion.iterrows():
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, ['Style']] = row.values[0]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [0]] = row.values[1]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [1]] = row.values[2]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [2]] = row.values[3]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [3]] = row.values[4]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [4]] = row.values[5]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [5]] = row.values[6]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [6]] = row.values[7]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [7]] = row.values[8]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [8]] = row.values[9]
        InputsSolvenciaUnion.loc[InputsSolvenciaUnion['Title'] == index, [9]] = row.values[10]

    InputsSolvenciaUnion = pd.DataFrame(InputsSolvenciaUnion, columns=["Title", 0, 1, 3, 4, 5, 6, 7, 8, 9, 'Style'])
    InputsSolvenciaUnion.rename(columns={0: 'Value'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={1: 'Value2'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={2: 'Value3'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={3: 'Value4'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={4: 'Value5'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={5: 'Value6'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={6: 'Value7'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={7: 'Value8'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={8: 'Value9'}, inplace=True)
    InputsSolvenciaUnion.rename(columns={9: 'Value10'}, inplace=True)

    InputsSolvenciaUnion.drop(['Style'], axis=1).to_excel(writer, sheet_name='InputsSolvencia', index=None, float_format='%.15f', startrow=0, header=True)

    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['InputsSolvencia']

    InputsSolvenciaUnion = InputsSolvenciaUnion.reset_index()
    InputsSolvenciaUnion['colNum'] = InputsSolvenciaUnion.index

    # --- ANCHO DE COLUMNA --- #
    for col_num, value in enumerate(InputsSolvenciaUnion.columns.values):
        column_len = InputsSolvenciaUnion[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)

    # --- ESTILOS --- #
    for index, row in InputsSolvenciaUnion.iterrows():
        if row['Style'] == 'title':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#366092')
            formatTitle.set_font_color('#FFFFFF')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'percent':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('0.0%')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        elif row['Style'] == 'price':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('#,##0')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        else:
            format = workbook.add_format()
            format.set_num_format('General')
            worksheet.set_row(row['colNum'] + 1, 12, format)

    format1 = workbook.add_format()
    format1.set_bg_color('#D9D9D9')
    format1.set_font_color('#808080')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)

    # ---------------------------------------------------------------------------------------------------- #
    # --------------------------------------Imprimir MK_Shocks
    # ---------------------------------------------------------------------------------------------------- #
    """
    MK_Shocks.drop(['Style'], axis=1).to_excel(writer, sheet_name='MK_Shocks', index=None, float_format='%.15f', startrow=0, header=True)
    MK_Shocks['colNum'] = MK_Shocks.index
    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['MK_Shocks']
    # --- ANCHO DE COLUMNA --- #
    for col_num, value in enumerate(MK_Shocks.columns.values):
        column_len = MK_Shocks[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    # --- ESTILOS --- #
    for index, row in MK_Shocks.iterrows():
        if row['Style'] == 'title':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#366092')
            formatTitle.set_font_color('#FFFFFF')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'title2':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#B8CCE4')
            formatTitle.set_font_color('#000000')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'percent':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('0.0%')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        elif row['Style'] == 'price':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('#,##0')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        else:
            format = workbook.add_format()
            format.set_num_format('General')
            worksheet.set_row(row['colNum'] + 1, 12, format)
    format1 = workbook.add_format()
    format1.set_bg_color('#D9D9D9')
    format1.set_font_color('#808080')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    """
    # ---------------------------------------------------------------------------------------------------- #
    # --------------------------------------Imprimir shock parameters
    # ---------------------------------------------------------------------------------------------------- #
    """
    shockParameters.drop(['Style'], axis=1).to_excel(writer, sheet_name='Shock parameters', index=None, float_format='%.15f', startrow=0, header=True)
    shockParameters['colNum'] = shockParameters.index
    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['Shock parameters']
    # --- ANCHO DE COLUMNA --- #
    for col_num, value in enumerate(shockParameters.columns.values):
        column_len = shockParameters[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    # --- ESTILOS --- #
    for index, row in shockParameters.iterrows():
        if row['Style'] == 'title':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#366092')
            formatTitle.set_font_color('#FFFFFF')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'title2':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#B8CCE4')
            formatTitle.set_font_color('#000000')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'percent':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('0.0%')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        elif row['Style'] == 'price':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('#,##0')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        else:
            format = workbook.add_format()
            format.set_num_format('General')
            worksheet.set_row(row['colNum'] + 1, 12, format)
    format1 = workbook.add_format()
    format1.set_bg_color('#D9D9D9')
    format1.set_font_color('#808080')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    """
    # ---------------------------------------------------------------------------------------------------- #
    # -------------------------------------------Imprimir SCR_NL-------------------------------------------#
    # ---------------------------------------------------------------------------------------------------- #
    """
    PrimasXRiesgoTable = InputsNonLifeSCR['PrimasXRiesgoTable'].T
    ParticipacionXLoB = InputsNonLifeSCR['ParticipacionXLoB'].T
    Loadings = InputsNonLifeSCR['Loadings'].T
    RT = InputsNonLifeSCR['RT'].T
    Sigma = InputsNonLifeSCR['Sigma'].T
    Correlation = InputsNonLifeSCR['Correlation'].T
    RiskFreeCurve = InputsNonLifeSCR['RiskFreeCurve'].T
    PremiumDevPattern = InputsNonLifeSCR['PremiumDevPattern'].T
    SCR_NLCorrelation = InputsNonLifeSCR['SCR_NLCorrelation'].T
    LapsesRatesStress = InputsNonLifeSCR['LapsesRatesStress'].T
    percentNl = InputsNonLifeSCR['percentNl'].T
    Years = InputsNonLifeSCR['Years'].T
    VPremium = InputsNonLifeSCR['VPremium'].T
    VReserves = InputsNonLifeSCR['VReserves'].T
    VLoB = InputsNonLifeSCR['VLoB'].T
    SigmaPremium = InputsNonLifeSCR['SigmaPremium'].T
    SigmaLoB = InputsNonLifeSCR['SigmaLoB'].T
    V_lob_Sigma_lob = InputsNonLifeSCR['V_lob_Sigma_lob'].T
    SCR_PyR = InputsNonLifeSCR['SCR_PyR'].T
    SCR_Lapse_Up = InputsNonLifeSCR['SCR_Lapse_Up'].T
    SCR_Lapse_Mass = InputsNonLifeSCR['SCR_Lapse_Mass'].T
    SCR_Lapse = InputsNonLifeSCR['SCR_Lapse'].T
    SCR_Cat = InputsNonLifeSCR['SCR_Cat'].T
    ValueSCR_Cat = InputsNonLifeSCR['ValueSCR_Cat'].T
    SCR_NL = InputsNonLifeSCR['SCR_NL'].T

    SCR_NL = pd.concat([PrimasXRiesgoTable,
                        ParticipacionXLoB,
                        Loadings,
                        RT,
                        Sigma,
                        Correlation,
                        RiskFreeCurve,
                        PremiumDevPattern,
                        SCR_NLCorrelation,
                        LapsesRatesStress,
                        percentNl,
                        Years,
                        VPremium,
                        VReserves,
                        VLoB,
                        SigmaPremium,
                        SigmaLoB,
                        V_lob_Sigma_lob,
                        SCR_PyR,
                        SCR_Lapse_Up,
                        SCR_Lapse_Mass,
                        SCR_Lapse,
                        SCR_Cat,
                        ValueSCR_Cat,
                        SCR_NL,
                        ])

    SCR_NL['Title'] = SCR_NL.index
    SCR_NL['Style'] = ''
    for index, row in SCR_NL.iterrows():
        SCR_NL.loc[SCR_NL['Title'] == index, ['Style']] = row.values[0]
        SCR_NL.loc[SCR_NL['Title'] == index, [0]] = row.values[1]
        SCR_NL.loc[SCR_NL['Title'] == index, [1]] = row.values[2]
        SCR_NL.loc[SCR_NL['Title'] == index, [2]] = row.values[3]
        SCR_NL.loc[SCR_NL['Title'] == index, [3]] = row.values[4]
        SCR_NL.loc[SCR_NL['Title'] == index, [4]] = row.values[5]
        SCR_NL.loc[SCR_NL['Title'] == index, [5]] = row.values[6]
        SCR_NL.loc[SCR_NL['Title'] == index, [6]] = row.values[7]
        SCR_NL.loc[SCR_NL['Title'] == index, [7]] = row.values[8]
        SCR_NL.loc[SCR_NL['Title'] == index, [8]] = row.values[9]
        SCR_NL.loc[SCR_NL['Title'] == index, [9]] = row.values[10]
        SCR_NL.loc[SCR_NL['Title'] == index, [10]] = row.values[11]
        SCR_NL.loc[SCR_NL['Title'] == index, [11]] = row.values[12]
        SCR_NL.loc[SCR_NL['Title'] == index, [12]] = row.values[13]
        SCR_NL.loc[SCR_NL['Title'] == index, [13]] = row.values[14]
        SCR_NL.loc[SCR_NL['Title'] == index, [14]] = row.values[15]
        SCR_NL.loc[SCR_NL['Title'] == index, [15]] = row.values[16]
        SCR_NL.loc[SCR_NL['Title'] == index, [16]] = row.values[17]
        SCR_NL.loc[SCR_NL['Title'] == index, [17]] = row.values[18]
        SCR_NL.loc[SCR_NL['Title'] == index, [18]] = row.values[19]
        SCR_NL.loc[SCR_NL['Title'] == index, [19]] = row.values[20]
        SCR_NL.loc[SCR_NL['Title'] == index, [20]] = row.values[21]
        SCR_NL.loc[SCR_NL['Title'] == index, [21]] = row.values[22]
        SCR_NL.loc[SCR_NL['Title'] == index, [22]] = row.values[23]
        SCR_NL.loc[SCR_NL['Title'] == index, [23]] = row.values[24]

    SCR_NL = pd.DataFrame(SCR_NL, columns=["Title", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 'Style'])
    SCR_NL.rename(columns={0: 'Value'}, inplace=True)
    SCR_NL.rename(columns={1: 'Value2'}, inplace=True)
    SCR_NL.rename(columns={2: 'Value3'}, inplace=True)
    SCR_NL.rename(columns={3: 'Value4'}, inplace=True)
    SCR_NL.rename(columns={4: 'Value5'}, inplace=True)
    SCR_NL.rename(columns={5: 'Value6'}, inplace=True)
    SCR_NL.rename(columns={6: 'Value7'}, inplace=True)
    SCR_NL.rename(columns={7: 'Value8'}, inplace=True)
    SCR_NL.rename(columns={8: 'Value9'}, inplace=True)
    SCR_NL.rename(columns={9: 'Value10'}, inplace=True)
    SCR_NL.rename(columns={10: 'Value11'}, inplace=True)
    SCR_NL.rename(columns={11: 'Value12'}, inplace=True)
    SCR_NL.rename(columns={12: 'Value13'}, inplace=True)
    SCR_NL.rename(columns={13: 'Value14'}, inplace=True)
    SCR_NL.rename(columns={14: 'Value15'}, inplace=True)
    SCR_NL.rename(columns={15: 'Value16'}, inplace=True)
    SCR_NL.rename(columns={16: 'Value17'}, inplace=True)
    SCR_NL.rename(columns={17: 'Value18'}, inplace=True)
    SCR_NL.rename(columns={18: 'Value19'}, inplace=True)
    SCR_NL.rename(columns={19: 'Value20'}, inplace=True)
    SCR_NL.rename(columns={20: 'Value21'}, inplace=True)
    SCR_NL.rename(columns={21: 'Value22'}, inplace=True)
    SCR_NL.rename(columns={22: 'Value23'}, inplace=True)
    SCR_NL.rename(columns={23: 'Value24'}, inplace=True)

    SCR_NL.drop(['Style'], axis=1).to_excel(writer, sheet_name='SCR_NL', index=None, float_format='%.15f', startrow=0, header=True)

    SCR_NL = SCR_NL.reset_index()
    SCR_NL['colNum'] = SCR_NL.index

    # ----- FORMATO ----- #
    workbook = writer.book
    worksheet = writer.sheets['SCR_NL']
    # --- ANCHO DE COLUMNA --- #
    for col_num, value in enumerate(SCR_NL.columns.values):
        column_len = SCR_NL[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 0
        worksheet.set_column(col_num, col_num, column_len)
    # --- ESTILOS --- #
    for index, row in SCR_NL.iterrows():
        if row['Style'] == 'title':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#366092')
            formatTitle.set_font_color('#FFFFFF')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'title2':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#B8CCE4')
            formatTitle.set_font_color('#000000')
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'title3':
            formatTitle = workbook.add_format()
            formatTitle.set_bg_color('#34bfa3')
            formatTitle.set_font_color('#FFFFFF')
            formatTitle.set_num_format('$ #,##0')
            formatTitle.set_indent(1)
            worksheet.set_row(row['colNum'] + 1, 12, formatTitle)
        elif row['Style'] == 'percent':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('0.0%')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        elif row['Style'] == 'price':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('$ #,##0')
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        elif row['Style'] == 'price2':
            formatPercent = workbook.add_format()
            formatPercent.set_num_format('$ #,##0')
            formatPercent.set_indent(1)
            worksheet.set_row(row['colNum'] + 1, 12, formatPercent)
        else:
            format = workbook.add_format()
            format.set_num_format('General')
            worksheet.set_row(row['colNum'] + 1, 12, format)

    format1 = workbook.add_format()
    format1.set_bg_color('#D9D9D9')
    format1.set_font_color('#808080')
    format1.set_align('center')
    format1.set_bold()
    format1.set_font_size(10)
    format1.set_font_name('Calibri')
    worksheet.set_row(0, 13, format1)
    """

    Outputs_SII.to_excel(writer, sheet_name='Outputs_SII', index=None, float_format='%.15f', startrow=0, header=True)

    return writer
