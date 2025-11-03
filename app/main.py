import streamlit as st

# Global page config
st.set_page_config(
    page_title="Cross-Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Equities",
        "FX",
        "Rates",
        "Commodities",
        "ETFs",
        "Options & Volatility",
        "Alternatives"
    ]
)

# Import pages directly (relative to app/)
from app.pages import overview
from pages import (
    p2_equities,
    p3_fx,
    p4_rates,
    p5_commo,
    p6_etfs,
    p7_options,
    p8_alter
)

# Route to the right page
if page == "Overview":
    overview.show()

elif page == "Equities":
    p2_equities.show()

elif page == "FX":
    p3_fx.show()

elif page == "Rates":
    p4_rates.show()

elif page == "Commodities":
    p5_commo.show()

elif page == "ETFs":
    p6_etfs.show()

elif page == "Options & Volatility":
    p7_options.show()

elif page == "Alternatives":
    p8_alter.show()