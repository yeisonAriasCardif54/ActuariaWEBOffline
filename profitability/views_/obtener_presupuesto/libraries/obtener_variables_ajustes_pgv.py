''' Obtener los variables_ajustes_pgv '''

import pandas as pd
import numpy as np


def obtener_variables_ajustes_pgv(OutPut, tasadesemen, tasadeseanu, ctmktc, ctmkac):
    ### (OutPut['fincomec'] + OutPut['fincomer']) = Financial Incomes
    OutPut['Year'] = np.ceil(OutPut['TEMP_numeromes'] / 12)

    OutPut['NOI'] = OutPut['gross2'] - OutPut['taxreal']
    OutPut['PVFP'] = (OutPut['NOI']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['PVGWP'] = (OutPut['gwp']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['PVEP'] = (OutPut['earnedP']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['PVCOMMISION'] = (OutPut['commin']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['PVCLAIMS'] = (OutPut['incurC']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['PV Cap Req'] = (OutPut['reqcapy']) / ((1 + tasadeseanu) ** OutPut['Year'])
    OutPut['Variacion Req Capital'] = np.where(
        OutPut['TEMP_numeromes'] == 1,
        (0 - OutPut['reqcap']),
        OutPut['reqcap'].shift(1) - OutPut['reqcap']
    )
    OutPut['Value Creation'] = ((OutPut['gross2'] - OutPut['taxreal']) + OutPut['Variacion Req Capital']) / ((1 + tasadeseanu) ** OutPut['Year'])
    OutPut['Technical NOI'] = OutPut['NOI'] - (OutPut['fincomec'] + OutPut['fincomer'])  # NOI - Financial Incomes
    OutPut['Technical PVFP'] = (OutPut['Technical NOI']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['Financial PVFP'] = (OutPut['fincomec'] + OutPut['fincomer']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['NBV'] = OutPut['Value Creation']
    OutPut['PV NEP'] = (OutPut['earnedP'] - OutPut['earnedC']) / ((1 + tasadesemen) ** OutPut['TEMP_numeromes'])
    OutPut['APE'] = np.where(
        OutPut['Oferta'] == "Compulsory",
        OutPut['gwp'],
        np.where((OutPut['Tipo Prima'] == "Mensual"),
                 (OutPut['nuevos'] * OutPut['Vlr. Prima Prom']) * 12,
                 np.where((OutPut['Tipo Prima'] == "Anual"),
                          (OutPut['nuevos'] * OutPut['Vlr. Prima Prom']),
                          np.where((OutPut['Tipo Prima'] == "Única"),
                                   ((OutPut['nuevos'] * OutPut['Vlr. Prima Prom']) / OutPut['Duración']) * 12,
                                   0)
                          )
                 )
    )
    OutPut['APE'] = np.where(
        OutPut['Year'] != 1,
        0,
        OutPut['APE']
    )
    OutPut['Prima Media'] = OutPut['Vlr. Prima Prom']
    OutPut['Duración'] = OutPut['Duración']
    return OutPut
