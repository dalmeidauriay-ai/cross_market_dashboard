# app/pages/p4_rates.py

import streamlit as st
import pandas as pd
from datetime import date

from services.data_loader import load_us_yields, load_oecd_yields
from services.tickers_mapping import US_YIELD_TICKERS, OECD_YIELD_TICKERS
from services.transforms import (
    plot_timeseries_lines,
    plot_oecd_snapshot,
    plot_us_yield_curve,
)

# ---------------------------------------------------------
# Page: Rates (p4_rates)
# Responsibility: Layout only — titles, controls, and display.
# ---------------------------------------------------------


def show():
    st.title("📊 Rates Dashboard")
    st.caption("U.S. Treasury yields and OECD 10Y government bond yields")

    # =========================================================
    # Sidebar controls
    # =========================================================
    with st.sidebar:
        st.subheader("Rates Controls")

        # Date range
        date_range = st.date_input(
            "Select date range",
            [pd.to_datetime("1990-01-01"), date.today()],
            key="rates_date_range"
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = date_range[0]
            end_date = date.today()

        # OECD country selector
        all_oecd_countries = list(OECD_YIELD_TICKERS.values())
        selected_countries = st.multiselect(
            "Select OECD countries (time-series)",
            options=all_oecd_countries,
            default=all_oecd_countries,
            key="rates_oecd_countries"
        )

        # U.S. Treasury maturity selector
        all_maturities = list(US_YIELD_TICKERS.values())
        default_maturities = [
            "U.S. 1M Treasury", "U.S. 6M Treasury", "U.S. 1Y Treasury",
            "U.S. 2Y Treasury", "U.S. 10Y Treasury", "U.S. 30Y Treasury"
        ]
        selected_maturities = st.multiselect(
            "Select U.S. Treasury maturities (time-series)",
            options=all_maturities,
            default=default_maturities,
            key="rates_us_maturities"
        )

        # Force refresh option
        force_refresh = st.checkbox(
            "Force refresh from FRED",
            value=False,
            key="rates_force_refresh"
        )

    # =========================================================
    # Data loading
    # =========================================================
    us_data = load_us_yields(force_refresh=force_refresh,
                             start_date=start_date, end_date=end_date)
    oecd_data = load_oecd_yields(force_refresh=force_refresh,
                                 start_date=start_date, end_date=end_date)

    # Apply friendly names
    us_data = us_data.rename(columns=US_YIELD_TICKERS)
    oecd_data = oecd_data.rename(columns=OECD_YIELD_TICKERS)

    # Apply sidebar filters
    oecd_filtered = oecd_data[selected_countries] if selected_countries else oecd_data
    us_filtered = us_data[selected_maturities] if selected_maturities else us_data

    # =========================================================
    # Layout
    # =========================================================
    st.subheader("Latest Snapshots")
    if not oecd_data.empty:
        st.pyplot(plot_oecd_snapshot(oecd_data, "OECD 10Y Government Bond Yields"))
    if not us_data.empty:
        st.pyplot(plot_us_yield_curve(us_data, "U.S. Yield Curve Snapshot"))

    st.subheader("Time-Series Evolution")
    if not oecd_filtered.empty:
        st.pyplot(plot_timeseries_lines(oecd_filtered, "OECD 10Y Yields Over Time"))
    if not us_filtered.empty:
        st.pyplot(plot_timeseries_lines(us_filtered, "U.S. Treasury Yields Over Time"))