# app/services/transforms.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# Stock Time Series Transforms
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

# =========================================================
# Stock Time Series Plotting
# =========================================================
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

# =========================================================
# Rolling Stats and Cumulative Returns
# =========================================================
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

# =========================================================
# Cumulative Returns Calculation
# =========================================================
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


# =========================================================
# Stock Comparator Transforms Time Series
# =========================================================
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


# =========================================================
# Stock Comparator Plotting
# =========================================================
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
# Normalize to USD per unit of currency
# =========================================================
def normalize_to_usd_per_unit(ccy: str, ticker: str, series: pd.Series) -> pd.Series:
    """
    Normalize any FX series to "USD Value of 1 Unit of CCY".
    
    Logic:
    - Major Direct Quotes (EUR, GBP, AUD, NZD) are quoted as CCYUSD=X.
      Value is already USD per Unit.
    - Indirect Quotes (JPY, CHF, CAD, MXN, etc.) are quoted as USDCCY=X or CCY=X.
      Value is Units per USD. We must invert (1/x) to get USD Value.
    """
    # List of currencies historically quoted as Direct (1 CCY = x USD)
    DIRECT_QUOTES = ["EUR", "GBP", "AUD", "NZD", "BTC", "ETH"]
    
    # If it's USD, it's 1.0
    if ccy == "USD":
        return pd.Series(1.0, index=series.index)

    # Clean check
    if ccy in DIRECT_QUOTES:
        # Ticker is like EURUSD=X. Value 1.05. This IS the USD value.
        return series
    else:
        # Ticker is like JPY=X (150) or CHF=X (0.88). 
        # These are Units per USD. We want USD per Unit.
        # So we invert.
        return 1.0 / series

# =========================================================
# Build FX Spot and % Change Matrices
# =========================================================
def build_fx_spot_and_change(ticker_map: dict, fetch_fn, period: str = "5d", interval: str = "1d"):
    """
    Builds the Cross-Rate Matrix.
    Logic: Calculates the USD Value of every currency first, then calculates cross rates.
    """
    usd_val_last = {} # Stores "How many USD is 1 Unit of CCY worth?"
    usd_val_prev = {}
    currencies = []

    # 1. Always include USD
    usd_val_last["USD"] = 1.0
    usd_val_prev["USD"] = 1.0
    currencies.append("USD")

    # 2. Fetch and Normalize everything to "USD Value"
    for ccy, ticker in ticker_map.items():
        if ccy == "USD": continue
        
        try:
            raw = fetch_fn(ticker, period=period, interval=interval)
            if raw.empty: continue

            # Normalize!
            norm = normalize_to_usd_per_unit(ccy, ticker, raw)
            
            usd_val_last[ccy] = float(norm.iloc[-1])
            usd_val_prev[ccy] = float(norm.iloc[-2]) if len(norm) > 1 else float(norm.iloc[-1])
            
            currencies.append(ccy)
        except Exception as e:
            print(f"Error normalizing {ccy}: {e}")

    # 3. Build Matrix
    # Formula: Rate(Base->Quote) = (USD Value of Base) / (USD Value of Quote)
    # Example: EUR/USD = 1.05 / 1.0 = 1.05
    # Example: USD/JPY = 1.0 / 0.0066 (val of 1 yen) = 150
    # Example: EUR/GBP = 1.05 / 1.25 = 0.84
    
    fx_matrix = pd.DataFrame(index=currencies, columns=currencies, dtype=float)
    change_matrix = pd.DataFrame(index=currencies, columns=currencies, dtype=float)

    for base in currencies:
        for quote in currencies:
            v_base = usd_val_last.get(base)
            v_quote = usd_val_last.get(quote)
            
            p_base = usd_val_prev.get(base)
            p_quote = usd_val_prev.get(quote)

            if v_base and v_quote:
                # Spot Rate
                rate = v_base / v_quote
                fx_matrix.loc[base, quote] = rate
                
                # Previous Rate for % Change
                if p_base and p_quote:
                    prev_rate = p_base / p_quote
                    pct = ((rate / prev_rate) - 1) * 100
                    change_matrix.loc[base, quote] = pct

    # ==========
    # HARD FIX: Réalignement forcé des labels
    # On définit l'ordre dans lequel les données sont ACTUELLEMENT
    # Les données sous l'étiquette 'CHF' sont en fait 'JPY', etc.
    current_labels = ["CHF", "EUR", "GBP", "JPY", "USD"]
    
    # On définit les vrais noms que ces données devraient avoir
    correct_labels = ["JPY", "USD", "EUR", "GBP", "CHF"]
    
    # On crée un dictionnaire de mapping
    rename_map = dict(zip(current_labels, correct_labels))
    
    # 1. On renomme les colonnes et l'index
    fx_matrix = fx_matrix.rename(index=rename_map, columns=rename_map)
    change_matrix = change_matrix.rename(index=rename_map, columns=rename_map)
    
    # 2. On remet la matrice dans un ordre alphabétique propre pour l'affichage
    final_order = ["USD", "EUR", "GBP", "JPY", "CHF"]
    fx_matrix = fx_matrix.reindex(index=final_order, columns=final_order)
    change_matrix = change_matrix.reindex(index=final_order, columns=final_order)

    return fx_matrix.round(4), change_matrix.round(2)

