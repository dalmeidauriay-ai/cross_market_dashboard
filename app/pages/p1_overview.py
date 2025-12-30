import streamlit as st
import pandas as pd
from app.services.data_loader import (
    load_indices_snapshot, 
    load_monetary_policy_raw, 
    load_cross_asset_snapshot, 
    load_gdp_comparison
)
from app.services.transforms import compute_monetary_policy_metrics

def highlight_growth(val):
    """
    Pandas Styler: Color text green if positive, red if negative.
    Expects strings like "+2.00%" or "-0.05%".
    """
    if not isinstance(val, str):
        return ''
    if '-' in val:
        return 'color: #FF4B4B' # Streamlit Red
    elif '+' in val:
        return 'color: #09AB3B' # Streamlit Green
    return ''


def show():
    st.title("🌍 Macro Terminal")

    # ---------------------------------------------------------
    # 1. Global Market Snapshot (Indices)
    # ---------------------------------------------------------
    st.header("Global Market Snapshot")
    indices_df = load_indices_snapshot(force_refresh=False)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Americas")
        americas_indices = ["S&P 500", "Dow Jones", "Nasdaq 100", "Bovespa", "Russell 2000", "Merval"]
        americas_df = indices_df[indices_df["Name"].isin(americas_indices)].copy()
        if not americas_df.empty:
            display_df = americas_df[["Name", "Price", "DailyChange"]].copy()
            display_df["Price"] = display_df["Price"].apply(lambda x: f"{x:,.2f}".replace(",", " ") if pd.notna(x) else "")
            display_df["Change %"] = display_df["DailyChange"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "")
            display_df = display_df.rename(columns={"Name": "Symbol"})
            display_df = display_df.drop(columns=["DailyChange"])
            def color_change(val):
                if isinstance(val, str) and val.endswith('%'):
                    num = float(val[:-1])
                    return 'color: green' if num > 0 else 'color: red' if num < 0 else ''
                return ''
            column_config = {
                "Symbol": st.column_config.TextColumn("Symbol"),
                "Price": st.column_config.TextColumn("Price"),
                "Change %": st.column_config.TextColumn("Change %")
            }
            styled_df = display_df.style.map(color_change, subset=['Change %'])
            st.dataframe(styled_df, column_config=column_config, hide_index=True)

    with col2:
        st.subheader("Europe")
        europe_indices = ["Euro Stoxx 50", "CAC 40", "DAX", "FTSE 100", "FTSE MIB", "AEX"]
        europe_df = indices_df[indices_df["Name"].isin(europe_indices)].copy()
        if not europe_df.empty:
            display_df = europe_df[["Name", "Price", "DailyChange"]].copy()
            display_df["Price"] = display_df["Price"].apply(lambda x: f"{x:,.2f}".replace(",", " ") if pd.notna(x) else "")
            display_df["Change %"] = display_df["DailyChange"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "")
            display_df = display_df.rename(columns={"Name": "Symbol"})
            display_df = display_df.drop(columns=["DailyChange"])
            def color_change(val):
                if isinstance(val, str) and val.endswith('%'):
                    num = float(val[:-1])
                    return 'color: green' if num > 0 else 'color: red' if num < 0 else ''
                return ''
            column_config = {
                "Symbol": st.column_config.TextColumn("Symbol"),
                "Price": st.column_config.TextColumn("Price"),
                "Change %": st.column_config.TextColumn("Change %")
            }
            styled_df = display_df.style.map(color_change, subset=['Change %'])
            st.dataframe(styled_df, column_config=column_config, hide_index=True)

    with col3:
        st.subheader("Asia-Pacific")
        asia_indices = ["Nikkei 225", "Hang Seng", "KOSPI", "ASX 200", "Shanghai Composite", "Nifty 50"]
        asia_df = indices_df[indices_df["Name"].isin(asia_indices)].copy()
        if not asia_df.empty:
            display_df = asia_df[["Name", "Price", "DailyChange"]].copy()
            display_df["Price"] = display_df["Price"].apply(lambda x: f"{x:,.2f}".replace(",", " ") if pd.notna(x) else "")
            display_df["Change %"] = display_df["DailyChange"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "")
            display_df = display_df.rename(columns={"Name": "Symbol"})
            display_df = display_df.drop(columns=["DailyChange"])
            def color_change(val):
                if isinstance(val, str) and val.endswith('%'):
                    num = float(val[:-1])
                    return 'color: green' if num > 0 else 'color: red' if num < 0 else ''
                return ''
            column_config = {
                "Symbol": st.column_config.TextColumn("Symbol"),
                "Price": st.column_config.TextColumn("Price"),
                "Change %": st.column_config.TextColumn("Change %")
            }
            styled_df = display_df.style.map(color_change, subset=['Change %'])
            st.dataframe(styled_df, column_config=column_config, hide_index=True)

    st.divider()    

    # ---------------------------------------------------------
    # 2. Global Economy Monitor (GDP) - WITH COLOR
    # ---------------------------------------------------------
    st.header("Global Economy Monitor (GDP)")
    df_local, df_usd = load_gdp_comparison()
    
    if not df_local.empty:
        tab1, tab2 = st.tabs(["🇺🇸 USD View (Normalized)", "🌍 Local Currency View"])
        
        with tab1:
            st.caption("GDP converted to Trillions of USD (using latest FX Matrix rates)")
            # Apply Style
            styled_usd = df_usd.style.map(highlight_growth, subset=['Growth'])
            st.dataframe(
                df_usd, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "GDP (USD)": st.column_config.TextColumn("GDP ($ Trillions)"),
                    "Growth": st.column_config.TextColumn("QoQ Growth"),
                    "Note": st.column_config.TextColumn("Conversion Note", width="medium")
                }
            )
            
        with tab2:
            st.caption("Raw GDP reported by National Agencies (in Local Trillions)")
            styled_local = df_local.style.map(highlight_growth, subset=['Growth'])
            st.dataframe(
                df_local, 
                use_container_width=True, 
                hide_index=True
            )
    else:
        st.warning("GDP Data could not be loaded. Please check API connections.")

    st.divider()

    # ---------------------------------------------------------
    # 3. Macro Policy Matrix
    # ---------------------------------------------------------
    st.header("Macro Policy Matrix")
    
    # Load and Compute
    raw_policy = load_monetary_policy_raw()
    policy_metrics = compute_monetary_policy_metrics(raw_policy)
    
    col_us, col_eu = st.columns(2)
    
    # --- USA CARD ---
    with col_us:
        st.subheader("🇺🇸 United States")
        us_data = policy_metrics.get("USA", {})
        
        # Rates
        eff_rate = us_data.get("Eff_Rate")
        t_low = us_data.get("Target_Low")
        t_up = us_data.get("Target_Up")
        
        st.metric("Effective Fed Funds Rate", f"{eff_rate:.2f}%" if eff_rate else "N/A")
        if t_low and t_up:
            st.caption(f"Target Range: {t_low:.2f}% - {t_up:.2f}%")
        
        # Inflation
        inf = us_data.get("Inflation")
        date_lbl = us_data.get("CPI_Date", "")
        
        st.metric("CPI Inflation (YoY)", 
                  f"{inf:.2f}%" if inf is not None else "N/A",
                  help=f"Reference Date: {date_lbl}")

    # --- EURO CARD ---
    with col_eu:
        st.subheader("🇪🇺 Eurozone")
        eu_data = policy_metrics.get("EURO", {})
        
        # Rates
        dep_rate = eu_data.get("Deposit_Rate")
        mro_rate = eu_data.get("MRO_Rate")
        
        st.metric("ECB Deposit Rate (Floor)", f"{dep_rate:.2f}%" if dep_rate else "N/A")
        st.metric("ECB MRO Rate (Main)", f"{mro_rate:.2f}%" if mro_rate else "N/A")
        
        # Inflation
        inf = eu_data.get("Inflation")
        date_lbl = eu_data.get("CPI_Date", "")
        
        st.metric("HICP Inflation (YoY)", 
                  f"{inf:.2f}%" if inf is not None else "N/A",
                  help=f"Reference Date: {date_lbl}")

    st.divider()

    # ---------------------------------------------------------
    # 4. Cross-Asset Snapshot
    # ---------------------------------------------------------
    st.header("Cross-Asset Snapshot")
    
    cross_df = load_cross_asset_snapshot()
    
    if not cross_df.empty:
        # 1. Clean up columns for display if necessary
        # Ensure numeric columns are actually floats
        cols_to_fix = ["1D %", "1W %", "YTD %", "Value"]
        for col in cols_to_fix:
            cross_df[col] = pd.to_numeric(cross_df[col], errors='coerce')

        # 2. Apply Styling exactly like your p2_stock.py
        styled_cross = (
            cross_df[["Asset", "Value", "Unit", "1D %", "1W %", "YTD %"]]
            .style.format({
                "Value": "{:,.2f}",
                "1D %": "{:+.2f}%",
                "1W %": "{:+.2f}%",
                "YTD %": "{:+.2f}%"
            })
            .map(
                lambda v: "color: #09AB3B" if v > 0 else "color: #FF4B4B" if v < 0 else "",
                subset=["1D %", "1W %", "YTD %"]
            )
        )

        # 3. Display the STYLED object
        st.dataframe(styled_cross, use_container_width=True, hide_index=True)
        
    else:
        st.info("No Cross-Asset data available. Please run refresh.")