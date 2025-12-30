# app/pages/p5_commo.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import datetime

from app.services.transforms import compute_commodity_snapshot, add_commodity_ratios

# Paths
PROCESSED_DIR = os.path.join("data", "processed")
FUTURES_DIR = os.path.join(PROCESSED_DIR, "futures_curves")

# --- Helpers ---
def load_history_file(group_name):
    """Loads CSV from data/processed/hist_{group_name}.csv"""
    path = os.path.join(PROCESSED_DIR, f"hist_{group_name}.csv")
    if os.path.exists(path):
        return pd.read_csv(path, index_col=0, parse_dates=True)
    return None

def style_negative_positive(val):
    """Matches the style of p1_overview and p2_stocks."""
    if not isinstance(val, (int, float)): return ''
    color = '#09AB3B' if val > 0 else '#FF4B4B' if val < 0 else 'white' # Green/Red
    return f'color: {color}'

def show():
    st.title("📦 Commodities & Futures Hub")
    
    # =========================================================================
    # ROW 1: MARKET SNAPSHOT (Static Tables)
    # =========================================================================
    st.markdown("### 📊 Market Snapshot")
    
    groups = ["metals", "energy", "agriculture"]
    cols = st.columns(3)
    
    for i, grp in enumerate(groups):
        with cols[i]:
            st.caption(f"**{grp.upper()}**")
            df_hist = load_history_file(grp)
            
            if df_hist is not None:
                metrics = compute_commodity_snapshot(df_hist)
                if not metrics.empty:
                    # Apply standard formatting
                    st.dataframe(
                        metrics.style
                        .map(style_negative_positive, subset=["1D %", "1W %", "1M %", "YTD %"])
                        .format({
                            "Price": "{:,.2f}", 
                            "1D %": "{:+.2f}%", 
                            "1W %": "{:+.2f}%", 
                            "1M %": "{:+.2f}%", 
                            "YTD %": "{:+.2f}%"
                        }),
                        hide_index=True,
                        use_container_width=True,
                        height=400  # Increased height to avoid scrolling
                    )
            else:
                st.info(f"Loading {grp} data...")

    st.divider()

    # =========================================================================
    # ROW 2: MACRO RATIOS (Interactive Charts)
    # =========================================================================
    st.markdown("### 🏗️ Macro Sentiment Ratios")
    
    df_metals = load_history_file("metals")
    
    if df_metals is not None:
        df_ratios = add_commodity_ratios(df_metals)
        
        # Default dates
        max_date = df_ratios.index[-1].date()
        min_date = df_ratios.index[0].date()
        default_start = max_date - datetime.timedelta(days=5*365) # 5 years default
        
        # Layout: 2 columns
        r1, r2 = st.columns(2)
        
        # --- LEFT: COPPER / GOLD ---
        with r1:
            st.subheader("🏗️ Doctor Copper (Copper/Gold)")
            
            # Date Selectors for Chart 1
            d1_col1, d1_col2 = st.columns(2)
            with d1_col1:
                start_cg = st.date_input("Start", value=default_start, min_value=min_date, max_value=max_date, key="s_cg")
            with d1_col2:
                end_cg = st.date_input("End", value=max_date, min_value=min_date, max_value=max_date, key="e_cg")
            
            if 'Copper/Gold' in df_ratios.columns:
                filtered_cg = df_ratios.loc[str(start_cg):str(end_cg)]
                st.line_chart(filtered_cg['Copper/Gold'], color="#FFAA00", height=300)
                
                # Explainer Box
                with st.expander("💡 Understanding the Copper/Gold Ratio", expanded=True):
                    st.markdown("""
                    **The "Doctor Copper" Indicator:**
                    * **High / Rising:** Signals **Economic Optimism** (Industrial demand > Safe haven).
                    * **Low / Falling:** Signals **Economic Fear / Recession** (Safe haven > Industrial demand).
                    """)

        # --- RIGHT: GOLD / SILVER ---
        with r2:
            st.subheader("🛡️ Risk Gauge (Gold/Silver)")
            
            # Date Selectors for Chart 2
            d2_col1, d2_col2 = st.columns(2)
            with d2_col1:
                start_gs = st.date_input("Start", value=default_start, min_value=min_date, max_value=max_date, key="s_gs")
            with d2_col2:
                end_gs = st.date_input("End", value=max_date, min_value=min_date, max_value=max_date, key="e_gs")

            if 'Gold/Silver' in df_ratios.columns:
                filtered_gs = df_ratios.loc[str(start_gs):str(end_gs)]
                st.line_chart(filtered_gs['Gold/Silver'], color="#29B5E8", height=300)
                
                # Explainer Box
                with st.expander("💡 Understanding the Gold/Silver Ratio", expanded=True):
                    st.markdown("""
                    **The Precious Metals Barometer:**
                    * **High (>80):** Signals **Defensive/Risk-Off** (Gold outperforms Silver).
                    * **Low (<60):** Signals **Risk-On / Inflationary** (Silver outperforms Gold).
                    """)

        st.caption("📝 *Note: The Copper/Gold ratio is calculated using Copper futures ($/lb) and Gold futures ($/oz). The Gold/Silver ratio uses prices per ounce for both assets.*")

    else:
        st.warning("Historical data for Metals not found.")

    st.divider()

    # =========================================================================
    # ROW 3: FORWARD CURVES (Explorer)
    # =========================================================================
    st.markdown("### 📉 Futures Forward Curves")
    
    # Check if folder exists
    if os.path.exists(FUTURES_DIR):
        files = [f for f in os.listdir(FUTURES_DIR) if f.startswith("curve_")]
        assets_avail = [f.replace("curve_", "").replace(".csv", "").replace("_", " ").title() for f in files]
        assets_avail.sort()
    else:
        assets_avail = []

    if assets_avail:
        # Selector
        c_sel, c_info = st.columns([1, 3])
        with c_sel:
            selected_asset = st.selectbox("Select Asset Chain", assets_avail)
        
        # Load Data
        file_p = os.path.join(FUTURES_DIR, f"curve_{selected_asset.lower().replace(' ', '_')}.csv")
        df_curve = pd.read_csv(file_p)
        
        # Calculate Term Structure
        first_p = df_curve['Price'].iloc[0]
        last_p = df_curve['Price'].iloc[-1]
        spread_pct = ((last_p - first_p) / first_p) * 100
        
        # Determine Status & Color
        if spread_pct > 0.5:
            status = "CONTANGO (Upward Sloping)"
            color_code = "#09AB3B" # Green
        elif spread_pct < -0.5:
            status = "BACKWARDATION (Downward Sloping)"
            color_code = "#FF4B4B" # Red
        else:
            status = "FLAT"
            color_code = "#FFFFFF"

        with c_info:
            m1, m2, m3 = st.columns(3)
            m1.metric("Front Month", f"${first_p:,.2f}")
            m2.metric("Back Month", f"${last_p:,.2f}")
            
            # Custom HTML to fit text properly
            with m3:
                st.markdown(f"""
                <div style="line-height: 1.2;">
                    <p style="font-size: 14px; margin-bottom: 0px; color: #fafafa; font-weight: 400;">
                        Structure
                    </p>
                    <p style="font-size: 18px; font-weight: bold; color: {color_code}; margin-top: 0px; margin-bottom: 0px;">
                        {status}
                    </p>
                    <p style="font-size: 16px; font-weight: bold; color: {color_code}; margin-top: -5px;">
                        {spread_pct:+.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Plotly Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_curve['Delivery'],
            y=df_curve['Price'],
            mode='lines+markers',
            line=dict(color=color_code, width=3),
            marker=dict(size=8),
            hovertemplate="Delivery: %{x}<br>Price: $%{y:.2f}<extra></extra>"
        ))
        
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
            xaxis_title="Delivery Month",
            yaxis_title="Price ($)",
            xaxis={'type': 'category'} # Preserves specific contract order
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Futures data not yet generated. Please wait for the background refresh to complete.")