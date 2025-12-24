# =========================================================
# Data Loader
# =========================================================
# Responsibility: Orchestrate fetch → transform → cache → load.
# Pages call here; they never touch raw APIs or files directly.
# =========================================================

import os
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------------------------------
# Imports from services
# ---------------------------------------------------------
from .transforms import (
    build_fx_spot_and_change,
    merge_fx_and_change,
    resample_fx_series,
    build_fx_history_series,
    compute_stock_snapshot_metrics,
    compute_stock_timeseries,
    compute_stock_comparator_timeseries,
)

from .yf_client import (
    download_close_fxmatrix_series,
    download_stock_history_series,
    download_stock_snapshot_series,
    download_index_snapshot_series,
    download_macro_yahoo_series,
    download_news,
)

from .fred_client import (
    download_us_yields, 
    download_oecd_yields,
    download_fred_series,
)

from .tickers_mapping import (
    FX_PAIRS, 
    US_YIELD_TICKERS, 
    OECD_YIELD_TICKERS,
    STOCK_TICKERS,
    STOCK_CURRENCIES,
    INDICES,
    MACRO_INDICATORS,
    COMMODITIES,
)


# ---------------------------------------------------------
# Cache paths
# ---------------------------------------------------------
STOCK_HISTORY_PATH = os.path.join("data", "processed", "stocks_history.csv")
STOCK_SNAPSHOT_PATH = os.path.join("data", "processed", "stocks_snapshot.csv")

FX_MATRIX_PROCESSED_PATH = os.path.join("data", "processed", "FX_rate_matrix.csv")
FX_HISTORY_PATH = os.path.join("data", "processed", "FX_historical.csv")

US_YIELDS_PATH = os.path.join("data", "processed", "us_yields.csv")
OECD_YIELDS_PATH = os.path.join("data", "processed", "oecd_yields.csv")

INDICES_SNAPSHOT_PATH = os.path.join("data", "processed", "indices_snapshot.csv")
INDICES_HISTORY_PATH = os.path.join("data", "processed", "indices_historical.csv")
MACRO_DATA_PATH = os.path.join("data", "processed", "macro_data.csv")
NEWS_DATA_PATH = os.path.join("data", "processed", "news_data.csv")

# =========================================================
# Stocks Snapshot Loader
# =========================================================
def load_stock_snapshot(force_refresh: bool = False) -> pd.DataFrame:
    """
    Load stock snapshot table (Price + % changes).
    - If force_refresh=False → load from existing CSV.
    - If force_refresh=True → fetch fresh data, transform, overwrite CSV.
    """
    # Check last update time
    tracker_path = os.path.join("data", "processed", "refresh_tracker.csv")
    if os.path.exists(tracker_path):
        tracker = pd.read_csv(tracker_path, index_col="csv_name")
        tracker["last_update"] = pd.to_datetime(tracker["last_update"])
        last_update_time = tracker.loc["stocks_snapshot.csv", "last_update"] if "stocks_snapshot.csv" in tracker.index else pd.Timestamp.min
        print(f"DEBUG: Loading stock data updated at {last_update_time}")
        if (datetime.now() - last_update_time.to_pydatetime()) > timedelta(hours=24):
            force_refresh = True

    if not force_refresh:
        df = pd.read_csv(STOCK_SNAPSHOT_PATH, index_col=0)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Price'}, inplace=True)
        return df

    # Fetch snapshot series for all tickers
    snapshot_frames = {}
    for name, ticker in STOCK_TICKERS.items():
        df = download_stock_snapshot_series(ticker)
        metrics = compute_stock_snapshot_metrics(df)
        metrics.insert(0, "Name", name)
        metrics.insert(1, "Ticker", ticker)
        snapshot_frames[name] = metrics

    merged = pd.concat(snapshot_frames.values(), ignore_index=True)
    merged.set_index('Price', inplace=True)
    merged.to_csv(STOCK_SNAPSHOT_PATH)
    merged.reset_index(inplace=True)
    return merged


