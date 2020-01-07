# --  -- #

import pandas as pd
import numpy as np
import os
import xlrd

pd.set_option("display.precision", 20)


def getShockParameters():
    # -- Leer datos de MK Shocks
    file = '/static/pricing/business_plan_templates/Shock parameters.xlsx'
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../../../' + file)
    xlsxFile = pd.ExcelFile(path)

    EIOPA = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='EIOPA parameters (QIS5)'))
    Country = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Country'))
    BSCR = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='BSCR'))
    Market_Down = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Market Down'))
    Market_Up = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Market Up'))
    Life = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Life'))
    HEALTH_SLT = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='HEALTH  SLT'))
    Health = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Health'))
    Health_NSLT = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Health NSLT'))
    Non_Life = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='Non Life'))
    PremiumReserve = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='PremiumReserve'))

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------Unificar tablas
    # ---------------------------------------------------------------------------------------------------- #
    Tables = pd.concat([EIOPA,
                        Country,
                        BSCR,
                        Market_Down,
                        Market_Up,
                        Life,
                        HEALTH_SLT,
                        Health,
                        Health_NSLT,
                        Non_Life,
                        PremiumReserve,
                        ])
    Tables = Tables.reset_index()
    del (Tables['index'])
    return Tables
