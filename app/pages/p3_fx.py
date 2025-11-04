# app/pages/p3_fx.py

import streamlit as st
import plotly.express as px
import pandas as pd

from services.data_loader import load_fx_matrix, load_fx_timeseries

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
    st.dataframe(styled, use_container_width=True)

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

def show():
    # Page header
    st.title("💱 FX matrix")
    st.caption("Spot and daily % change across selected currencies, cached for speed.")

    # Sidebar controls
    with st.sidebar:
        st.subheader("FX controls")
        force_refresh = st.checkbox(
            "Force refresh from Yahoo Finance",
            value=False,
            key="fx_force_refresh"
        )
        st.info("If unchecked, the page loads the cached matrix from data/processed/.")

        st.subheader("Time Series controls")
        pair = st.selectbox(
            "Select FX pair",
            ["EURUSD=X", "GBPUSD=X", "JPY=X", "CHFUSD=X"],
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
    render_fx_timeseries(pair, freq)