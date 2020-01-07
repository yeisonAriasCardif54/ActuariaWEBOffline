''' Obtener Resultado Tecnico '''

import pandas as pd
import numpy as np
# import time


def obtener_resultado_tecnico(OutPut, Pu, ngrupos, meses):
    # start_time = time.time()

    w, h = ngrupos, meses

    OutPut_newOutPut = pd.DataFrame()
    OutPut_newOutPut['ResulTec'] = [0 for i in [0] * len(OutPut)]
    OutPut_newOutPut['Id_ Grupo_PU'] = OutPut['Id_ Grupo_PU']
    OutPut_newOutPut['TEMP_numeromes'] = OutPut['TEMP_numeromes']
    Pu['ResulTecAcum'] = [[0] * h for i in [0] * w]

    ########################## Pasamos el list de purealg a DataFrame ##########################

    purealg = pd.DataFrame.from_items(zip(Pu['purealg'].index, Pu['purealg'].values)).T
    purealg = purealg.stack()  # Crear filas de meses
    purealg = pd.DataFrame({'index': purealg.index, 'valorPurealg': purealg.values})  # Convertir nuevamente en DataFrame
    purealg['index'] = purealg['index'].astype(np.str).replace('[()]', '', regex=True)  # procesamos index
    purealg['Id_ Grupo_PU'] = purealg['index'].str.split(',', expand=True)[0].astype(np.int64)  # Extraemos Id_ Grupo_PU
    purealg['TEMP_numeromes'] = purealg['index'].str.split(',', expand=True)[1].astype(np.int64) + 1  # Extraemos TEMP_numeromes+1
    del (purealg['index'])  # Limpiamos

    # Unificamos OutPut_newOutPut y purealg
    OutPut_newOutPut = pd.merge(OutPut_newOutPut, purealg, on=['Id_ Grupo_PU', 'TEMP_numeromes'], how='left')

    ########################## resultado tecnico ##########################
    try:
        OutPut['Ecosistema'] = np.where(
            OutPut['TEMP_numeromes'] >= OutPut['Inicio mes ecosistema'],
            OutPut['Ecosistema'] * OutPut['vigentes'],
            0
        )
    except:
        OutPut['Ecosistema'] = 0

    OutPut_newOutPut['ResulTec'] = np.where(
        OutPut_newOutPut['valorPurealg'] > 0,
        OutPut['earnedP'] - OutPut['earnedC'] - OutPut['incurC'] - OutPut['Ecosistema'],
        0
    )

    ########################## Recorrido para agrupar el resultado tecnico positivo dependiendo de la utilidad de la PU ##########################
    # Extraemos los resultados tecnicos positivos
    OutPut_newOutPut['ResulTecTEMP'] = np.where(
        OutPut_newOutPut['ResulTec'] > 0,
        OutPut_newOutPut['ResulTec'],
        0
    )
    # Sumatoria teniendo en cuenta la llave "Id_ Grupo_PU-TEMP_numeromes"
    # Obtenemos Id_ Grupo_PU-TEMP_numeromes de purealg
    Grupo_PU_numeromes = purealg
    OutPut_ResulTec = OutPut_newOutPut.groupby(('Id_ Grupo_PU', 'TEMP_numeromes')).ResulTecTEMP.sum()  # Agrupamos y sumamos por  Id_ Grupo_PU-TEMP_numeromes
    OutPut_ResulTec = [list(key) + [str(value)] for key, value in OutPut_ResulTec.to_dict().items()]
    labels = ['Id_ Grupo_PU', 'TEMP_numeromes', 'ResulTecTEMP']
    OutPut_ResulTec = pd.DataFrame.from_records(OutPut_ResulTec, columns=labels)  # Creamos nuevo dataframe
    Grupo_PU_numeromes = pd.merge(Grupo_PU_numeromes, OutPut_ResulTec, on=['Id_ Grupo_PU', 'TEMP_numeromes'], how='left')
    Grupo_PU_numeromes['ResulTecTEMP'] = Grupo_PU_numeromes['ResulTecTEMP'].astype(np.float64)
    Grupo_PU_numeromes['ResulTecTEMP'] = Grupo_PU_numeromes['ResulTecTEMP'].fillna(0)
    Grupo_PU_numeromes['ResulTecA'] = np.where(Grupo_PU_numeromes['valorPurealg'] > 0, Grupo_PU_numeromes['ResulTecTEMP'], 0)
    Grupo_PU_numeromes['TEMP_numeromes'] = Grupo_PU_numeromes['TEMP_numeromes'] - 1
    Pu['ResulTecAcum'] = Grupo_PU_numeromes.groupby(['Id_ Grupo_PU', 'TEMP_numeromes'])['ResulTecA'].sum().groupby(level=0).apply(list)

    # Reemplazar nulos por cero
    OutPut['ResulTec'] = OutPut_newOutPut['ResulTec'].fillna(0)
    Pu['ResulTecAcum'] = Pu['ResulTecAcum'].fillna(0)

    #print("\n\n obtener_resultado_tecnico \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut, Pu
