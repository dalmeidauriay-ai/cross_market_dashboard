# app/pages/p3_fx.py

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date

from services.data_loader import load_fx_matrix, load_fx_timeseries
from services.tickers_mapping import FX_PAIRS, FX_GROUPS

# ---------------------------------------------------------
# Page: FX (p3_fx)
# Responsibility: Layout only — titles, controls, and display.
# ---------------------------------------------------------


# =========================================================
# Figure: FX spot + % change matrix
# Purpose: Display matrix of spot rates and daily % changes.
# =========================================================

def _highlight_changes(val: str) -> str:
    """
    Style helper to color % change inside merged cell strings.
    Expects strings like '1.1675 (+0.32%)' or '1.1675'.
    """
    if isinstance(val, str) and "(" in val and ")" in val:
        try:
            pct_str = val.split("(")[1].split(")")[0]  # e.g., '+0.32%'
            pct = float(pct_str.replace("%", "").replace("+", ""))
            color = "green" if pct > 0 else "red" if pct < 0 else "black"
            return f"color: {color}"
        except Exception:
            return ""
    return ""


def render_fx_matrix(force_refresh: bool):
    """Render the FX spot + % change matrix."""
    merged = load_fx_matrix(force_refresh=force_refresh)
    st.subheader("Spot + % change matrix")
    styled = merged.style.map(_highlight_changes)
    st.dataframe(styled)

    with st.expander("Show raw values"):
        st.write(merged)


# =========================================================
# Figure: FX time series line chart
# Purpose: Display long-range FX history with resampling.
# =========================================================

def render_fx_timeseries(pair: str, freq: str):
    """Render a time series line chart for a selected FX pair."""
    st.subheader("📈 FX Time Series")

    series = load_fx_timeseries(pair, freq=freq)
    if series is None or series.empty:
        st.warning("No data available for this pair.")
        return

    # Ensure datetime index
    if not isinstance(series.index, pd.DatetimeIndex):
        series.index = pd.to_datetime(series.index)

    # 🔹 NEW: Date range slicer
    min_date = series.index.min().date()
    max_date = series.index.max().date()
    today = date.today()

    start_date = st.date_input(
        "Start date",
        value=min_date,          # default earliest available
        min_value=min_date,
        max_value=today,
        key="fx_start_date"
    )
    end_date = st.date_input(
        "End date",
        value=today,             # default today
        min_value=min_date,
        max_value=today,
        key="fx_end_date"
    )

    if start_date > end_date:
        st.error("Start date must be before end date.")
        return

    # Slice the series based on selected date range
    mask = (series.index.date >= start_date) & (series.index.date <= end_date)
    series = series.loc[mask]

    # Convert to DataFrame with explicit column names
    df = series.reset_index()
    df.columns = ["Date", "Price"]

    # Now Plotly Express can handle it safely
    fig = px.line(df, x="Date", y="Price", title=f"{pair} ({freq})")
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        height=400,
        legend=dict(orientation="h")
    )
    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# Main show() entry point
# =========================================================

from services.tickers_mapping import FX_GROUPS, FX_PAIRS

def show():
    st.title("💱 FX matrix")
    st.caption("Spot and daily % change across selected currencies, cached for speed.")

    with st.sidebar:
        st.subheader("FX controls")
        force_refresh = st.checkbox(
            "Force refresh from Yahoo Finance",
            value=False,
            key="fx_force_refresh"
        )
        st.info("If unchecked, the page loads the cached matrix from data/processed/.")

        st.subheader("Time Series controls")

        # 🔹 NEW: first select region
        region = st.selectbox(
            "Select FX region",
            options=list(FX_GROUPS.keys()),
            index=0,
            key="fx_region"
        )

        # 🔹 NEW: then select pair within region
        pair_name = st.selectbox(
            "Select FX pair",
            options=list(FX_GROUPS[region].keys()),
            index=0,
            key="fx_timeseries_pair"
        )

        freq = st.radio(
            "Select frequency",
            ["D", "W", "M", "Y"],
            index=0,
            key="fx_timeseries_freq"
        )

    # Render figures
    render_fx_matrix(force_refresh)
    render_fx_timeseries(pair_name, freq)