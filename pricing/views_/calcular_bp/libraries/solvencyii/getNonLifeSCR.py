import pandas as pd
import numpy as np


def matMult(a, b):
    zip_b = zip(*b)
    zip_b = list(zip_b)
    return [[sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]


def NonLifeSCR(InputsSolvencia, shockParameters, OutPut_productsBP_anual, MK_Shocks):
    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------0. Inputs
    # ---------------------------------------------------------------------------------------------------- #

    # -----------------------------------0.1. Primas x Riesgo
    PrimasXRiesgoTable = InputsSolvencia['PremiumDataTable']
    PrimasXRiesgoTable.rename(columns={'Premium Data': '0.1. Primas x Riesgo'}, inplace=True)

    # -----------------------------------0.2. % Participacion x LoB
    ParticipacionXLoB = InputsSolvencia['RiskPremiumRepartition1Table']
    ParticipacionXLoB.rename(columns={'Risk premium repartition ': '0.2. % Participacion x LoB'}, inplace=True)
    ParticipacionXLoB = ParticipacionXLoB.drop(['Life repartition: Death', 'Life repartition: TPD', 'Health repartition (SLT & Non SLT): TD',
                                                'Health repartition (SLT & Non SLT): TPD', 'Health repartition (SLT & Non SLT): Accidental  Death',
                                                'Health repartition (SLT & Non SLT): Hospitalization', 'Health repartition (SLT & Non SLT): Other health'], axis=1)

    # -----------------------------------0.3. Loadings
    Loadings = InputsSolvencia['ProductTable']
    Loadings = Loadings.filter(['Product', 'Commission', 'Annual Lapse rate', 'Acquisition costs loading', 'Insurer capital cost loading', 'Operating expenses loading', '', ' '])
    Loadings.rename(columns={'Product': '0.3. Loadings'}, inplace=True)

    # -----------------------------------0.4. RT
    OutPut_productsBP_anualFILTER = OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'].isin(['Total Earned Risk Premium', 'Claims',
                                                                                                      '- Insurer Earned Operating Expenses Loading', 'OVERHEADS',
                                                                                                      'Incurred Claims', 'Technical Result', 'Earned_Premium'])]
    OutPut_productsBP_anualFILTER.index = OutPut_productsBP_anualFILTER['item']
    OutPut_productsBP_anualFILTER = OutPut_productsBP_anualFILTER.drop(columns=['Producto', 'item'])
    OutPut_productsBP_anualFILTER = OutPut_productsBP_anualFILTER.T
    OutPut_productsBP_anualFILTER = OutPut_productsBP_anualFILTER[['Total Earned Risk Premium', 'Claims',
                                                                   '- Insurer Earned Operating Expenses Loading', 'OVERHEADS',
                                                                   'Incurred Claims', 'Technical Result', 'Earned_Premium']]

    itemsRT = ['title']
    itemsTotalEarnedRiskPremium = ['price']
    itemsClaims = ['price']
    itemsInsurerEarnedOperatingExpensesLoading = ['price']
    itemsOVERHEADS = ['price']
    itemsIncurredClaims = ['price']
    itemsTechnicalResult = ['price']
    itemsEarnedPremium = ['price']

    for index, row in OutPut_productsBP_anualFILTER.iterrows():
        itemsRT.append(index)
        itemsTotalEarnedRiskPremium.append(row[0])
        itemsClaims.append(row[1])
        itemsInsurerEarnedOperatingExpensesLoading.append(row[2])
        itemsOVERHEADS.append(row[3])
        itemsIncurredClaims.append(row[4])
        itemsTechnicalResult.append(row[5])
        itemsEarnedPremium.append(row[6])

    RT = pd.DataFrame({
        '0.4. RT': itemsRT,
        'Total Earned Risk Premium': itemsTotalEarnedRiskPremium,
        'Claims': itemsClaims,
        '- Insurer Earned Operating Expenses Loading': itemsInsurerEarnedOperatingExpensesLoading,
        'OVERHEADS': itemsOVERHEADS,
        'Incurred Claims': itemsIncurredClaims,
        'Technical Result': itemsTechnicalResult,
        'Earned_Premium': itemsEarnedPremium,
        '': '',
        ' ': ''
    })

    # -----------------------------------0.6. Sigma (parametros)
    EIOPA = shockParameters.loc[shockParameters['Item'].isin([
        'Lapse down shock',
        'Lapse up shock',
        'Mass lapse shock',
        'Sigma Premium - Motor',
        'Sigma Reserve - Motor',
        'Sigma Premium - Fire',
        'Sigma Reserve - Fire',
        'Sigma Premium - Miscellaneous',
        'Sigma Reserve - Miscellaneous',
        'Cat - Motor',
        'Cat - Fire & Other damage',
        'Cat - Miscallaneous',
    ])].filter(['Value'])

    itemsSigma = ['title']
    itemsLapseDownShock = ['percent']
    itemsLapseUpShock = ['percent']
    itemsMassLapseShock = ['percent']
    itemsSigmaPremiumMotor = ['percent']
    itemsSigmaReserveMotor = ['percent']
    itemsSigmaPremiumFire = ['percent']
    itemsSigmaReserveFire = ['percent']
    itemsSigmaPremiumMiscellaneous = ['percent']
    itemsSigmaReserveMiscellaneous = ['percent']
    itemsCatMotor = ['percent']
    itemsCatFireYOtherDamage = ['percent']
    itemsCatMiscallaneous = ['percent']

    for index, row in EIOPA.T.iterrows():
        itemsSigma.append(index)
        itemsLapseDownShock.append(row[31])
        itemsLapseUpShock.append(row[32])
        itemsMassLapseShock.append(row[33])
        itemsSigmaPremiumMotor.append(row[34])
        itemsSigmaReserveMotor.append(row[35])
        itemsSigmaPremiumFire.append(row[36])
        itemsSigmaReserveFire.append(row[37])
        itemsSigmaPremiumMiscellaneous.append(row[38])
        itemsSigmaReserveMiscellaneous.append(row[39])
        itemsCatMotor.append(row[40])
        itemsCatFireYOtherDamage.append(row[41])
        itemsCatMiscallaneous.append(row[42])

    Sigma = pd.DataFrame({
        '0.6. Sigma (parametros Non Life)': itemsSigma,
        'Lapse down shock': itemsLapseDownShock,
        'Lapse up shock': itemsLapseUpShock,
        'Mass lapse shock': itemsMassLapseShock,
        'Sigma Premium - Motor': itemsSigmaPremiumMotor,
        'Sigma Reserve - Motor': itemsSigmaReserveMotor,
        'Sigma Premium - Fire': itemsSigmaPremiumFire,
        'Sigma Reserve - Fire': itemsSigmaReserveFire,
        'Sigma Premium - Miscellaneous': itemsSigmaPremiumMiscellaneous,
        'Sigma Reserve - Miscellaneous': itemsSigmaReserveMiscellaneous,
        'Cat - Motor': itemsCatMotor,
        'Cat - Fire & Other damage': itemsCatFireYOtherDamage,
        'Cat - Miscallaneous': itemsCatMiscallaneous,
        '': '',
        ' ': ''
    })

    # -----------------------------------0.7. LoB Correlation
    PremiumReserve = shockParameters.loc[shockParameters['Item'].isin([
        'Gap',
        'EW',
        'Other',
    ])].filter(['Value', 'Value2', 'Value3'])

    itemsCorrelation = ['title']
    itemsGap = ['percent']
    itemsEW = ['percent']
    itemsOther = ['percent']

    for index, row in PremiumReserve.T.iterrows():
        itemsCorrelation.append(index)
        itemsGap.append(row[201])
        itemsEW.append(row[202])
        itemsOther.append(row[203])

    Correlation = pd.DataFrame({
        '0.7. LoB Correlation': itemsCorrelation,
        'Gap': itemsGap,
        'EW': itemsEW,
        'Other': itemsOther,
        '': '',
        ' ': ''
    })

    # -----------------------------------0.8. Risk Free Curve
    InterestRateYieldCurve = MK_Shocks.loc[MK_Shocks['Item'].isin([
        'Central Yield Curve'
    ])]

    del (InterestRateYieldCurve['Item'])

    InterestRateYieldCurve = InterestRateYieldCurve.T
    InterestRateYieldCurve[3] = np.arange(len(InterestRateYieldCurve)) + 1
    InterestRateYieldCurve = InterestRateYieldCurve.T

    itemsRiskFreeCurve = ['title']
    itemsCentralYieldCurve = ['percent']
    itemsCentralYieldCurveF1 = ['percent']
    itemsCentralYieldCurveF2 = ['percent']
    itemsCentralYieldCurveF3 = ['percent']
    itemsCentralYieldCurveF4 = ['percent']
    itemsCentralYieldCurveF5 = ['percent']
    itemsCentralYieldCurveF6 = ['percent']
    itemsCentralYieldCurveF7 = ['percent']
    itemsCentralYieldCurveF8 = ['percent']
    itemsCentralYieldCurveF9 = ['percent']
    itemsCentralYieldCurveF10 = ['percent']
    itemsCentralYieldCurveF11 = ['percent']
    itemsCentralYieldCurveF12 = ['percent']
    itemsDeflactor = ['percent']
    itemsDeflactorD1 = ['percent']
    itemsDeflactorD2 = ['percent']
    itemsDeflactorD3 = ['percent']
    itemsDeflactorD4 = ['percent']
    itemsDeflactorD5 = ['percent']
    itemsDeflactorD6 = ['percent']
    itemsDeflactorD7 = ['percent']
    itemsDeflactorD8 = ['percent']
    itemsDeflactorD9 = ['percent']
    itemsDeflactorD10 = ['percent']
    itemsDeflactorD11 = ['percent']
    itemsDeflactorD12 = ['percent']

    # -- INICIO Calcular Forward y Deflactor
    InterestRateYieldCurve['Style'] = 0
    TInterestRateYieldCurve = InterestRateYieldCurve.T
    TInterestRateYieldCurve['Forward1'] = np.where(TInterestRateYieldCurve[3] > 1, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value']) ** TInterestRateYieldCurve[3]['Value'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward2'] = np.where(TInterestRateYieldCurve[3] > 2, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value2']) ** TInterestRateYieldCurve[3]['Value2'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value2']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value2']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward3'] = np.where(TInterestRateYieldCurve[3] > 3, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value3']) ** TInterestRateYieldCurve[3]['Value3'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value3']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value3']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward4'] = np.where(TInterestRateYieldCurve[3] > 4, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value4']) ** TInterestRateYieldCurve[3]['Value4'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value4']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value4']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward5'] = np.where(TInterestRateYieldCurve[3] > 5, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value5']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value5']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward6'] = np.where(TInterestRateYieldCurve[3] > 6, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value6']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value6']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward7'] = np.where(TInterestRateYieldCurve[3] > 7, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value7']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value7']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward8'] = np.where(TInterestRateYieldCurve[3] > 8, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value8']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value8']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward9'] = np.where(TInterestRateYieldCurve[3] > 9, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value9']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value9']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward10'] = np.where(TInterestRateYieldCurve[3] > 10, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value10']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value10']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward11'] = np.where(TInterestRateYieldCurve[3] > 11, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value11']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value11']) != 0) - 1), 0)
    TInterestRateYieldCurve['Forward12'] = np.where(TInterestRateYieldCurve[3] > 12, ((((1 + TInterestRateYieldCurve[2]) ** TInterestRateYieldCurve[3]) / ((1 + TInterestRateYieldCurve[2]['Value5']) ** TInterestRateYieldCurve[3]['Value5'])) ** np.divide(1, (TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value12']), where=(TInterestRateYieldCurve[3] - TInterestRateYieldCurve[3]['Value12']) != 0) - 1), 0)
    TInterestRateYieldCurve['Deflactor1'] = np.where(TInterestRateYieldCurve[3] > 1, (1 / ((1 + TInterestRateYieldCurve['Forward1']) ** TInterestRateYieldCurve[3].shift(1))), 0)
    TInterestRateYieldCurve['Deflactor2'] = np.where(TInterestRateYieldCurve[3] > 2, (1 / ((1 + TInterestRateYieldCurve['Forward2']) ** TInterestRateYieldCurve[3].shift(2))), 0)
    TInterestRateYieldCurve['Deflactor3'] = np.where(TInterestRateYieldCurve[3] > 3, (1 / ((1 + TInterestRateYieldCurve['Forward3']) ** TInterestRateYieldCurve[3].shift(3))), 0)
    TInterestRateYieldCurve['Deflactor4'] = np.where(TInterestRateYieldCurve[3] > 4, (1 / ((1 + TInterestRateYieldCurve['Forward4']) ** TInterestRateYieldCurve[3].shift(4))), 0)
    TInterestRateYieldCurve['Deflactor5'] = np.where(TInterestRateYieldCurve[3] > 5, (1 / ((1 + TInterestRateYieldCurve['Forward5']) ** TInterestRateYieldCurve[3].shift(5))), 0)
    TInterestRateYieldCurve['Deflactor6'] = np.where(TInterestRateYieldCurve[3] > 6, (1 / ((1 + TInterestRateYieldCurve['Forward6']) ** TInterestRateYieldCurve[3].shift(6))), 0)
    TInterestRateYieldCurve['Deflactor7'] = np.where(TInterestRateYieldCurve[3] > 7, (1 / ((1 + TInterestRateYieldCurve['Forward7']) ** TInterestRateYieldCurve[3].shift(7))), 0)
    TInterestRateYieldCurve['Deflactor8'] = np.where(TInterestRateYieldCurve[3] > 8, (1 / ((1 + TInterestRateYieldCurve['Forward8']) ** TInterestRateYieldCurve[3].shift(8))), 0)
    TInterestRateYieldCurve['Deflactor9'] = np.where(TInterestRateYieldCurve[3] > 9, (1 / ((1 + TInterestRateYieldCurve['Forward9']) ** TInterestRateYieldCurve[3].shift(9))), 0)
    TInterestRateYieldCurve['Deflactor10'] = np.where(TInterestRateYieldCurve[3] > 10, (1 / ((1 + TInterestRateYieldCurve['Forward10']) ** TInterestRateYieldCurve[3].shift(10))), 0)
    TInterestRateYieldCurve['Deflactor11'] = np.where(TInterestRateYieldCurve[3] > 11, (1 / ((1 + TInterestRateYieldCurve['Forward11']) ** TInterestRateYieldCurve[3].shift(11))), 0)
    TInterestRateYieldCurve['Deflactor12'] = np.where(TInterestRateYieldCurve[3] > 12, (1 / ((1 + TInterestRateYieldCurve['Forward12']) ** TInterestRateYieldCurve[3].shift(12))), 0)
    # -- FIN Calcular Forward y Deflactor

    TInterestRateYieldCurve = TInterestRateYieldCurve.fillna(0)

    for index, row in TInterestRateYieldCurve.iterrows():
        itemsRiskFreeCurve.append(index)
        itemsCentralYieldCurve.append(row[2])
        try:
            newValueDeflactor = 1 / ((1 + float(row[2])) ** float(row[3]))
        except:
            newValueDeflactor = 0
        itemsDeflactor.append(newValueDeflactor)
        # -- Forward
        itemsCentralYieldCurveF1.append(row['Forward1'])
        itemsCentralYieldCurveF2.append(row['Forward2'])
        itemsCentralYieldCurveF3.append(row['Forward3'])
        itemsCentralYieldCurveF4.append(row['Forward4'])
        itemsCentralYieldCurveF5.append(row['Forward5'])
        itemsCentralYieldCurveF6.append(row['Forward6'])
        itemsCentralYieldCurveF7.append(row['Forward7'])
        itemsCentralYieldCurveF8.append(row['Forward8'])
        itemsCentralYieldCurveF9.append(row['Forward9'])
        itemsCentralYieldCurveF10.append(row['Forward10'])
        itemsCentralYieldCurveF11.append(row['Forward11'])
        itemsCentralYieldCurveF12.append(row['Forward12'])
        itemsDeflactorD1.append(row['Deflactor1'])
        itemsDeflactorD2.append(row['Deflactor2'])
        itemsDeflactorD3.append(row['Deflactor3'])
        itemsDeflactorD4.append(row['Deflactor4'])
        itemsDeflactorD5.append(row['Deflactor5'])
        itemsDeflactorD6.append(row['Deflactor6'])
        itemsDeflactorD7.append(row['Deflactor7'])
        itemsDeflactorD8.append(row['Deflactor8'])
        itemsDeflactorD9.append(row['Deflactor9'])
        itemsDeflactorD10.append(row['Deflactor10'])
        itemsDeflactorD11.append(row['Deflactor11'])
        itemsDeflactorD12.append(row['Deflactor12'])

    RiskFreeCurve = pd.DataFrame({
        '0.8. Risk Free Curve': itemsRiskFreeCurve,
        'Central Yield Curve': itemsCentralYieldCurve,
        'Forward t=1': itemsCentralYieldCurveF1,
        'Forward t=2': itemsCentralYieldCurveF2,
        'Forward t=3': itemsCentralYieldCurveF3,
        'Forward t=4': itemsCentralYieldCurveF4,
        'Forward t=5': itemsCentralYieldCurveF5,
        'Forward t=6': itemsCentralYieldCurveF6,
        'Forward t=7': itemsCentralYieldCurveF7,
        'Forward t=8': itemsCentralYieldCurveF8,
        'Forward t=9': itemsCentralYieldCurveF9,
        'Forward t=10': itemsCentralYieldCurveF10,
        'Forward t=11': itemsCentralYieldCurveF11,
        'Forward t=12': itemsCentralYieldCurveF12,
        'Deflactor': itemsDeflactor,
        'Deflactor t=1': itemsDeflactorD1,
        'Deflactor t=2': itemsDeflactorD2,
        'Deflactor t=3': itemsDeflactorD3,
        'Deflactor t=4': itemsDeflactorD4,
        'Deflactor t=5': itemsDeflactorD5,
        'Deflactor t=6': itemsDeflactorD6,
        'Deflactor t=7': itemsDeflactorD7,
        'Deflactor t=8': itemsDeflactorD8,
        'Deflactor t=9': itemsDeflactorD9,
        'Deflactor t=10': itemsDeflactorD10,
        'Deflactor t=11': itemsDeflactorD11,
        'Deflactor t=12': itemsDeflactorD12,
        '': '',
        ' ': ''
    })

    # -----------------------------------0.9. Premium Dev Pattern
    PremiumDevPattern = pd.DataFrame({
        '0.9. Premium Dev Pattern': ['title', 'Value', 'Value2', 'Value3', 'Value4', 'Value5', 'Value6', 'Value7', 'Value8', 'Value9', 'Value10', 'Value11', 'Value12'],
        'St': ['percent', 1, 0.668213457076566, 0.333333333333333, 0.00689655172413812, 0, 0, 0, 0, 0, 0, 0, 0],
        'St2': ['percent', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        '': '',
        ' ': ''
    })

    # -----------------------------------0.10. SCR_NL Correlation
    NonLife = shockParameters.loc[shockParameters['Item'].isin([
        'NL P&R',
        'NL lapse',
        'NL cat',
    ])].filter(['Value', 'Value2', 'Value3'])

    itemsSCR_NLCorrelation = ['title']
    itemsNLPYR = ['percent']
    itemsNLlapse = ['percent']
    itemsNLcat = ['percent']

    for index, row in NonLife.T.iterrows():
        itemsSCR_NLCorrelation.append(index)
        itemsNLPYR.append(row[196])
        itemsNLlapse.append(row[197])
        itemsNLcat.append(row[198])

    SCR_NLCorrelation = pd.DataFrame({
        '0.10. SCR_NL Correlation': itemsCorrelation,
        'NL P&R': itemsNLPYR,
        'NL lapse': itemsNLlapse,
        'NL cat': itemsNLcat,
        '': '',
        ' ': '',
    })

    # -----------------------------------0.11. Lapses rates stress
    numYears = len(PrimasXRiesgoTable)
    # -- Crear ciclo alrededor del # de años simulados.
    LapsesRatesStressTitle = ['title']
    LapsesRatesStressSt = ['text']
    LapsesRatesStressStUp = ['text']
    LapsesRatesStressStMass = ['text']
    LapsesRatesStressDeltaUps = ['text']
    LapsesRatesStressDeltaMass = ['text']
    for year in range(numYears):
        if year != 0:
            LapsesRatesStressTitle.append(year)
            LapsesRatesStressSt.append((1 - Loadings['Annual Lapse rate'][1]) ** year)
            LapsesRatesStressStUp.append((1 - Loadings['Annual Lapse rate'][1] * 1.5) ** year)
            LapsesRatesStressStMass.append((1 - Loadings['Annual Lapse rate'][1] * 1.3) ** year)
            LapsesRatesStressDeltaUps.append(((1 - Loadings['Annual Lapse rate'][1]) ** year) - ((1 - Loadings['Annual Lapse rate'][1] * 1.5) ** year))
            LapsesRatesStressDeltaMass.append(((1 - Loadings['Annual Lapse rate'][1]) ** year) - ((1 - Loadings['Annual Lapse rate'][1] * 1.3) ** year))

    LapsesRatesStress = pd.DataFrame({
        '0.11. Lapses rates stress': LapsesRatesStressTitle,
        '0.11. St': LapsesRatesStressSt,
        '0.11. St Up': LapsesRatesStressStUp,
        '0.11. St Mass': LapsesRatesStressStMass,
        '0.11. Delta Up': LapsesRatesStressDeltaUps,
        '0.11. Delta Mass': LapsesRatesStressDeltaMass,
        '': '',
        ' ': '',
    })

    # -----------------------------------0.12. % NL
    PremiumDataTable = InputsSolvencia['PremiumDataTable']
    numYears = len(PrimasXRiesgoTable)

    percentNlTitle = ['title']
    percentNlValue = ['text']
    for year in range(numYears):
        if year != 0:
            percentNlTitle.append(year)
            percentNlValue.append((PremiumDataTable['PD_Other Non Life'].loc[1:].sum() / PremiumDataTable['Written Premium Net of Tax'].loc[1:].sum()))

    percentNl = pd.DataFrame({
        '0.12. % NL': percentNlTitle,
        '% NL': percentNlValue,
        '': '',
        ' ': '',
    })

    # -----------------------------------0.13 Years
    Years = pd.DataFrame({
        '0.13 Years': ['title', '1'],
        'Year 1': ['','1.2'],
        'Year 2': ['',''],
        '': '',
        ' ': '',
    })

    # ---------------------------------------------------------------------------------------------------- #
    # --------------------------------------------1.1 SCR_PyR----------------------------------------------#
    # ---------------------------------------------------------------------------------------------------- #

    # ---------------------------------------------V Premium---------------------------------------------- #
    PremiumDataTable = InputsSolvencia['PremiumDataTable']
    RiskPremiumRepartition1Table = InputsSolvencia['RiskPremiumRepartition1Table']
    ProductTable = InputsSolvencia['ProductTable']
    TotalEarnedRiskPremium = OutPut_productsBP_anualFILTER.filter(['Total Earned Risk Premium', 'Earned_Premium'])
    SumOtherNonLife = PremiumDataTable['PD_Other Non Life'].loc[1:].sum()
    SumWrittenPremiumNetOfTax = PremiumDataTable['Written Premium Net of Tax'].loc[1:].sum()
    Motor = RiskPremiumRepartition1Table['"Motor"'][1]
    FireYOtherDamage = RiskPremiumRepartition1Table['"Fire & Other damage"'][1]
    MiscSubjectToCat = RiskPremiumRepartition1Table['"Misc." Subject to Cat'][1]
    MiscNonSubjectToCat = RiskPremiumRepartition1Table['"Misc." Non subject to Cat'][1]
    Commission = ProductTable['Commission'][1]
    # MaxERP = TotalEarnedRiskPremium['Total Earned Risk Premium'].iloc[[0, 1]].max()
    MaxEP = TotalEarnedRiskPremium['Earned_Premium'].iloc[[0, 1]].max()
    VPremiumLoBVPremMotor = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * (1 - Commission) * MaxEP
    VPremiumLoBVPremFire = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * FireYOtherDamage * (1 - Commission) * MaxEP
    VPremiumLoBVPremMiscellaneous = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * (MiscSubjectToCat + MiscNonSubjectToCat) * (1 - Commission) * MaxEP
    Total = VPremiumLoBVPremMotor + VPremiumLoBVPremFire + VPremiumLoBVPremMiscellaneous
    VPremium_V_Premium = ['title', '% NL', '% LoB', '1- % Comm', 'Max ERP (t,t+1)', 'V_Premium_LoB']
    VPremium_V_Prem_Motor = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), Motor, (1 - Commission), MaxEP, VPremiumLoBVPremMotor]
    VPremium_V_prem_Fire_Other_damage = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), FireYOtherDamage, (1 - Commission), MaxEP, VPremiumLoBVPremFire]
    VPremium_V_Prem_Miscellaneous_Non_Life = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), (MiscSubjectToCat + MiscNonSubjectToCat), (1 - Commission), MaxEP, VPremiumLoBVPremMiscellaneous]
    VPremium_Total = ['text', '', '', '', '', Total]
    VPremium_e1 = ['', '', '', '', '', '']
    VPremium_e2 = ['', '', '', '', '', '']
    # -- INICIO Agregar valores desde Year2 hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 1:
            VPremium_V_Premium.append('V_Premium_LoB ' + str(year))
            try:
                # -- MaxERP = TotalEarnedRiskPremium['Total Earned Risk Premium'].iloc[[int(year) - 1, year]].max()
                MaxEP = TotalEarnedRiskPremium['Earned_Premium'].iloc[[int(year) - 1, year]].max()
            except IndexError:
                # -- Posible error: limite del DataFrame, columna "year" no existe, por ende solo se extrae max de columna "int(year - 1)"
                # -- MaxERP = TotalEarnedRiskPremium['Total Earned Risk Premium'].iloc[[int(year - 1), int(year - 1)]].max()
                MaxEP = TotalEarnedRiskPremium['Earned_Premium'].iloc[[int(year - 1), int(year - 1)]].max()
            SUMVPremium_V_Prem_Motor = np.maximum(MaxEP, 0) * (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * (1 - Commission)
            VPremium_V_Prem_Motor.append(SUMVPremium_V_Prem_Motor)
            SUMVPremium_V_prem_Fire_Other_damage = np.maximum(MaxEP, 0) * (SumOtherNonLife / SumWrittenPremiumNetOfTax) * FireYOtherDamage * (1 - Commission)
            VPremium_V_prem_Fire_Other_damage.append(SUMVPremium_V_prem_Fire_Other_damage)
            SUMVPremium_V_Prem_Miscellaneous_Non_Life = np.maximum(MaxEP, 0) * (SumOtherNonLife / SumWrittenPremiumNetOfTax) * (MiscSubjectToCat + MiscNonSubjectToCat) * (1 - Commission)
            VPremium_V_Prem_Miscellaneous_Non_Life.append(SUMVPremium_V_Prem_Miscellaneous_Non_Life)
            VPremium_Total.append(SUMVPremium_V_Prem_Motor + SUMVPremium_V_prem_Fire_Other_damage + SUMVPremium_V_Prem_Miscellaneous_Non_Life)
            VPremium_e1.append('')
            VPremium_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    VPremium = pd.DataFrame()
    VPremium['V Premium'] = VPremium_V_Premium
    VPremium['V Prem - Motor'] = VPremium_V_Prem_Motor
    VPremium['V prem - Fire & Other damage'] = VPremium_V_prem_Fire_Other_damage
    VPremium['V Prem - Miscellaneous Non Life'] = VPremium_V_Prem_Miscellaneous_Non_Life
    VPremium['Total'] = VPremium_Total
    VPremium[''] = VPremium_e1
    VPremium[' '] = VPremium_e2

    # --------------------------------------------V Reserves---------------------------------------------- #
    VReservesLoBVPremMotor = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * itemsClaims[2]
    VReservesLoBVPremFire = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * FireYOtherDamage * itemsClaims[2]
    VReservesLoBVPremMiscellaneous = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * (MiscSubjectToCat + MiscNonSubjectToCat) * itemsClaims[2]
    Total = VReservesLoBVPremMotor + VReservesLoBVPremFire + VReservesLoBVPremMiscellaneous
    VReserves_V_Reserves = ['title', '% NL', '% LoB', 'Claims Reserves', 'V_Reserve_LoB']
    VReserves_Reserves_V_reserve_Motor = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), Motor, itemsClaims[2], VReservesLoBVPremMotor]
    VReserves_Reserves_V_reserve_Fire_Other_damage = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), FireYOtherDamage, itemsClaims[2], VReservesLoBVPremFire]
    VReserves_Reserves_V_reserve_MiscellaneousNonLife = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), (MiscSubjectToCat + MiscNonSubjectToCat), itemsClaims[2], VReservesLoBVPremMiscellaneous]
    VReserves_Reserves_Total = ['text', '', '', '', Total]
    VReserves_e1 = ['', '', '', '', '']
    VReserves_e2 = ['', '', '', '', '']
    # -- INICIO Agregar valores desde Year2 hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 1:
            VReserves_V_Reserves.append('V_Reserve_LoB ' + str(year))
            try:
                SELECTEDItemsClaims = itemsClaims[int(year + 1)]
            except IndexError:
                SELECTEDItemsClaims = 0
            MULVReserves_Reserves_V_reserve_Motor = SELECTEDItemsClaims * (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor
            VReserves_Reserves_V_reserve_Motor.append(MULVReserves_Reserves_V_reserve_Motor)
            MULVReserves_Reserves_V_reserve_Fire_Other_damage = SELECTEDItemsClaims * (SumOtherNonLife / SumWrittenPremiumNetOfTax) * FireYOtherDamage
            VReserves_Reserves_V_reserve_Fire_Other_damage.append(MULVReserves_Reserves_V_reserve_Fire_Other_damage)
            MUlVReserves_Reserves_V_reserve_MiscellaneousNonLife = SELECTEDItemsClaims * (SumOtherNonLife / SumWrittenPremiumNetOfTax) * (MiscSubjectToCat + MiscNonSubjectToCat)
            VReserves_Reserves_V_reserve_MiscellaneousNonLife.append(MUlVReserves_Reserves_V_reserve_MiscellaneousNonLife)
            VReserves_Reserves_Total.append(MULVReserves_Reserves_V_reserve_Motor + MULVReserves_Reserves_V_reserve_Fire_Other_damage + MUlVReserves_Reserves_V_reserve_MiscellaneousNonLife)
            VReserves_e1.append('')
            VReserves_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    VReserves = pd.DataFrame()
    VReserves['V Reserves'] = VReserves_V_Reserves
    VReserves['Reserves │ V reserve - Motor'] = VReserves_Reserves_V_reserve_Motor
    VReserves['Reserves │ V reserve - Fire & Other damage'] = VReserves_Reserves_V_reserve_Fire_Other_damage
    VReserves['Reserves │ V reserve - Miscellaneous Non Life'] = VReserves_Reserves_V_reserve_MiscellaneousNonLife
    VReserves['Reserves │ Total'] = VReserves_Reserves_Total
    VReserves[''] = VReserves_e1
    VReserves[' '] = VReserves_e2

    # -------------------------------------------- V LoB ------------------------------------------------- #
    VLoBLoBVPremMotor = VPremiumLoBVPremMotor + VReservesLoBVPremMotor
    VLoBLoBVPremFire = VPremiumLoBVPremFire + VReservesLoBVPremFire
    VLoBLoBVPremMiscellaneous = VPremiumLoBVPremMiscellaneous + VReservesLoBVPremMiscellaneous
    LoB_V_Total = VLoBLoBVPremMotor + VLoBLoBVPremFire + VLoBLoBVPremMiscellaneous
    VLoB_V_LoB = ['title', 'V_PyR_LoB']
    VLoB_LoB_V_Prem_Motor = ['text', VLoBLoBVPremMotor]
    VLoB_LoB_V_prem_Fire_Other_damage = ['text', VLoBLoBVPremFire]
    VLoB_LoB_V_Prem_Miscellaneous_Non_Life = ['text', VLoBLoBVPremMiscellaneous]
    VLoB_LoB_V_Total = ['text', LoB_V_Total]
    VLoB_e1 = ['', '']
    VLoB_e2 = ['', '']
    # -- INICIO Agregar valores desde Year2 hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 1:
            INICIOVPremium = 6
            INICIOVReserves = 5
            VLoB_V_LoB.append('V_PyR_LoB ' + str(year))
            SUMVPremiumVReserves1 = VPremium.loc[VPremium['V Premium'] == 'V_Premium_LoB ' + str(year)]['V Prem - Motor'][int(INICIOVPremium + (year - 2))] + \
                                    VReserves.loc[VReserves['V Reserves'] == 'V_Reserve_LoB ' + str(year)]['Reserves │ V reserve - Motor'][int(INICIOVReserves + (year - 2))]
            VLoB_LoB_V_Prem_Motor.append(SUMVPremiumVReserves1)
            SUMVPremiumVReserves2 = VPremium.loc[VPremium['V Premium'] == 'V_Premium_LoB ' + str(year)]['V prem - Fire & Other damage'][int(INICIOVPremium + (year - 2))] + \
                                    VReserves.loc[VReserves['V Reserves'] == 'V_Reserve_LoB ' + str(year)]['Reserves │ V reserve - Fire & Other damage'][int(INICIOVReserves + (year - 2))]
            VLoB_LoB_V_prem_Fire_Other_damage.append(SUMVPremiumVReserves2)
            SUMVPremiumVReserves3 = VPremium.loc[VPremium['V Premium'] == 'V_Premium_LoB ' + str(year)]['V Prem - Miscellaneous Non Life'][int(INICIOVPremium + (year - 2))] + \
                                    VReserves.loc[VReserves['V Reserves'] == 'V_Reserve_LoB ' + str(year)]['Reserves │ V reserve - Miscellaneous Non Life'][int(INICIOVReserves + (year - 2))]
            VLoB_LoB_V_Prem_Miscellaneous_Non_Life.append(SUMVPremiumVReserves3)
            VLoB_LoB_V_Total.append(SUMVPremiumVReserves1 + SUMVPremiumVReserves2 + SUMVPremiumVReserves3)
            VLoB_e1.append('')
            VLoB_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    VLoB = pd.DataFrame()
    VLoB['V LoB'] = VLoB_V_LoB
    VLoB['LoB │ V Prem - Motor'] = VLoB_LoB_V_Prem_Motor
    VLoB['LoB │ V prem - Fire & Other damage'] = VLoB_LoB_V_prem_Fire_Other_damage
    VLoB['LoB │ V Prem - Miscellaneous Non Life'] = VLoB_LoB_V_Prem_Miscellaneous_Non_Life
    VLoB['LoB │ V. Total'] = VLoB_LoB_V_Total
    VLoB[''] = VLoB_e1
    VLoB[' '] = VLoB_e2

    # -------------------------------------------- Sigma Premium ------------------------------------------------- #
    SigmaPremium = pd.DataFrame()
    SigmaPremium['Sigma Premium'] = ['title', 'Sigma P', 'Sigma R']
    SigmaPremium['SigmaPremium │ V reserve - Motor'] = ['percent', itemsSigmaPremiumMotor[1], itemsSigmaReserveMotor[1]]
    SigmaPremium['SigmaPremium │ V reserve - Fire & Other damage'] = ['percent', itemsSigmaPremiumFire[1], itemsSigmaReserveFire[1]]
    SigmaPremium['SigmaPremium │ V reserve - Miscellaneous Non Life'] = ['percent', itemsSigmaPremiumMiscellaneous[1], itemsSigmaReserveMiscellaneous[1]]
    SigmaPremium[''] = ['', '', '']
    SigmaPremium[' '] = ['', '', '']

    # -------------------------------------------- Sigma LoB ------------------------------------------------- #
    try:
        SigmaLoBVPremMotor = np.sqrt(
            (itemsSigmaPremiumMotor[1] * VPremiumLoBVPremMotor) ** 2 +
            (itemsSigmaReserveMotor[1] * VReservesLoBVPremMotor) ** 2 +
            (itemsSigmaPremiumMotor[1] * itemsSigmaReserveMotor[1] * VPremiumLoBVPremMotor * VReservesLoBVPremMotor)) \
                             / (VPremiumLoBVPremMotor + VReservesLoBVPremMotor)
    except:
        SigmaLoBVPremMotor = 0
    SigmaLoBVPremMotor = np.nan_to_num(SigmaLoBVPremMotor)

    try:
        SigmaLoBVPremFire = np.sqrt(
            (itemsSigmaPremiumFire[1] * VPremiumLoBVPremFire) ** 2 +
            (itemsSigmaReserveFire[1] * VReservesLoBVPremFire) ** 2 +
            (itemsSigmaPremiumFire[1] * itemsSigmaReserveFire[1] * VPremiumLoBVPremFire * VReservesLoBVPremFire)) \
                            / (VPremiumLoBVPremFire + VReservesLoBVPremFire)
    except:
        SigmaLoBVPremFire = 0
    SigmaLoBVPremFire = np.nan_to_num(SigmaLoBVPremFire)

    try:
        SigmaLoBPremMiscellaneous = np.sqrt(
            (itemsSigmaPremiumMiscellaneous[1] * VPremiumLoBVPremMiscellaneous) ** 2 +
            (itemsSigmaReserveMiscellaneous[1] * VReservesLoBVPremMiscellaneous) ** 2 +
            (itemsSigmaPremiumMiscellaneous[1] * itemsSigmaReserveMiscellaneous[1] * VPremiumLoBVPremMiscellaneous * VReservesLoBVPremMiscellaneous)) \
                                    / (VPremiumLoBVPremMiscellaneous + VReservesLoBVPremMiscellaneous)
    except:
        SigmaLoBPremMiscellaneous = 0
    SigmaLoBPremMiscellaneous = np.nan_to_num(SigmaLoBPremMiscellaneous)

    SigmaLoB = pd.DataFrame()
    SigmaLoB['Sigma LoB'] = ['title', 'Sigma_PyR_LoB']
    SigmaLoB['SigmaLoB │ V Prem - Motor'] = ['percent', SigmaLoBVPremMotor]
    SigmaLoB['SigmaLoB │ V prem - Fire & Other damage'] = ['percent', SigmaLoBVPremFire]
    SigmaLoB['SigmaLoB │ V Prem - Miscellaneous Non Life'] = ['percent', SigmaLoBPremMiscellaneous]
    SigmaLoB[''] = ['', '']
    SigmaLoB[' '] = ['', '']

    # -------------------------------------------- V_lob * Sigma_lob ------------------------------------------------- #
    V_lob_Sigma_lob_V_lob_Sigma_lob = ['title', 'V*Sigma']
    V_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Motor = ['percent', SigmaLoBVPremMotor * VLoBLoBVPremMotor]
    V_lob_Sigma_lob_V_lob_Sigma_lob_V_prem_Fire_Other_damage = ['percent', SigmaLoBVPremFire * VLoBLoBVPremFire]
    V_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Miscellaneous_Non_Life = ['percent', SigmaLoBPremMiscellaneous * VLoBLoBVPremMiscellaneous]
    V_lob_Sigma_lob_e1 = ['', '']
    V_lob_Sigma_lob_e2 = ['', '']
    # -- INICIO Agregar valores desde Year2 hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 1:
            INICIOVLoB = 2
            V_lob_Sigma_lob_V_lob_Sigma_lob.append('V*Sigma ' + str(year))
            RESV_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Motor = SigmaLoBVPremMotor * VLoB.loc[VLoB['V LoB'] == 'V_PyR_LoB ' + str(year)]['LoB │ V Prem - Motor'][int(INICIOVLoB + (year - 2))]
            V_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Motor.append(RESV_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Motor)
            RESV_lob_Sigma_lob_V_lob_Sigma_lob_V_prem_Fire_Other_damage = SigmaLoBVPremFire * VLoB.loc[VLoB['V LoB'] == 'V_PyR_LoB ' + str(year)]['LoB │ V prem - Fire & Other damage'][int(INICIOVLoB + (year - 2))]
            V_lob_Sigma_lob_V_lob_Sigma_lob_V_prem_Fire_Other_damage.append(RESV_lob_Sigma_lob_V_lob_Sigma_lob_V_prem_Fire_Other_damage)
            RESV_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Miscellaneous_Non_Life = SigmaLoBPremMiscellaneous * VLoB.loc[VLoB['V LoB'] == 'V_PyR_LoB ' + str(year)]['LoB │ V Prem - Miscellaneous Non Life'][int(INICIOVLoB + (year - 2))]
            V_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Miscellaneous_Non_Life.append(RESV_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Miscellaneous_Non_Life)
            V_lob_Sigma_lob_e1.append('')
            V_lob_Sigma_lob_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    V_lob_Sigma_lob = pd.DataFrame()
    V_lob_Sigma_lob['V_lob * Sigma_lob'] = V_lob_Sigma_lob_V_lob_Sigma_lob
    V_lob_Sigma_lob['V_lob_Sigma_lob │ V Prem - Motor'] = V_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Motor
    V_lob_Sigma_lob['V_lob_Sigma_lob │ V prem - Fire & Other damage'] = V_lob_Sigma_lob_V_lob_Sigma_lob_V_prem_Fire_Other_damage
    V_lob_Sigma_lob['V_lob_Sigma_lob │ V Prem - Miscellaneous Non Life'] = V_lob_Sigma_lob_V_lob_Sigma_lob_V_Prem_Miscellaneous_Non_Life
    V_lob_Sigma_lob[''] = V_lob_Sigma_lob_e1
    V_lob_Sigma_lob[' '] = V_lob_Sigma_lob_e2

    # -- -------------- -- #
    # -- Calcular Sigma -- #
    # -- -------------- -- #

    # -- Paso 1
    x = [[(SigmaLoBVPremMotor * VLoBLoBVPremMotor), (SigmaLoBVPremFire * VLoBLoBVPremFire), (SigmaLoBPremMiscellaneous * VLoBLoBVPremMiscellaneous)]]
    y = [[itemsGap[1], itemsGap[2], itemsGap[3]], [itemsEW[1], itemsEW[2], itemsEW[3]], [itemsOther[1], itemsOther[2], itemsOther[3]]]
    z = [[(SigmaLoBVPremMotor * VLoBLoBVPremMotor)], [(SigmaLoBVPremFire * VLoBLoBVPremFire)], [(SigmaLoBPremMiscellaneous * VLoBLoBVPremMiscellaneous)]]
    mxy = matMult(x, y)
    # -- Paso 2
    mxyz = matMult(mxy, z)
    # -- Paso 3
    SCR_PyRSigma = (np.sqrt(mxyz[0][0])) / LoB_V_Total

    # -------------------------------------------- RESULTADO SCR_PyR ------------------------------------------------- #
    SCR_PyR_Volumen = ['text', VLoB.loc[VLoB['V LoB'] == 'V_PyR_LoB']['LoB │ V. Total'][1]]
    SCR_PyR_Sigma = ['percent', SCR_PyRSigma]
    SCR_PyR_SCR_PyR = ['text', VLoB.loc[VLoB['V LoB'] == 'V_PyR_LoB']['LoB │ V. Total'][1] * SCR_PyRSigma * 3]
    SCR_PyR_e1 = ['', '']
    SCR_PyR_e2 = ['', '']
    # -- INICIO Agregar valores desde Year2 hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 1:
            INICIOVLoB = 2
            VOL = VLoB.loc[VLoB['V LoB'] == 'V_PyR_LoB ' + str(year)]['LoB │ V. Total'][int(INICIOVLoB + (year - 2))]
            SCR_PyR_Volumen.append(VOL)
            INICIOV_lob_Sigma_lob = 2
            # -- Calcular Sigma -- #
            # -- Paso 1
            SIGV1 = V_lob_Sigma_lob.loc[V_lob_Sigma_lob['V_lob * Sigma_lob'] == 'V*Sigma ' + str(year)]['V_lob_Sigma_lob │ V Prem - Motor'][int(INICIOV_lob_Sigma_lob + (year - 2))]
            SIGV2 = V_lob_Sigma_lob.loc[V_lob_Sigma_lob['V_lob * Sigma_lob'] == 'V*Sigma ' + str(year)]['V_lob_Sigma_lob │ V prem - Fire & Other damage'][int(INICIOV_lob_Sigma_lob + (year - 2))]
            SIGS3 = V_lob_Sigma_lob.loc[V_lob_Sigma_lob['V_lob * Sigma_lob'] == 'V*Sigma ' + str(year)]['V_lob_Sigma_lob │ V Prem - Miscellaneous Non Life'][int(INICIOV_lob_Sigma_lob + (year - 2))]
            SIGLoB_V_Total = VOL
            x = [[(SIGV1), (SIGV2), (SIGS3)]]
            y = [[itemsGap[1], itemsGap[2], itemsGap[3]], [itemsEW[1], itemsEW[2], itemsEW[3]], [itemsOther[1], itemsOther[2], itemsOther[3]]]
            z = [[(SIGV1)], [(SIGV2)], [(SIGS3)]]
            mxy = matMult(x, y)
            # -- Paso 2
            mxyz = matMult(mxy, z)
            # -- Paso 3
            SIGMA = (np.sqrt(mxyz[0][0])) / SIGLoB_V_Total
            SCR_PyR_Sigma.append(SIGMA)
            SCR_PyR_SCR_PyR.append(VOL * SIGMA * 3)
            SCR_PyR_e1.append('')
            SCR_PyR_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    SCR_PyR = pd.DataFrame()
    SCR_PyR['Volumen'] = SCR_PyR_Volumen
    SCR_PyR['Sigma'] = SCR_PyR_Sigma
    SCR_PyR['SCR_PyR'] = SCR_PyR_SCR_PyR
    SCR_PyR[''] = SCR_PyR_e1
    SCR_PyR[' '] = SCR_PyR_e2

    # ------------------------------------------------------------------------------------------------------ #
    # --------------------------------------------1.2 SCR_Lapse----------------------------------------------#
    # ------------------------------------------------------------------------------------------------------ #

    # -------------------------------------------- 1.2.1 SCR_Lapse_Up ------------------------------------------------- #
    SumOtherNonLife = PremiumDataTable['PD_Other Non Life'].loc[1:].sum()
    SumWrittenPremiumNetOfTax = PremiumDataTable['Written Premium Net of Tax'].loc[1:].sum()
    percentLapse = InputsSolvencia['ProductTable']['Annual Lapse rate'][1]
    FilterOpex = OutPut_productsBP_anualFILTER.filter(['- Insurer Earned Operating Expenses Loading', 'OVERHEADS', 'Technical Result'])  # Opex
    NegativeInsurerEarnedOperatingExpensesLoadingYear2 = FilterOpex['- Insurer Earned Operating Expenses Loading']['Año 2']
    OVERHEADSYear2 = FilterOpex['OVERHEADS']['Año 2']
    TechnicalResultYear2 = FilterOpex['Technical Result']['Año 2']
    SCR_Lapse_UpBestEstimate1 = NegativeInsurerEarnedOperatingExpensesLoadingYear2 * (1 - percentLapse)
    SCR_Lapse_UpBestEstimate2 = OVERHEADSYear2 * (1 - percentLapse)
    SCR_Lapse_UpBestEstimate3 = TechnicalResultYear2 * (1 - percentLapse)
    SCR_Lapse_UpStress1 = NegativeInsurerEarnedOperatingExpensesLoadingYear2 * (1 - (percentLapse * (1 + 0.5)))
    SCR_Lapse_UpStress2 = OVERHEADSYear2 * (1 - (percentLapse * (1 + 0.5)))
    SCR_Lapse_UpStress3 = TechnicalResultYear2 * (1 - (percentLapse * (1 + 0.5)))
    SCR_Lapse_UpSt = 0.668213457076566
    SCR_Lapse_UpSCRLapseUp1 = (SCR_Lapse_UpBestEstimate1 - SCR_Lapse_UpStress1) * itemsDeflactor[2] * SCR_Lapse_UpSt * (SumOtherNonLife / SumWrittenPremiumNetOfTax)
    SCR_Lapse_UpSCRLapseUp2 = (SCR_Lapse_UpBestEstimate2 - SCR_Lapse_UpStress2) * itemsDeflactor[2] * SCR_Lapse_UpSt * (SumOtherNonLife / SumWrittenPremiumNetOfTax)
    SCR_Lapse_UpSCRLapseUp3 = (SCR_Lapse_UpBestEstimate3 - SCR_Lapse_UpStress3) * itemsDeflactor[2] * SCR_Lapse_UpSt * (SumOtherNonLife / SumWrittenPremiumNetOfTax)

    SCR_Lapse_Up_121SCR_Lapse_Up = ['title', '% NL', '% Lapse', 'Shock', '% Lapse + Stress', 'Best Estimate', 'Stress', 'St']
    SCR_Lapse_Up_Up_Decrease_in_opex_and_margin = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), percentLapse, 0.5, percentLapse * (1 + 0.5), SCR_Lapse_UpBestEstimate1, SCR_Lapse_UpStress1, SCR_Lapse_UpSt]
    SCR_Lapse_Up_Up_Decrease_in_overheads = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), percentLapse, 0.5, percentLapse * (1 + 0.5), SCR_Lapse_UpBestEstimate2, SCR_Lapse_UpStress2, SCR_Lapse_UpSt]
    SCR_Lapse_Up_Up_Decrease_in_claims_result = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), percentLapse, 0.5, percentLapse * (1 + 0.5), SCR_Lapse_UpBestEstimate3, SCR_Lapse_UpStress3, SCR_Lapse_UpSt]
    SCR_Lapse_Up_Up_Direct_Variable_Commission_Mitigation = ['text', '', '', '', '', '', '', '']
    SCR_Lapse_Up_e1 = ['', '', '', '', '', '', '', '']
    SCR_Lapse_Up_e2 = ['', '', '', '', '', '', '', '']

    # -- INICIO Agregar valores desde Year hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 0:
            SCR_Lapse_Up_121SCR_Lapse_Up.append('SCR Lapse Up ' + str(year))
            # -- Filtro para matrices
            SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M1 = RT['- Insurer Earned Operating Expenses Loading'].loc[int(year + 1):int(numYears - 1)]
            # -- Si year > 1, se extrae St2
            if year > 1:
                SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M2 = PremiumDevPattern['St2'].loc[int(year + 1):int(numYears - 1)]
            else:
                SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M2 = PremiumDevPattern['St'].loc[int(year + 1):int(numYears - 1)]
            # -- Si year > 1, se extrae de columna Deflactor t=n
            if year > 1:
                SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M3 = RiskFreeCurve['Deflactor t=' + str(year - 1)].loc[int(year):int(numYears - 2)]
            else:
                SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M3 = RiskFreeCurve['Deflactor'].loc[int(year):int(numYears - 2)]
            SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M4 = LapsesRatesStress['0.11. Delta Up'].loc[1:int(numYears - year)]
            SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M5 = percentNl['% NL'].loc[int(year):int(numYears - 2)]
            SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_MFINAL = SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M1.reset_index(drop=True) * \
                                                                 SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M2.reset_index(drop=True) * \
                                                                 SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M3.reset_index(drop=True) * \
                                                                 SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M4.reset_index(drop=True) * \
                                                                 SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M5.reset_index(drop=True)
            SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_MFINAL = SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_MFINAL.fillna(0).sum()
            # ---------------------------------------
            SCR_Lapse_Up_Up_Decrease_in_overheads_M1 = RT['OVERHEADS'].loc[int(year + 1):int(numYears - 1)]
            SCR_Lapse_Up_Up_Decrease_in_overheads_MFINAL = SCR_Lapse_Up_Up_Decrease_in_overheads_M1.reset_index(drop=True) * \
                                                           SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M2.reset_index(drop=True) * \
                                                           SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M3.reset_index(drop=True) * \
                                                           SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M4.reset_index(drop=True) * \
                                                           SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M5.reset_index(drop=True)
            SCR_Lapse_Up_Up_Decrease_in_overheads_MFINAL = SCR_Lapse_Up_Up_Decrease_in_overheads_MFINAL.fillna(0).sum()
            SCR_Lapse_Up_Up_Decrease_in_overheads_MFINAL = SCR_Lapse_Up_Up_Decrease_in_overheads_MFINAL * -1
            # ---------------------------------------
            SCR_Lapse_Up_Up_Decrease_in_claims_result_M1 = RT['Technical Result'].loc[int(year + 1):int(numYears - 1)]
            SCR_Lapse_Up_Up_Decrease_in_claims_result_MFINAL = SCR_Lapse_Up_Up_Decrease_in_claims_result_M1.reset_index(drop=True) * \
                                                               SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M2.reset_index(drop=True) * \
                                                               SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M3.reset_index(drop=True) * \
                                                               SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M4.reset_index(drop=True) * \
                                                               SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_M5.reset_index(drop=True)
            SCR_Lapse_Up_Up_Decrease_in_claims_result_MFINAL = SCR_Lapse_Up_Up_Decrease_in_claims_result_MFINAL.fillna(0).sum()
            # ---------------------------------------
            # ---------------------------------------
            # ---------------------------------------
            SCR_Lapse_Up_Up_Decrease_in_opex_and_margin.append(SCR_Lapse_Up_Up_Decrease_in_opex_and_margin_MFINAL)
            SCR_Lapse_Up_Up_Decrease_in_overheads.append(SCR_Lapse_Up_Up_Decrease_in_overheads_MFINAL)
            SCR_Lapse_Up_Up_Decrease_in_claims_result.append(SCR_Lapse_Up_Up_Decrease_in_claims_result_MFINAL)
            SCR_Lapse_Up_Up_Direct_Variable_Commission_Mitigation.append(SCR_Lapse_Up_Up_Decrease_in_claims_result_MFINAL * -1)
            SCR_Lapse_Up_e1.append('')
            SCR_Lapse_Up_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección

    SCR_Lapse_Up = pd.DataFrame()
    SCR_Lapse_Up['1.2.1 SCR_Lapse_Up'] = SCR_Lapse_Up_121SCR_Lapse_Up
    SCR_Lapse_Up['Up - Decrease in opex and margin'] = SCR_Lapse_Up_Up_Decrease_in_opex_and_margin
    SCR_Lapse_Up['Up - Decrease in overheads'] = SCR_Lapse_Up_Up_Decrease_in_overheads
    SCR_Lapse_Up['Up - Decrease in claims result'] = SCR_Lapse_Up_Up_Decrease_in_claims_result
    SCR_Lapse_Up['Up - Direct Variable Commission Mitigation'] = SCR_Lapse_Up_Up_Direct_Variable_Commission_Mitigation
    SCR_Lapse_Up[''] = SCR_Lapse_Up_e1
    SCR_Lapse_Up[' '] = SCR_Lapse_Up_e2

    # -------------------------------------------- 1.2.2 SCR_Lapse_Mass ------------------------------------------------- #

    SCR_Lapse_MassBestEstimate1 = NegativeInsurerEarnedOperatingExpensesLoadingYear2
    SCR_Lapse_MassBestEstimate2 = OVERHEADSYear2
    SCR_Lapse_MassBestEstimate3 = TechnicalResultYear2
    SCR_Lapse_MassStress1 = NegativeInsurerEarnedOperatingExpensesLoadingYear2 * 0.3
    SCR_Lapse_MassStress2 = OVERHEADSYear2 * 0.3
    SCR_Lapse_MassStress3 = TechnicalResultYear2 * 0.3
    SCR_Lapse_MassSCRLapseUp1 = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * 0.668213457076566 * SCR_Lapse_MassStress1 * itemsDeflactor[2]
    SCR_Lapse_MassSCRLapseUp2 = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * 0.668213457076566 * SCR_Lapse_MassStress2 * itemsDeflactor[2]
    SCR_Lapse_MassSCRLapseUp3 = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * 0.668213457076566 * SCR_Lapse_MassStress3 * itemsDeflactor[2]

    SCR_Lapse_Mass_1_2_2_SCR_Lapse_Mass = ['title', '% NL', 'Shock', 'Best Estimate', 'Stress', 'St']
    SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), 0.3, SCR_Lapse_MassBestEstimate1, SCR_Lapse_MassStress1, 0.668213457076566]
    SCR_Lapse_Mass_Mass_Decrease_in_overheads = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), 0.3, SCR_Lapse_MassBestEstimate2, SCR_Lapse_MassStress2, 0.668213457076566]
    SCR_Lapse_Mass_Mass_Decrease_in_claims_result = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), 0.3, SCR_Lapse_MassBestEstimate3, SCR_Lapse_MassStress3, 0.668213457076566]
    SCR_Lapse_Mass_Mass_Direct_Variable_Commission_Mitigation = ['text', '', '', '', '', '']
    SCR_Lapse_Mass_e1 = ['', '', '', '', '', '']
    SCR_Lapse_Mass_e2 = ['', '', '', '', '', '']

    # -- INICIO Agregar valores desde Year hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 0:
            SCR_Lapse_Mass_1_2_2_SCR_Lapse_Mass.append('SCR Lapse Up ' + str(year))
            # -- Filtro para matrices
            SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M1 = RT['- Insurer Earned Operating Expenses Loading'].loc[int(year + 1):int(numYears - 1)]
            # -- Si year > 1, se extrae St2
            if year > 1:
                SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M2 = PremiumDevPattern['St2'].loc[int(year + 1):int(numYears - 1)]
            else:
                SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M2 = PremiumDevPattern['St'].loc[int(year + 1):int(numYears - 1)]
            # -- Si year > 1, se extrae de columna Deflactor t=n
            if year > 1:
                SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M3 = RiskFreeCurve['Deflactor t=' + str(year - 1)].loc[int(year):int(numYears - 2)]
            else:
                SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M3 = RiskFreeCurve['Deflactor'].loc[int(year):int(numYears - 2)]

            SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M5 = percentNl['% NL'].loc[int(year):int(numYears - 2)]
            SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M1.reset_index(drop=True) * \
                                                                     SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M2.reset_index(drop=True) * \
                                                                     SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M3.reset_index(drop=True) * \
                                                                     SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M5.reset_index(drop=True)
            SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_MFINAL.fillna(0).sum()
            SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_MFINAL * 0.3

            # ---------------------------------------
            SCR_Lapse_Mass_Mass_Decrease_in_overheads_M1 = RT['OVERHEADS'].loc[int(year + 1):int(numYears - 1)]
            SCR_Lapse_Mass_Mass_Decrease_in_overheads_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_overheads_M1.reset_index(drop=True) * \
                                                               SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M2.reset_index(drop=True) * \
                                                               SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M3.reset_index(drop=True) * \
                                                               SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M5.reset_index(drop=True)
            SCR_Lapse_Mass_Mass_Decrease_in_overheads_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_overheads_MFINAL.fillna(0).sum()
            SCR_Lapse_Mass_Mass_Decrease_in_overheads_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_overheads_MFINAL * 0.3 * -1
            # ---------------------------------------
            SCR_Lapse_Mass_Mass_Decrease_in_claims_result_M1 = RT['Technical Result'].loc[int(year + 1):int(numYears - 1)]
            SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_claims_result_M1.reset_index(drop=True) * \
                                                                   SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M2.reset_index(drop=True) * \
                                                                   SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M3.reset_index(drop=True) * \
                                                                   SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_M5.reset_index(drop=True)
            SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL.fillna(0).sum()
            SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL = SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL * 0.3
            # ---------------------------------------
            # ---------------------------------------
            # ---------------------------------------
            SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin.append(SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin_MFINAL)
            SCR_Lapse_Mass_Mass_Decrease_in_overheads.append(SCR_Lapse_Mass_Mass_Decrease_in_overheads_MFINAL)
            SCR_Lapse_Mass_Mass_Decrease_in_claims_result.append(SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL)
            SCR_Lapse_Mass_Mass_Direct_Variable_Commission_Mitigation.append(SCR_Lapse_Mass_Mass_Decrease_in_claims_result_MFINAL * -1)
            SCR_Lapse_Mass_e1.append('')
            SCR_Lapse_Mass_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección

    SCR_Lapse_Mass = pd.DataFrame()
    SCR_Lapse_Mass['1.2.2 SCR_Lapse_Mass'] = SCR_Lapse_Mass_1_2_2_SCR_Lapse_Mass
    SCR_Lapse_Mass['Mass - Decrease in opex and margin'] = SCR_Lapse_Mass_Mass_Decrease_in_opex_and_margin
    SCR_Lapse_Mass['Mass - Decrease in overheads'] = SCR_Lapse_Mass_Mass_Decrease_in_overheads
    SCR_Lapse_Mass['Mass - Decrease in claims result'] = SCR_Lapse_Mass_Mass_Decrease_in_claims_result
    SCR_Lapse_Mass['Mass - Direct Variable Commission Mitigation'] = SCR_Lapse_Mass_Mass_Direct_Variable_Commission_Mitigation
    SCR_Lapse_Mass[''] = SCR_Lapse_Mass_e1
    SCR_Lapse_Mass[' '] = SCR_Lapse_Mass_e2

    # -------------------------------------------- Value 1.2 SCR_Lapse ------------------------------------------------- #
    SCR_Lapse_SCR_Lapse = ['text']
    SCR_Lapse_e1 = ['']
    SCR_Lapse_e2 = ['']
    # -- INICIO Agregar valores desde Year hasta # meses de proyección
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 0:
            # 1.2.1 Suma SCR Lapse Up
            Suma1 = SCR_Lapse_Up.loc[SCR_Lapse_Up['1.2.1 SCR_Lapse_Up'] == 'SCR Lapse Up ' + str(year)].filter(['Up - Decrease in opex and margin', 'Up - Decrease in overheads', 'Up - Decrease in claims result', 'Up - Direct Variable Commission Mitigation']).sum(axis=1)
            Suma1 = Suma1.reset_index()[0][0]
            # 1.2.2 Suma SCR Lapse Up
            Suma2 = SCR_Lapse_Mass.loc[SCR_Lapse_Mass['1.2.2 SCR_Lapse_Mass'] == 'SCR Lapse Up ' + str(year)].filter(['Mass - Decrease in opex and margin', 'Mass - Decrease in overheads', 'Mass - Decrease in claims result', 'Mass - Direct Variable Commission Mitigation']).sum(axis=1)
            Suma2 = Suma2.reset_index()[0][0]
            Mayor = np.where(
                Suma1 > Suma2,
                Suma1,
                Suma2
            )
            Mayor = np.where(
                Mayor > 0,
                Mayor,
                0
            )
            SCR_Lapse_SCR_Lapse.append(Mayor)
            SCR_Lapse_e1.append('')
            SCR_Lapse_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    SCR_Lapse = pd.DataFrame()
    SCR_Lapse['SCR_Lapse'] = SCR_Lapse_SCR_Lapse
    SCR_Lapse[''] = SCR_Lapse_e1
    SCR_Lapse[' '] = SCR_Lapse_e2

    # ---------------------------------------------------------------------------------------------------- #
    # --------------------------------------------1.3 SCR_Cat----------------------------------------------#
    # ---------------------------------------------------------------------------------------------------- #

    # -------------------------------------------- 1.3.1 SCR_Cat ------------------------------------------------- #

    FilterPrimasXRiesgoTable = PrimasXRiesgoTable.filter(['Written Premium Net of Tax'])
    WrittenPremiumNetOfTaxYear2 = FilterPrimasXRiesgoTable['Written Premium Net of Tax'][2]
    SCR_CatTotalMotor = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * 0.2 * itemsIncurredClaims[2]
    SCR_CatTotalFire = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * 0 * itemsIncurredClaims[2]
    SCR_CatTotalMiscellaneous = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * 0.4 * itemsIncurredClaims[2] * (itemsTotalEarnedRiskPremium[2] + WrittenPremiumNetOfTaxYear2 * (Loadings['Commission'][1] + Loadings['Acquisition costs loading'][1])) / (1 - Loadings['Insurer capital cost loading'][1] - Loadings['Operating expenses loading'][1])
    SCR_CatTotalOverheads = (0.03 * (SCR_CatTotalMotor + SCR_CatTotalFire + SCR_CatTotalMiscellaneous))

    SCR_Cat_1_3_1_SCR_Cat = ['title', '% NL', '% LoB', 'Shock']
    SCR_Cat_SCR_Cat_Motor = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), Motor, 0.2]
    SCR_Cat_SCR_Cat_Fire_Other_damage = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), FireYOtherDamage, 0]
    SCR_Cat_SCR_Cat_Miscellaneous_Non_Life = ['text', (SumOtherNonLife / SumWrittenPremiumNetOfTax), MiscSubjectToCat, 0.4]
    SCR_Cat_SCR_Cat_Overheads = ['text', '', '', 0.03]
    SCR_Cat_e1 = ['', '', '', '']
    SCR_Cat_e2 = ['', '', '', '']

    # -- INICIO Agregar valores desde Year hasta # meses de proyección 0453
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 0:
            SCR_Cat_1_3_1_SCR_Cat.append('SCR Cat ' + str(year))
            yIncurredClaims = RT['Incurred Claims'].loc[int(year):int(year)][int(year)]
            yTechnicalResult = RT['Technical Result'].loc[int(year):int(year)][int(year)]
            ResultSCR_Cat_SCR_Cat_Motor = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * Motor * 0.2 * yIncurredClaims
            SCR_Cat_SCR_Cat_Motor.append(ResultSCR_Cat_SCR_Cat_Motor)
            ResultSCR_Cat_SCR_Cat_Fire_Other_damage = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * FireYOtherDamage * 0 * yTechnicalResult
            SCR_Cat_SCR_Cat_Fire_Other_damage.append(ResultSCR_Cat_SCR_Cat_Fire_Other_damage)
            ResultSCR_Cat_SCR_Cat_Miscellaneous_Non_Life = (SumOtherNonLife / SumWrittenPremiumNetOfTax) * MiscSubjectToCat * 0.4 * 0
            SCR_Cat_SCR_Cat_Miscellaneous_Non_Life.append(ResultSCR_Cat_SCR_Cat_Miscellaneous_Non_Life)
            ResultSCR_Cat_SCR_Cat_Overheads = 0 * 0 * 0.03 * 0
            SCR_Cat_SCR_Cat_Overheads.append(ResultSCR_Cat_SCR_Cat_Overheads)
            SCR_Cat_e1.append('')
            SCR_Cat_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    SCR_Cat = pd.DataFrame()
    SCR_Cat['1.3.1 SCR_Cat'] = SCR_Cat_1_3_1_SCR_Cat
    SCR_Cat['SCR_Cat - Motor'] = SCR_Cat_SCR_Cat_Motor
    SCR_Cat['SCR_Cat - Fire & Other damage'] = SCR_Cat_SCR_Cat_Fire_Other_damage
    SCR_Cat['SCR_Cat - Miscellaneous Non Life'] = SCR_Cat_SCR_Cat_Miscellaneous_Non_Life
    SCR_Cat['SCR_Cat - Overheads'] = SCR_Cat_SCR_Cat_Overheads
    SCR_Cat[''] = SCR_Cat_e1
    SCR_Cat[' '] = SCR_Cat_e2

    # -------------------------------------------- Value 1.3 SCR_Cat ------------------------------------------------- #
    ValueSCR_Cat_1_3_SCR_Cat = ['text']
    ValueSCR_Cat_e1 = ['']
    ValueSCR_Cat_e2 = ['']
    # -- INICIO Agregar valores desde Year hasta # meses de proyección 0453
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 0:
            SUM_SCR_Cat = SCR_Cat.loc[SCR_Cat['1.3.1 SCR_Cat'] == 'SCR Cat ' + str(year)].filter(['SCR_Cat - Motor', 'SCR_Cat - Fire & Other damage', 'SCR_Cat - Miscellaneous Non Life', 'SCR_Cat - Overheads']).sum(axis=1)
            SUM_SCR_Cat = SUM_SCR_Cat.reset_index()[0][0]
            ValueSCR_Cat_1_3_SCR_Cat.append(SUM_SCR_Cat)
            ValueSCR_Cat_e1.append('')
            ValueSCR_Cat_e2.append('')
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    ValueSCR_Cat = pd.DataFrame()
    ValueSCR_Cat['1.3 SCR_Cat'] = ValueSCR_Cat_1_3_SCR_Cat
    ValueSCR_Cat[''] = ValueSCR_Cat_e1
    ValueSCR_Cat[' '] = ValueSCR_Cat_e2

    # --------------------------------------------------------------------------------------------------- #
    # --------------------------------------------1.1 SCR NL----------------------------------------------#
    # --------------------------------------------------------------------------------------------------- #
    SCR_NL_SCR_NL = ['title3']
    SCR_NL_SCR_PyR = ['price2']
    SCR_NL_SCR_Lapse = ['price2']
    SCR_NL_SCR_Cat = ['price2']
    # -- INICIO Agregar valores desde Year hasta # meses de proyección 0453
    numYears = len(PrimasXRiesgoTable)
    for year in range(numYears):
        if year > 0:
            MTSCR_NL_SCR_PyR = SCR_PyR_SCR_PyR[year]
            MTSCR_NL_SCR_Lapse = SCR_Lapse_SCR_Lapse[year]
            MTSCR_NL_SCR_Cat = ValueSCR_Cat_1_3_SCR_Cat[year]
            # -- -------------- -- #
            # -- Calcular SCR_NL --#
            # -- -------------- -- #
            # -- Paso 1
            x = [[MTSCR_NL_SCR_PyR, MTSCR_NL_SCR_Lapse, MTSCR_NL_SCR_Cat]]
            y = [[itemsNLPYR[1], itemsNLPYR[2], itemsNLPYR[3]], [itemsNLlapse[1], itemsNLlapse[2], itemsNLlapse[3]], [itemsNLcat[1], itemsNLcat[2], itemsNLcat[3]]]
            z = [[(MTSCR_NL_SCR_PyR)], [(MTSCR_NL_SCR_Lapse)], [(MTSCR_NL_SCR_Cat)]]
            mxy = matMult(x, y)
            # -- Paso 2
            mxyz = matMult(mxy, z)
            # -- Paso 3
            SCR_NLTotal = (np.sqrt(mxyz[0][0]))
            SCR_NL_SCR_NL.append(SCR_NLTotal)
            SCR_NL_SCR_PyR.append(MTSCR_NL_SCR_PyR)
            SCR_NL_SCR_Lapse.append(MTSCR_NL_SCR_Lapse)
            SCR_NL_SCR_Cat.append(MTSCR_NL_SCR_Cat)
    # -- FIN Agregar valores desde Year2 hasta # meses de proyección
    SCR_NL = pd.DataFrame()
    SCR_NL['SCR_NL'] = SCR_NL_SCR_NL
    SCR_NL[' SCR_PyR'] = SCR_NL_SCR_PyR
    SCR_NL[' SCR_Lapse'] = SCR_NL_SCR_Lapse
    SCR_NL[' SCR_Cat'] = SCR_NL_SCR_Cat

    # -----------------------------------\\------------------------------------ #
    # -----------------------------------\\------------------------------------ #
    # -----------------------------------\\------------------------------------ #
    InputsNonLifeSCR = {
        'PrimasXRiesgoTable': PrimasXRiesgoTable,
        'ParticipacionXLoB': ParticipacionXLoB,
        'Loadings': Loadings,
        'RT': RT,
        'Sigma': Sigma,
        'Correlation': Correlation,
        'RiskFreeCurve': RiskFreeCurve,
        'PremiumDevPattern': PremiumDevPattern,
        'SCR_NLCorrelation': SCR_NLCorrelation,
        'LapsesRatesStress': LapsesRatesStress,
        'percentNl': percentNl,
        'Years': Years,
        'VPremium': VPremium,
        'VReserves': VReserves,
        'VLoB': VLoB,
        'SigmaPremium': SigmaPremium,
        'SigmaLoB': SigmaLoB,
        'V_lob_Sigma_lob': V_lob_Sigma_lob,
        'SCR_PyR': SCR_PyR,
        'SCR_Lapse_Up': SCR_Lapse_Up,
        'SCR_Lapse_Mass': SCR_Lapse_Mass,
        'SCR_Lapse': SCR_Lapse,
        'SCR_Cat': SCR_Cat,
        'ValueSCR_Cat': ValueSCR_Cat,
        'SCR_NL': SCR_NL,
    }

    return InputsNonLifeSCR
