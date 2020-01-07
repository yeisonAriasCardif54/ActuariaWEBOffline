# --  -- #

import pandas as pd
import os

pd.set_option("display.precision", 20)


def solvencyII_MK_Shocks():
    # -- Leer datos de MK Shocks
    file = '/static/pricing/business_plan_templates/MK Shocks.xlsx'
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../../../' + file)
    xlsxFile = pd.ExcelFile(path)

    InterestRateYieldCurve = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Interest Rate Yield Curve'))
    ShocksToBeapplied = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Shocks to be applied'))
    CorrelationMatrixes = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Correlation Matrixes'))

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------Unificar tablas
    # ---------------------------------------------------------------------------------------------------- #
    Tables = pd.concat([InterestRateYieldCurve,
                        ShocksToBeapplied,
                        CorrelationMatrixes
                        ], sort=False)
    Tables = Tables.reset_index()

    del (Tables['index'])
    return Tables
