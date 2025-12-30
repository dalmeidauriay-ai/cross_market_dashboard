# app/services/yf_client.py

"""
    Two type of data: Snapshot and Historical.

-> Historical:
Download long-range history for a given ticker.

Default: full history ('max') at daily frequency.
For FX, 'Close' and 'Adj Close' are equivalent. We prefer 'Adj Close'
if available, otherwise fall back to 'Close'.
For Stock, 'Close' is preferred becaus 'Adj Close' only exits some few US stocks.

Handles both flat and MultiIndex column formats returned by yfinance.

Returns
-------
pd.Series
    Series of prices indexed by datetime.



-> Snapshot:
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

import yfinance as yf
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Yahoo Finance client helpers
# ---------------------------------------------------------
# Responsibility: Fetch raw series from Yahoo Finance.
# No transformations here beyond basic cleaning.
# ---------------------------------------------------------

# =========================================================
# Page: Stocks (p3_stocks) — Historical data.
# =========================================================
def download_stock_history_series(ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    """
    Download historical raw close prices for a stock from Yahoo Finance.
    For European/Global tickers (.PA, .T), use auto_adjust=False and prefer 'Close'.
    For others, use auto_adjust=True and prefer 'Adj Close', fallback to 'Close'.
    """
    # For European/Global tickers, use auto_adjust=False and prefer 'Close'
    if ticker.endswith('.PA') or ticker.endswith('.T'):
        auto_adjust = False
        prefer_adj = False
    else:
        auto_adjust = True
        prefer_adj = True

    df = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        progress=False,
        auto_adjust=auto_adjust
    )

    # Handle MultiIndex (common when fetching single tickers)
    if isinstance(df.columns, pd.MultiIndex):
        if prefer_adj and ("Adj Close", ticker) in df.columns:
            series = df[("Adj Close", ticker)].astype(float)
            if series.dropna().empty:
                # Fallback to Close
                if ("Close", ticker) in df.columns:
                    series = df[("Close", ticker)].astype(float)
        elif ("Close", ticker) in df.columns:
            series = df[("Close", ticker)].astype(float)
        else:
            return pd.DataFrame(columns=["Price"])
    else:
        if prefer_adj and "Adj Close" in df.columns:
            series = df["Adj Close"].astype(float)
            if series.dropna().empty:
                # Fallback to Close
                if "Close" in df.columns:
                    series = df["Close"].astype(float)
        elif "Close" in df.columns:
            series = df["Close"].astype(float)
        else:
            return pd.DataFrame(columns=["Price"])

    series.name = "Price"
    return series.to_frame()



# =========================================================
# Page: Stocks (p3_stocks) — Snapshot data.
# =========================================================
def download_stock_snapshot_series(ticker: str) -> pd.DataFrame:
    """
    Download current year raw close prices for a stock.
    For European/Global tickers (.PA, .T), use auto_adjust=False and prefer 'Close'.
    For others, use auto_adjust=True and prefer 'Adj Close', fallback to 'Close'.
    """
    start = pd.to_datetime("today").replace(month=1, day=1)
    end = pd.to_datetime("today")

    # For European/Global tickers, use auto_adjust=False and prefer 'Close'
    if ticker.endswith('.PA') or ticker.endswith('.T'):
        auto_adjust = False
        prefer_adj = False
    else:
        auto_adjust = True
        prefer_adj = True

    df = yf.download(
        ticker,
        start=start,
        end=end,
        interval="1d",
        progress=False,
        auto_adjust=auto_adjust
    )

    if isinstance(df.columns, pd.MultiIndex):
        if prefer_adj and ("Adj Close", ticker) in df.columns:
            series = df[("Adj Close", ticker)].astype(float)
            if series.dropna().empty:
                # Fallback to Close
                if ("Close", ticker) in df.columns:
                    series = df[("Close", ticker)].astype(float)
        elif ("Close", ticker) in df.columns:
            series = df[("Close", ticker)].astype(float)
        else:
            return pd.DataFrame(columns=["Price"])
    else:
        if prefer_adj and "Adj Close" in df.columns:
            series = df["Adj Close"].astype(float)
            if series.dropna().empty:
                # Fallback to Close
                if "Close" in df.columns:
                    series = df["Close"].astype(float)
        elif "Close" in df.columns:
            series = df["Close"].astype(float)
        else:
            return pd.DataFrame(columns=["Price"])

    series.name = "Price"
    return series.to_frame()



# =========================================================
# Page: Overview (p1_overview) — Index Snapshot data.
# =========================================================
def download_index_snapshot_series(ticker: str) -> pd.DataFrame:
    """
    Download current year raw close prices for an index.
    Prefer 'Close' for indices.
    """
    start = pd.to_datetime("today").replace(month=1, day=1)
    end = pd.to_datetime("today")

    df = yf.download(
        ticker,
        start=start,
        end=end,
        interval="1d",
        progress=False,
        auto_adjust=False  # Indices typically use Close
    )

    if isinstance(df.columns, pd.MultiIndex):
        if ("Close", ticker) in df.columns:
            series = df[("Close", ticker)].astype(float)
        else:
            return pd.DataFrame(columns=["Price"])
    else:
        if "Close" in df.columns:
            series = df["Close"].astype(float)
        else:
            return pd.DataFrame(columns=["Price"])

    series.name = "Price"
    return series.to_frame()



# =========================================================
# Page: Overview (p1_overview) — Macro Yahoo data.
# =========================================================
def download_macro_yahoo_series(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """
    Download macro series from Yahoo Finance.
    """
    try:
        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True
        )

        if isinstance(df.columns, pd.MultiIndex):
            if ("Close", ticker) in df.columns:
                series = df[("Close", ticker)].astype(float)
            else:
                return pd.DataFrame(columns=["Price"])
        else:
            if "Close" in df.columns:
                series = df["Close"].astype(float)
            else:
                return pd.DataFrame(columns=["Price"])

        series.name = "Price"
        return series.to_frame()
    except Exception as e:
        print(f"⚠️ Skipping {ticker}: {e}")
        return pd.DataFrame(columns=["Price"])



# =========================================================
# Page: Stocks (p2_stocks) — Indices Historical data.
# =========================================================
def download_indices_history(tickers: list, start_date: str = "2010-01-01", end_date: str = None) -> pd.DataFrame:
    """
    Download historical data for multiple indices from Yahoo Finance.
    Uses Adj Close with fallback to Close for consistency.
    """
    try:
        df = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        # Handle MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            # Extract Adj Close or Close for each ticker
            series_dict = {}
            for ticker in tickers:
                if ("Adj Close", ticker) in df.columns:
                    series = df[("Adj Close", ticker)].astype(float)
                    if series.dropna().empty:
                        if ("Close", ticker) in df.columns:
                            series = df[("Close", ticker)].astype(float)
                elif ("Close", ticker) in df.columns:
                    series = df[("Close", ticker)].astype(float)
                else:
                    continue  # Skip this ticker
                series_dict[ticker] = series

            result_df = pd.DataFrame(series_dict)
        else:
            # Single ticker case, but since we pass list, unlikely
            result_df = df

        return result_df.dropna(how='all')
    except Exception as e:
        print(f"⚠️ Error downloading indices history: {e}")
        return pd.DataFrame()



# =========================================================
# Page: FX (p3_fx) — Snapshot data.
# =========================================================
def download_close_fxmatrix_series(ticker: str, period: str = "5d", interval: str = "1d") -> pd.Series:

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
# Page: FX (p3_fx) — Historical data.
# =========================================================
def download_fx_history_series(ticker: str, period: str = "max", interval: str = "1d") -> pd.Series:

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