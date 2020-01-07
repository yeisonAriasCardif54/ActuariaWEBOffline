def obtener_comisiones(OutPut):
    # -- Obtiene las comisiones diferidas -- #
    OutPut['dac'] = OutPut['upr'] * OutPut['Comisión Total']
    # -- Total Earned_Commissions -- #
    OutPut['earnedC'] = OutPut['earnedP'] * OutPut['Comisión Total']
    # -- Partner Earned_Commissions -- #
    OutPut['ecs'] = OutPut['earnedP'] * (OutPut['Comisión Total'] * OutPut['Comisión Socio'])
    # -- Broker Earned_Commissions -- #
    OutPut['ecb'] = OutPut['earnedP'] * (OutPut['Comisión Total'] * OutPut['Comisión Broker'])

    return OutPut
