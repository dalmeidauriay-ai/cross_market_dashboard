# app/services/transforms.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------------------------------------
# Transforms for Stocks (Yahoo Finance data)
# ---------------------------------------------------------
# Responsibility: Take raw stock Close series and produce
# visualization‑ready DataFrames or Matplotlib figures.
# ---------------------------------------------------------

# =========================================================
# Snapshot table transform
# =========================================================
def compute_stock_snapshot_metrics(snapshot_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute snapshot metrics for a stock from current year closes:
    - Price (last close)
    - Daily % change (t-1 vs t-2)
    - Weekly % change (t-1 vs t-5)
    - Monthly % change (t-1 vs t-21)
    - YTD % change (last vs first of year)
    """
    closes = snapshot_df["Price"].ffill()
    if len(closes) < 2:
        return pd.DataFrame()

    price = closes.iloc[-1]
    daily = (closes.iloc[-1] / closes.iloc[-2] - 1) * 100 if len(closes) >= 2 else np.nan
    weekly = (closes.iloc[-1] / closes.iloc[-5] - 1) * 100 if len(closes) >= 5 else np.nan
    monthly = (closes.iloc[-1] / closes.iloc[-21] - 1) * 100 if len(closes) >= 21 else np.nan
    ytd = (closes.iloc[-1] / closes.iloc[0] - 1) * 100 if len(closes) >= 2 else np.nan

    return pd.DataFrame({
        "Price": [price],
        "DailyChange": [daily],
        "WeeklyChange": [weekly],
        "MonthlyChange": [monthly],
        "YTDChange": [ytd],
    })


# =========================================================
# Single stock performance timeseries
# =========================================================
def compute_stock_timeseries(history_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute enriched time series for a single stock:
    - Price
    - Return (% change)
    - Log return
    - 10-day moving average
    - 30-day moving average
    """
    price = history_df["Price"].ffill()
    returns = price.pct_change()
    log_returns = np.log(price / price.shift(1))
    ma10 = price.rolling(10).mean()
    ma30 = price.rolling(30).mean()

    return pd.DataFrame({
        "Price": price,
        "Return": returns,
        "LogReturn": log_returns,
        "MA10": ma10,
        "MA30": ma30,
    })


def plot_stock_timeseries(dataframe: pd.DataFrame, title: str,
                          y_label: str = "Price / Return",
                          series: list[str] | None = None):
    """
    Plot a single stock time series with optional selection of series
    (Price, Return, LogReturn, MA10, MA30).
    """
    if series:
        dataframe = dataframe[series]

    fig, ax = plt.subplots(figsize=(12, 6))
    dataframe.plot(ax=ax)
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    ax.tick_params(axis="both", labelsize=12)
    ax.legend(fontsize=12)
    fig.tight_layout()
    return fig


# Compute rolling annualized return & volatility

def compute_rolling_stats(price_series: pd.Series, windows=[252, 756, 2520], log_returns=True):
    """
    Compute rolling annualized mean return and volatility for a given price series.
    
    Parameters:
        price_series (pd.Series): Daily price series (indexed by Date).
        windows (list): List of rolling window lengths in trading days (default: [252, 756, 2520]).
        log_returns (bool): If True, use log returns; if False, use arithmetic returns.
    
    Returns:
        pd.DataFrame: DataFrame with columns for returns and rolling stats.
    """
    df = pd.DataFrame({"Price": price_series})
    if log_returns:
        df["ret"] = np.log(df["Price"] / df["Price"].shift(1))
    else:
        df["ret"] = df["Price"].pct_change()

    for w in windows:
        df[f"roll_mean_{w}"] = df["ret"].rolling(w).mean() * 252
        df[f"roll_vol_{w}"]  = df["ret"].rolling(w).std() * np.sqrt(252)

    return df

def compute_cumulative_returns(price_series: pd.Series, log_returns=True, freq='D'):
    """
    Compute cumulative returns since the start of the series, optionally resampled to a frequency.
    
    Parameters:
        price_series (pd.Series): Daily price series.
        log_returns (bool): If True, use log cumulative returns; if False, use arithmetic.
        freq (str): Resampling frequency ('D', 'W', 'M', 'Y').
    
    Returns:
        pd.Series: Cumulative returns series.
    """
    # Resample if needed
    if freq != 'D':
        price_series = price_series.resample(freq).last().dropna()
    
    if price_series.empty:
        return pd.Series(dtype=float)
    
    price_start = price_series.iloc[0]
    if log_returns:
        cum_ret = np.log(price_series / price_start)
    else:
        cum_ret = (price_series / price_start) - 1
    return cum_ret
def compute_stock_comparator_timeseries(history_dict: dict,
                                        log: bool = False) -> pd.DataFrame:
    """
    Compute returns or log returns for multiple stocks side by side.
    history_dict: {name: DataFrame with 'Price'}
    log: if True, compute log returns instead of simple returns
    """
    data = {}
    for name, df in history_dict.items():
        price = df["Price"].ffill()
        if log:
            data[name] = np.log(price / price.shift(1))
        else:
            data[name] = price.pct_change()
    return pd.DataFrame(data)


def plot_stock_comparator(cum_returns_dict: dict, log_returns: bool, title: str, benchmarks: list = []):
    """
    Plot cumulative returns for multiple stocks and benchmarks.
    cum_returns_dict: {name: Series of cumulative returns}
    log_returns: whether log or arithmetic
    benchmarks: list of benchmark names to style differently
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    for name, cum_ret in cum_returns_dict.items():
        if name in benchmarks:
            (cum_ret * 100).plot(ax=ax, label=name, linestyle='--', linewidth=2) if not log_returns else cum_ret.plot(ax=ax, label=name, linestyle='--', linewidth=2)
        else:
            if log_returns:
                cum_ret.plot(ax=ax, label=name)
            else:
                (cum_ret * 100).plot(ax=ax, label=name)
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    if log_returns:
        ax.set_ylabel("Cumulative Log Return", fontsize=14)
    else:
        ax.set_ylabel("Cumulative Return (%)", fontsize=14)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
    ax.axhline(0, color='black', linestyle='--')
    ax.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))
    fig.tight_layout()
    return fig




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
        return (1.0 / series).ffill()
    else:
        # Assume ticker is CCY/USD → already USD per CCY
        return series.ffill()


def build_fx_spot_and_change(ticker_map: dict, fetch_fn, period: str = "5d", interval: str = "1d"):
    """
    Given a map { 'CCY': 'YF_TICKER' }, build:
    - fx_matrix: spot conversion matrix (base/quote)
    - change_matrix: daily % change differential matrix (base minus quote)

    fetch_fn: callable(ticker, period, interval) -> pd.Series (Close series)
    """
    usd_per_ccy_last = {}
    usd_per_ccy_prev = {}
    currencies = []

    # Always include USD as base reference
    usd_per_ccy_last["USD"] = 1.0
    usd_per_ccy_prev["USD"] = 1.0
    currencies.append("USD")

    # Step 1: Normalize each currency to USD per unit
    for ccy, ticker in ticker_map.items():
        if ccy == "USD":
            continue  # already handled
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
    return series.resample(freq).last().ffill()


# =========================================================
# Page: FX (p3_fx) — Transformation: Build consolidated FX history
# Purpose: Download long-range FX history for all currency pairs,
# align them on a common datetime index, and return a wide DataFrame
# with one column per FX pair (friendly name).
# =========================================================

# Imports required for FX history transformation
from .tickers_mapping import FX_PAIRS
from .yf_client import download_fx_history_series

def build_fx_history_series() -> pd.DataFrame:
    """
    Build consolidated FX history for all pairs in FX_PAIRS.

    Workflow:
    - Loop through all FX pairs defined in FX_PAIRS.
    - Download full historical series from Yahoo Finance.
    - Keep only valid Series with a DateTime index.
    - Align all series on their datetime index.
    - Return a wide DataFrame with one column per FX pair (friendly name).

    Returns
    -------
    pd.DataFrame
        Wide DataFrame with one column per FX pair (friendly name).
    """
    all_series = {}
    for pair_name, ticker in FX_PAIRS.items():
        series = download_fx_history_series(ticker, period="max", interval="1d")

        # ✅ Only keep if it's a proper Series with a DateTime index
        if isinstance(series, pd.Series) and not series.empty:
            # Friendly name for the column (e.g. "USD/EUR")
            series = series.ffill()
            series.name = pair_name
            all_series[pair_name] = series
            print(f"✔ Added {pair_name} ({ticker}) with {len(series)} rows")
        else:
            print(f"⚠️ Skipping {pair_name} ({ticker}) — no data returned")

    if not all_series:
        raise ValueError("No FX history could be downloaded — check tickers or API.")

    # Align all series on their datetime index
    return pd.concat(all_series.values(), axis=1)





# ---------------------------------------------------------
# Transforms for Rates (FRED data)
# ---------------------------------------------------------
# Responsibility: Take raw FRED series and produce
# visualization‑ready DataFrames or Matplotlib figures.
# ---------------------------------------------------------


# =========================================================
# Generic line chart transform
# =========================================================

def plot_timeseries_lines(dataframe: pd.DataFrame, title: str,
                          y_label: str = "Yield (%)",
                          names: dict | None = None):
    """
    Plot time series lines with clean names and bigger fonts.
    """
    if names:
        dataframe = dataframe.rename(columns=names)

    fig, ax = plt.subplots(figsize=(12, 6))
    dataframe.plot(ax=ax)
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    ax.tick_params(axis="both", labelsize=12)
    ax.legend(fontsize=12, ncol=2)
    fig.tight_layout()
    return fig


# =========================================================
# OECD snapshot: horizontal bar
# =========================================================
def plot_oecd_snapshot(dataframe: pd.DataFrame, title: str,
                       y_label: str = "Yield (%)",
                       names: dict | None = None):
    """
    Plot OECD 10Y yields snapshot as a horizontal bar chart.
    """
    if names:
        dataframe = dataframe.rename(columns=names)

    latest = dataframe.ffill().iloc[-1].sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    latest.plot(kind="barh", ax=ax, color="skyblue", edgecolor="black")
    ax.set_title(title, fontsize=18)
    ax.set_xlabel(y_label, fontsize=14)
    ax.set_ylabel("")
    ax.tick_params(axis="both", labelsize=12)

    for i, v in enumerate(latest):
        ax.text(v + 0.05, i, f"{v:.2f}", va="center", fontsize=10)

    fig.tight_layout()
    return fig


# =========================================================
# U.S. yield curve snapshot
# =========================================================
def plot_us_yield_curve(dataframe: pd.DataFrame, title: str,
                        y_label: str = "Yield (%)",
                        names: dict | None = None):
    """
    Plot the latest U.S. yield curve snapshot as a line chart.
    """
    if names:
        dataframe = dataframe.rename(columns=names)

    latest = dataframe.ffill().iloc[-1]

    maturity_order = [
        "U.S. 1M Treasury", "U.S. 3M Treasury", "U.S. 6M Treasury",
        "U.S. 1Y Treasury", "U.S. 2Y Treasury", "U.S. 3Y Treasury",
        "U.S. 5Y Treasury", "U.S. 7Y Treasury", "U.S. 10Y Treasury",
        "U.S. 20Y Treasury", "U.S. 30Y Treasury"
    ]
    latest = latest.reindex(maturity_order)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(latest.index, latest.values, marker="o", linestyle="-", color="blue")
    ax.set_title(title, fontsize=18)
    ax.set_ylabel(y_label, fontsize=14)
    ax.set_xlabel("Maturity", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)

    # Rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    for i, v in enumerate(latest.values):
        ax.text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=10)

    fig.tight_layout()
    return fig
