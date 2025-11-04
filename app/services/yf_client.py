# app/services/yf_client.py

import yfinance as yf
import pandas as pd

# ---------------------------------------------------------
# Yahoo Finance client helpers
# ---------------------------------------------------------
# Responsibility: Fetch raw series from Yahoo Finance.
# No transformations here beyond basic cleaning.
# ---------------------------------------------------------


# =========================================================
# Page: FX (p3_fx) — Figure: FX spot + % change matrix
# Purpose: Short-horizon close prices used to compute the FX matrix.
# =========================================================

def download_close_fxmatrix_series(ticker: str, period: str = "5d", interval: str = "1d") -> pd.Series:
    """
    Download a short-horizon price series for a given FX ticker.

    For FX, 'Close' and 'Adj Close' are equivalent (no dividends/splits).
    Yahoo sometimes only provides 'Adj Close', so we prefer that if present,
    otherwise fall back to 'Close'.

    Handles both flat and MultiIndex column formats returned by yfinance.

    Returns
    -------
    pd.Series
        Series of prices indexed by datetime.
    """
    hist = yf.download(
        ticker, period=period, interval=interval,
        auto_adjust=True, progress=False
    )

    if hist.empty:
        return pd.Series(dtype=float)

    # Handle MultiIndex columns (common for FX tickers)
    if isinstance(hist.columns, pd.MultiIndex):
        if ("Adj Close", ticker) in hist.columns:
            series = hist[("Adj Close", ticker)]
        elif ("Close", ticker) in hist.columns:
            series = hist[("Close", ticker)]
        else:
            return pd.Series(dtype=float)
    else:
        if "Adj Close" in hist.columns:
            series = hist["Adj Close"]
        elif "Close" in hist.columns:
            series = hist["Close"]
        else:
            return pd.Series(dtype=float)

    return series.dropna()


# =========================================================
# Page: FX (p3_fx) — Figure: Time series line chart
# Purpose: Long-range history to power the FX time series visualization.
# Notes: Fetched at daily frequency; resampling handled in transforms.
# =========================================================

def download_fx_history_series(ticker: str, period: str = "max", interval: str = "1d") -> pd.Series:
    """
    Download long-range FX history for a given ticker.

    Default: full history ('max') at daily frequency.
    For FX, 'Close' and 'Adj Close' are equivalent. We prefer 'Adj Close'
    if available, otherwise fall back to 'Close'.

    Handles both flat and MultiIndex column formats returned by yfinance.

    Returns
    -------
    pd.Series
        Series of prices indexed by datetime.
    """
    hist = yf.download(
        ticker, period=period, interval=interval,
        auto_adjust=True, progress=False
    )

    if hist.empty:
        return pd.Series(dtype=float)

    # Handle MultiIndex columns (common for FX tickers)
    if isinstance(hist.columns, pd.MultiIndex):
        if ("Adj Close", ticker) in hist.columns:
            series = hist[("Adj Close", ticker)]
        elif ("Close", ticker) in hist.columns:
            series = hist[("Close", ticker)]
        else:
            return pd.Series(dtype=float)
    else:
        if "Adj Close" in hist.columns:
            series = hist["Adj Close"]
        elif "Close" in hist.columns:
            series = hist["Close"]
        else:
            return pd.Series(dtype=float)

    return series.dropna()