def refresh_stock_snapshot() -> pd.DataFrame:
    """
    Force refresh of stock snapshot data.
    """
    return load_stock_snapshot(force_refresh=True)


# =========================================================
# Indices Snapshot Loader
# =========================================================
def load_indices_snapshot(force_refresh: bool = False) -> pd.DataFrame:
    """
    Load indices snapshot table (Price + % changes).
    - If force_refresh=False → load from existing CSV.
    - If force_refresh=True → fetch fresh data, transform, overwrite CSV.
    """
    if not force_refresh:
        df = pd.read_csv(INDICES_SNAPSHOT_PATH, index_col=0)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Price'}, inplace=True)
        return df

    # Fetch snapshot series for all indices
    snapshot_frames = {}
    for region, indices in INDICES.items():
        for name, ticker in indices.items():
            df = download_index_snapshot_series(ticker)
            metrics = compute_stock_snapshot_metrics(df)  # Reuse the function
            metrics.insert(0, "Name", name)
            metrics.insert(1, "Region", region)
            snapshot_frames[name] = metrics

    merged = pd.concat(snapshot_frames.values(), ignore_index=True)
    merged.set_index('Price', inplace=True)
    merged.to_csv(INDICES_SNAPSHOT_PATH)
    merged.reset_index(inplace=True)
    return merged


def refresh_indices_snapshot() -> pd.DataFrame:
    """
    Force refresh of indices snapshot data.
    """
    return load_indices_snapshot(force_refresh=True)


# =========================================================
# Macro Data Loader
# =========================================================
def load_macro_data(force_refresh: bool = False) -> dict:
    """
    Load macro indicators data.
    Returns a dict with processed data for display.
    """
    if not force_refresh:
        # For now, always refresh as it's not cached
        pass

    macro_data = {}

    # FRED data
    fred_series = []
    for category, items in MACRO_INDICATORS["FRED"].items():
        for name, code in items.items():
            fred_series.append(code)

    fred_df = download_fred_series(fred_series, start_date="2010-01-01")

    # Process GDP: quarterly, most recent vs previous year
    gdp_data = {}
    for country, code in MACRO_INDICATORS["FRED"]["GDP"].items():
        if code in fred_df.columns:
            series = fred_df[code].dropna()
            if not series.empty:
                latest = series.iloc[-1]
                prev_year = series.iloc[-5] if len(series) > 4 else series.iloc[0]  # approx 1 year ago
                change = (latest - prev_year) / prev_year * 100
                gdp_data[country] = {"value": latest, "change": change}

    macro_data["GDP"] = gdp_data

    # Process Inflation: YoY CPI change
    inflation_data = {}
    for name, code in MACRO_INDICATORS["FRED"]["Inflation"].items():
        if code in fred_df.columns:
            series = fred_df[code].dropna()
            if len(series) > 12:
                latest = series.iloc[-1]
                year_ago = series.iloc[-13]
                yoy = (latest - year_ago) / year_ago * 100
                inflation_data[name] = yoy

    macro_data["Inflation"] = inflation_data

    # Rates: latest
    rates_data = {}
    for name, code in MACRO_INDICATORS["FRED"]["Interest Rates"].items():
        if code in fred_df.columns:
            series = fred_df[code].dropna()
            if not series.empty:
                rates_data[name] = series.iloc[-1]

    macro_data["Rates"] = rates_data

    # Yahoo data
    yahoo_data = {}
    for category, items in MACRO_INDICATORS["Yahoo"].items():
        for name, ticker in items.items():
            df = download_macro_yahoo_series(ticker, period="1y")
            if not df.empty:
                latest = df["Price"].iloc[-1]
                yahoo_data[name] = latest

    macro_data["Yahoo"] = yahoo_data

    return macro_data


def load_news_data(ticker: str = "^GSPC", max_news: int = 50) -> list:
    """
    Load news headlines for a ticker.
    """
    return download_news(ticker, max_news)


