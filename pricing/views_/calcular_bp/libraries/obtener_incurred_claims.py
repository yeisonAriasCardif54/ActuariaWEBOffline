def obtener_incurred_claims(OutPut):
    # -- Iva no descontable -- #
    OutPut['vatp'] = OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['commin'] * OutPut['IVA']
    OutPut['vata'] = OutPut['% VAT'] * OutPut['% Com Non'] * OutPut['earnedC'] * OutPut['IVA']

    # -- Obtiene las incurred claims -- #
    OutPut['incurC'] = OutPut['earnedP'] * OutPut['Claims rate']

    return OutPut
