''' Obtener incurred claims '''

import numpy as np


def obtener_incurred_claims(OutPut, piva):
    # start_time = time.time()
    # Iva no descontable
    OutPut['vatp'] = OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['commin'] * piva
    OutPut['vata'] = OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['earnedC'] * piva

    # indicador del año segùn el # del mes
    OutPut['yclaim'] = ((OutPut['TEMP_numeromes'] - OutPut['Mes Inicio'] + 1) / 12)
    OutPut['yclaim'] = OutPut['yclaim'].astype(np.float64)
    OutPut['yclaim'] = round(OutPut['yclaim'], 1)
    OutPut['yclaim'] = np.ceil(OutPut['yclaim'])

    # -- Aplicar Factor siniestralidad año 1 -- #
    #OutPut['ClaimsRate_Y1_BACKUP'] = OutPut['ClaimsRate_Y1']
    try:
            OutPut['ClaimsRate_Y1'] = OutPut['ClaimsRate_Y1'] * OutPut['Factor siniestralidad año 1']
    except:
        OutPut['ClaimsRate_Y1'] = OutPut['ClaimsRate_Y1']

    # -- Aplicar Factor siniestralidad año 2 -- #
    #OutPut['ClaimsRate_Y1_BACKUP'] = OutPut['ClaimsRate_Y1']
    try:
        OutPut['ClaimsRate_Y2'] = OutPut['ClaimsRate_Y2'] * OutPut['Factor siniestralidad año 2']
    except:
        OutPut['ClaimsRate_Y2'] = OutPut['ClaimsRate_Y2']

    # Obtiene las incurred claims
    OutPut['incurC'] = np.where(
        OutPut['yclaim'] < 2,
        OutPut['earnedP'] * OutPut['ClaimsRate_Y1'],
        np.where(
            OutPut['yclaim'] < 3,
            OutPut['earnedP'] * OutPut['ClaimsRate_Y2'],
            OutPut['earnedP'] * OutPut['ClaimsRate_Y3+'],
        )
    )

    # print("\n\n obtener_incurred_claims \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut
