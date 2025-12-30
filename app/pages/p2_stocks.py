# pages/p2_stocks.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.services.data_loader import (
    load_stock_snapshot,
    load_stock_timeseries,
    load_stock_comparator,
    load_us10y_yield,
    calculate_correlation_matrix,
)
from app.services.transforms import (
    compute_rolling_stats,
    compute_cumulative_returns,
    plot_stock_comparator,
)
from app.services.tickers_mapping import STOCK_GROUPS, STOCK_CURRENCIES, INDICES, COUNTRY_TO_REGION, SYMBOLES


def clean_name(name: str) -> str:
    """Remove the _XX country/index suffix from stock names for display."""
    return name.split("_")[0] if "_" in name else name


def get_currency_symbol(name: str) -> str:
    """Get currency symbol for a stock name."""
    country = name.split('_')[-1]
    currency = STOCK_CURRENCIES.get(country, 'USD')
    return SYMBOLES.get(currency, currency)


def show():
    st.title("📈 Stocks Dashboard")

    # Load last update timestamp
    import os
    tracker_path = os.path.join("data", "processed", "refresh_tracker.csv")
    if os.path.exists(tracker_path):
        tracker = pd.read_csv(tracker_path, index_col="csv_name")
        tracker["last_update"] = pd.to_datetime(tracker["last_update"])
        last_update = tracker.loc["stocks_snapshot.csv", "last_update"] if "stocks_snapshot.csv" in tracker.index else "Unknown"
        st.caption(f"Last Market Update: {last_update}")
    else:
        st.caption("Last Market Update: Unknown")

    # ---------------------------------------------------------
    # Load snapshot data (full universe)
    # ---------------------------------------------------------
    snapshot_df = load_stock_snapshot(force_refresh=False)

    # ---------------------------------------------------------
    # Sidebar Filters
    # ---------------------------------------------------------
    st.sidebar.title("Filters")

    # 1. Market Movers filters
    st.sidebar.subheader("Market Movers")
    mm_index_choice = st.sidebar.selectbox(
        "Select Index / Exchange (Top 5 Gainers/Losers)",
        options=["All"] + list(STOCK_GROUPS.keys())
    )

    # 2. Market Snapshot filters
    st.sidebar.subheader("Market Snapshot")
    ms_index_choice = st.sidebar.selectbox(
        "Select Index / Exchange (Snapshot)",
        options=["All"] + list(STOCK_GROUPS.keys())
    )
    if ms_index_choice != "All":
        allowed_names = STOCK_GROUPS.get(ms_index_choice, [])
        snapshot_index_df = snapshot_df[snapshot_df["Name"].isin(allowed_names)]
    else:
        snapshot_index_df = snapshot_df.copy()

    ms_stock_choices = st.sidebar.multiselect(
        "Select Specific Stocks (Snapshot only)",
        options=snapshot_index_df["Name"].tolist(),
        default=[]
    )
    if ms_stock_choices:
        snapshot_snapshot_df = snapshot_index_df[snapshot_index_df["Name"].isin(ms_stock_choices)]
    else:
        snapshot_snapshot_df = snapshot_index_df.copy()

    # 3. Single Stock Analysis filters
    st.sidebar.subheader("Single Stock Analysis")
    ssa_roll_choice = st.sidebar.radio(
        "Rolling Window",
        options=["1Y (252d)", "3Y (756d)", "10Y (2520d)"],
        index=0
    )
    roll_map = {"1Y (252d)": 252, "3Y (756d)": 756, "10Y (2520d)": 2520}
    ssa_window = roll_map[ssa_roll_choice]

    ssa_benchmark = []  # placeholder, will be set inside

    # 4. Comparator Analysis filters
    st.sidebar.subheader("Comparator Analysis")
    corr_toggle = st.sidebar.checkbox(
        "Show correlation matrix", 
        key="comp_corr_toggle"
    )
    log_toggle = st.sidebar.checkbox(
        "Use log returns", 
        key="comp_log_toggle"
    )
    # Benchmarks moved to main UI


    # ---------------------------------------------------------
    # Market Movers (Top Gainers/Losers) → index filter only
    # ---------------------------------------------------------
    if mm_index_choice != "All":
        allowed_names = STOCK_GROUPS.get(mm_index_choice, [])
        movers_df = snapshot_df[snapshot_df["Name"].isin(allowed_names)]
    else:
        movers_df = snapshot_df.copy()

    if not movers_df.empty:
        st.header("Market Movers")
        col1, col2 = st.columns(2)

        top_gainers = movers_df.nlargest(5, "DailyChange")[["Name", "Price", "DailyChange"]].copy()
        top_gainers["Currency"] = top_gainers["Name"].apply(get_currency_symbol)
        top_gainers["Formatted Price"] = top_gainers.apply(lambda row: f"{row['Currency']}{row['Price']:.2f}", axis=1)
        top_gainers["Name"] = top_gainers["Name"].apply(clean_name)
        with col1:
            st.subheader("📈 Top 5 Gainers")
            st.dataframe(
                top_gainers[["Name", "Formatted Price", "DailyChange", "Currency"]].reset_index(drop=True).style
                .format({"DailyChange": "{:+.2f}%"})
                .map(lambda v: "color: green" if v > 0 else "color: red", subset=["DailyChange"])
            )

        top_losers = movers_df.nsmallest(5, "DailyChange")[["Name", "Price", "DailyChange"]].copy()
        top_losers["Currency"] = top_losers["Name"].apply(get_currency_symbol)
        top_losers["Formatted Price"] = top_losers.apply(lambda row: f"{row['Currency']}{row['Price']:.2f}", axis=1)
        top_losers["Name"] = top_losers["Name"].apply(clean_name)
        with col2:
            st.subheader("📉 Top 5 Losers")
            st.dataframe(
                top_losers[["Name", "Formatted Price", "DailyChange", "Currency"]].reset_index(drop=True).style
                .format({"DailyChange": "{:+.2f}%"})
                .map(lambda v: "color: green" if v > 0 else "color: red", subset=["DailyChange"])
            )

    # ---------------------------------------------------------
    # Market Snapshot → index filter + optional multi-stock filter
    # ---------------------------------------------------------
    st.header("Market Snapshot")
    snapshot_display_df = snapshot_snapshot_df.copy()
    snapshot_display_df["Currency"] = snapshot_display_df["Name"].apply(get_currency_symbol)
    snapshot_display_df["Formatted Price"] = snapshot_display_df.apply(lambda row: f"{row['Currency']}{row['Price']:.2f}", axis=1)
    snapshot_display_df["Name"] = snapshot_display_df["Name"].apply(clean_name)

    st.dataframe(
        snapshot_display_df[["Name", "Formatted Price", "DailyChange", "WeeklyChange", "MonthlyChange", "YTDChange", "Currency"]].reset_index(drop=True).style
        .format({
            "DailyChange": "{:+.2f}%",
            "WeeklyChange": "{:+.2f}%",
            "MonthlyChange": "{:+.2f}%",
            "YTDChange": "{:+.2f}%"
        })
        .map(
            lambda v: "color: green" if v > 0 else "color: red",
            subset=["DailyChange", "WeeklyChange", "MonthlyChange", "YTDChange"]
        )
    )

    # ---------------------------------------------------------
    # Single Stock Analysis → independent selector inside page
    # ---------------------------------------------------------
    st.header("Single Stock Analysis")

    if not snapshot_df.empty:
        stock_choice = st.selectbox("Select a stock", snapshot_df["Name"].tolist())
        
        # Smart benchmark options based on stock country
        country = stock_choice.split('_')[-1] if '_' in stock_choice else 'US'
        if country == 'US':
            benchmark_options = list(INDICES['Americas'].keys()) + ['US10Y']
        elif country == 'JP':
            benchmark_options = ['Nikkei 225', 'Japan 10Y']
        elif country == 'FR':
            benchmark_options = ['CAC 40', 'Euro Stoxx 50', 'AEX', 'France 10Y']
        else:
            benchmark_options = ['MSCI World', 'US10Y']
        
        ssa_benchmark = st.multiselect(
            "Select Benchmark (optional)",
            options=benchmark_options,
            default=[]
        )
        
        ts_df = load_stock_timeseries(stock_choice, start_date="2000-01-01")

        if not ts_df.empty:
            # Date range selectors
            start_date = st.date_input("Start date", value=ts_df.index.min().date(), key="ssa_start_date")
            end_date   = st.date_input("End date", value=ts_df.index.max().date(), key="ssa_end_date")
            ts_filtered = ts_df.loc[str(start_date):str(end_date)]

            # Compute rolling stats for chosen window
            stats_df = compute_rolling_stats(ts_filtered["Price"], windows=[ssa_window])


            # --- Plot rolling mean & vol for the selected stock ---
            fig, ax = plt.subplots(figsize=(12,6))
            (stats_df[f"roll_mean_{ssa_window}"] * 100).plot(ax=ax, label="Annualized Return", color="blue")
            (stats_df[f"roll_vol_{ssa_window}"] * 100).plot(ax=ax, label="Annualized Volatility", color="red")
            
            # --- Benchmark overlay ---
            for bench in ssa_benchmark:
                if bench in INDICES['Americas'] or bench in INDICES['Europe'] or bench in INDICES['Asia']:
                    # Load index timeseries by name
                    bench_df = load_stock_timeseries(bench, start_date="2000-01-01")
                    if not bench_df.empty:
                        bench_prices = bench_df["Price"].loc[str(start_date):str(end_date)]
                        bench_stats = compute_rolling_stats(bench_prices, windows=[ssa_window])
                        (bench_stats[f"roll_mean_{ssa_window}"] * 100).plot(ax=ax, label=f"{bench} Return")
                        (bench_stats[f"roll_vol_{ssa_window}"] * 100).plot(ax=ax, label=f"{bench} Volatility")
                elif bench == "US10Y":
                    us10y_series = load_us10y_yield()
                    us10y_filtered = us10y_series.loc[str(start_date):str(end_date)]
                    us10y_stats = compute_rolling_stats(us10y_filtered, windows=[ssa_window])
                    (us10y_stats[f"roll_mean_{ssa_window}"] * 100).plot(ax=ax, label="US10Y Return", color="green")
                    (us10y_stats[f"roll_vol_{ssa_window}"] * 100).plot(ax=ax, label="US10Y Volatility", color="orange")
                elif bench == "France 10Y":
                    # Load France yield from OECD
                    from app.services.data_loader import load_oecd_yields
                    oecd_df = load_oecd_yields(["IRLTLT01FRM156N"])
                    if not oecd_df.empty:
                        fr10y = oecd_df["IRLTLT01FRM156N"].loc[str(start_date):str(end_date)]
                        fr_stats = compute_rolling_stats(fr10y.to_frame(), windows=[ssa_window])
                        (fr_stats[f"roll_mean_{ssa_window}"] * 100).plot(ax=ax, label="France 10Y Return")
                        (fr_stats[f"roll_vol_{ssa_window}"] * 100).plot(ax=ax, label="France 10Y Volatility")
                elif bench == "Japan 10Y":
                    oecd_df = load_oecd_yields(["IRLTLT01JPM156N"])
                    if not oecd_df.empty:
                        jp10y = oecd_df["IRLTLT01JPM156N"].loc[str(start_date):str(end_date)]
                        jp_stats = compute_rolling_stats(jp10y.to_frame(), windows=[ssa_window])
                        (jp_stats[f"roll_mean_{ssa_window}"] * 100).plot(ax=ax, label="Japan 10Y Return")
                        (jp_stats[f"roll_vol_{ssa_window}"] * 100).plot(ax=ax, label="Japan 10Y Volatility")        
            
            ax.set_title(f"{stock_choice}: Rolling {ssa_roll_choice}")
            ax.set_ylabel("Annualized Value (%)")
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
            ax.axhline(0, color='black', linestyle='--')
            ax.legend()
            st.pyplot(fig)


    # ---------------------------------------------------------
    # Comparator Analysis → enhanced with date range & rolling windows
    # ---------------------------------------------------------
    st.header("Comparator Analysis")

    if not snapshot_df.empty:
        # Stock selection
        selected_stocks = st.multiselect(
            "Select stocks to compare",
            snapshot_df["Name"].tolist(),
            default=snapshot_df["Name"].tolist()[:2],
            key="comp_stock_select"
        )

        if selected_stocks:
            # Get countries from selected stocks
            countries = set()
            for stock in selected_stocks:
                country = stock.split('_')[-1]
                countries.add(country)
            
            # Filter benchmark options based on countries
            available_regions = set(COUNTRY_TO_REGION.get(country, '') for country in countries if country in COUNTRY_TO_REGION)
            benchmark_options = []
            for region in available_regions:
                if region in INDICES:
                    benchmark_options.extend(INDICES[region].keys())
            benchmark_options = sorted(list(set(benchmark_options)))

            # Load comp_df for date defaults
            comp_df = load_stock_comparator(selected_stocks, log=log_toggle)
            if not comp_df.empty:
                start_date_default = comp_df.index.min().to_pydatetime().date()
                end_date_default = comp_df.index.max().to_pydatetime().date()

                # UI Layout: Single row with 4 columns
                col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
                
                with col1:
                    # Stocks already selected above
                    st.write("**Selected Stocks:**")
                    st.write(", ".join(selected_stocks))
                
                with col2:
                    selected_benchmarks = st.multiselect(
                        "Select Benchmarks",
                        options=benchmark_options,
                        default=[],
                        key="comp_benchmarks_main"
                    )
                
                with col3:
                    start_date = st.date_input("Start Date", value=start_date_default, key="comp_start_date")
                
                with col4:
                    end_date = st.date_input("End Date", value=end_date_default, key="comp_end_date")

                # Apply date filter
                comp_df_filtered = comp_df.loc[str(start_date):str(end_date)]

                # Compute cumulative returns for each stock
                cum_returns = {}
                for stock in selected_stocks:
                    price_series = load_stock_timeseries(stock, start_date="2000-01-01")["Price"]
                    price_series = price_series.loc[str(start_date):str(end_date)]
                    cum_returns[stock] = compute_cumulative_returns(price_series, log_returns=log_toggle, freq='D')

                # Add benchmarks if selected
                for bench_name in selected_benchmarks:
                    try:
                        bench_df = load_stock_timeseries(bench_name, start_date="2000-01-01")
                        if not bench_df.empty and 'Price' in bench_df.columns:
                            bench_prices = bench_df["Price"]
                            bench_prices = bench_prices.loc[str(start_date):str(end_date)]
                            cum_returns[bench_name] = compute_cumulative_returns(bench_prices, log_returns=log_toggle, freq='D')
                        else:
                            st.warning(f"Could not load data for {bench_name}")
                    except Exception as e:
                        st.warning(f"Failed to load {bench_name}: {str(e)}")

                # Plot cumulative performance
                title = "Stock Comparator: Cumulative Performance"
                if selected_benchmarks:
                    title += f" vs. {', '.join(selected_benchmarks)}"
                fig = plot_stock_comparator(cum_returns, log_toggle, title, benchmarks=selected_benchmarks)
                st.pyplot(fig)

                # --- Correlation matrix ---
                if corr_toggle and (selected_stocks or selected_benchmarks):
                    st.subheader("Diversification Analysis: Assets vs. Benchmarks")
                    corr_matrix = calculate_correlation_matrix(selected_stocks, selected_benchmarks, str(start_date), str(end_date), log_returns=log_toggle)
                    
                    if not corr_matrix.empty:
                        # Use Plotly for heatmap
                        import plotly.express as px
                        fig_corr = px.imshow(
                            corr_matrix,
                            text_auto=".2f",
                            aspect="auto",
                            color_continuous_scale="RdYlGn",
                            title="Correlation Heatmap"
                        )
                        st.plotly_chart(fig_corr)
                    else:
                        st.write("No data available for correlation calculation.")