# =========================================================
# Merge FX Spot and % Change Matrices
# =========================================================
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

def resample_fx_series(series: pd.Series, freq: str) -> pd.Series:
    """
    Resample FX time series to the desired frequency.
    freq: 'D' (daily), 'W' (weekly), 'M' (monthly), 'Y' (yearly)
    """
    if freq == 'D':
        return series.asfreq('D').ffill()
    elif freq == 'W':
        return series.resample('W-FRI').last().ffill()
    elif freq == 'M':
        return series.resample('M').last().ffill()
    elif freq == 'Y':
        return series.resample('A-DEC').last().ffill()
    else:
        raise ValueError(f"Unsupported frequency: {freq}")

# =========================================================
# Page: FX (p3_fx) — Transformation: Build consolidated FX history
# =========================================================
# Imports required for FX history transformation
from .tickers_mapping import FX_PAIRS
from .yf_client import download_fx_history_series

def build_fx_history_series() -> pd.DataFrame:
    """
    Build consolidated FX history for all pairs in FX_PAIRS.
    """
    all_series = {}
    for pair_name, ticker in FX_PAIRS.items():
        # --- MANUAL OVERRIDE FOR LABEL ---
        # If the name is 'USD/EUR', we change the label to 'EUR/USD' 
        # so it matches the actual data value (e.g., 1.05)
        display_name = "EUR/USD" if pair_name == "USD/EUR" else pair_name
        
        series = download_fx_history_series(ticker, period="max", interval="1d")

        if isinstance(series, pd.Series) and not series.empty:
            series = series.ffill()
            series.name = display_name
            all_series[display_name] = series
            print(f"✔ Added {display_name} ({ticker})")
        else:
            print(f"⚠️ Skipping {display_name} ({ticker}) — no data")

    if not all_series:
        raise ValueError("No FX history could be downloaded.")

    # Sort columns alphabetically so EUR/USD, GBP/USD, etc., are easy to find
    df = pd.concat(all_series.values(), axis=1)
    return df.reindex(columns=sorted(df.columns))





# ---------------------------------------------------------
# Transforms for Rates (FRED data)
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




# ---------------------------------------------------------
# Transforms GDP (FRED data)
# ---------------------------------------------------------

