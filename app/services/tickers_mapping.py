# app/services/tickers_mapping.py

# =========================================================
# Central ticker → display name mappings
# Used across pages (Stocks, FX, Commodities, ETFs, etc.)
# =========================================================



# -------------------------
# Stocks Tickers Mapping
# -------------------------
# Responsibility: Provide a flat dictionary of stock tickers.
# Keys are "CompanyName_COUNTRYCODE" where COUNTRYCODE is
# ISO 3166‑1 alpha‑2 (two‑letter country code).
# Values are Yahoo Finance ticker symbols.
# -------------------------

# -------------------------
# Stocks Tickers Mapping
# -------------------------
# Responsibility: Provide a flat dictionary of stock tickers.
# Keys are "CompanyName_COUNTRYCODE" where COUNTRYCODE is
# ISO 3166‑1 alpha‑2 (two‑letter country code).
# Values are Yahoo Finance ticker symbols.
# -------------------------

STOCK_TICKERS = {
    # ------ USA ------
    # SP500 members (partial list for brevity)
    "Apple_US": "AAPL",
    "Microsoft_US": "MSFT",
    "Amazon_US": "AMZN",
    "Tesla_US": "TSLA",
    "Meta_US": "META",
    "Nvidia_US": "NVDA",
    "Alphabet_US": "GOOGL",
    "Johnson&Johnson_US": "JNJ",
    "JPMorganChase_US": "JPM",
    "Visa_US": "V",
    "Walmart_US": "WMT",
    "Procter&Gamble_US": "PG",
    "UnitedHealth_US": "UNH",
    "HomeDepot_US": "HD",
    "Mastercard_US": "MA",
    "BankofAmerica_US": "BAC",
    "Disney_US": "DIS",
    "PayPal_US": "PYPL",
    "Adobe_US": "ADBE",
    "Netflix_US": "NFLX",
    "CocaCola_US": "KO",
    "PepsiCo_US": "PEP",
    "Intel_US": "INTC",
    "Verizon_US": "VZ",
    "AT&T_US": "T",
    "Pfizer_US": "PFE",
    "Merck_US": "MRK",
    "Chevron_US": "CVX",
    "ExxonMobil_US": "XOM",
    "AbbVie_US": "ABBV",
    "Cisco_US": "CSCO",
    "Nike_US": "NKE",
    "McDonalds_US": "MCD",
    "WellsFargo_US": "WFC",
    "Citigroup_US": "C",
    "Boeing_US": "BA",
    "3M_US": "MMM",
    "GoldmanSachs_US": "GS",
    "MorganStanley_US": "MS",
    "AmericanExpress_US": "AXP",
    "IBM_US": "IBM",
    "Caterpillar_US": "CAT",
    "Honeywell_US": "HON",
    "LockheedMartin_US": "LMT",
    "GeneralElectric_US": "GE",
    "Ford_US": "F",
    "GeneralMotors_US": "GM",
    "Starbucks_US": "SBUX",
    "Costco_US": "COST",
    "CVSHealth_US": "CVS",
    "Target_US": "TGT",
    "TJXCompanies_US": "TJX",
    "DeltaAirLines_US": "DAL",
    "AmericanAirlines_US": "AAL",
    "Uber_US": "UBER",
    "Lyft_US": "LYFT",
    "ZoomVideo_US": "ZM",
    "Salesforce_US": "CRM",
    "Twitter_US": "TWTR",
    "eBay_US": "EBAY",
    "Qualcomm_US": "QCOM",
    "TexasInstruments_US": "TXN",
    "Broadcom_US": "AVGO",
    "AMD_US": "AMD",
    "Starbucks_US": "SBUX",
    "GoldmanSachs_US": "GS",
    "MorganStanley_US": "MS",
    "Oracle_US": "ORCL",
    "Palantir_US": "PLTR",
    "Snowflake_US": "SNOW",
    "CrowdStrike_US": "CRWD",
    "DocuSign_US": "DOCU",
    "Pinterest_US": "PINS",
    "Snap_US": "SNAP",
    "Roku_US": "ROKU",
    "Moderna_US": "MRNA",
    "ZoomInfo_US": "ZI",
    "Twilio_US": "TWLO",
    "Workday_US": "WDAY",
    "Okta_US": "OKTA",
    "Zscaler_US": "ZS",
    "Datadog_US": "DDOG",
    "FidelityNationalInformationServices_US": "FIS",
    "eTradeFinancial_US": "ETFC",
    "MarriottInternational_US": "MAR",
    "HiltonWorldwideHoldings_US": "HLT",
    "BookingHoldings_US": "BKNG",
    "ExpediaGroup_US": "EXPE",
    "Carnival_US": "CCL",
    "RoyalCaribbeanCruises_US": "RCL",
    "NorwegianCruiseLineHoldings_US": "NCLH",
    "BlackRock_US": "BLK",
    "CharlesSchwab_US": "SCHW",
    "FidelityNationalInformationServices_US": "FIS",
    


    # ------ Europe ------
    # Swiss Market Index members
    "Nestle_CH": "NESN.SW",
    "Roche_CH": "ROG.SW",
    "Novartis_CH": "NOVN.SW",
    "UBSGroup_CH": "UBSG.SW",
    "CreditSuisse_CH": "CSGN.SW",
    "ZurichInsuranceGroup_CH": "ZURN.SW",
    "SwissRe_CH": "SREN.SW",
    "ABB_CH": "ABBN.SW",
    "Glencore_CH": "GLEN.SW",
    "LonzaGroup_CH": "LONN.SW",
    "Swisscom_CH": "SCMN.SW",
    "Givaudan_CH": "GIVN.SW",
    "Sika_CH": "SIKA.SW",
    "Geberit_CH": "GEBN.SW",
    "Richemont_CH": "CFR.SW",
    "Clariant_CH": "CLN.SW",
    "SwatchGroup_CH": "UHR.SW",
    "Logitech_CH": "LOGN.SW",
    "SwissLife_CH": "SLHN.SW",
    "PartnersGroup_CH": "PGHN.SW",
    "Alcon_CH": "ALC.SW",
    "ViforPharma_CH": "VIFN.SW",
    "Sartorius_CH": "SART.SW",
    "Temenos_CH": "TEMN.SW",
    "AMS_CH": "AMS.SW",
    "Sonova_CH": "SOON.SW",
    "BaloiseHolding_CH": "BALN.SW",
    "JuliusBaerGroup_CH": "BAER.SW",
    "Schindler_CH": "SCHP.SW",
    "Straumann_CH": "STMN.SW",
    "SwissPrime_CH": "SPHN.SW",
    "Helvetia_CH": "HELN.SW",
    "OCB_CH": "OCBN.SW",
    "SFSGroup_CH": "SFSN.SW",
    "Kuehne+Nagel_CH": "KNIN.SW",
    "Dufry_CH": "DUFN.SW",
    "Galenco_CH": "GALE.SW",
    "VATGroup_CH": "VATN.SW",
    "BucherIndustries_CH": "BUCN.SW",
    "MobimoHoldings_CH": "MOBN.SW",
    "GeorgFischer_CH": "GEFN.SW",

    # DAX members
    "Siemens_DE": "SIE.DE",
    "Volkswagen_DE": "VOW3.DE",
    "Allianz_DE": "ALV.DE",
    "BASF_DE": "BAS.DE",
    "DeutscheBank_DE": "DBK.DE",
    "Bayer_DE": "BAYN.DE",
    "Adidas_DE": "ADS.DE",
    "Daimler_DE": "DAI.DE",
    "SAP_DE": "SAP.DE",
    "BMW_DE": "BMW.DE",
    "Linde_DE": "LIN.DE",
    "Henkel_DE": "HEN3.DE",
    "Infineon_DE": "IFX.DE",
    "Continental_DE": "CON.DE",
    "Merck_DE": "MRK.DE",
    "DeutscheTelekom_DE": "DTE.DE",
    "Fresenius_DE": "FRE.DE",
    "Vonovia_DE": "VNA.DE",
    "E.ON_DE": "EOAN.DE",
    "RWE_DE": "RWE.DE",
    "Beiersdorf_DE": "BEI.DE",
    "Covestro_DE": "1COV.DE",
    "MTU_AeroEngines_DE": "MTX.DE",
    "PorscheAutomobilHolding_DE": "PAH3.DE",
    "Zalando_DE": "ZAL.DE",
    "HelloFresh_DE": "HFG.DE",
    "SiemensHealthineers_DE": "SHL.DE",
    "DeutschePost_DE": "DPW.DE",
    "DeutscheLufthansa_DE": "LHA.DE",
    "Symrise_DE": "SY1.DE",
    "Qiagen_DE": "QIA.DE",
    "Knorr-Bremse_DE": "KBX.DE",
    "FreseniusMedicalCare_DE": "FME.DE",
    "Wirecard_DE": "WDI.DE",
    "MercedesBenz_DE": "MBG.DE",
    "Puma_DE": "PUM.DE",
    "HugoBoss_DE": "BOSS.DE",
    "EvonikIndustries_DE": "EVK.DE",
    "DeutscheBörse_DE": "DB1.DE",
    "Porsche_DE": "P911.DE",
   

    # UK FTSE 100 members
    "AstraZeneca_GB": "AZN.L",
    "Unilever_GB": "ULVR.L",
    "BP_GB": "BP.L",
    "HSBC_GB": "HSBA.L",
    "GlaxoSmithKline_GB": "GSK.L",
    "Diageo_GB": "DGE.L",
    "BritishAmericanTobacco_GB": "BATS.L",
    "RioTinto_GB": "RIO.L",
    "Barclays_GB": "BARC.L",
    "LloydsBankingGroup_GB": "LLOY.L",
    "Prudential_GB": "PRU.L",
    "BTGroup_GB": "BT.A.L",
    "Aviva_GB": "AV.L",
    "Tesco_GB": "TSCO.L",
    "Glencore_GB": "GLEN.L",
    "StandardChartered_GB": "STAN.L",
    "RollsRoyce_GB": "RR.L",
    "NationalGrid_GB": "NG.L",
    "SSE_GB": "SSE.L",
    "CompassGroup_GB": "CPG.L",
    "Smith&Nephew_GB": "SN.L",
    "Experian_GB": "EXPN.L",
    "Shell_GB": "SHEL.L",
    "InterContinentalHotels_GB": "IHG.L",
    "BAESystems_GB": "BA.L",
    "WPP_GB": "WPP.L",
    "ImperialBrands_GB": "IMB.L",
    "Centrica_GB": "CNA.L",
    "AshteadGroup_GB": "AHT.L",
    "Meggitt_GB": "MGGT.L",
    "Persimmon_GB": "PSN.L",
    "BarrattDevelopments_GB": "BDEV.L",
    "TaylorWimpey_GB": "TW.L",
    "Kingfisher_GB": "KGF.L",

    # CAC 40 members
    "AirLiquide_FR": "AI.PA",
    "Airbus_FR": "AIR.PA",
    "Alstom_FR": "ALO.PA",
    "ArcelorMittal_FR": "MT.AS",
    "AXA_FR": "CS.PA",
    "BNPParibas_FR": "BNP.PA",
    "Bouygues_FR": "EN.PA",
    "Capgemini_FR": "CAP.PA",
    "Carrefour_FR": "CA.PA",
    "CréditAgricole_FR": "ACA.PA",
    "Danone_FR": "BN.PA",
    "DassaultSystèmes_FR": "DSY.PA",
    "Engie_FR": "ENGI.PA",
    "EssilorLuxottica_FR": "EL.PA",
    "EurofinsScientific_FR": "ERF.PA",
    "Hermès_FR": "RMS.PA",
    "Kering_FR": "KER.PA",
    "Legrand_FR": "LR.PA",
    "LOréal_FR": "OR.PA",
    "LVMH_FR": "MC.PA",
    "Michelin_FR": "ML.PA",
    "Orange_FR": "ORA.PA",
    "PernodRicard_FR": "RI.PA",
    "Publicis_FR": "PUB.PA",
    "Renault_FR": "RNO.PA",
    "Safran_FR": "SAF.PA",
    "SaintGobain_FR": "SGO.PA",
    "Sanofi_FR": "SAN.PA",
    "SchneiderElectric_FR": "SU.PA",
    "SociétéGénérale_FR": "GLE.PA",
    "STMicroelectronics_FR": "STMPA.PA",
    "Teleperformance_FR": "TEP.PA",
    "Thales_FR": "HO.PA",
    "TotalEnergies_FR": "TTE.PA",
    "UnibailRodamcoWestfield_FR": "URW.PA",
    "Veolia_FR": "VIE.PA",
    "Vinci_FR": "DG.PA",
    "Vivendi_FR": "VIV.PA",
    "Worldline_FR": "WLN.PA",


    #Italy (FTSE MIB members)
    "Eni_IT": "ENI.MI",
    "IntesaSanpaolo_IT": "ISP.MI",
    "UniCredit_IT": "UCG.MI",
    "Generali_IT": "G.MI",
    "Ferrari_IT": "RACE.MI",
    "FiatChrysler_IT": "FCA.MI",
    "TelecomItalia_IT": "TIT.MI",
    "Enel_IT": "ENEL.MI",


    # ------ China (Mainland & Hong Kong) ------
    # Tech & E-commerce (The "Big Three")
    "Alibaba_CN": "BABA",         # E-commerce Giant (NYSE ADR)
    "Tencent_CN": "TCEHY",        # Gaming/Social Media (OTC ADR)
    "JD.com_CN": "JD",            # Retail/E-commerce (Nasdaq ADR)
    
    # Growth & AI
    "Baidu_CN": "BIDU",           # Search/AI (Nasdaq ADR)
    "Pinduoduo_CN": "PDD",        # High-growth E-commerce (Nasdaq ADR)
    "Meituan_HK": "3690.HK",      # Delivery/Services (HK Exchange)
    "NetEase_CN": "NTES",         # Gaming (Nasdaq ADR)
    
    # Electric Vehicles (The "Tesla Competitors")
    "BYD_Company_HK": "1211.HK",  # World's largest EV maker (HK Exchange)
    "Li_Auto_CN": "LI",           # EV Manufacturer (Nasdaq ADR)
    "NIO_CN": "NIO",              # EV Manufacturer (NYSE ADR)
    "XPeng_CN": "XPEV",           # EV Manufacturer (NYSE ADR)
    
    # Financials & Insurance
    "ICBC_HK": "1398.HK",         # World's largest bank by assets (HK Exchange)
    "China_Const_Bank_HK": "0939.HK", # Banking (HK Exchange)
    "Ping_An_Insurance_HK": "2318.HK",# Insurance/Fintech (HK Exchange)
    "Bank_of_China_HK": "3988.HK", # Banking (HK Exchange)
    
    # Energy & Industrials
    "PetroChina_SS": "601857.SS", # Energy (Shanghai Exchange)
    "China_Life_HK": "2628.HK",   # Insurance (HK Exchange)
    "CNOOC_HK": "0883.HK",        # Offshore Oil/Gas (HK Exchange)
    
    # Consumer & Semiconductors
    "Xiaomi_HK": "1810.HK",       # Consumer Electronics (HK Exchange)
    "SMIC_HK": "0981.HK",         # Largest Chinese Chipmaker (HK Exchange)
    "Kweichow_Moutai_SS": "600519.SS", # Luxury Liquor (Heavy weighting in A-shares)

    # ------ Japan ------
    # (Nikkei 225 Leaders)
    "Toyota_JP": "7203.T",        # Automotive Leader
    "Sony_Group_JP": "6758.T",    # Tech/Entertainment
    "SoftBank_Group_JP": "9984.T",# Tech Investment (Fixed Ticker)
    "Keyence_JP": "6861.T",       # Automation/Electronics
    "Tokyo_Electron_JP": "8035.T",# Semiconductors
    "Mitsubishi_UFJ_JP": "8306.T",# Largest Bank
    "Nintendo_JP": "7974.T",      # Gaming
    "Fast_Retailing_JP": "9983.T",# Retail (Uniqlo) - Heavy Nikkei weighting
    "Shin-Etsu_Chem_JP": "4063.T",# Semiconductor Materials
    "Nippon_Steel_JP": "5401.T",  # Steel/Industrials
    "Honda_Motor_JP": "7267.T",   # Automotive
    "Mitsubishi_Corp_JP": "8058.T",# Trading House (Warren Buffett play)
    "Itochu_JP": "8001.T",        # Trading House
    "Mitsui_&_Co_JP": "8031.T",   # Trading House
    "Takeda_Pharm_JP": "4502.T",  # Healthcare
    "Daikin_JP": "6367.T",        # Industrials/AC
    "Fanuc_JP": "6954.T",         # Robotics
    "Recruit_Holdings_JP": "6098.T", # Services/HR
    "Hitachi_JP": "6501.T",       # Conglomerate
    "Mizuho_Financial_JP": "8411.T", # Banking
    "Sumitomo_Mitsui_JP": "8316.T", # Banking
    "Oriental_Land_JP": "4661.T", # Leisure (Tokyo Disney)
    "Seven_&_i_JP": "3382.T",    # Retail (7-Eleven)
    "Denso_JP": "6902.T",         # Auto Parts
    "Bridgestone_JP": "5108.T",   # Rubber/Auto
            



    # ------ Americas (non‑US) ------
    "Shopify_CA": "SHOP.TO",
    "Vale_BR": "VALE",
    "Petrobras_BR": "PBR",
    "GrupoBimbo_MX": "BIMBOA.MX",

    # ------ Asia (non China/Japan) ------
    "SamsungElectronics_KR": "005930.KQ",
    "HyundaiMotor_KR": "005380.KQ",
    "TataConsultancy_IN": "TCS.NS",
    "RelianceIndustries_IN": "RELIANCE.NS",
    "TataMotors_IN": "TMPV.NS",
    "TSMC_TW": "2330.TW",

    # ------ Emerging ------
    "Lukoil_RU": "LKOH.ME",
    #"Gazprom_RU": "OGZPY", # Delisted
    "Naspers_ZA": "NPSNY",
    "SaudiAramco_SA": "2222.SR",
}


