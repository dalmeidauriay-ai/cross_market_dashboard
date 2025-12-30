# =========================================================
# Data Loader
# =========================================================
# Responsibility: Orchestrate fetch → transform → cache → load.
# Pages call here; they never touch raw APIs or files directly.
# =========================================================

import os
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import datetime as dt

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
    compute_cumulative_returns,
    build_gdp_monitor_table,
    build_gdp_comparison_tables,
    compute_cross_asset_table,

)

from .yf_client import (
    download_close_fxmatrix_series,
    download_stock_history_series,
    download_stock_snapshot_series,
    download_index_snapshot_series,
)

from .fred_client import (
    download_us_yields, 
    download_oecd_yields,
    download_fred_series,
)

from .tickers_mapping import (
    US_YIELD_TICKERS, 
    OECD_YIELD_TICKERS,
    STOCK_TICKERS,
    STOCK_CURRENCIES,
    INDICES,
    MONETARY_POLICY_TICKERS,
    COMMODITY_GROUPS, 
    COMMODITY_FUTURES_CONFIG, 
    FUTURE_MONTH_MAP
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
# Monetary Policy Loader (Robust Local CSV)
# =========================================================
def refresh_monetary_policy() -> None:
    """
    Downloads the latest data for US and EU policy from FRED
    and saves them as individual raw CSVs in data/raw/.
    """
    raw_dir = os.path.join("data", "raw")
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
        
    # We fetch 3 years to ensure we have enough history for YoY calculations (-13 months)
    start_date = (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d')
    
    print("  -> Refreshing Monetary Policy Data...")
    
    for region, tickers in MONETARY_POLICY_TICKERS.items():
        for name, code in tickers.items():
            try:
                # Download single series to avoid index collisions
                df = download_fred_series([code], start_date=start_date)
                if not df.empty:
                    # Naming convention: Region_Key_Ticker.csv
                    filename = f"{region}_{name}_{code}.csv"
                    path = os.path.join(raw_dir, filename)
                    df.to_csv(path)
            except Exception as e:
                print(f"⚠️ Error refreshing {region} {name}: {e}")

# ==========================
# Monetary Policy Raw Loader
# ==========================
def load_monetary_policy_raw() -> dict:
    """
    Loads the raw CSVs from data/raw/ into a dictionary of DataFrames.
    This function DOES NOT compute metrics; it just retrieves the files.
    """
    raw_dir = os.path.join("data", "raw")
    data = {}
    
    for region, tickers in MONETARY_POLICY_TICKERS.items():
        data[region] = {}
        for name, code in tickers.items():
            filename = f"{region}_{name}_{code}.csv"
            path = os.path.join(raw_dir, filename)
            
            if os.path.exists(path):
                # Parse dates to ensure index is DatetimeIndex
                data[region][name] = pd.read_csv(path, index_col=0, parse_dates=True)
            else:
                data[region][name] = pd.DataFrame() # Empty if missing
                
    return data


# =========================================================
# Cross-Asset Snapshot Loader
# =========================================================

def refresh_cross_asset_snapshot():
    """Download raw data and save the processed snapshot table."""
    from .tickers_mapping import CROSS_ASSET_TICKERS
    
    raw_dir = os.path.join("data", "raw")
    
    # 1. Download
    data_map = {}
    for name, (ticker, unit) in CROSS_ASSET_TICKERS.items():
        df = download_stock_snapshot_series(ticker)
        data_map[ticker] = df
    
    # 2. Save Individual Raw Files (standard behavior)
    raw_series_dict = {}
    for ticker, df in data_map.items():
        safe_name = ticker.replace("^", "").replace("=", "").replace("/", "")
        df.to_csv(os.path.join(raw_dir, f"cross_{safe_name}.csv"))
        raw_series_dict[ticker] = df["Close"] if "Close" in df.columns else df.iloc[:,0]

    # 3. Compute and Save the Processed Snapshot
    final_df = compute_cross_asset_table(raw_series_dict)
    if not final_df.empty:
        final_df.to_csv(os.path.join("data", "processed", "cross_asset_snapshot.csv"), index=False)

def load_cross_asset_snapshot():
    path = os.path.join("data", "processed", "cross_asset_snapshot.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()




# =========================================================
# GDP Loader
# =========================================================
def load_gdp_refined(force_refresh: bool = False) -> pd.DataFrame:
    """
    Loads FRED GDP data and transforms it into the Monitor Table format.
    Returns DataFrame: [Country, GDP Current ($B), GDP Prev ($B), Change, Current Q, Prev Q]
    """
    # 1. Load raw GDP series from FRED
    from .tickers_mapping import MACRO_INDICATORS
    gdp_codes = list(MACRO_INDICATORS["FRED"]["GDP"].values())
    raw_data = {}
    fred_df = download_fred_series(gdp_codes, start_date="2010-01-01")
    for code in gdp_codes:
        if code in fred_df.columns:
            raw_data[code] = fred_df[code]
    
    # 2. Transform into the table
    # We don't need FX matrix for this specific table as user requested USD Nominal
    gdp_table = build_gdp_monitor_table(raw_data)
    
    return gdp_table


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
    from .tickers_mapping import FX_MATRIX_TICKERS
    default_tickers = FX_MATRIX_TICKERS

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

# =========================================================
# GDP Comparison Loader
# =========================================================
def load_gdp_comparison(force_refresh=False):
    """
    Orchestrates fetching GDP data and generating the comparison tables.
    Uses FX_historical.csv as the source for latest exchange rates.
    Returns: (df_local, df_usd)
    """
    # 1. Define Tickers
    from .tickers_mapping import GDP_COMPARISON_TICKERS
    country_tickers = GDP_COMPARISON_TICKERS

    # 2. Fetch Raw Data (FRED)
    raw_data = {}
    for country, ticker in country_tickers.items():
        df = download_fred_series([ticker])
        if not df.empty:
            raw_data[country] = df

    # 3. Load FX Rates from Historical Data (The "Robust" Source)
    # On va chercher la dernière ligne du fichier historique
    fx_path = os.path.join("data", "processed", "FX_historical.csv")
    fx_rates = pd.Series(dtype=float)
    
    if os.path.exists(fx_path):
        try:
            df_hist = pd.read_csv(fx_path, index_col=0)
            if not df_hist.empty:
                # On prend la toute dernière ligne (les taux les plus récents)
                fx_rates = df_hist.iloc[-1]
                # Optionnel: on s'assure que l'index est propre
                fx_rates.index = fx_rates.index.str.strip()
        except Exception as e:
            print(f"Error loading FX Historical for GDP: {e}")

    # 4. Transform
    # build_gdp_comparison_tables utilisera maintenant ces taux numériques
    df_local, df_usd = build_gdp_comparison_tables(raw_data, fx_rates)
    
    return df_local, df_usd






# =========================================================
# Commodity Data Loader
# =========================================================

PROCESSED_DIR = os.path.join("data", "processed")

def refresh_commodity_history():
    """Downloads historical data for Metals, Energy, and Agri."""
    start_date = "2015-01-01"
    
    for group_name, tickers in COMMODITY_GROUPS.items():
        print(f"--- Downloading Commodity Group: {group_name} ---")
        group_df = pd.DataFrame()
        
        for name, ticker in tickers.items():
            try:
                # Use standard yfinance download
                data = yf.download(ticker, start=start_date, progress=False)
                if not data.empty:
                    # Handle MultiIndex headers in newer yfinance
                    if 'Adj Close' in data.columns:
                        col = data['Adj Close']
                    elif 'Close' in data.columns:
                        col = data['Close']
                    else:
                        continue
                    
                    if isinstance(col, pd.DataFrame):
                        col = col.iloc[:, 0]
                        
                    group_df[name] = col
            except Exception as e:
                print(f"Error downloading {name}: {e}")
                
        if not group_df.empty:
            group_df.sort_index(inplace=True)
            group_df.ffill(inplace=True)
            # Save: data/processed/hist_metals.csv
            filepath = os.path.join(PROCESSED_DIR, f"hist_{group_name.lower()}.csv")
            group_df.to_csv(filepath)
            print(f"✅ Saved {filepath}")

def refresh_commodity_futures():
    """Scans for futures contracts to build forward curves."""
    today = dt.date.today()
    start_date = (today - dt.timedelta(days=10)).strftime("%Y-%m-%d")
    
    futures_dir = os.path.join(PROCESSED_DIR, "futures_curves")
    if not os.path.exists(futures_dir):
        os.makedirs(futures_dir)

    for name, config in COMMODITY_FUTURES_CONFIG.items():
        chain_data = []
        current_year_short = int(today.strftime("%y"))
        # Check this year and next year
        years = [current_year_short, current_year_short + 1]
        
        for year in years:
            for m_code in config["months"]:
                ticker = f"{config['root']}{m_code}{year}{config['suffix']}"
                try:
                    df = yf.download(ticker, start=start_date, progress=False)
                    if not df.empty:
                        # Get last available price
                        if 'Close' in df.columns:
                            val = df['Close'].iloc[-1]
                            # Handle scalar or series
                            if isinstance(val, pd.Series): val = val.iloc[0]
                            
                            last_price = float(val)
                            
                            # Create a sortable date for the delivery month
                            # Year 20xx, Month Index + 1, Day 1
                            month_idx = list(FUTURE_MONTH_MAP.keys()).index(m_code) + 1
                            sort_date = dt.datetime(2000+year, month_idx, 1)
                            
                            chain_data.append({
                                "Date": sort_date,
                                "Contract": ticker,
                                "Delivery": f"{FUTURE_MONTH_MAP[m_code]} ' {year}",
                                "Price": last_price
                            })
                except Exception:
                    continue

        if chain_data:
            res_df = pd.DataFrame(chain_data).sort_values("Date")
            filename = f"curve_{name.lower().replace(' ', '_')}.csv"
            res_df.to_csv(os.path.join(futures_dir, filename), index=False)
            print(f"✅ Saved Curve: {name}")



# PROCESSED_DIR = os.path.join("data", "processed")
# if not os.path.exists(PROCESSED_DIR):
#     os.makedirs(PROCESSED_DIR)

# def update_commodity_history():
#     """Télécharge l'historique long terme (ex-test.py)"""
#     start_date = "2010-01-01"
    
#     for group, tickers in COMMODITY_HISTORICAL_TICKERS.items():
#         print(f"--- Downloading Historical Group: {group} ---")
#         group_df = pd.DataFrame()
        
#         for name, ticker in tickers.items():
#             try:
#                 data = yf.download(ticker, start=start_date, progress=False)
#                 if not data.empty:
#                     # Gestion version yfinance (MultiIndex ou pas)
#                     if 'Adj Close' in data.columns:
#                         col = data['Adj Close']
#                     elif 'Close' in data.columns:
#                         col = data['Close']
#                     else:
#                         continue
                        
#                     # Si c'est un DataFrame à une colonne, on prend la série
#                     if isinstance(col, pd.DataFrame):
#                         col = col.iloc[:, 0]
                        
#                     group_df[name] = col
#             except Exception as e:
#                 print(f"Error downloading {name}: {e}")
                
#         if not group_df.empty:
#             group_df.sort_index(inplace=True)
#             group_df.ffill(inplace=True)
            
#             # Sauvegarde : data/processed/hist_metals.csv
#             filename = f"hist_{group.lower()}.csv"
#             filepath = os.path.join(PROCESSED_DIR, filename)
#             group_df.to_csv(filepath)
#             print(f"✅ Saved {filename}")

# def update_commodity_futures_curves():
#     """Télécharge les courbes forward (ex-test4.py)"""
#     today = dt.date.today()
#     # Fenêtre courte pour avoir le dernier prix
#     start_date = (today - dt.timedelta(days=10)).strftime("%Y-%m-%d")
    
#     # Sous-dossier pour ne pas polluer la racine processed
#     futures_dir = os.path.join(PROCESSED_DIR, "futures_curves")
#     if not os.path.exists(futures_dir):
#         os.makedirs(futures_dir)

#     for name, config in COMMODITY_FUTURES_CONFIG.items():
#         print(f"--- Scanning Futures Chain for {name} ---")
#         chain_data = []
        
#         # Année en cours et suivante
#         current_year_short = int(today.strftime("%y"))
#         years = [current_year_short, current_year_short + 1]
        
#         for year in years:
#             for m_code in config["months"]:
#                 ticker = f"{config['root']}{m_code}{year}{config['suffix']}"
#                 try:
#                     df = yf.download(ticker, start=start_date, progress=False, group_by='ticker')
                    
#                     if not df.empty:
#                         # Extraction du dernier prix
#                         if 'Close' in df.columns:
#                             last_price = df['Close'].iloc[-1]
#                         else:
#                             # Gestion MultiIndex (Ticker, Close)
#                             try:
#                                 last_price = df.iloc[-1, df.columns.get_loc((ticker, 'Close'))]
#                             except:
#                                 last_price = df.iloc[-1, 0] # Fallback brutal

#                         if pd.notnull(last_price):
#                             # Date artificielle pour le tri
#                             sort_date = dt.datetime(2000+year, list(FUTURE_MONTH_MAP.keys()).index(m_code)+1, 1)
                            
#                             chain_data.append({
#                                 "Date": sort_date,
#                                 "Contract": ticker,
#                                 "Delivery": f"{FUTURE_MONTH_MAP[m_code]} 20{year}",
#                                 "Price": round(float(last_price), 2)
#                             })
#                 except Exception:
#                     continue

#         if chain_data:
#             res_df = pd.DataFrame(chain_data).sort_values("Date")
#             filename = f"curve_{name.lower().replace(' ', '_')}.csv"
#             filepath = os.path.join(futures_dir, filename)
#             res_df.to_csv(filepath, index=False)
#             print(f"✅ Saved Curve: {filename}")
#         else:
#             print(f"⚠️ No curve data for {name}")

# def run_full_update():
#     """Fonction wrapper pour tout mettre à jour"""
#     print("🚀 Starting Commodity Data Update...")
#     update_commodity_history()
#     update_commodity_futures_curves()
#     print("🏁 Update Complete.")