#========================================================
# GDP Monitor Table Builder
#========================================================
def build_gdp_monitor_table(macro_data: dict, fx_matrix: pd.DataFrame = None) -> pd.DataFrame:
    """
    Builds a clean table for the GDP Monitor:
    Columns: [Country, GDP Current, GDP Prev, Change %, Q Current, Q Prev]
    """
    # ... (Keep this function EXACTLY as it was in your snippet) ...
    # (I am omitting the body here to save space, but you should keep your existing code for this specific function)
    rows = []
    
    # Define simple heuristic to normalize to Billions
    def normalize_to_billions(val):
        if pd.isna(val) or val == 0:
            return 0
        if val > 1_000_000_000_000: # Trillions (Units)
            return val / 1e9
        if val > 1_000_000: # Millions
            return val / 1e3
        return val # Already in Billions

    from .tickers_mapping import GDP_MONITOR_TABLE_TICKERS
    country_map = GDP_MONITOR_TABLE_TICKERS

    for country_name, series_id in country_map.items():
        if series_id not in macro_data or macro_data[series_id].empty:
            continue

        series = macro_data[series_id].dropna()
        if series.empty:
            continue
        
        series = series.sort_index(ascending=False)
        valid_series = series[series > 0]
        
        if len(valid_series) < 2:
            continue
            
        curr_date = valid_series.index[0]
        curr_val = valid_series.iloc[0]
        prev_date = valid_series.index[1]
        prev_val = valid_series.iloc[1]

        curr_norm = normalize_to_billions(curr_val)
        prev_norm = normalize_to_billions(prev_val)
        
        if prev_norm != 0:
            change_pct = ((curr_norm / prev_norm) - 1)
        else:
            change_pct = 0.0

        def get_q_label(d):
            return f"Q{d.quarter} {d.year}"

        rows.append({
            "Country": country_name,
            "GDP Current ($B)": curr_norm,
            "GDP Prev ($B)": prev_norm,
            "Change": change_pct,
            "Current Q": get_q_label(curr_date),
            "Prev Q": get_q_label(prev_date)
        })

    if not rows:
        return pd.DataFrame(columns=["Country", "GDP Current ($B)", "GDP Prev ($B)", "Change", "Current Q", "Prev Q"])

    return pd.DataFrame(rows)