COUNTRY_TO_REGION = {
    'US': 'Americas',
    'CA': 'Americas',
    'MX': 'Americas',
    'BR': 'Americas',
    'AR': 'Americas',
    'DE': 'Europe',
    'FR': 'Europe',
    'GB': 'Europe',
    'IT': 'Europe',
    'NL': 'Europe',
    'CH': 'Europe',
    'ES': 'Europe',
    'SE': 'Europe',
    'NO': 'Europe',
    'DK': 'Europe',
    'FI': 'Europe',
    'AT': 'Europe',
    'BE': 'Europe',
    'PT': 'Europe',
    'IE': 'Europe',
    'JP': 'Asia',
    'HK': 'Asia',
    'KR': 'Asia',
    'IN': 'Asia',
    'AU': 'Asia',
    'CN': 'Asia',
    'TW': 'Asia',
    'SG': 'Asia',
    'MY': 'Asia',
    'TH': 'Asia',
    'ID': 'Asia',
    'PH': 'Asia',
}

SYMBOLES = {'USD': '$', 
            'EUR': '€', 
            'GBP': '£', 
            'JPY': '¥', 
            'KRW': '₩', 
            'CHF': 'CHF', 
            'MXN': '$', 
            'BRL': 'R$', 
            'INR': '₹', 
            'TWD': 'NT$', 
            'ZAR': 'R', 
            'SAR': '﷼', 
            'RUB': '₽', 
            'CNY': '¥', 
            'HKD': 'HK$'}

