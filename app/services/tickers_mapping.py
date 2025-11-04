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