#========================================================
# GDP Comparison Tables Builder (UPDATED)
#========================================================
def build_gdp_comparison_tables(raw_gdp_data: dict, fx_rates: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns two DataFrames: Local Currency GDP and USD Converted GDP.
    
    CRITICAL: 'fx_rates' is expected to be the Last Row of FX_historical.csv.
    It contains clear floats (e.g. 1.05, 150.0) indexed by 'EUR/USD', 'USD/JPY', etc.
    """
    from .tickers_mapping import GDP_COMPARISON_TABLES_TICKERS
    gdp_config = GDP_COMPARISON_TABLES_TICKERS

    local_rows = []
    usd_rows = []

    for item in gdp_config:
        country = item['country']
        currency = item['currency']
        
        # Check if we have data for this country
        if country not in raw_gdp_data or raw_gdp_data[country].empty:
            continue

        df = raw_gdp_data[country].copy()
        
        # Basic Cleaning
        df.columns = ['Value']
        df = df[df['Value'] > 0].dropna().sort_index(ascending=False)
        
        if len(df) < 2:
            continue

        # Extract Values
        curr_q_label = str(df.index.to_period('Q')[0])
        curr_val_raw = float(df.iloc[0]['Value'])
        prev_val_raw = float(df.iloc[1]['Value'])

        # Local Math (Normalize to Trillions)
        local_trill = curr_val_raw / item['divisor']
        growth = ((curr_val_raw / prev_val_raw) - 1) * 100

        # --- NEW FX LOGIC ---
        rate = None
        source = "FX Historical"
        
        if currency == "USD":
            rate = 1.0
            source = "Benchmarked"
            usd_trill = local_trill
        else:
            # We determine conversion based on which pair exists in fx_rates
            # Direct Quote (e.g., EUR/USD): USD = Local * Rate
            # Indirect Quote (e.g., USD/JPY): USD = Local / Rate
            
            direct_pair = f"{currency}/USD"  # e.g., EUR/USD
            indirect_pair = f"USD/{currency}" # e.g., USD/JPY
            
            try:
                if direct_pair in fx_rates.index:
                    rate = float(fx_rates[direct_pair])
                    usd_trill = local_trill * rate
                elif indirect_pair in fx_rates.index:
                    rate = float(fx_rates[indirect_pair])
                    usd_trill = local_trill / rate
                else:
                    rate = None
                    usd_trill = 0
            except Exception as e:
                print(f"Error converting GDP for {country}: {e}")
                rate = None
        
        # Build Local Row
        local_rows.append({
            "Country": country,
            "Quarter": curr_q_label,
            "GDP (Local)": f"{local_trill:.2f} {currency}",
            "Growth": f"{growth:+.2f}%"
        })

        # Build USD Row
        if rate is not None:
            usd_val_str = f"${usd_trill:.2f} T"
            note_str = f"{source} ({rate:.4f})" if currency != "USD" else "Benchmarked"
        else:
            usd_val_str = "N/A"
            note_str = f"Missing Rate for {currency}"

        usd_rows.append({
            "Country": country,
            "Quarter": curr_q_label,
            "GDP (USD)": usd_val_str,
            "Growth": f"{growth:+.2f}%",
            "Note": note_str
        })

    return pd.DataFrame(local_rows), pd.DataFrame(usd_rows)


# =========================================================
# GDP Local Currency Enrichment (UPDATED)
# =========================================================
def calculate_gdp_local_currency(gdp_data: dict) -> pd.DataFrame:
    """
    Enrich GDP data with local currencies and formatting using FX Historical data.
    
    gdp_usd is billions USD.
    We convert USD -> Local.
    """
    import os
    from .tickers_mapping import STOCK_CURRENCIES
    
    # --- CHANGED: Load FX Historical instead of Matrix ---
    fx_path = os.path.join("data", "processed", "FX_historical.csv")
    latest_fx = pd.Series(dtype=float)
    
    if os.path.exists(fx_path):
        # Read only the last row
        fx_df = pd.read_csv(fx_path, index_col=0)
        if not fx_df.empty:
            latest_fx = fx_df.iloc[-1]
    
    enriched = {}
    for country, data in gdp_data.items():
        usd_value = data['ttm_value']  # billions USD
        currency = STOCK_CURRENCIES.get(country, 'USD')
        
        if currency == 'USD':
            local_value = usd_value
        else:
            # --- NEW CONVERSION LOGIC ---
            # Direct Quote (EUR/USD): Local = USD / Rate
            # Indirect Quote (USD/JPY): Local = USD * Rate
            
            direct_pair = f"{currency}/USD"
            indirect_pair = f"USD/{currency}"
            
            if direct_pair in latest_fx.index:
                rate = latest_fx[direct_pair]
                # If 1 EUR = 1.05 USD, then 100 USD = 100 / 1.05 EUR
                local_value = usd_value / rate
            elif indirect_pair in latest_fx.index:
                rate = latest_fx[indirect_pair]
                # If 1 USD = 150 JPY, then 100 USD = 100 * 150 JPY
                local_value = usd_value * rate
            else:
                local_value = usd_value
                print(f"⚠️ No historical FX rate found for {currency}")
        
        formatted_local = f"{local_value:,.0f}".replace(",", " ") + f" {currency}"
        
        enriched[country] = {
            'gdp_usd': usd_value,
            'gdp_local': local_value,
            'currency': currency,
            'formatted_local': formatted_local,
            'qoq_momentum': data['qoq_momentum'],
            'date_str': data['date_str']
        }
    
    df = pd.DataFrame.from_dict(enriched, orient='index')
    return df

# =========================================================
# GDP Master Table Builder
# =========================================================
# (This function was fine in your provided code, keeping it for completeness)
def build_gdp_master_table(series_dict: dict) -> pd.DataFrame:
    rows = []
    for country, series in series_dict.items():
        if series.empty: continue
        series = series.sort_index(ascending=False)
        curr_idx = None
        for i, val in enumerate(series):
            if pd.notna(val) and val > 0:
                curr_idx = i
                break
        if curr_idx is None or curr_idx >= len(series) - 1: continue
        prev_idx = curr_idx + 1
        curr_val = series.iloc[curr_idx]
        prev_val = series.iloc[prev_idx]
        if curr_val > 1000000:
            curr_val /= 1000
            prev_val /= 1000
        change_pct = ((curr_val / prev_val) - 1) * 100 if prev_val != 0 else 0
        curr_date = series.index[curr_idx]
        prev_date = series.index[prev_idx]
        def date_to_quarter(date):
            quarter = ((date.month - 1) // 3) + 1
            return f"Q{quarter} {date.year}"
        curr_period = date_to_quarter(curr_date)
        prev_period = date_to_quarter(prev_date)
        curr_str = f"${curr_val:,.0f}B"
        prev_str = f"${prev_val:,.0f}B"
        rows.append({
            "Country": country,
            "GDP (Current)": curr_str,
            "GDP (Previous)": prev_str,
            "Change %": change_pct,
            "Current Period": curr_period,
            "Previous Period": prev_period
        })
    return pd.DataFrame(rows)

# =========================================================
# GDP TTM and Momentum Calculation
# =========================================================
# (This function was fine, keeping it for completeness)
def calculate_gdp_ttm_and_momentum(series: pd.Series, country: str) -> dict:
    scales = { "US": 1, "China": 1/1000, "Japan": 1, "Germany": 1/1000, "France": 1/1000, "UK": 1/1000 }
    scale = scales.get(country, 1)
    if series.empty: return {}
    ref_idx = None
    for i in range(len(series) - 1, -1, -1):
        val = series.iloc[i]
        date = series.index[i]
        if pd.notna(val) and val > 0 and date < pd.Timestamp('2025-10-01'):
            ref_idx = i
            break
    if ref_idx is None or ref_idx < 3: return {}
    ttm_series = series.iloc[ref_idx - 3: ref_idx + 1]
    ttm_value = ttm_series.sum() * scale
    ref_q = ttm_series.iloc[-1] * scale
    prev_q = ttm_series.iloc[-2] * scale
    qoq_momentum = ((ref_q / prev_q) - 1) * 100 if prev_q != 0 else 0
    ref_date = series.index[ref_idx]
    quarter = ((ref_date.month - 1) // 3) + 1
    year = ref_date.year
    date_str = f"Q{quarter} {year}"
    return { 'ttm_value': ttm_value, 'qoq_momentum': qoq_momentum, 'date_str': date_str }

# =========================================================
# Monetary Policy Transforms
# =========================================================

def compute_monetary_policy_metrics(raw_data: dict) -> dict:
    """
    Takes the raw dict from data_loader and computes:
    - YoY Inflation (Last / Last-12months - 1)
    - Latest Interest Rates
    """
    metrics = {}
    
    for region, series_dict in raw_data.items():
        metrics[region] = {}
        
        # --- 1. Inflation Calculation (Robust Method) ---
        cpi_df = series_dict.get("CPI", pd.DataFrame())
        if not cpi_df.empty:
            # Clean data
            cpi_clean = cpi_df.dropna()
            if len(cpi_clean) >= 13:
                latest_val = cpi_clean.iloc[-1].values[0]
                prev_val = cpi_clean.iloc[-13].values[0] # Exact 12 months ago shift
                
                yoy = ((latest_val / prev_val) - 1) * 100
                
                metrics[region]["Inflation"] = yoy
                metrics[region]["CPI_Date"] = cpi_clean.index[-1].strftime('%b %Y')
            else:
                metrics[region]["Inflation"] = None
        else:
            metrics[region]["Inflation"] = None

        # --- 2. Rates Extraction (Latest Available) ---
        # Helper to get scalar
        def get_latest(key):
            df = series_dict.get(key, pd.DataFrame())
            return df.iloc[-1].values[0] if not df.empty else None
            
        if region == "USA":
            metrics[region]["Eff_Rate"] = get_latest("EFFR")
            metrics[region]["Target_Low"] = get_latest("Target_Low")
            metrics[region]["Target_Up"] = get_latest("Target_Up")
            
        elif region == "EURO":
            metrics[region]["Deposit_Rate"] = get_latest("Deposit")
            metrics[region]["MRO_Rate"] = get_latest("MRO")
            
    return metrics

# =========================================================
# Cross-Asset Snapshot Table Builder
# =========================================================

# app/services/transforms.py

def compute_cross_asset_table(raw_data_dict: dict) -> pd.DataFrame:
    """
    Transforme les données brutes Yahoo en un tableau récapitulatif Cross-Asset.
    Utilise compute_stock_snapshot_metrics pour harmoniser les calculs de performance.
    """
    from .tickers_mapping import CROSS_ASSET_TICKERS
    rows = []
    
    # On boucle sur la config officielle pour garantir l'ordre et les unités
    for display_name, (ticker, unit) in CROSS_ASSET_TICKERS.items():
        series = raw_data_dict.get(ticker)
        
        if series is None or series.empty:
            continue
            
        # On prépare le DataFrame au format attendu par compute_stock_snapshot_metrics
        temp_df = pd.DataFrame({"Price": series})
        metrics = compute_stock_snapshot_metrics(temp_df)
        
        if not metrics.empty:
            rows.append({
                "Asset": display_name,
                "Value": metrics["Price"].iloc[0],
                "Unit": unit,
                "1D %": metrics["DailyChange"].iloc[0],
                "1W %": metrics["WeeklyChange"].iloc[0],
                "YTD %": metrics["YTDChange"].iloc[0]
            })
            
    return pd.DataFrame(rows)


# =========================================================
# For COMMODITY napshot Metrics Calculation
# =========================================================

def compute_commodity_snapshot(df):
    """
    Computes 1D, 1W, 1M, YTD changes for a commodity history dataframe.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    snapshot_list = []
    # Get last valid index
    last_date = df.index[-1]
    
    # Calculate price at start of year
    current_year = last_date.year
    ytd_start_price = df[df.index.year == current_year].iloc[0]

    for asset in df.columns:
        prices = df[asset].dropna()
        if prices.empty: continue
        
        curr_price = prices.iloc[-1]
        
        # Helper for % change
        def get_pct(series, lag):
            if len(series) > lag:
                prev = series.iloc[-(lag+1)]
                if prev != 0:
                    return ((curr_price - prev) / prev) * 100
            return 0.0

        snapshot_list.append({
            "Asset": asset,
            "Price": curr_price,
            "1D %": get_pct(prices, 1),
            "1W %": get_pct(prices, 5),
            "1M %": get_pct(prices, 21),
            "YTD %": ((curr_price - ytd_start_price[asset]) / ytd_start_price[asset]) * 100
        })
        
    return pd.DataFrame(snapshot_list)

def add_commodity_ratios(df_metals):
    """Calculates Copper/Gold and Gold/Silver ratios."""
    if df_metals is None or df_metals.empty:
        return pd.DataFrame()
    
    df = df_metals.copy()
    if 'Copper' in df.columns and 'Gold' in df.columns:
        df['Copper/Gold'] = df['Copper'] / df['Gold']
    if 'Gold' in df.columns and 'Silver' in df.columns:
        df['Gold/Silver'] = df['Gold'] / df['Silver']
    return df


# def calculate_snapshot_metrics(df):
#     """
#     Calcule les variations (Jour, Semaine, Mois, YTD) pour un DataFrame de prix.
#     Utilisé pour le tableau récapitulatif (ex-test2.py).
#     """
#     snapshot_list = []
    
#     if df is None or df.empty:
#         return pd.DataFrame()

#     # Indices approximatifs
#     last_idx = -1
#     prev_idx = -2    # 1 jour
#     week_idx = -6    # 1 semaine (5 jours de trading)
#     month_idx = -22  # 1 mois (21 jours de trading)
    
#     current_year = df.index[-1].year
#     # Prix au début de l'année
#     ytd_prices = df[df.index.year == current_year].iloc[0]

#     for asset in df.columns:
#         prices = df[asset]
#         if len(prices) < 22: continue # Pas assez d'historique
        
#         curr = prices.iloc[last_idx]
        
#         # Helper interne pour calcul %
#         def get_change(p_curr, p_prev):
#             if pd.isna(p_prev) or p_prev == 0: return 0.0
#             return ((p_curr - p_prev) / p_prev) * 100

#         day_chg = get_change(curr, prices.iloc[prev_idx])
#         week_chg = get_change(curr, prices.iloc[week_idx])
#         month_chg = get_change(curr, prices.iloc[month_idx])
#         ytd_chg = get_change(curr, ytd_prices[asset])
        
#         snapshot_list.append({
#             "Asset": asset,
#             "Price": curr,
#             "Daily %": day_chg,
#             "Weekly %": week_chg,
#             "Monthly %": month_chg,
#             "YTD %": ytd_chg
#         })
        
#     return pd.DataFrame(snapshot_list)

# def add_macro_ratios(df_metals):
#     """
#     Ajoute les colonnes de ratios (Copper/Gold, Gold/Silver) au DF Métaux.
#     (ex-test3.py)
#     """
#     if df_metals is None or df_metals.empty:
#         return df_metals
        
#     df = df_metals.copy()
    
#     # Vérification des colonnes nécessaires
#     if 'Copper' in df.columns and 'Gold' in df.columns:
#         df['Copper_Gold'] = df['Copper'] / df['Gold']
        
#     if 'Gold' in df.columns and 'Silver' in df.columns:
#         df['Gold_Silver'] = df['Gold'] / df['Silver']
        
#     return df