# app/services/data_loader.py

import os
import pandas as pd

# =========================================================
# Data Loader
# =========================================================
# Responsibility: Orchestrate fetch → transform → cache → load.
# Pages call here; they never touch raw APIs or files directly.
# =========================================================

from .yf_client import (
    download_close_fxmatrix_series,
    download_fx_history_series,
)
from .transforms import (
    build_fx_spot_and_change,
    merge_fx_and_change,
    resample_fx_series,
)
from .tickers_mapping import FX_PAIRS


# =========================================================
# Cache directories
# =========================================================

# FX matrix cache (spot + % change)
FX_MATRIX_PROCESSED_PATH = os.path.join("data", "processed", "FX_rate_matrix.csv")

# FX historical time series cache (all pairs in one file)
FX_HISTORY_PATH = os.path.join("data", "processed", "FX_historical.csv")
os.makedirs(os.path.dirname(FX_HISTORY_PATH), exist_ok=True)


# =========================================================
# FX Matrix (Spot + % Change)
# Purpose: Normalize FX quotes, build spot and % change matrices,
# and merge them into a display-ready DataFrame.
# =========================================================

def load_fx_matrix(
    force_refresh: bool = False,
    tickers: dict | None = None,
    period: str = "5d",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Load the merged FX matrix (spot + % change) as a display-ready DataFrame.

    Workflow:
    - If a cached CSV exists and force_refresh=False → load from cache.
    - Otherwise → fetch from Yahoo Finance, transform, cache, and return.
    """
    tickers = tickers or FX_PAIRS

    # Fast path: load cached file if available
    if (not force_refresh) and os.path.exists(FX_MATRIX_PROCESSED_PATH):
        return pd.read_csv(FX_MATRIX_PROCESSED_PATH, index_col=0)

    # Regenerate from source
    fx_matrix, change_matrix = build_fx_spot_and_change(
        ticker_map=tickers,
        fetch_fn=download_close_fxmatrix_series,
        period=period,
        interval=interval,
    )
    merged = merge_fx_and_change(fx_matrix, change_matrix)

    # Ensure processed folder exists, then save cache
    os.makedirs(os.path.dirname(FX_MATRIX_PROCESSED_PATH), exist_ok=True)
    merged.to_csv(FX_MATRIX_PROCESSED_PATH)

    return merged


# =========================================================
# FX Historical Time Series (All pairs in one CSV)
# Purpose: Download once for all pairs, store in fx_history.csv,
# then slice/resample per pair for visualization.
# =========================================================

def build_fx_history(force_refresh: bool = False) -> pd.DataFrame:
    """
    Build consolidated FX history for all pairs in FX_PAIRS.

    - If fx_history.csv exists and force_refresh=False → load from cache.
    - Otherwise → download all pairs from Yahoo Finance, save one big CSV.

    Returns
    -------
    pd.DataFrame
        Wide DataFrame with one column per FX pair (friendly name).
    """
    if (not force_refresh) and os.path.exists(FX_HISTORY_PATH):
        return pd.read_csv(FX_HISTORY_PATH, index_col=0, parse_dates=True)

    all_series = {}
    for pair_name, ticker in FX_PAIRS.items():
        series = download_fx_history_series(ticker, period="max", interval="1d")

        # Only keep if it's a proper Series with a DateTime index
        if isinstance(series, pd.Series) and not series.empty:
            # ✅ Ensure column name is the friendly name (e.g. "USD/EUR")
            series.name = pair_name
            all_series[pair_name] = series
            print(f"✔ Added {pair_name} ({ticker}) with {len(series)} rows")
        else:
            print(f"⚠️ Skipping {pair_name} ({ticker}) — no data returned")

    if not all_series:
        raise ValueError("No FX history could be downloaded — check tickers or API.")

    # Align all series on their datetime index
    df = pd.concat(all_series.values(), axis=1)

    os.makedirs(os.path.dirname(FX_HISTORY_PATH), exist_ok=True)
    df.to_csv(FX_HISTORY_PATH)

    print(f"\n✅ FX historical data saved to {FX_HISTORY_PATH}")
    print(f"Shape: {df.shape}")

    return df


def load_fx_timeseries(pair_name: str, freq: str = "D") -> pd.Series:
    """
    Load FX time series for a given currency pair (friendly name).
    Reads from consolidated fx_history.csv and resamples.

    Parameters
    ----------
    pair_name : str
        Friendly name of the FX pair (e.g. "USD/EUR").
    freq : str
        Resampling frequency: 'D' (daily), 'W' (weekly),
        'M' (monthly), 'Y' (yearly).

    Returns
    -------
    pd.Series
        Resampled FX time series.
    """
    # Ensure consolidated history exists
    if not os.path.exists(FX_HISTORY_PATH):
        build_fx_history(force_refresh=True)

    df = pd.read_csv(FX_HISTORY_PATH, index_col=0, parse_dates=True)

    if pair_name not in df.columns:
        return pd.Series(dtype=float)

    series = df[pair_name].dropna()
    return resample_fx_series(series, freq)