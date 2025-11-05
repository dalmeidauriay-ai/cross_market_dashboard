# app/services/fred_client.py

import pandas as pd
import pandas_datareader.data as web
import warnings

# ---------------------------------------------------------
# FRED client helpers
# ---------------------------------------------------------
# Responsibility: Fetch raw series from FRED.
# No transformations here beyond basic cleaning (e.g. ffill).
# ---------------------------------------------------------

# Suppress noisy warnings from pandas_datareader
warnings.simplefilter(action="ignore", category=FutureWarning)


# =========================================================
# Generic FRED downloader
# =========================================================

def download_fred_series(series_names, start_date="1990-01-01", end_date=None) -> pd.DataFrame:
    """
    Download one or more FRED series.

    Parameters
    ----------
    series_names : list[str] or str
        FRED series codes (e.g. ["DGS10", "DGS2"]).
    start_date : str or datetime
        Start date for the data (default "1990-01-01").
    end_date : str or datetime, optional
        End date for the data (default None = today).

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and one column per series.
        Missing values forward-filled.
    """
    if isinstance(series_names, str):
        series_names = [series_names]

    frames = []
    for s in series_names:
        try:
            df = web.DataReader(s, "fred", start=start_date, end=end_date)
            frames.append(df)
        except Exception as e:
            # We don't raise here — just skip and continue
            print(f"⚠️ Skipping {s}: {e}")

    if frames:
        return pd.concat(frames, axis=1).ffill()
    else:
        return pd.DataFrame()


# =========================================================
# Convenience wrappers
# =========================================================

def download_us_yields(series_names, start_date="1990-01-01", end_date=None) -> pd.DataFrame:
    """
    Download U.S. Treasury yields from FRED.
    """
    return download_fred_series(series_names, start_date, end_date)


def download_oecd_yields(series_names, start_date="1990-01-01", end_date=None) -> pd.DataFrame:
    """
    Download OECD 10Y government bond yields from FRED.
    """
    return download_fred_series(series_names, start_date, end_date)