# -------------------------
# Stock Groups (indexes/exchanges)
# -------------------------
# Responsibility: Provide groupings of STOCK_TICKERS by index/exchange.
# Keys are index names, values are lists of STOCK_TICKERS keys.
# -------------------------

STOCK_GROUPS = {
    "CAC40": [
        "AirLiquide_FR", "Airbus_FR", "Alstom_FR", "ArcelorMittal_FR", "AXA_FR",
        "BNPParibas_FR", "Bouygues_FR", "Capgemini_FR", "Carrefour_FR", "CréditAgricole_FR",
        "Danone_FR", "DassaultSystèmes_FR", "Engie_FR", "EssilorLuxottica_FR", "EurofinsScientific_FR",
        "Hermès_FR", "Kering_FR", "Legrand_FR", "LOréal_FR", "LVMH_FR",
        "Michelin_FR", "Orange_FR", "PernodRicard_FR", "Publicis_FR", "Renault_FR",
        "Safran_FR", "SaintGobain_FR", "Sanofi_FR", "SchneiderElectric_FR", "SociétéGénérale_FR",
        "STMicroelectronics_FR", "Teleperformance_FR", "Thales_FR", "TotalEnergies_FR",
        "UnibailRodamcoWestfield_FR", "Veolia_FR", "Vinci_FR", "Vivendi_FR", "Worldline_FR",
    ],
    "SP500": [
        "Apple_US", "Microsoft_US", "Amazon_US", "Tesla_US", "Meta_US",
        "Nvidia_US", "Alphabet_US", "Johnson&Johnson_US",
        "JPMorganChase_US", "Visa_US", "Walmart_US", "Procter&Gamble_US", "UnitedHealth_US", "HomeDepot_US", 
        "Mastercard_US", "BankofAmerica_US", "Disney_US", "PayPal_US", "Adobe_US", "Netflix_US",
        "CocaCola_US", "PepsiCo_US", "Intel_US", "Verizon_US", "AT&T_US", "Pfizer_US", "Merck_US",
        "Chevron_US", "ExxonMobil_US", "AbbVie_US", "Cisco_US", "Nike_US", "McDonalds_US",
        "WellsFargo_US", "Citigroup_US", "Boeing_US", "3M_US", "GoldmanSachs_US", "MorganStanley_US",
        "AmericanExpress_US", "IBM_US", "Caterpillar_US", "Honeywell_US", "LockheedMartin_US",
        "GeneralElectric_US", "Ford_US", "GeneralMotors_US", "Starbucks_US", "Costco_US",
        "CVSHealth_US", "Target_US", "TJXCompanies_US", "DeltaAirLines_US", "AmericanAirlines_US",
        "Uber_US", "Lyft_US", "ZoomVideo_US", "Salesforce_US", "Twitter_US", "eBay_US",
        "Qualcomm_US", "TexasInstruments_US", "Broadcom_US", "AMD_US", "Starbucks_US",
        "GoldmanSachs_US", "MorganStanley_US",
        "Oracle_US", "Palantir_US", "Snowflake_US", "CrowdStrike_US", "DocuSign_US",
        "Pinterest_US", "Snap_US", "Roku_US", "Moderna_US", "ZoomInfo_US", "Twilio_US",
        "Workday_US", "Okta_US", "Zscaler_US", "Datadog_US", "FidelityNationalInformationServices_US",
        "eTradeFinancial_US", "MarriottInternational_US", "HiltonWorldwideHoldings_US",
        "BookingHoldings_US", "ExpediaGroup_US", "Carnival_US", "RoyalCaribbeanCruises_US",
        "NorwegianCruiseLineHoldings_US", "BlackRock_US", "CharlesSchwab_US",
        "FidelityNationalInformationServices_US", "eTradeFinancial_US",
        # extend with full list later
    ],
    "DAX": [
        "Siemens_DE", "Volkswagen_DE", "Allianz_DE", "BASF_DE", "DeutscheBank_DE",
        "Bayer_DE", "Adidas_DE", "Daimler_DE", "SAP_DE", "BMW_DE",
        "Linde_DE", "Henkel_DE", "Infineon_DE", "Continental_DE", "Merck_DE",
        "DeutscheTelekom_DE", "Fresenius_DE", "Vonovia_DE", "E.ON_DE", "RWE_DE",
        "Beiersdorf_DE", "Covestro_DE", "MTU_AeroEngines_DE", "PorscheAutomobilHolding_DE",
        "Zalando_DE", "HelloFresh_DE", "SiemensHealthineers_DE", "DeutschePost_DE",
        "DeutscheLufthansa_DE", "Symrise_DE", "Qiagen_DE", "Knorr-Bremse_DE",
        "FreseniusMedicalCare_DE", "Wirecard_DE", "MercedesBenz_DE", "Puma_DE",
        "HugoBoss_DE", "EvonikIndustries_DE", "DeutscheBörse_DE", "Porsche_DE", 
        # extend with full list later
    ],
    "Nikkei225": [
        "Toyota_JP", "Sony_JP", "SoftBank_JP", "Nintendo_JP", "Honda_JP",
        "Keyence_JP", "KDDI_JP", "Mitsubishi_JP", "TakedaPharmaceutical_JP",
        "TokyoElectron_JP", "FastRetailing_JP", "Shin-EtsuChemical_JP",
        "DaiichiSankyo_JP", "Bridgestone_JP", "SumitomoMitsuiFinancial_JP",
        "NomuraHoldings_JP", "Itochu_JP", "Panasonic_JP", "Canon_JP",
        "Nissan_JP", "JapanTobacco_JP", "Mitsui_JP", "Seven&IHoldings_JP",
        "Denso_JP", "Olympus_JP", "Subaru_JP", "ChubuElectricPower_JP",
        "Komatsu_JP", "EastJapanRailway_JP", "Shiseido_JP",
        "Kao_JP", "Toshiba_JP", "Ajinomoto_JP", "MurataManufacturing_JP",
        "JFEHoldings_JP", "NipponSteel_JP", "Bridgestone_JP",
        "SumitomoMitsuiFinancial_JP", "NomuraHoldings_JP", 
        "Itochu_JP", "Panasonic_JP", "Canon_JP",
        # extend with full list later
    ],
    "FTSE100": [
        "AstraZeneca_GB", "Unilever_GB", "BP_GB", "HSBC_GB", "GlaxoSmithKline_GB",
        "Diageo_GB", "BritishAmericanTobacco_GB", "RioTinto_GB", "Barclays_GB",
        "LloydsBankingGroup_GB", "Prudential_GB", "BTGroup_GB", "Aviva_GB",
        "Tesco_GB", "Glencore_GB", "StandardChartered_GB", "RollsRoyce_GB",
        "NationalGrid_GB", "SSE_GB", "CompassGroup_GB", "Smith&Nephew_GB",
        "Experian_GB", "Shell_GB", "InterContinentalHotels_GB", "BAESystems_GB",
        "WPP_GB", "ImperialBrands_GB", "Centrica_GB", "AshteadGroup_GB",
        "Meggitt_GB", "Persimmon_GB", "BarrattDevelopments_GB", "TaylorWimpey_GB",
        "Kingfisher_GB",
    ],
    "DAX": [
        "Siemens_DE", "Volkswagen_DE", "Allianz_DE", "BASF_DE", "DeutscheBank_DE",
        "Bayer_DE", "Adidas_DE", "Daimler_DE", "SAP _DE", "BMW_DE",
        "Linde_DE", "Henkel_DE", "Infineon_DE", "Continental_DE", "Merck_DE",
        "DeutscheTelekom_DE", "Fresenius_DE", "Vonovia_DE", "E.ON_DE", "RWE_DE",
        "Beiersdorf_DE", "Covestro_DE", "MTU_AeroEngines_DE", "PorscheAutomobilHolding_DE",
        "Zalando_DE", "HelloFresh_DE", "SiemensHealthineers_DE", "DeutschePost_DE",
        "DeutscheLufthansa_DE", "Symrise_DE", "Qiagen_DE", "Knorr-Bremse_DE",
        "FreseniusMedicalCare_DE", "Wirecard_DE", "MercedesBenz_DE", "Puma_DE",
        "HugoBoss_DE", "EvonikIndustries_DE", "DeutscheBörse_DE", "Porsche_DE", 
        # extend with full list later
    ],

    "China": [
        "Alibaba_CN", "JD.com_CN", "Tencent_CN", "Baidu_CN", "Pinduoduo_CN",
        "Meituan_HK", "BYD_Company_HK", "Li_Auto_CN", "NIO_CN", "XPeng_CN",
        "ICBC_HK", "China_Const_Bank_HK", "Ping_An_Insurance_HK", "Bank_of_China_HK",
        "PetroChina_SS", "China_Life_HK", "CNOOC_HK",
        "Xiaomi_HK", "SMIC_HK", "Kweichow_Moutai_SS",
    ],
    "Emerging": [
        "Vale_BR", "Petrobras_BR", "GrupoBimbo_MX",
        "SamsungElectronics_KR", "HyundaiMotor_KR",
        "TataConsultancy_IN", "RelianceIndustries_IN", "TataMotors_IN", "TSMC_TW",
        "Lukoil_RU", "Gazprom_RU", "Naspers_ZA", "SaudiAramco_SA",
        "Alibaba_CN", "JDcom_CN", "Tencent_CN", "PetroChina_CN",

    ],
}


