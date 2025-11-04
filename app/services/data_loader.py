# app/services/data_loader.py

import os
import pandas as pd

# =========================================================
# Data Loader
# =========================================================
# Responsibility: Orchestrate fetch → transform → cache → load.
# Pages call here; they never touch raw APIs or files directly.


# =========================================================
# Page: FX (p3_fx) — Figure: FX spot + % change matrix
# Purpose: Normalize FX quotes, build spot and % change matrices,
# and merge them into a display-ready DataFrame.
# =========================================================

from .yf_client import download_close_fxmatrix_series
from .transforms import build_fx_spot_and_change, merge_fx_and_change

# Default location for processed FX matrix
FX_PROCESSED_PATH = os.path.join("data", "processed", "FX_rate_matrix.csv")

# Default tickers (all quoted vs USD)
DEFAULT_FX_TICKERS = {
    "EUR": "EURUSD=X",
    "GBP": "GBPUSD=X",
    "JPY": "JPY=X",       # USD/JPY (will be inverted to USD per JPY)
    "CHF": "CHFUSD=X",
    # Add more currencies here if needed
}


def load_fx_matrix(
    force_refresh: bool = False,
    tickers: dict | None = None,
    period: str = "5d",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Load the merged FX matrix (spot + % change) as a display-ready DataFrame of strings.

    - If a cached CSV exists and force_refresh=False → load from cache.
    - Otherwise → fetch from Yahoo Finance, transform, cache, and return.

    Parameters
    ----------
    force_refresh : bool
        If True, ignore cache and fetch fresh data.
    tickers : dict
        Mapping of currency codes to Yahoo Finance tickers.
    period : str
        Period to fetch from Yahoo Finance (default '5d').
    interval : str
        Interval for Yahoo Finance data (default '1d').

    Returns
    -------
    pd.DataFrame
        Merged FX matrix with spot and % change formatted as strings.
    """
    tickers = tickers or DEFAULT_FX_TICKERS

    # Fast path: load cached file if available
    if (not force_refresh) and os.path.exists(FX_PROCESSED_PATH):
        return pd.read_csv(FX_PROCESSED_PATH, index_col=0)

    # Regenerate from source
    fx_matrix, change_matrix = build_fx_spot_and_change(
        ticker_map=tickers,
        fetch_fn=download_close_fxmatrix_series,
        period=period,
        interval=interval
    )
    merged = merge_fx_and_change(fx_matrix, change_matrix)

    # Ensure processed folder exists
    os.makedirs(os.path.dirname(FX_PROCESSED_PATH), exist_ok=True)
    merged.to_csv(FX_PROCESSED_PATH)

    return merged


# =========================================================
# Page: FX (p3_fx) — Figure: Time series line chart
# Purpose: Resample long-range FX history into different frequencies
# (daily, weekly, monthly, yearly) for visualization.
# =========================================================

from .yf_client import download_fx_history_series
from .transforms import resample_fx_series

def load_fx_timeseries(ticker: str, freq: str = "D") -> pd.Series:
    """
    Load FX time series for a given ticker and resample to desired frequency.
    freq: 'D', 'W', 'M', 'Y'
    """
    series = download_fx_history_series(ticker, period="max", interval="1d")
    if series.empty:
        return series
    return resample_fx_series(series, freq)