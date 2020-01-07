''' Obtener siniestros '''

#import time

def obtener_siniestros(OutPut):
    #start_time = time.time()
    OutPut['siniestros'] = OutPut['Frecuencia'] * OutPut['vigentes']
    #print("\n\n obtener_siniestros \n--- %s seconds ---" % (time.time() - start_time))
    return OutPut