# =========================================================
# Stocks Historical Loader
# =========================================================
def load_stock_timeseries(stock_name: str,
                          start_date: str = "2010-01-01",
                          end_date: str | None = None,
                          force_refresh: bool = False) -> pd.DataFrame:
    """
    Load historical time series for a given stock or index (friendly name).
    - If force_refresh=True → rebuild history, save CSV.
    - Otherwise → read from existing CSV.
    - Handles both stocks and indices.
    """
    from .tickers_mapping import STOCK_TICKERS, INDICES

    # Determine if it's a stock or index
    if stock_name in STOCK_TICKERS:
        # It's a stock
        if force_refresh:
            df = refresh_stock_history(start_date=start_date, end_date=end_date)
        else:
            df = pd.read_csv(STOCK_HISTORY_PATH, index_col=0, parse_dates=True)
        column_name = stock_name
    else:
        # Check if it's an index
        ticker = None
        for region in INDICES.values():
            if stock_name in region:
                ticker = region[stock_name]
                break
        if ticker is None:
            return pd.DataFrame()  # Not found

        if force_refresh:
            df = refresh_indices_history(start_date=start_date, end_date=end_date)
        else:
            df = pd.read_csv(INDICES_HISTORY_PATH, index_col=0, parse_dates=True)
        column_name = ticker  # Indices csv has tickers as columns

    if column_name not in df.columns:
        return pd.DataFrame()

    series = df[column_name]
    return compute_stock_timeseries(series.to_frame(name="Price"))

# =========================================================
# Stocks Comparator Loader
# =========================================================
def load_stock_comparator(stock_names: list[str],
                          log: bool = False,
                          force_refresh: bool = False) -> pd.DataFrame:
    """
    Load comparator time series for multiple stocks.
    - If force_refresh=True → rebuild history, save CSV.
    - Otherwise → read from existing CSV.
    - Returns DataFrame of returns/log returns for selected stocks.
    """
    # Refresh or load consolidated history
    if force_refresh:
        df = refresh_stock_history()
    else:
        df = pd.read_csv(STOCK_HISTORY_PATH, index_col=0, parse_dates=True)

    # Build dictionary of selected stocks
    history_dict = {}
    for stock in stock_names:
        if stock in df.columns:
            history_dict[stock] = df[stock].to_frame(name="Price")

    if not history_dict:
        return pd.DataFrame()

    # Compute comparator series (returns or log returns)
    comparator_df = compute_stock_comparator_timeseries(history_dict, log=log)
    return comparator_df

# =========================================================
# Stocks Historical Helper
# =========================================================
def refresh_stock_history(start_date: str = "2010-01-01",
                          end_date: str | None = None) -> pd.DataFrame:
    """
    Force rebuild of the entire stocks historical dataset.
    - Calls download_stock_history_series() for each ticker.
    - Normalizes prices to USD for non-US stocks.
    - Saves consolidated DataFrame to STOCK_HISTORY_PATH.
    - Returns the DataFrame.
    """
    from .yf_client import download_fx_history_series

    history_frames = {}
    for name, ticker in STOCK_TICKERS.items():
        df = download_stock_history_series(ticker, start=start_date, end=end_date)
        series = df.squeeze()   # single-column DataFrame → Series
        
        # Normalize to USD
        country = name.split('_')[-1]
        currency = STOCK_CURRENCIES.get(country, 'USD')
        if currency != 'USD':
            # Fetch FX rate: USD per currency
            fx_ticker = f"{currency}USD=X" if currency != 'EUR' else "EURUSD=X"  # EUR is special
            fx_series = download_fx_history_series(fx_ticker, period="max")
            if not fx_series.empty:
                # Resample FX to match series dates
                fx_resampled = fx_series.reindex(series.index, method='ffill')
                series = series / fx_resampled
        
        history_frames[name] = series

    merged = pd.DataFrame(history_frames)
    merged.to_csv(STOCK_HISTORY_PATH)
    print(f"✅ Stocks historical data refreshed and saved to {STOCK_HISTORY_PATH}")
    return merged


