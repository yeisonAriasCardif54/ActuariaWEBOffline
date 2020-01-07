''' Distribuir la PU para cada uno de los productos que tiene resultado tecnico positivo '''

import pandas as pd
import numpy as np


# import time


def distribuir_PU(OutPut, ngrupos, Pu, nproduct, meses, Up):
    # start_time = time.time()

    OutPut['gross2m'] = 0
    OutPut['pureal'] = 0
    OutPut['puincur'] = 0

    OutPut_newOutPut = pd.DataFrame()
    OutPut_newOutPut['pureal'] = [0 for i in [0] * len(OutPut)]
    OutPut_newOutPut['puincur'] = [0 for i in [0] * len(OutPut)]
    OutPut_newOutPut['pureal'] = OutPut_newOutPut['pureal'].astype(np.float64)
    OutPut_newOutPut['puincur'] = OutPut_newOutPut['puincur'].astype(np.float64)

    meses = meses + 1
    OutPut_newOutPut2 = pd.DataFrame()
    OutPut_newOutPut2['gross2m'] = [0 for i in [0] * meses]
    OutPut_newOutPut2['Acumgross2'] = [0 for i in [0] * meses]

    ##### Extraer informacion de Pu['purealg'] y Pu['ResulTecAcum'] y Pu['puincurg'] #####
    OutPut_newOutPut['Id_ Grupo_PU'] = OutPut['Id_ Grupo_PU']
    OutPut_newOutPut['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    OutPut_newOutPut['ResulTec'] = OutPut['ResulTec']

    ########################################################### Pu['purealg'] ###########################################################
    purealg = pd.DataFrame.from_items(zip(Pu['purealg'].index, Pu['purealg'].values)).T
    purealg = purealg.stack()  # Crear filas de meses
    purealg = pd.DataFrame({'index': purealg.index, 'valorPurealg': purealg.values})  # Convertir nuevamente en DataFrame
    purealg['index'] = purealg['index'].astype(np.str).replace('[()]', '', regex=True)  # procesamos index
    purealg['Id_ Grupo_PU'] = purealg['index'].str.split(',', expand=True)[0].astype(np.int64)  # Extraemos Id_ Grupo_PU
    purealg['TEMP_numeromes'] = purealg['index'].str.split(',', expand=True)[1].astype(np.int64) + 1  # Extraemos TEMP_numeromes+1
    del (purealg['index'])  # Limpiamos
    OutPut_newOutPut = pd.merge(OutPut_newOutPut, purealg, on=['Id_ Grupo_PU', 'TEMP_numeromes'], how='left')

    ########################################################### Pu['ResulTecAcum'] ###########################################################
    ResulTecAcum = pd.DataFrame.from_items(zip(Pu['ResulTecAcum'].index, Pu['ResulTecAcum'].values)).T
    ResulTecAcum = ResulTecAcum.stack()  # Crear filas de meses
    ResulTecAcum = pd.DataFrame({'index': ResulTecAcum.index, 'valorResulTecAcum': ResulTecAcum.values})  # Convertir nuevamente en DataFrame
    ResulTecAcum['index'] = ResulTecAcum['index'].astype(np.str).replace('[()]', '', regex=True)  # procesamos index
    ResulTecAcum['Id_ Grupo_PU'] = ResulTecAcum['index'].str.split(',', expand=True)[0].astype(np.int64)  # Extraemos Id_ Grupo_PU
    ResulTecAcum['TEMP_numeromes'] = ResulTecAcum['index'].str.split(',', expand=True)[1].astype(np.int64) + 1  # Extraemos TEMP_numeromes+1
    del (ResulTecAcum['index'])  # Limpiamos
    OutPut_newOutPut = pd.merge(OutPut_newOutPut, ResulTecAcum, on=['Id_ Grupo_PU', 'TEMP_numeromes'], how='left')

    ########################################################### Pu['puincurg'] ###########################################################
    puincurg = pd.DataFrame.from_items(zip(Pu['puincurg'].index, Pu['puincurg'].values)).T
    puincurg = puincurg.stack()  # Crear filas de meses
    puincurg = pd.DataFrame({'index': puincurg.index, 'valorpuincurg': puincurg.values})  # Convertir nuevamente en DataFrame
    puincurg['index'] = puincurg['index'].astype(np.str).replace('[()]', '', regex=True)  # procesamos index
    puincurg['Id_ Grupo_PU'] = puincurg['index'].str.split(',', expand=True)[0].astype(np.int64)  # Extraemos Id_ Grupo_PU
    puincurg['TEMP_numeromes'] = puincurg['index'].str.split(',', expand=True)[1].astype(np.int64) + 1  # Extraemos TEMP_numeromes+1
    del (puincurg['index'])  # Limpiamos
    OutPut_newOutPut = pd.merge(OutPut_newOutPut, puincurg, on=['Id_ Grupo_PU', 'TEMP_numeromes'], how='left')

    # Obtener pureal
    OutPut_newOutPut['pureal'] = np.where(
        OutPut_newOutPut['valorPurealg'] > 0,
        np.where(
            OutPut_newOutPut['ResulTec'] > 0,
            (OutPut_newOutPut['ResulTec'] / OutPut_newOutPut['valorResulTecAcum']) * OutPut_newOutPut['valorPurealg'],
            0
        ),
        0
    )
    # Obtener puincur
    OutPut_newOutPut['puincur'] = np.where(
        OutPut_newOutPut['valorPurealg'] > 0,
        np.where(
            OutPut_newOutPut['ResulTec'] > 0,
            (OutPut_newOutPut['ResulTec'] / OutPut_newOutPut['valorResulTecAcum']) * OutPut_newOutPut['valorpuincurg'],
            0
        ),
        0
    )

    OutPut_newOutPut['gross2'] = OutPut['gross2']
    OutPut_newOutPut['gross2'] = OutPut_newOutPut['gross2'] - OutPut_newOutPut['puincur']

    # Obtener gross2m
    OutPut_newOutPut['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    OutPut_newOutPut2['gross2m'] = OutPut_newOutPut.groupby(('TEMP_numeromes'))['gross2'].sum()
    OutPut_newOutPut2['gross2m'] = OutPut_newOutPut2['gross2m'].fillna(0)

    # Obtener Acumgross2
    OutPut_newOutPut2['Acumgross2'] = OutPut_newOutPut.query("gross2 > 0").groupby(('TEMP_numeromes'))['gross2'].sum()
    OutPut_newOutPut2['Acumgross2'] = OutPut_newOutPut2['Acumgross2'].fillna(0)


    OutPut['ResulTec'] = OutPut['earnedP'] - OutPut['earnedC'] - OutPut['incurC'] - OutPut_newOutPut['puincur'] - OutPut['Ecosistema']
    OutPut['TNBI'] = OutPut['earnedP'] - OutPut['earnedC'] - OutPut['incurC'] - OutPut_newOutPut['puincur'] - OutPut['Ecosistema'] - OutPut['vata']

    # -- Recalcular ResulTec restando ecosistema
    # -- Calculos para Ecosistema

    # OutPut['ResulTecV2'] = OutPut['ResulTec'] - OutPut['Ecosistema']

    OutPut['pureal'] = OutPut_newOutPut['pureal'].fillna(0)
    OutPut['puincur'] = OutPut_newOutPut['puincur'].fillna(0)
    OutPut['gross2'] = OutPut_newOutPut['gross2'].fillna(0)

    OutPut['pureal'] = OutPut['pureal'].astype(np.float64)
    OutPut['puincur'] = OutPut['puincur'].astype(np.float64)
    OutPut['gross2'] = OutPut['gross2'].astype(np.float64)

    Up['gross2m'] = OutPut_newOutPut2['gross2m'].fillna(0)
    Up['Acumgross2'] = OutPut_newOutPut2['Acumgross2'].fillna(0)

    Up['gross2m'] = Up['gross2m'].astype(np.float64)
    Up['Acumgross2'] = Up['Acumgross2'].astype(np.float64)

    # print("\n\n distribuir_PU \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, Up