# -------------------------
# Index Tickers Mapping
# -------------------------
# Global indices for benchmarking
INDEX_TICKERS = {
    "S&P 500": "^GSPC",
    "Nikkei 225": "^N225",
    "CAC 40": "^FCHI",
    "DAX": "^GDAXI",
    "FTSE 100": "^FTSE",
    "Hang Seng": "^HSI",
    "Shanghai Composite": "000001.SS",
    "Bovespa": "^BVSP",
}


STOCK_CURRENCIES = {
    "US": "USD",
    "CH": "CHF",
    "DE": "EUR",
    "GB": "GBP",
    "FR": "EUR",
    "JP": "JPY",
    "KR": "KRW",
    "MX": "MXN",
    "BR": "BRL",
    "IN": "INR",
    "TW": "TWD",
    "ZA": "ZAR",
    "SA": "SAR",
    "RU": "RUB",
    "CN": "CNY",
    "HK": "HKD",
}

# -------------------------
# Tickers load_fx_matrix
# -------------------------
FX_MATRIX_TICKERS = {
    "EUR": "EURUSD=X",  # 1 EUR = x USD (Direct Quote)
    "GBP": "GBPUSD=X",  # 1 GBP = x USD (Direct Quote)
    "JPY": "JPY=X",     # 1 USD = x JPY (Indirect Quote)
    "CHF": "CHF=X",     # 1 USD = x CHF (Indirect Quote)
    "USD": None,        # Pivot
}

