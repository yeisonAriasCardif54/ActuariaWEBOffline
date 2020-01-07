''' Calculo de la PU por grupo de PU '''

import numpy as np
# import time


def obtener_PU(OutPut, ngrupos, meses, data_grupos_pu, Pu):
    # start_time = time.time()

    w, h = ngrupos, meses
    Pu['goi1'] = [[0] * h for i in [0] * w]
    Pu['capitalcost'] = [[0] * h for i in [0] * w]
    Pu['profit1g'] = [[0] * h for i in [0] * w]
    Pu['acumprofitg'] = [[0] * h for i in [0] * w]
    Pu['profit2g'] = [[0] * h for i in [0] * w]
    Pu['purealg'] = [[0] * h for i in [0] * w]
    Pu['puincurg'] = [[0] * h for i in [0] * w]
    Pu['acumpurealg'] = [[0] * h for i in [0] * w]
    Pu['resulTecg'] = [[0] * h for i in [0] * w]
    Pu['goi2'] = [[0] * h for i in [0] * w]

    def get_goi1(a, b, c, d, e, f, g, h, i, j, k):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        d = np.array(d)
        e = np.array(e)
        f = np.array(f)
        g = np.array(g)
        h = np.array(h)
        i = np.array(i)
        j = np.array(j)
        k = np.array(k)
        return a - b - c - d - e - f - g - h - i - j - k

    def multi_2(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.multiply(a, b)

    def rest_2(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.subtract(a, b)

    def resulTecg(a, b, c, d):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        d = np.array(d)
        return a - b - c - d

    Pu['goi1'] = [get_goi1(a, b, c, d, e, f, g, h, i, j, k) for a, b, c, d, e, f, g, h, i, j, k in zip(Pu['earnedPreg'], Pu['earnedCog'], Pu['incurCg'], Pu['VAT_Amortig'], Pu['incentig'], Pu['tmktCostg'], Pu['overheadg'], Pu['icag'], Pu['gmfg'], Pu['vatincentg'], Pu['vatmkg'])]
    Pu['capitalcost'] = [multi_2(a, b) for a, b in zip(Pu['earnedPreg'], Pu['CapitalCost'])]
    Pu['profit1g'] = [rest_2(a, b) for a, b in zip(Pu['goi1'], Pu['capitalcost'])]

    # acumprofitg
    for i in range(1, ngrupos + 1):
        for k in range(meses):
            if k == 0:
                Pu['acumprofitg'][i][k] = Pu['profit1g'][i][k] + Pu['Claims Result to Share'][i]
            else:
                Pu['acumprofitg'][i][k] = Pu['profit1g'][i][k] + Pu['acumprofitg'][i][k - 1]

    Pu['profit2g'] = [multi_2(a, b) for a, b in zip(Pu['acumprofitg'], Pu['Share_PU'])]  # Puede ser negativo tambien 'PU
    Pu['purealg'] = [rest_2(a, b) for a, b in zip(Pu['profit2g'], Pu['Paid/Liberación'])]  # Se referirá a la PU_eop que es como la "reserva" ( eop = end of period )

    # puincurg
    for i in range(1, ngrupos + 1):
        for k in range(meses):
            if k == 0:
                Pu['puincurg'][i][k] = Pu['purealg'][i][k] - ((Pu['Share_PU'][i] * Pu['Claims Result to Share'][i]) - Pu['Paid/Liberación'][i])
            else:
                Pu['puincurg'][i][k] = Pu['purealg'][i][k] - Pu['purealg'][i][k - 1]

    Pu['acumpurealg'] = Pu['Paid/Liberación']  # se mantiene constante la PU pagada
    Pu['resulTecg'] = [resulTecg(a, b, c, d) for a, b, c, d in zip(Pu['earnedPreg'], Pu['earnedCog'], Pu['incurCg'], Pu['puincurg'])]
    Pu['goi2'] = [rest_2(a, b) for a, b in zip(Pu['goi1'], Pu['puincurg'])]

    #print("\n\n obtener_PU \n--- %s seconds ---" % (time.time() - start_time))
    return Pu
