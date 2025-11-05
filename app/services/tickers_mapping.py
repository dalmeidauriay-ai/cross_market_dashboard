# app/services/tickers_mapping.py

# =========================================================
# Central ticker → display name mappings
# Used across pages (FX, Equities, Commodities, ETFs, etc.)
# =========================================================

# -------------------------
# FX pairs
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
# Equity indexes (placeholder)
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
