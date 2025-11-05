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

from .fred_client import (
    download_us_yields,
    download_oecd_yields,
)

from .transforms import (
    build_fx_spot_and_change,
    merge_fx_and_change,
    resample_fx_series,
)

from .tickers_mapping import (
    FX_PAIRS,
    US_YIELD_TICKERS,
    OECD_YIELD_TICKERS,
)



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

    # 🔹 NEW: Restrict to a fixed set of currencies with clean labels
    default_tickers = {
        "EUR": "EURUSD=X",   # EUR/USD
        "GBP": "GBPUSD=X",   # GBP/USD
        "JPY": "JPY=X",      # USD/JPY
        "CHF": "CHFUSD=X",   # CHF/USD
        "USD": None,         # USD is the base reference
    }
    tickers = tickers or default_tickers

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

    # 🔹 Ensure rows/columns are labeled with raw currency codes (USD, EUR, GBP, JPY, CHF)
    fx_matrix.index = list(tickers.keys())
    fx_matrix.columns = list(tickers.keys())
    change_matrix.index = list(tickers.keys())
    change_matrix.columns = list(tickers.keys())

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




# =========================================================
# Cache directories for Rates
# =========================================================

RATES_DIR = os.path.join("data", "processed")
US_YIELDS_PATH = os.path.join(RATES_DIR, "us_yields.csv")
OECD_YIELDS_PATH = os.path.join(RATES_DIR, "oecd_yields.csv")
os.makedirs(RATES_DIR, exist_ok=True)


# =========================================================
# U.S. Treasury Yields
# =========================================================

def load_us_yields(force_refresh: bool = False,
                   start_date: str = "1990-01-01",
                   end_date: str | None = None) -> pd.DataFrame:
    """
    Load U.S. Treasury yields (from cache if available, otherwise download).

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and columns for each maturity.
    """
    if (not force_refresh) and os.path.exists(US_YIELDS_PATH):
        return pd.read_csv(US_YIELDS_PATH, index_col=0, parse_dates=True)

    df = download_us_yields(list(US_YIELD_TICKERS.keys()),
                            start_date=start_date, end_date=end_date)

    if df.empty:
        raise ValueError("No U.S. yield data could be downloaded.")

    df.to_csv(US_YIELDS_PATH)
    return df


# =========================================================
# OECD 10Y Government Bond Yields
# =========================================================

def load_oecd_yields(force_refresh: bool = False,
                     start_date: str = "1990-01-01",
                     end_date: str | None = None) -> pd.DataFrame:
    """
    Load OECD 10Y government bond yields (from cache if available, otherwise download).

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and columns for each country.
    """
    if (not force_refresh) and os.path.exists(OECD_YIELDS_PATH):
        return pd.read_csv(OECD_YIELDS_PATH, index_col=0, parse_dates=True)

    df = download_oecd_yields(list(OECD_YIELD_TICKERS.keys()),
                              start_date=start_date, end_date=end_date)

    if df.empty:
        raise ValueError("No OECD yield data could be downloaded.")

    df.to_csv(OECD_YIELDS_PATH)
    return df
