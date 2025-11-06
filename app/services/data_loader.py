# =========================================================
# Data Loader
# =========================================================
# Responsibility: Orchestrate fetch → transform → cache → load.
# Pages call here; they never touch raw APIs or files directly.
# =========================================================

import os
import pandas as pd

# ---------------------------------------------------------
# Imports from services
# ---------------------------------------------------------
from .transforms import (
    build_fx_spot_and_change,
    merge_fx_and_change,
    resample_fx_series,
    build_fx_history_series,   # moved from data_loader to transforms
)
from .yf_client import download_close_fxmatrix_series
from .fred_client import download_us_yields, download_oecd_yields
from .tickers_mapping import FX_PAIRS, US_YIELD_TICKERS, OECD_YIELD_TICKERS


# ---------------------------------------------------------
# Cache paths
# ---------------------------------------------------------
FX_MATRIX_PROCESSED_PATH = os.path.join("data", "processed", "FX_rate_matrix.csv")
FX_HISTORY_PATH = os.path.join("data", "processed", "FX_historical.csv")
US_YIELDS_PATH = os.path.join("data", "processed", "us_yields.csv")
OECD_YIELDS_PATH = os.path.join("data", "processed", "oecd_yields.csv")


# =========================================================
# FX Matrix Loader
# =========================================================
def load_fx_matrix(
    force_refresh: bool = False,
    tickers: dict | None = None,
    period: str = "5d",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Load the merged FX matrix (spot + % change).
    - If force_refresh=False → load from existing CSV.
    - If force_refresh=True → fetch fresh data, transform, overwrite CSV.
    """
    default_tickers = {
        "EUR": "EURUSD=X",
        "GBP": "GBPUSD=X",
        "JPY": "JPY=X",
        "CHF": "CHFUSD=X",
        "USD": None,
    }
    tickers = tickers or default_tickers

    if not force_refresh:
        return pd.read_csv(FX_MATRIX_PROCESSED_PATH, index_col=0)

    fx_matrix, change_matrix = build_fx_spot_and_change(
        ticker_map=tickers,
        fetch_fn=download_close_fxmatrix_series,
        period=period,
        interval=interval,
    )

    fx_matrix.index = list(tickers.keys())
    fx_matrix.columns = list(tickers.keys())
    change_matrix.index = list(tickers.keys())
    change_matrix.columns = list(tickers.keys())

    merged = merge_fx_and_change(fx_matrix, change_matrix)
    merged.to_csv(FX_MATRIX_PROCESSED_PATH)
    return merged


# =========================================================
# FX Historical Loader
# =========================================================
def load_fx_timeseries(pair_name: str, freq: str = "D", force_refresh: bool = False) -> pd.Series:
    """
    Load FX time series for a given currency pair (friendly name).
    - If force_refresh=True → rebuild history via transforms, save CSV.
    - Otherwise → read from existing CSV.
    Then resample to the requested frequency.
    """
    if force_refresh:
        df = build_fx_history_series()
        df.to_csv(FX_HISTORY_PATH)
    else:
        df = pd.read_csv(FX_HISTORY_PATH, index_col=0, parse_dates=True)

    if pair_name not in df.columns:
        return pd.Series(dtype=float)

    series = df[pair_name].dropna()
    return resample_fx_series(series, freq)


# =========================================================
# FX Historical Helper
# =========================================================
def refresh_fx_history() -> pd.DataFrame:
    """
    Force rebuild of the entire FX historical dataset.
    - Calls build_fx_history_series() from transforms.
    - Saves the consolidated DataFrame to FX_HISTORY_PATH.
    - Returns the DataFrame.
    """
    df = build_fx_history_series()
    df.to_csv(FX_HISTORY_PATH)
    print(f"✅ FX historical data refreshed and saved to {FX_HISTORY_PATH}")
    return df


# =========================================================
# U.S. Treasury Yields Loader
# =========================================================
def load_us_yields(force_refresh: bool = False,
                   start_date: str = "1990-01-01",
                   end_date: str | None = None) -> pd.DataFrame:
    """
    Load U.S. Treasury yields.
    - If force_refresh=False → load from existing CSV.
    - If force_refresh=True → fetch from FRED, overwrite CSV.
    """
    if not force_refresh:
        return pd.read_csv(US_YIELDS_PATH, index_col=0, parse_dates=True)

    df = download_us_yields(list(US_YIELD_TICKERS.keys()),
                            start_date=start_date, end_date=end_date)
    if df.empty:
        raise ValueError("No U.S. yield data could be downloaded.")

    df.to_csv(US_YIELDS_PATH)
    return df


# =========================================================
# OECD Yields Loader
# =========================================================
def load_oecd_yields(force_refresh: bool = False,
                     start_date: str = "1990-01-01",
                     end_date: str | None = None) -> pd.DataFrame:
    """
    Load OECD 10Y government bond yields.
    - If force_refresh=False → load from existing CSV.
    - If force_refresh=True → fetch from FRED, overwrite CSV.
    """
    if not force_refresh:
        return pd.read_csv(OECD_YIELDS_PATH, index_col=0, parse_dates=True)

    df = download_oecd_yields(list(OECD_YIELD_TICKERS.keys()),
                              start_date=start_date, end_date=end_date)
    if df.empty:
        raise ValueError("No OECD yield data could be downloaded.")

    df.to_csv(OECD_YIELDS_PATH)
    return df