# --  -- #

import pandas as pd
import numpy as np


def SolvencyII_CalcularInputs(xlsxFile, Inputs, OutPut, OutPut_productsBP_anual):
    InputsSolvenciaII = pd.DataFrame(pd.read_excel(xlsxFile, sheet_name='SolvenciaII'))

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------GlobalTable
    # ---------------------------------------------------------------------------------------------------- #

    GlobalTable = pd.DataFrame({
        #'Global': ['title', ''],
        #'ID Producto': ['text', InputsSolvenciaII['Producto'][0]],
        'Country': ['text', 'Colombia'],
        'Corporate Tax rate': ['percent', Inputs['Taxes'][0]],
        'Discount rate': ['percent', Inputs['Discount Rate annual'][0]],
        'Capital remuneration rate': ['percent', Inputs['Investment Rate anual'][0]],
        'Retail / non retail': ['text', InputsSolvenciaII['Retail / non retail'][0]],
        'SPACE | Variable Commission': ['text', ''],
        'Result put into equalization reserve': ['percent', InputsSolvenciaII['Result put into equalization reserve'][0]],
        'Partner Direct Variable Commission': ['percent', Inputs['% PU'][0]],
        'Partner Deffered Variable Commission': ['percent', InputsSolvenciaII['Partner Deffered Variable Commission'][0]],
        'Loss Carried Forward?': ['text', InputsSolvenciaII['Loss Carried Forward?'][0]],
        'SPACE | 2': ['text', ''],
        'SPACE | Asset by type': ['text', ''],
        'State bond, fixed interest rate': ['percent', InputsSolvenciaII['State bond, fixed interest rate'][0]],
        'State bond, variable interest rate': ['percent', InputsSolvenciaII['State bond, variable interest rate'][0]],
        'Corporate bond, fixed interest rate': ['percent', InputsSolvenciaII['Corporate bond, fixed interest rate'][0]],
        'Corporate bond, variable interest rate': ['percent', InputsSolvenciaII['Corporate bond, variable interest rate'][0]],
        'Equity - OECD zone': ['percent', InputsSolvenciaII['Equity - OECD zone'][0]],
        'Equity - Non OECD zone': ['percent', InputsSolvenciaII['Equity - Non OECD zone'][0]],
        'Property': ['percent', InputsSolvenciaII['Property'][0]],
        'Structured Credit': ['percent', InputsSolvenciaII['Structured Credit'][0]],
        'Credit Derivatives': ['percent', InputsSolvenciaII['Credit Derivatives'][0]],
        'Cash': ['percent', InputsSolvenciaII['Cash'][0]],
        #'Sensi du portefeuille': ['text', InputsSolvenciaII['Sensi du portefeuille'][0]],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------RiskPremiumRepartitionTable
    # ---------------------------------------------------------------------------------------------------- #

    # -- Precalculo de variables RiskPremiumRepartition #
    RPR_Life = (InputsSolvenciaII['Life Others'][0] + InputsSolvenciaII['Life TPD'][0])
    RPR_Health_SLT = (InputsSolvenciaII['Health SLT Hospitalization'][0] + InputsSolvenciaII['Health SLT TD'][0] + InputsSolvenciaII['Health SLT TPD'][0])
    RPR_Health_Non_SLT_IncProt = (InputsSolvenciaII['Healt non SLT ACC Accidental death'][0] + InputsSolvenciaII['Healt non SLT ACC Hospitalization'][0] + InputsSolvenciaII['Healt non SLT ACC Others'][0] + InputsSolvenciaII['Healt non SLT ACC TPD'][0])
    RPR_Health_Non_SLT_Medex = (InputsSolvenciaII['Healt non SLT Sick Hospitalization'][0] + InputsSolvenciaII['Healt non SLT Sick Others'][0] + InputsSolvenciaII['Healt non SLT Sick TPD'][0])
    RPR_Other_Non_Life = (InputsSolvenciaII['Non Life Misc. Motor'][0] + InputsSolvenciaII['Non Life Misc. Others'][0])

    # -- Suma RiskPremiumRepartition -- #
    RiskPremiumRepartition = RPR_Life + \
                             RPR_Health_SLT + \
                             RPR_Health_Non_SLT_IncProt + \
                             RPR_Health_Non_SLT_Medex + \
                             RPR_Other_Non_Life
    RiskPremiumRepartitionTable = pd.DataFrame({
        'Risk premium repartition': ['title', ''],
        'RPR_Life': ['percent', RPR_Life],
        'RPR_Health SLT': ['percent', RPR_Health_SLT],
        'RPR_Health Non SLT - IncProt': ['percent', RPR_Health_Non_SLT_IncProt],
        'RPR_Health Non SLT - Medex': ['percent', RPR_Health_Non_SLT_Medex],
        'RPR_Other Non Life': ['percent', RPR_Other_Non_Life],
        '': '',
        ' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------ProductTable
    # ---------------------------------------------------------------------------------------------------- #
    Inputs['Duración del producto financiero'] = Inputs['Duración del producto financiero'].astype(np.float32)
    ProductTable = pd.DataFrame({
        #'Product': ['title', ''],
        'Type of premium': ['text', Inputs['Tipo de prima'][0]],
        'Annual Lapse rate': ['percent', Inputs['Caida'][0]],
        'Delay after launch to detect a problem on loss-ratio': ['text', InputsSolvenciaII['Delay after launch to detect a problem on loss-ratio'][0]],
        'Premium revisability on stock?': ['text', InputsSolvenciaII['Premium revisability on stock?'][0]],
        'Revisability delay on stock': ['text', InputsSolvenciaII['Revisability delay on stock'][0]],

        'Policy duration (without lapse)': ['text', Inputs['Duración del producto financiero'][0]],

        'Life (incl. non unbundled TPD)': ['text', np.where(RiskPremiumRepartition > 0, Inputs['Duración del producto financiero'][0], 0)],
        'Health SLT': ['text', np.where(RiskPremiumRepartition > 0, Inputs['Duración del producto financiero'][0], 1)],
        'Health Non SLT - IncProt': ['text', np.where(RiskPremiumRepartition > 0, Inputs['Duración del producto financiero'][0], 2)],
        'Health Non SLT - Medex': ['text', np.where(RiskPremiumRepartition > 0, Inputs['Duración del producto financiero'][0], 3)],
        'Other Non Life': ['text', np.where(RiskPremiumRepartition > 0, Inputs['Duración del producto financiero'][0], 4)],
        'SPACE | Loadings': ['text', ''],

        'Commission': ['percent', np.where(RiskPremiumRepartition > 0, Inputs['Comisión Total'][0], 0)],
        'Insurer capital cost loading': ['percent', np.where(RiskPremiumRepartition > 0, Inputs['Costo de Capital'][0], 0)],
        'Acquisition costs loading': ['percent', np.where(RiskPremiumRepartition > 0, Inputs['% Costo de adquisición'][0], 0)],
        'Operating expenses loading': ['percent', np.where(RiskPremiumRepartition > 0, Inputs['Overheads'][0], 0)],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------AssetByRatingTable
    # ---------------------------------------------------------------------------------------------------- #

    AssetByRatingTable = pd.DataFrame({
        #'Asset by rating': ['title', 'State (Non EEA)', 'Corporate'],
        'AAA': ['percent', InputsSolvenciaII['Asset by rating: AAA (State)'][0], InputsSolvenciaII['Asset by rating: AAA (Corporate)'][0]],
        'AA': ['percent', InputsSolvenciaII['Asset by rating: AA (State)'][0], InputsSolvenciaII['Asset by rating: AA (Corporate)'][0]],
        'A': ['percent', InputsSolvenciaII['Asset by rating: A (State)'][0], InputsSolvenciaII['Asset by rating: A (Corporate)'][0]],
        'BBB': ['percent', InputsSolvenciaII['Asset by rating: BBB (State)'][0], InputsSolvenciaII['Asset by rating: BBB (Corporate)'][0]],
        'BB': ['percent', InputsSolvenciaII['Asset by rating: BB (State)'][0], InputsSolvenciaII['Asset by rating: BB (Corporate)'][0]],
        'B': ['percent', InputsSolvenciaII['Asset by rating: B (State)'][0], InputsSolvenciaII['Asset by rating: B (Corporate)'][0]],
        'CCC or lower': ['percent', InputsSolvenciaII['Asset by rating: CCC or lower (State)'][0], InputsSolvenciaII['Asset by rating: CCC or lower (Corporate)'][0]],
        'Unrated': ['percent', InputsSolvenciaII['Asset by rating: Unrated (Corporate)'][0], InputsSolvenciaII['Asset by rating: Unrated (Corporate)'][0]],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------RiskPremiumRepartition1Table
    # ---------------------------------------------------------------------------------------------------- #

    # -- Precalculo de variables RiskPremiumRepartition1 #
    suma1 = (InputsSolvenciaII['Healt non SLT ACC Accidental death'][0] +
             InputsSolvenciaII['Healt non SLT ACC Hospitalization'][0] +
             InputsSolvenciaII['Healt non SLT ACC Others'][0] +
             InputsSolvenciaII['Healt non SLT ACC TPD'][0] +
             InputsSolvenciaII['Healt non SLT Sick Hospitalization'][0] +
             InputsSolvenciaII['Healt non SLT Sick Others'][0] +
             InputsSolvenciaII['Healt non SLT Sick TPD'][0] +
             InputsSolvenciaII['Health SLT Hospitalization'][0] +
             InputsSolvenciaII['Health SLT TD'][0] +
             InputsSolvenciaII['Health SLT TPD'][0]
             )
    suma2 = (InputsSolvenciaII['Health SLT TPD'][0] +
             InputsSolvenciaII['Healt non SLT Sick TPD'][0] +
             InputsSolvenciaII['Healt non SLT ACC TPD'][0]
             )
    suma3 = (InputsSolvenciaII['Health SLT Hospitalization'][0] +
             InputsSolvenciaII['Healt non SLT Sick Hospitalization'][0] +
             InputsSolvenciaII['Healt non SLT ACC Hospitalization'][0]
             )
    try:
        LifeRepartitionDeath = InputsSolvenciaII['Life Others'][0] / (InputsSolvenciaII['Life Others'][0] + InputsSolvenciaII['Life TPD'][0])
    except ZeroDivisionError:
        LifeRepartitionDeath = 0
    try:
        LifeRepartitionTPD = InputsSolvenciaII['Life TPD'][0] / (InputsSolvenciaII['Life Others'][0] + InputsSolvenciaII['Life TPD'][0])
    except ZeroDivisionError:
        LifeRepartitionTPD = 0
    try:
        HealthRepartitionSLTYNonSLTTD = InputsSolvenciaII['Health SLT TD'][0] / suma1
    except ZeroDivisionError:
        HealthRepartitionSLTYNonSLTTD = 0
    try:
        HealthRepartitionSLTYNonSLTTPD = suma2 / suma1
    except ZeroDivisionError:
        HealthRepartitionSLTYNonSLTTPD = 0
    try:
        HealthRepartitionSLTYNonSLAccidentalDeath = InputsSolvenciaII['Healt non SLT ACC Accidental death'][0] / suma1
    except ZeroDivisionError:
        HealthRepartitionSLTYNonSLAccidentalDeath = 0
    try:
        HealthRepartitionSLTYNonSLTHospitalization = suma3 / suma1
    except ZeroDivisionError:
        HealthRepartitionSLTYNonSLTHospitalization = 0
    try:
        Motor = InputsSolvenciaII['Non Life Misc. Motor'][0] / (InputsSolvenciaII['Non Life Misc. Motor'][0] + InputsSolvenciaII['Non Life Misc. Others'][0])
    except ZeroDivisionError:
        Motor = 0
    try:
        MiscNonSubjectToCat = InputsSolvenciaII['Non Life Misc. Others'][0] / (InputsSolvenciaII['Non Life Misc. Motor'][0] + InputsSolvenciaII['Non Life Misc. Others'][0])
    except ZeroDivisionError:
        MiscNonSubjectToCat = 0

    suma4 = (HealthRepartitionSLTYNonSLTTD +
             HealthRepartitionSLTYNonSLTTPD +
             HealthRepartitionSLTYNonSLAccidentalDeath +
             HealthRepartitionSLTYNonSLTHospitalization
             )

    RiskPremiumRepartition1Table = pd.DataFrame({
        #'Risk premium repartition ': ['title', ''],
        'Life repartition: Death': ['percent', LifeRepartitionDeath],
        'Life repartition: TPD': ['percent', LifeRepartitionTPD],
        'Health repartition (SLT & Non SLT): TD': ['percent', HealthRepartitionSLTYNonSLTTD],
        'Health repartition (SLT & Non SLT): TPD': ['percent', HealthRepartitionSLTYNonSLTTPD],
        'Health repartition (SLT & Non SLT): Accidental  Death': ['percent', HealthRepartitionSLTYNonSLAccidentalDeath],
        'Health repartition (SLT & Non SLT): Hospitalization': ['percent', HealthRepartitionSLTYNonSLTHospitalization],
        'Health repartition (SLT & Non SLT): Other health': ['percent', (1 - suma4)],
        '"Motor"': ['percent', Motor],
        '"Fire & Other damage"': ['percent', 0],
        '"Misc." Subject to Cat': ['percent', 0],
        '"Misc." Non subject to Cat': ['percent', MiscNonSubjectToCat],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------ExposedAmountTable
    # ---------------------------------------------------------------------------------------------------- #

    ExposedAmountTable = pd.DataFrame({
        #'Exposed Amount': ['title', ''],
        'Initial stock of policies': ['percent', Inputs['Stock inicial'][0]],
        'Monthly number of new policies on a cruse-speed basis': OutPut['nuevos'][int(Inputs['Se alcanza la penetración en No. Meses'][0]) - 1],
        'Average policy duration': ['text', Inputs['Persistencia'][0]],
        'Average monthly premium excluding commission': ['percent', 0],  # -- PENDIENTE -- #
        'Confidence in technical basis quality': ['percent', InputsSolvenciaII['Confidence in technical basis quality'][0]],
        'Confidence in information quality': ['percent', InputsSolvenciaII['Confidence in information quality'][0]],
        'Upfront Payment': ['percent', InputsSolvenciaII['Upfront Payment'][0]],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------LossRatiosPTLR
    # ---------------------------------------------------------------------------------------------------- #

    Loss_ratio = 0.95  # -- PENDIENTE DE DEFINIR -- #
    sumaProducto1 = (InputsSolvenciaII['Life Others'][0] * Loss_ratio) + (InputsSolvenciaII['Life TPD'][0] * Loss_ratio)
    suma1 = InputsSolvenciaII['Life Others'][0] + InputsSolvenciaII['Life TPD'][0]
    sumaProducto2 = (InputsSolvenciaII['Health SLT Hospitalization'][0] * Loss_ratio) + (InputsSolvenciaII['Health SLT TD'][0] * Loss_ratio) + (InputsSolvenciaII['Health SLT TPD'][0] * Loss_ratio)
    suma2 = InputsSolvenciaII['Health SLT Hospitalization'][0] + InputsSolvenciaII['Health SLT TD'][0] + InputsSolvenciaII['Health SLT TPD'][0]
    sumaProducto3 = (InputsSolvenciaII['Healt non SLT ACC Accidental death'][0] * Loss_ratio) + \
                    (InputsSolvenciaII['Healt non SLT ACC Hospitalization'][0] * Loss_ratio) + \
                    (InputsSolvenciaII['Healt non SLT ACC Others'][0] * Loss_ratio) + \
                    (InputsSolvenciaII['Healt non SLT ACC TPD'][0] * Loss_ratio)
    suma3 = InputsSolvenciaII['Healt non SLT ACC Accidental death'][0] + \
            InputsSolvenciaII['Healt non SLT ACC Hospitalization'][0] + \
            InputsSolvenciaII['Healt non SLT ACC Others'][0] + \
            InputsSolvenciaII['Healt non SLT ACC TPD'][0]
    sumaProducto4 = (InputsSolvenciaII['Healt non SLT Sick Hospitalization'][0] * Loss_ratio) + \
                    (InputsSolvenciaII['Healt non SLT Sick Others'][0] * Loss_ratio) + \
                    (InputsSolvenciaII['Healt non SLT Sick TPD'][0] * Loss_ratio)
    suma4 = InputsSolvenciaII['Healt non SLT Sick Hospitalization'][0] + \
            InputsSolvenciaII['Healt non SLT Sick Others'][0] + \
            InputsSolvenciaII['Healt non SLT Sick TPD'][0]
    sumaProducto5 = (InputsSolvenciaII['Non Life Misc. Motor'][0] * Loss_ratio) + (InputsSolvenciaII['Non Life Misc. Others'][0] * Loss_ratio)
    suma5 = InputsSolvenciaII['Non Life Misc. Motor'][0] + InputsSolvenciaII['Non Life Misc. Others'][0]

    try:
        Life = sumaProducto1 / suma1
    except ZeroDivisionError:
        Life = 0
    try:
        HealthSLT = sumaProducto2 / suma2
    except ZeroDivisionError:
        HealthSLT = 0
    try:
        HealthNonSLTIncProt = sumaProducto3 / suma3
    except ZeroDivisionError:
        HealthNonSLTIncProt = 0
    try:
        HealthNonSLTMedex = sumaProducto4 / suma4
    except ZeroDivisionError:
        HealthNonSLTMedex = 0
    try:
        OtherNonLife = sumaProducto5
    except ZeroDivisionError:
        OtherNonLife = 0

    LossRatiosPTLRTable = pd.DataFrame({
        #'Loss Ratios (PTLR) ': ['title', ''],
        'LR_Life': ['percent', Life],
        'LR_Health SLT': ['percent', HealthSLT],
        'LR_Health Non SLT - IncProt': ['percent', HealthNonSLTIncProt],
        'LR_Health Non SLT - Medex': ['percent', HealthNonSLTMedex],
        'LR_Other Non Life': ['percent', OtherNonLife],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------LossRatiosPTLR
    # ---------------------------------------------------------------------------------------------------- #

    ClaimManagementOverheadsTable = pd.DataFrame({
        #'Claim management overheads': ['title', ''],
        'CMO_Life': ['', 0],
        'CMO_Health SLT': ['', 0],
        'CMO_Health Non SLT - IncProt': ['', 0],
        'CMO_Health Non SLT - Medex': ['', 0],
        'CMO_Other Non Life': ['', 0],
        '': '',
        ' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------ExclusionPeriodTable
    # ---------------------------------------------------------------------------------------------------- #

    ExclusionPeriodTable = pd.DataFrame({
        'Exclusion Period': ['title', InputsSolvenciaII['Exclusion Period'][0]],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------TopKapiTable
    # ---------------------------------------------------------------------------------------------------- #

    TopKapiTable = pd.DataFrame({
        #'Topkapi': ['title', ''],
        'CPI Mortgage / Death, TD, TPD, Health': ['percent', InputsSolvenciaII['CPI Mortgage / Death, TD, TPD, Health'][0]],
        'CPI Mortgage / IU & Other': ['percent', InputsSolvenciaII['CPI Mortgage / IU & Other'][0]],
        'CPI Non-Mortgage / Death, TD, TPD, Health': ['percent', InputsSolvenciaII['CPI Non-Mortgage / Death, TD, TPD, Health'][0]],
        'CPI Non-Mortgage / IU & Other': ['percent', InputsSolvenciaII['CPI Non-Mortgage / IU & Other'][0]],
        'Goods Protection / EW, GAP, Home, Motor': ['percent', InputsSolvenciaII['Goods Protection / EW, GAP, Home, Motor'][0]],
        'Other': ['percent', InputsSolvenciaII['Other'][0]],
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # -----------------------------------HealtTable
    # ---------------------------------------------------------------------------------------------------- #

    HealtTable = pd.DataFrame({
        'Healt': ['title', ''],
        'Healt non SLT ACC Accidental death': ['percent', InputsSolvenciaII['Healt non SLT ACC Accidental death'][0]],
        'Healt non SLT ACC Hospitalization': ['percent', InputsSolvenciaII['Healt non SLT ACC Hospitalization'][0]],
        'Healt non SLT ACC Others': ['percent', InputsSolvenciaII['Healt non SLT ACC Others'][0]],
        'Healt non SLT ACC TPD': ['percent', InputsSolvenciaII['Healt non SLT ACC TPD'][0]],
        'Healt non SLT Sick Hospitalization': ['percent', InputsSolvenciaII['Healt non SLT Sick Hospitalization'][0]],
        'Healt non SLT Sick Others': ['percent', InputsSolvenciaII['Healt non SLT Sick Others'][0]],
        'Healt non SLT Sick TPD': ['percent', InputsSolvenciaII['Healt non SLT Sick TPD'][0]],
        'Health SLT Hospitalization': ['percent', InputsSolvenciaII['Health SLT Hospitalization'][0]],
        'Health SLT TD': ['percent', InputsSolvenciaII['Health SLT TD'][0]],
        'Health SLT TPD': ['percent', InputsSolvenciaII['Health SLT TPD'][0]],
        'Life Others': ['percent', InputsSolvenciaII['Life Others'][0]],
        'Life TPD': ['percent', InputsSolvenciaII['Life TPD'][0]],
        'Non Life Misc. Motor': ['percent', InputsSolvenciaII['Non Life Misc. Motor'][0]],
        'Non Life Misc. Others': ['percent', InputsSolvenciaII['Non Life Misc. Others'][0]],
        '': '',
        ' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # --------------------------------------ProductionYProductTable
    # ---------------------------------------------------------------------------------------------------- #
    NewProductionVolume = OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'] == 'nuevos']
    NewProductionVolume = NewProductionVolume.drop(columns=['Producto', 'item'])

    TotalDeathBenefitEndOfYear = OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'] == 'Sum at risk Life']
    TotalDeathBenefitEndOfYear = TotalDeathBenefitEndOfYear.drop(columns=['Producto', 'item'])

    itemsProductionYProduct = ['title']
    itemsNumberOfNewContracts = ['price']
    itemsTotalDeathBenefitEndOfYear = ['price']

    for index, row in NewProductionVolume.T.iterrows():
        itemsProductionYProduct.append(index)
        itemsNumberOfNewContracts.append(row[1])

    for index, row in TotalDeathBenefitEndOfYear.T.iterrows():
        itemsTotalDeathBenefitEndOfYear.append(row[1])

    ProductionYProductTable = pd.DataFrame({
        #'Production & Product': itemsProductionYProduct,
        'Number of new contracts': itemsNumberOfNewContracts,
        'Total Death benefit - end of year': itemsTotalDeathBenefitEndOfYear,
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # ------------------------------------------PremiumDataTable
    # ---------------------------------------------------------------------------------------------------- #

    WrittenPremiumNetOfTax = OutPut_productsBP_anual.loc[OutPut_productsBP_anual['item'] == 'GWP']
    WrittenPremiumNetOfTax = WrittenPremiumNetOfTax.drop(columns=['Producto', 'item'])

    itemsPremiumData = ['title']
    itemsWrittenPremiumNetOfTax = ['price']
    itemsPD_Life = ['price']
    itemsPD_HealthSLT = ['price']
    itemsPD_HealthNonSLTIncProt = ['price']
    itemsPD_HealthNonSLTMedex = ['price']
    itemsPD_OtherNonLife = ['price']

    for index, row in WrittenPremiumNetOfTax.T.iterrows():
        itemsPremiumData.append(index)
        itemsWrittenPremiumNetOfTax.append(row[1])
        itemsPD_Life.append(row[1] * RPR_Life)
        itemsPD_HealthSLT.append(row[1] * RPR_Health_SLT)
        itemsPD_HealthNonSLTIncProt.append(row[1] * RPR_Health_Non_SLT_IncProt)
        itemsPD_HealthNonSLTMedex.append(row[1] * RPR_Health_Non_SLT_Medex)
        itemsPD_OtherNonLife.append(row[1] * RPR_Other_Non_Life)

    PremiumDataTable = pd.DataFrame({
        #'Premium Data': itemsPremiumData,
        #'Written Premium Net of Tax': itemsWrittenPremiumNetOfTax,
        'PD_Life': itemsPD_Life,
        'PD_Health SLT': itemsPD_HealthSLT,
        'PD_Health Non SLT - IncProt': itemsPD_HealthNonSLTIncProt,
        'PD_Health Non SLT - Medex': itemsPD_HealthNonSLTMedex,
        'PD_Other Non Life': itemsPD_OtherNonLife,
        #'Written Premium Net of Tax': itemsWrittenPremiumNetOfTax,
        #'': '',
        #' ': ''
    })

    # ---------------------------------------------------------------------------------------------------- #
    # ------------------------------------------Unificar tablas
    # ---------------------------------------------------------------------------------------------------- #

    InputsInputsSolvenciaII = {
        'GlobalTable': GlobalTable,
        'ProductTable': ProductTable,
        'AssetByRatingTable': AssetByRatingTable,
        'RiskPremiumRepartition1Table': RiskPremiumRepartition1Table,
        'ExposedAmountTable': ExposedAmountTable,
        'LossRatiosPTLRTable': LossRatiosPTLRTable,
        'ClaimManagementOverheadsTable': ClaimManagementOverheadsTable,
        'RiskPremiumRepartitionTable': RiskPremiumRepartitionTable,
        'ExclusionPeriodTable': ExclusionPeriodTable,
        'TopKapiTable': TopKapiTable,
        'HealtTable': HealtTable,
        'ProductionYProductTable': ProductionYProductTable,
        'PremiumDataTable': PremiumDataTable,
        '': '',
        ' ': ''
    }

    return InputsInputsSolvenciaII
