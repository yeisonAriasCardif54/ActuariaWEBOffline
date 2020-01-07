import numpy as np


def obtener_variables_agrupamiento_PU(ngrupos, meses, mesiniciost, OutPut, data_grupos_pu):
    OutPut['tipincent'] = 'Pagados'  # --  Cálculo RT con Incentivos -- #
    Pu = data_grupos_pu
    Pu = Pu.set_index(['Id_Grupo'])

    w, h = ngrupos, meses
    Pu['nuevosg'] = [[0] * h for i in [0] * w]
    Pu['vigenteg'] = [[0] * h for i in [0] * w]
    Pu['cancelag'] = [[0] * h for i in [0] * w]
    Pu['siniestrog'] = [[0] * h for i in [0] * w]
    Pu['GWPg'] = [[0] * h for i in [0] * w]
    Pu['earnedPreg'] = [[0] * h for i in [0] * w]
    Pu['coming'] = [[0] * h for i in [0] * w]
    Pu['DACg'] = [[0] * h for i in [0] * w]
    Pu['earnedCog'] = [[0] * h for i in [0] * w]
    Pu['incurCg'] = [[0] * h for i in [0] * w]
    Pu['VAT_Paidg'] = [[0] * h for i in [0] * w]
    Pu['VAT_Amortig'] = [[0] * h for i in [0] * w]
    Pu['incentig'] = [[0] * h for i in [0] * w]
    Pu['tmktCostg'] = [[0] * h for i in [0] * w]
    Pu['vatincentg'] = [[0] * h for i in [0] * w]
    Pu['vatmkg'] = [[0] * h for i in [0] * w]
    Pu['overheadg'] = [[0] * h for i in [0] * w]
    Pu['icag'] = [[0] * h for i in [0] * w]
    Pu['gmfg'] = [[0] * h for i in [0] * w]

    OutPut['TEMP_incentig'] = np.where(OutPut['tipincent'] == "Pagados", OutPut['incentp'], OutPut['incent'])
    OutPut['TEMP_overheadg'] = OutPut['Overheads'] * OutPut['earnedP']

    nuevosg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['nuevos'].sum().groupby('Id_ Grupo_PU')['nuevos'].apply(list)

    vigenteg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['vigentes'].sum().groupby('Id_ Grupo_PU')['vigentes'].apply(list)

    cancelag = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['cancelaciones'].sum().groupby('Id_ Grupo_PU')['cancelaciones'].apply(list)

    siniestrog = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['siniestros'].sum().groupby('Id_ Grupo_PU')['siniestros'].apply(list)

    GWPg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['gwp'].sum().groupby('Id_ Grupo_PU')['gwp'].apply(list)

    earnedPreg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['earnedP'].sum().groupby('Id_ Grupo_PU')['earnedP'].apply(list)

    coming = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['commin'].sum().groupby('Id_ Grupo_PU')['commin'].apply(list)

    DACg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['dac'].sum().groupby('Id_ Grupo_PU')['dac'].apply(list)

    earnedCog = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['earnedC'].sum().groupby('Id_ Grupo_PU')['earnedC'].apply(list)

    incurCg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['incurC'].sum().groupby('Id_ Grupo_PU')['incurC'].apply(list)

    VAT_Paidg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['vatp'].sum().groupby('Id_ Grupo_PU')['vatp'].apply(list)

    VAT_Amortig = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['vata'].sum().groupby('Id_ Grupo_PU')['vata'].apply(list)

    incentig = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['TEMP_incentig'].sum().groupby('Id_ Grupo_PU')['TEMP_incentig'].apply(list)

    tmktCostg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['tmkCost'].sum().groupby('Id_ Grupo_PU')['tmkCost'].apply(list)

    vatincentg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['vatincent'].sum().groupby('Id_ Grupo_PU')['vatincent'].apply(list)

    vatmkg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['vatmk'].sum().groupby('Id_ Grupo_PU')['vatmk'].apply(list)

    overheadg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['TEMP_overheadg'].sum().groupby('Id_ Grupo_PU')['TEMP_overheadg'].apply(list)

    icag = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['ica'].sum().groupby('Id_ Grupo_PU')['ica'].apply(list)

    gmfg = OutPut.groupby((['Id_ Grupo_PU', 'TEMP_numeromes']), as_index=False)['gmf'].sum().groupby('Id_ Grupo_PU')['gmf'].apply(list)

    Pu['nuevosg'], Pu['vigenteg'], Pu['cancelag'], Pu['siniestrog'], Pu['GWPg'], Pu['earnedPreg'], Pu['coming'], Pu['DACg'], Pu['earnedCog'], Pu['incurCg'] = nuevosg, vigenteg, cancelag, siniestrog, GWPg, earnedPreg, coming, DACg, earnedCog, incurCg
    Pu['VAT_Paidg'], Pu['VAT_Amortig'], Pu['incentig'], Pu['tmktCostg'], Pu['vatincentg'], Pu['vatmkg'], Pu['overheadg'], Pu['icag'], Pu['icag'], Pu['gmfg'] = VAT_Paidg, VAT_Amortig, incentig, tmktCostg, vatincentg, vatmkg, overheadg, icag, icag, gmfg

    for row in Pu.loc[Pu.nuevosg.isnull(), 'nuevosg'].index:
        Pu.nuevosg[row] = [0.0 * w for i in [0] * h]
        Pu.vigenteg[row] = [0.0 * w for i in [0] * h]
        Pu.cancelag[row] = [0.0 * w for i in [0] * h]
        Pu.siniestrog[row] = [0.0 * w for i in [0] * h]
        Pu.GWPg[row] = [0.0 * w for i in [0] * h]
        Pu.earnedPreg[row] = [0.0 * w for i in [0] * h]
        Pu.coming[row] = [0.0 * w for i in [0] * h]
        Pu.DACg[row] = [0.0 * w for i in [0] * h]
        Pu.earnedCog[row] = [0.0 * w for i in [0] * h]
        Pu.incurCg[row] = [0.0 * w for i in [0] * h]
        Pu.VAT_Paidg[row] = [0.0 * w for i in [0] * h]
        Pu.VAT_Amortig[row] = [0.0 * w for i in [0] * h]
        Pu.incentig[row] = [0.0 * w for i in [0] * h]
        Pu.tmktCostg[row] = [0.0 * w for i in [0] * h]
        Pu.vatincentg[row] = [0.0 * w for i in [0] * h]
        Pu.vatmkg[row] = [0.0 * w for i in [0] * h]
        Pu.overheadg[row] = [0.0 * w for i in [0] * h]
        Pu.icag[row] = [0.0 * w for i in [0] * h]
        Pu.gmfg[row] = [0.0 * w for i in [0] * h]

    return Pu