# -------------------------
# FX Groups (Time Series)
# -------------------------
FX_GROUPS = {
    "Majors": {
        "EUR/USD": "EURUSD=X",  # Renamed from USD/EUR to match market convention
        "USD/JPY": "JPY=X",
        "GBP/USD": "GBPUSD=X",
        "AUD/USD": "AUDUSD=X",
        "NZD/USD": "NZDUSD=X",
        "USD/CHF": "CHF=X",     # Added explicit USD/CHF
    },
    "Europe": {
        "EUR/JPY": "EURJPY=X",
        "GBP/JPY": "GBPJPY=X",
        "EUR/GBP": "EURGBP=X",
        "EUR/CAD": "EURCAD=X",
        "EUR/SEK": "EURSEK=X",
        "EUR/CHF": "EURCHF=X",
        "EUR/HUF": "EURHUF=X",
    },
    "Asia": {
        "USD/CNY": "CNY=X",
        "USD/HKD": "HKD=X",
        "USD/SGD": "SGD=X",
        "USD/INR": "INR=X",
        "USD/IDR": "IDR=X",
        "USD/THB": "THB=X",
        "USD/MYR": "MYR=X",
        "USD/PHP": "PHP=X",
    },
    "Emerging": {
        "USD/MXN": "MXN=X",
        "USD/ZAR": "ZAR=X",
        "USD/RUB": "RUB=X",
    },
}

