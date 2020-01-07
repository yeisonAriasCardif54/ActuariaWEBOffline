def obtener_siniestros(OutPut):
    OutPut['siniestros'] = OutPut['Incidence rate'] * OutPut['vigentes']
    # -- TODO: Aplicar % Stress -- #
    OutPut['siniestros'] = OutPut['siniestros'] * OutPut['Stress test Claims increase']

    return OutPut
