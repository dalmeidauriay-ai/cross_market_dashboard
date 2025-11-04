# app/services/transforms.py

import pandas as pd
import numpy as np

# ---------------------------------------------------------
# FX transforms
# ---------------------------------------------------------
# Responsibility: Convert raw FX quotes to USD-per-CCY,
# build spot and % change matrices, and merge them for display.
# Also includes helpers for resampling FX time series.
# This module does not fetch data itself; it only transforms.


# =========================================================
# Page: FX (p3_fx) — Figure: FX spot + % change matrix
# Purpose: Normalize FX quotes, build spot and % change matrices,
# and merge them into a display-ready DataFrame.
# =========================================================

def normalize_to_usd_per_unit(ccy: str, ticker: str, series: pd.Series) -> pd.Series:
    """
    Normalize any FX series to USD per 1 unit of the currency 'ccy'.

    Assumptions for common Yahoo tickers:
    - 'EURUSD=X', 'GBPUSD=X', 'CHFUSD=X' are USD per 1 EUR/GBP/CHF → already USD/CCY.
    - 'JPY=X' is USD/JPY (number of JPY per 1 USD) → invert to get USD per 1 JPY.
    """
    if ccy.upper() == "JPY" and ticker.upper() == "JPY=X":
        # JPY=X is USD/JPY → invert to get USD per 1 JPY
        return (1.0 / series).dropna()
    else:
        # Assume ticker is CCY/USD → already USD per CCY
        return series.dropna()


def build_fx_spot_and_change(ticker_map: dict, fetch_fn, period: str = "5d", interval: str = "1d"):
    """
    Given a map { 'CCY': 'YF_TICKER' }, build:
    - fx_matrix: spot conversion matrix (base/quote)
    - change_matrix: daily % change differential matrix (base minus quote)

    fetch_fn: callable(ticker, period, interval) -> pd.Series (Close series)
    """
    usd_per_ccy_last = {"USD": 1.0}
    usd_per_ccy_prev = {"USD": 1.0}
    currencies = ["USD"]

    # Step 1: Normalize each currency to USD per unit
    for ccy, ticker in ticker_map.items():
        try:
            raw = fetch_fn(ticker, period=period, interval=interval)
            if raw.empty:
                raise ValueError("No data returned")

            norm = normalize_to_usd_per_unit(ccy, ticker, raw)

            last = norm.iloc[-1]
            usd_per_ccy_last[ccy] = float(last)

            if len(norm) > 1:
                prev = norm.iloc[-2]
                usd_per_ccy_prev[ccy] = float(prev)
            else:
                usd_per_ccy_prev[ccy] = np.nan

            currencies.append(ccy)
        except Exception:
            usd_per_ccy_last[ccy] = np.nan
            usd_per_ccy_prev[ccy] = np.nan
            currencies.append(ccy)

    # Step 2: Build spot conversion matrix
    fx_matrix = pd.DataFrame(index=currencies, columns=currencies, dtype=float)
    for base in currencies:
        for quote in currencies:
            a = usd_per_ccy_last.get(base, np.nan)
            b = usd_per_ccy_last.get(quote, np.nan)
            fx_matrix.loc[base, quote] = (a / b) if (pd.notna(a) and pd.notna(b)) else np.nan
    fx_matrix = fx_matrix.round(4)

    # Step 3: Compute % change per currency vs USD
    pct_change = {}
    for ccy in currencies:
        last = usd_per_ccy_last.get(ccy, np.nan)
        prev = usd_per_ccy_prev.get(ccy, np.nan)
        if pd.notna(last) and pd.notna(prev) and prev != 0:
            pct_change[ccy] = (last - prev) / prev * 100.0
        else:
            pct_change[ccy] = np.nan

    # Step 4: Build % change differential matrix
    change_matrix = pd.DataFrame(index=currencies, columns=currencies, dtype=float)
    for base in currencies:
        for quote in currencies:
            cb = pct_change.get(base, np.nan)
            cq = pct_change.get(quote, np.nan)
            change_matrix.loc[base, quote] = (cb - cq) if (pd.notna(cb) and pd.notna(cq)) else np.nan
    change_matrix = change_matrix.round(2)

    return fx_matrix, change_matrix


def merge_fx_and_change(fx_matrix: pd.DataFrame, change_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Merge FX spot rates and % change into a single DataFrame with formatted strings.
    Example cell: '1.1675 (+0.32%)'
    """
    merged = fx_matrix.copy().astype(str)

    for row in fx_matrix.index:
        for col in fx_matrix.columns:
            spot = fx_matrix.loc[row, col]
            change = change_matrix.loc[row, col]

            if pd.notna(spot) and pd.notna(change):
                merged.loc[row, col] = f"{spot:.4f} ({change:+.2f}%)"
            elif pd.notna(spot):
                merged.loc[row, col] = f"{spot:.4f}"
            else:
                merged.loc[row, col] = "NaN"

    return merged


# =========================================================
# Page: FX (p3_fx) — Figure: Time series line chart
# Purpose: Resample long-range FX history into different frequencies
# (daily, weekly, monthly, yearly) for visualization.
# =========================================================

def resample_fx_series(series: pd.Series, freq: str) -> pd.Series:
    """
    Resample a daily FX series into a different frequency.
    freq options:
      - 'D' : daily (no change)
      - 'W' : weekly (last value of week)
      - 'M' : monthly (last value of month)
      - 'Y' : yearly (last value of year)
    """
    if freq == "D":
        return series
    return series.resample(freq).last().dropna()