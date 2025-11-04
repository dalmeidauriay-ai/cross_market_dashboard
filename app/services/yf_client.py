# app/services/yf_client.py

import yfinance as yf
import pandas as pd

# ---------------------------------------------------------
# Yahoo Finance client helpers
# ---------------------------------------------------------
# Responsibility: Fetch raw series from Yahoo Finance.
# No transformations here beyond basic cleaning.


# =========================================================
# Page: FX (p3_fx) — Figure: FX spot + % change matrix
# Purpose: Short-horizon close prices used to compute the FX matrix.
# =========================================================

def download_close_fxmatrix_series(ticker: str, period: str = "5d", interval: str = "1d") -> pd.Series:
    """
    Download a 'Close' price series for a given FX ticker.
    Returns a pandas Series indexed by datetime.
    Used specifically for building the FX matrix (short horizon).
    """
    hist = yf.download(
        ticker, period=period, interval=interval,
        auto_adjust=True, progress=False
    )
    if "Close" not in hist:
        return pd.Series(dtype=float)
    return hist["Close"].dropna()


# =========================================================
# Page: FX (p3_fx) — Figure: Time series line chart
# Purpose: Long-range history to power the FX time series visualization.
# Notes: Fetched at daily frequency; resampling handled in transforms.
# =========================================================

def download_fx_history_series(ticker: str, period: str = "max", interval: str = "1d") -> pd.Series:
    """
    Download long-range FX history for a given ticker.
    Default: full history ('max') at daily frequency.
    Returns a pandas Series indexed by datetime.
    Intended for the FX time series line chart.
    """
    hist = yf.download(
        ticker, period=period, interval=interval,
        auto_adjust=True, progress=False
    )
    if "Close" not in hist:
        return pd.Series(dtype=float)
    return hist["Close"].dropna()