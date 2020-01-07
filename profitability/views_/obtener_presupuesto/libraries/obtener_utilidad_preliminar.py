''' Utilidad preliminar '''

import pandas as pd
import numpy as np
# import time


def obtener_utilidad_preliminar(OutPut, tipincent, ngrupos, data_grupos_pu, nproduct, meses, OutPut_data_grupos_pu):
    # start_time = time.time()
    OutPut['pagincentivos2'] = np.where(
        tipincent == "Pagados",
        OutPut['incentp'],
        OutPut['incent']
    )

    newOutPut = pd.DataFrame()
    newOutPut['gastos'] = [0.0 for i in [0.0] * len(OutPut)]
    newOutPut['gross2'] = [0.0 for i in [0.0] * len(OutPut)]

    meses = meses + 1
    Up = pd.DataFrame()

    Up['gross1'] = [0 for i in [0] * meses]
    Up['capitalcost1'] = [0 for i in [0] * meses]
    Up['pu'] = [0 for i in [0] * meses]
    Up['acumpu'] = [0 for i in [0] * meses]
    Up['pu2'] = [0 for i in [0] * meses]

    Up['gross1'] = Up['gross1'].astype(np.float64)
    Up['capitalcost1'] = Up['capitalcost1'].astype(np.float64)
    Up['pu'] = Up['pu'].astype(np.float64)
    Up['acumpu'] = Up['acumpu'].astype(np.float64)
    Up['pu2'] = Up['pu2'].astype(np.float64)

    newOutPut['gastos'] = (OutPut['Overheads'] * OutPut['earnedP']) + OutPut['ica'] + OutPut['gmf']
    OutPut['gastos'] = newOutPut['gastos'].fillna(0)

    # Extraemos registros requeridos agrupados por TEMP_numeromes, teniendo en cuenta el ultimo Id_Tool

    OutPut_TEMPup = OutPut.query('Id_Tool==' + str(max(OutPut['Id_Tool']))).groupby(['TEMP_numeromes'])['earnedP', 'earnedC', 'vata', 'pagincentivos2', 'tmkCost', 'incurC', 'gastos', 'vatincent', 'vatmk', 'fincomer', 'fincomec'].sum()
    CapitalCost = OutPut_data_grupos_pu.query('Id_Tool==' + str(max(OutPut['Id_Tool'])))['CapitalCost'].tolist()
    OutPut_TEMPup['CapitalCost'] = CapitalCost
    Share_PU = OutPut_data_grupos_pu.query('Id_Tool==' + str(max(OutPut['Id_Tool'])))['Share_PU'].tolist()
    OutPut_TEMPup['Share_PU'] = Share_PU

    Up['gross1'] = OutPut_TEMPup['earnedP'] - OutPut_TEMPup['earnedC'] - OutPut_TEMPup['vata'] - OutPut_TEMPup['pagincentivos2'] - OutPut_TEMPup['tmkCost'] - OutPut_TEMPup['incurC'] - OutPut_TEMPup['gastos'] - OutPut_TEMPup['vatincent'] - OutPut_TEMPup['vatmk']
    Up['gross1'] = Up['gross1'].fillna(0)

    Up['capitalcost1'] = OutPut_TEMPup['earnedP'] * OutPut_TEMPup['CapitalCost']
    Up['capitalcost1'] = Up['capitalcost1'].fillna(0)

    Up['pu'] = (Up['gross1'] - Up['capitalcost1'])
    Up['pu'] = Up['pu'].fillna(0)

    Up['acumpu'] = Up.query("pu!=0")['pu'].cumsum()
    Up['acumpu'] = Up['acumpu'].fillna(0)

    Up['pu2'] = Up['acumpu'] * OutPut_TEMPup['Share_PU']  # Profit 2
    Up['pu2'] = Up['pu2'].fillna(0)

    # gross2 = gross1 + fincomer + fincomec
    newOutPut['gross2'] = (OutPut['earnedP'] - OutPut['earnedC'] - OutPut['vata'] - OutPut['pagincentivos2'] - OutPut['tmkCost'] - OutPut['incurC'] - OutPut['gastos'] - OutPut['vatincent'] - OutPut['vatmk']) + OutPut['fincomer'] + OutPut['fincomec']
    # -- Restar Ecosistema
    newOutPut['gross2'] = newOutPut['gross2'] - OutPut['Ecosistema']
    OutPut['gross2'] = newOutPut['gross2'].fillna(0)

    OutPut['gastos'] = OutPut['gastos'].astype(np.float64)
    OutPut['gross2'] = OutPut['gross2'].astype(np.float64)

    #print("\n\n obtener_utilidad_preliminar \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, Up
