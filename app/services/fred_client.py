# app/services/fred_client.py

import pandas as pd

# ---------------------------------------------------------
# FRED client helpers
# ---------------------------------------------------------
# Responsibility: Fetch raw series from FRED.
# No transformations here beyond basic cleaning (e.g. ffill).
# ---------------------------------------------------------

# ---------------------------------------------------------
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
            url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}"
            df = pd.read_csv(url, index_col=0, parse_dates=True)
            df.columns = [s]
            # Filter by date
            df = df[df.index >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df.index <= pd.to_datetime(end_date)]
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