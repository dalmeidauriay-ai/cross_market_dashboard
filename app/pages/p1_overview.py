import streamlit as st
import pandas as pd
from app.services.data_loader import load_indices_snapshot, load_macro_data, load_news_data
from app.services.tickers_mapping import INDICES

def show():
    st.title("🌍 Market Command Center")

    # Load data
    indices_df = load_indices_snapshot(force_refresh=False)
    macro_data = load_macro_data(force_refresh=False)
    news_headlines = load_news_data("^GSPC", 50)

    # Top Row: Indices by Region
    st.header("Global Indices")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Americas")
        americas_df = indices_df[indices_df["Region"] == "Americas"]
        if not americas_df.empty:
            display_df = americas_df[["Name", "Price", "DailyChange"]].copy()
            display_df["DailyChange"] = display_df["DailyChange"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "")
            st.dataframe(display_df.style.apply(lambda x: ['color: green' if isinstance(v, str) and v.startswith('+') else 'color: red' if isinstance(v, str) and v.startswith('-') else '' for v in x] if x.name == 'DailyChange' else [''] * len(x), axis=0))

    with col2:
        st.subheader("Europe")
        europe_df = indices_df[indices_df["Region"] == "Europe"]
        if not europe_df.empty:
            display_df = europe_df[["Name", "Price", "DailyChange"]].copy()
            display_df["DailyChange"] = display_df["DailyChange"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "")
            st.dataframe(display_df.style.apply(lambda x: ['color: green' if isinstance(v, str) and v.startswith('+') else 'color: red' if isinstance(v, str) and v.startswith('-') else '' for v in x] if x.name == 'DailyChange' else [''] * len(x), axis=0))

    with col3:
        st.subheader("Asia")
        asia_df = indices_df[indices_df["Region"] == "Asia"]
        if not asia_df.empty:
            display_df = asia_df[["Name", "Price", "DailyChange"]].copy()
            display_df["DailyChange"] = display_df["DailyChange"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "")
            st.dataframe(display_df.style.apply(lambda x: ['color: green' if isinstance(v, str) and v.startswith('+') else 'color: red' if isinstance(v, str) and v.startswith('-') else '' for v in x] if x.name == 'DailyChange' else [''] * len(x), axis=0))

    # Middle Row: Macro Indicators
    st.header("Macro Indicators")
    
    # GDP
    st.subheader("GDP (Quarterly, Billions USD)")
    gdp_cols = st.columns(len(macro_data.get("GDP", {})))
    for i, (country, data) in enumerate(macro_data.get("GDP", {}).items()):
        with gdp_cols[i]:
            st.metric(f"{country} GDP", f"${data['value']:.0f}B", f"{data['change']:+.1f}%")

    # Inflation
    st.subheader("Inflation (YoY %)")
    infl_data = macro_data.get("Inflation", {})
    if infl_data:
        euro_infl = infl_data.get("Euro Area CPI", 0)
        us_infl = infl_data.get("US CPI", 0)
        fr_infl = infl_data.get("France CPI", 0)
        st.metric("Euro Area Inflation", f"{euro_infl:+.1f}%")
        st.metric("US Inflation", f"{us_infl:+.1f}%", f"FR: {fr_infl:+.1f}%")

    # Rates
    st.subheader("Interest Rates")
    rates_data = macro_data.get("Rates", {})
    if rates_data:
        fed_rate = rates_data.get("Fed Funds Rate", 0)
        ecb_rate = rates_data.get("ECB Main Refinancing Rate", 0)
        st.metric("Fed Funds Rate", f"{fed_rate:.2f}%")
        st.metric("ECB Rate", f"{ecb_rate:.2f}%")

    # Commodities/Other
    st.subheader("Other Indicators")
    yahoo_data = macro_data.get("Yahoo", {})
    yahoo_cols = st.columns(len(yahoo_data))
    for i, (name, value) in enumerate(yahoo_data.items()):
        with yahoo_cols[i]:
            st.metric(name, f"{value:.2f}")

    # Bottom Row: News
    st.header("Market News (S&P 500)")
    with st.container(height=300):
        for headline in news_headlines:
            st.markdown(f"- {headline}")