FX_PAIRS = {pair: ticker for group in FX_GROUPS.values() for pair, ticker in group.items()}

# -------------------------
# Indexes (placeholder)
# -------------------------
INDEXES = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "Nasdaq 100": "^NDX",
    "Euro Stoxx 50": "^STOXX50E",
    "Nikkei 225": "^N225",
}

# -------------------------
# ETFs (placeholder)
# -------------------------
ETFS = {
    "SPY (S&P 500 ETF)": "SPY",
    "QQQ (Nasdaq 100 ETF)": "QQQ",
    "EFA (MSCI EAFE ETF)": "EFA",
    "EEM (MSCI Emerging Markets ETF)": "EEM",
}


# -------------------------
# Indices by Region
# -------------------------
INDICES = {
    "Americas": {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI", 
        "Nasdaq 100": "^IXIC",
        "Russell 2000": "^RUT",
        "S&P/TSX Composite": "^GSPTSE",
        "Bovespa": "^BVSP",
        "Merval": "^MERV"
    },
    "Europe": {
        "Euro Stoxx 50": "^STOXX50E",
        "CAC 40": "^FCHI", 
        "DAX": "^GDAXI",
        "FTSE 100": "^FTSE",
        "FTSE MIB": "FTSEMIB.MI",
        "IBEX 35": "^IBEX",
        "AEX": "^N100"
    },
    "Asia": {
        "Nikkei 225": "^N225", 
        "Hang Seng": "^HSI",
        "KOSPI": "^KS11", 
        "ASX 200": "^AXJO",
        "Shanghai Composite": "000001.SS", 
        "Nifty 50": "^NSEI"
    }
}


