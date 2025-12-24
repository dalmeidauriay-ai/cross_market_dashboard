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
    "Apple_US": "AAPL",
    "Microsoft_US": "MSFT",
    "Amazon_US": "AMZN",
    "Tesla_US": "TSLA",
    "Meta_US": "META",
    "Nvidia_US": "NVDA",
    "Alphabet_US": "GOOGL",
    "Johnson&Johnson_US": "JNJ",

    # ------ Europe ------
    "Nestle_CH": "NESN.SW",
    "Roche_CH": "ROG.SW",
    "Siemens_DE": "SIE.DE",
    "Volkswagen_DE": "VOW3.DE",
    "BP_GB": "BP.L",
    "HSBC_GB": "HSBA.L",
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
    "STMicroelectronics_FR": "STM.PA",
    "Teleperformance_FR": "TEP.PA",
    "Thales_FR": "HO.PA",
    "TotalEnergies_FR": "TTE.PA",
    "UnibailRodamcoWestfield_FR": "URW.AS",
    "Veolia_FR": "VIE.PA",
    "Vinci_FR": "DG.PA",
    "Vivendi_FR": "VIV.PA",
    "Worldline_FR": "WLN.PA",

    # ------ China ------
    "Alibaba_CN": "BABA",
    "JDcom_CN": "JD",
    "Tencent_CN": "TCEHY",
    "PetroChina_CN": "PTR",

    # ------ Japan ------
    "Toyota_JP": "7203.T",
    "Sony_JP": "6758.T",
    "SoftBank_JP": "9434.T",
    "Nintendo_JP": "7974.T",

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
    "TataMotors_IN": "TTM",
    "TSMC_TW": "2330.TW",

    # ------ Emerging ------
    "Lukoil_RU": "LKOH.ME",
    "Gazprom_RU": "OGZPY",
    "Naspers_ZA": "NPSNY",
    "SaudiAramco_SA": "2222.SR",
}

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
        # extend with full list later
    ],
    "DAX": [
        "Siemens_DE", "Volkswagen_DE",
        # extend with full list later
    ],
    "Nikkei225": [
        "Toyota_JP", "Sony_JP", "SoftBank_JP", "Nintendo_JP",
        # extend with full list later
    ],
    "Emerging": [
        "Vale_BR", "Petrobras_BR", "GrupoBimbo_MX",
        "SamsungElectronics_KR", "HyundaiMotor_KR",
        "TataConsultancy_IN", "RelianceIndustries_IN", "TataMotors_IN", "TSMC_TW",
        "Lukoil_RU", "Gazprom_RU", "Naspers_ZA", "SaudiAramco_SA",
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
FX_GROUPS = {
    "Majors": {
        "USD/EUR": "EURUSD=X",
        "USD/JPY": "JPY=X",
        "GBP/USD": "GBPUSD=X",
        "AUD/USD": "AUDUSD=X",
        "NZD/USD": "NZDUSD=X",
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

# Flattened version if needed elsewhere
FX_PAIRS = {pair: ticker for group in FX_GROUPS.values() for pair, ticker in group.items()}


# -------------------------
# Commodities (placeholder)
# -------------------------
COMMODITIES = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil WTI": "CL=F",
    "Crude Oil Brent": "BZ=F",
    "Natural Gas": "NG=F",
}

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
        "Bovespa": "^BVSP",
        "Russell 2000": "^RUT",
        "Merval": "^MERV"
    },
    "Europe": {
        "Euro Stoxx 50": "^STOXX50E",
        "CAC 40": "^FCHI", 
        "DAX": "^GDAXI",
        "FTSE 100": "^FTSE",
        "FTSE MIB": "FTSEMIB.MI",
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
MACRO_INDICATORS = {
    "FRED": {
        "GDP": {
            "US": "GDP", 
            "China": "CHNGDPNQDSMEI", 
            "Japan": "JPNGDPNQDSMEI", 
            "France": "FRAGDPNQDSMEI", 
            "UK": "GBRGDPNQDSMEI", 
            "Germany": "DEUGDPNQDSMEI"
        },
        "Interest Rates": {
            "Fed Funds Rate": "FEDFUNDS", 
            "ECB Main Refinancing Rate": "ECBMAIN"
        }, 
        "Inflation": {
            "US CPI": "CPIAUCSL", 
            "Euro Area CPI": "CP0000EZ19M086NEST", 
            "France CPI": "FRACPIALLMINMEI"
        }
    }, 
    "Yahoo": {
        "Volatility": {
            "VIX": "^VIX"
        }, 
        "Commodities": {
            "Gold": "GC=F", 
            "Brent Oil": "BZ=F"
        }, 
        "Crypto": {
            "BTC-USD": "BTC-USD", 
            "ETH-USD": "ETH-USD"
        }, 
        "Equity": {
            "MSCI World": "URTH"
        }
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
