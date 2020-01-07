# --  -- #

import pandas as pd
import numpy as np
import os
import xlrd


def solvencyII_Data(InputsSolvencia, OutPut):
    DataSolvencia = pd.merge(OutPut.filter(['Producto']), InputsSolvencia, on=['Producto'], how='left')

    return DataSolvencia