# -------------------------
# Macro Indicators
# -------------------------
# =========================================================
# Monetary Policy Tickers
# =========================================================
# Used for Macro Policy Matrix (US & EU)
MONETARY_POLICY_TICKERS = {
    "USA": {
        "CPI": "CPIAUCSL",          # US CPI (Index)
        "EFFR": "EFFR",             # Effective Fed Funds Rate
        "Target_Up": "DFEDTARU",    # Fed Target Upper
        "Target_Low": "DFEDTARL"    # Fed Target Lower
    },
    "EURO": {
        "CPI": "CP0000EZ19M086NEST", # EU HICP (Index) - The robust one
        "Deposit": "ECBDFR",         # ECB Deposit Facility (Floor)
        "MRO": "ECBMRRFR"            # ECB Main Refinancing (Pivot)
    }
}

# -------------------------
# Commodities (for Page 5) 
# -------------------------
COMMODITIES = {
    "Energy": {
        "WTI Crude Oil": "CL=F", 
        "Brent Crude Oil": "BZ=F", 
        "Natural Gas": "NG=F"
    }, 
    "Metals": {
        "Gold": "GC=F", 
        "Silver": "SI=F", 
        "Copper": "HG=F", 
        "Platinum": "PL=F"
    }, 
    "Agriculture": {
        "Corn": "ZC=F", 
        "Wheat": "W=F", 
        "Soybeans": "ZS=F", 
        "Coffee": "KC=F"
    }, 
    "Softs": {
        "Cotton": "CT=F", 
        "Sugar": "SB=F", 
        "Cocoa": "CC=F"
    }
}


# -------------------------
# Rates — FRED series mappings
# Responsibility: Centralize all FRED tickers and friendly names
# -------------------------

# U.S. Treasury yields (constant maturity, daily, from FRED)
US_YIELD_TICKERS = {
    "DGS1MO": "U.S. 1M Treasury",
    "DGS3MO": "U.S. 3M Treasury",
    "DGS6MO": "U.S. 6M Treasury",
    "DGS1":   "U.S. 1Y Treasury",
    "DGS2":   "U.S. 2Y Treasury",
    "DGS3":   "U.S. 3Y Treasury",
    "DGS5":   "U.S. 5Y Treasury",
    "DGS7":   "U.S. 7Y Treasury",
    "DGS10":  "U.S. 10Y Treasury",
    "DGS20":  "U.S. 20Y Treasury",
    "DGS30":  "U.S. 30Y Treasury",
}

# OECD 10Y government bond yields (monthly, from FRED)
OECD_YIELD_TICKERS = {
    "IRLTLT01USM156N": "United States (OECD)",
    "IRLTLT01DEM156N": "Germany",
    "IRLTLT01FRM156N": "France",
    "IRLTLT01ITM156N": "Italy",
    "IRLTLT01GBM156N": "United Kingdom",
    "IRLTLT01JPM156N": "Japan",
    "IRLTLT01ESM156N": "Spain",
    "IRLTLT01PTM156N": "Portugal",
    "IRLTLT01GRM156N": "Greece",
}