def refresh_stock_snapshot() -> pd.DataFrame:
    """
    Force rebuild of the stocks snapshot dataset.
    - Calls download_stock_snapshot_series() for each ticker.
    - Computes metrics, saves to STOCK_SNAPSHOT_PATH.
    - Returns the DataFrame.
    """
    snapshot_frames = []
    for name, ticker in STOCK_TICKERS.items():
        df = download_stock_snapshot_series(ticker)
        if not df.empty:
            metrics = compute_stock_snapshot_metrics(df)
            metrics["Name"] = name
            snapshot_frames.append(metrics)

    merged = pd.concat(snapshot_frames, ignore_index=True)
    merged.to_csv(STOCK_SNAPSHOT_PATH, index=False)
    print(f"✅ Stocks snapshot data refreshed and saved to {STOCK_SNAPSHOT_PATH}")
    return merged


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

    series = df[pair_name]
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

def load_us10y_yield(force_refresh: bool = False,
                     start_date: str = "1990-01-01",
                     end_date: str | None = None) -> pd.Series:
    """
    Convenience loader: return only the US 10Y Treasury yield series.
    """
    df = load_us_yields(force_refresh=force_refresh,
                        start_date=start_date,
                        end_date=end_date)
    # FRED code for 10Y is usually DGS10
    if "DGS10" in df.columns:
        return df["DGS10"].rename("US10Y")
    raise ValueError("10Y yield column not found in us_yields data.")


# =========================================================
# Indices Historical Loader
# =========================================================
def refresh_indices_history(start_date: str = "2010-01-01",
                            end_date: str | None = None) -> pd.DataFrame:
    """
    Force rebuild of the indices historical dataset.
    - Calls download_indices_history() for all indices tickers.
    - Saves consolidated DataFrame to INDICES_HISTORY_PATH.
    - Returns the DataFrame.
    """
    from .yf_client import download_indices_history
    from .tickers_mapping import INDICES

    # Flatten INDICES to get all tickers
    all_tickers = []
    for region in INDICES.values():
        all_tickers.extend(region.values())

    # Remove duplicates if any
    all_tickers = list(set(all_tickers))

    df = download_indices_history(all_tickers, start_date=start_date, end_date=end_date)
    if not df.empty:
        # Filter by date if provided
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        df.to_csv(INDICES_HISTORY_PATH)
        print(f"✅ Indices historical data refreshed and saved to {INDICES_HISTORY_PATH}")
    else:
        print("⚠️ No indices data downloaded")
    return df


# =========================================================
# Correlation Matrix Calculator
# =========================================================
def calculate_correlation_matrix(selected_stocks: list[str], selected_benchmarks: list[str], start_date: str, end_date: str, log_returns: bool = True) -> pd.DataFrame:
    """
    Calculate correlation matrix for stocks and benchmarks.
    Merges historical returns from stocks and indices, cleans NaNs, computes correlation.
    """
    # Load stocks data
    stocks_data = {}
    for stock in selected_stocks:
        df = load_stock_timeseries(stock, start_date="2000-01-01")
        if not df.empty and 'Price' in df.columns:
            price_series = df["Price"].loc[start_date:end_date]
            returns = compute_cumulative_returns(price_series, log_returns=log_returns, freq='D')
            stocks_data[stock] = returns

    # Load benchmarks data
    benchmarks_data = {}
    for bench in selected_benchmarks:
        df = load_stock_timeseries(bench, start_date="2000-01-01")
        if not df.empty and 'Price' in df.columns:
            price_series = df["Price"].loc[start_date:end_date]
            returns = compute_cumulative_returns(price_series, log_returns=log_returns, freq='D')
            benchmarks_data[bench] = returns

    # Combine all data
    all_data = {**stocks_data, **benchmarks_data}
    if not all_data:
        return pd.DataFrame()

    # Create DataFrame and drop NaNs
    combined_df = pd.DataFrame(all_data)
    combined_df = combined_df.dropna()

    if combined_df.empty:
        return pd.DataFrame()

    # Compute correlation
    corr_matrix = combined_df.corr()
    return corr_matrix