# Convenience lists
ALL_US_YIELDS = list(US_YIELD_TICKERS.keys())
ALL_OECD_YIELDS = list(OECD_YIELD_TICKERS.keys())


# =========================================================
# Cross-Asset Snapshot Tickers (Yahoo Finance)
# =========================================================
# Keys are display names. 
# Values are tuples: (Yahoo Ticker, Unit Label)
CROSS_ASSET_TICKERS = {
    "VIX Index":       ("^VIX",     "% (Vol)"),
    "Gold":            ("GC=F",     "$/oz"),
    "Brent Oil":       ("BZ=F",     "$/bbl"),
    "Bitcoin":         ("BTC-USD",  "USD"),
    "Ethereum":        ("ETH-USD",  "USD"),
    "MSCI World":      ("URTH",     "$"),       # ETF Proxy
    "EUR/USD":         ("EURUSD=X", "Rate"),
    "USD/JPY":         ("JPY=X",    "Rate"),
    "10Y Treasury":    ("^TNX",     "%")
}

# -------------------------
#  Tickers load_gdp_comparison
# -------------------------
# Used in GDP data loading and processing
GDP_COMPARISON_TICKERS = {
        "USA": "GDP",
        "China": "CHNGDPNQDSMEI",
        "Japan": "JPNNGDP",
        "UK": "UKNGDP",
        "Germany": "DEUGDPNQDSMEI",
        "France": "FRAGDPNQDSMEI"
    }

# -------------------------
# Tickers build_gdp_monitor_table
# -------------------------
# Used in building GDP comparison tables
GDP_MONITOR_TABLE_TICKERS = {
    "United States": "GDP",
    "China": "CHNGDPNQDSMEI", # Example ID, ensure it matches data_loader
    "Japan": "JPNGDPNQDSMEI",
    "Germany": "DEUGDPNQDSMEI",
    "France": "FRAGDPNQDSMEI",
    "United Kingdom": "GBRGDPNQDSMEI"
}

# -------------------------
# Tickers build_gdp_comparison_tables  
# -------------------------
# Used in building GDP comparison tables
GDP_COMPARISON_TABLES_TICKERS = [
    {'country': 'USA',     'currency': 'USD', 'divisor': 1e3},
    {'country': 'China',   'currency': 'CNY', 'divisor': 1e12},
    {'country': 'Japan',   'currency': 'JPY', 'divisor': 1e3}, # Adjusted 1e3 for Billions
    {'country': 'UK',      'currency': 'GBP', 'divisor': 1e6},
    {'country': 'Germany', 'currency': 'EUR', 'divisor': 1e12},
    {'country': 'France',  'currency': 'EUR', 'divisor': 1e12},
]



# ... (Keep existing STOCK_TICKERS, etc.)

# =========================================================
# Commodities Tickers Mapping
# =========================================================

COMMODITY_GROUPS = {
    "Metals": {
        "Gold": "GC=F", 
        "Silver": "SI=F", 
        "Copper": "HG=F", 
        "Platinum": "PL=F", 
        "Steel HRC": "HRC=F",
        "Nickel": "NIKL", # ETF proxy often used if futures data is restricted
        "Palladium": "PA=F",
        "Lithium": "LIT"
    },
    "Energy": {
        "Crude Oil WTI": "CL=F", 
        "Brent Oil": "BZ=F", 
        "Natural Gas": "NG=F", 
        "Heating Oil": "HO=F", 
        "RBOB Gasoline": "RB=F",
        "Ethanol": "CZ=F" 
    },
    "Agriculture": {
        "Wheat": "ZW=F", 
        "Corn": "ZC=F", 
        "Soybeans": "ZS=F", 
        "Cocoa": "CC=F", 
        "Coffee": "KC=F", 
        "Orange Juice": "OJ=F", 
        "Sugar": "SB=F", 
        "Cotton": "CT=F", 
        "Live Cattle": "LE=F", 
        "Lean Hogs": "HE=F"
    }
}

# Configuration for Futures Curves
FUTURE_MONTH_MAP = {
    "F": "Jan", "G": "Feb", "H": "Mar", "J": "Apr", "K": "May", "M": "Jun",
    "N": "Jul", "Q": "Aug", "U": "Sep", "V": "Oct", "X": "Nov", "Z": "Dec"
}

COMMODITY_FUTURES_CONFIG = {
    "Crude Oil":   {"root": "CL",  "suffix": ".NYM", "months": ["F","G","H","J","K","M","N","Q","U","V","X","Z"]},
    "Gold":        {"root": "GC",  "suffix": ".CMX", "months": ["F","G","H","J","M","Q","V","Z"]},
    "Silver":      {"root": "SI",  "suffix": ".CMX", "months": ["H","K","N","U","Z"]},
    "Natural Gas": {"root": "NG",  "suffix": ".NYM", "months": ["F","G","H","J","K","M","N","Q","U","V","X","Z"]},
    "Heating Oil": {"root": "HO",  "suffix": ".NYM", "months": ["F","G","H","J","K","M","N","Q","U","V","X","Z"]},
    "Corn":        {"root": "ZC",  "suffix": ".CBT", "months": ["H","K","N","U","Z"]},
    "Coffee":      {"root": "KC",  "suffix": ".NYB", "months": ["H","K","N","U","Z"]}
}