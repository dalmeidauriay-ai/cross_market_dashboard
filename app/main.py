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

# Route to the right page
if page == "Overview":
    from app.pages import p1_overview as overview
    overview.show()

elif page == "Equities":
    from app.pages import p2_equities as equities
    equities.show()

elif page == "FX":
    from app.pages import p3_fx as fx
    fx.show()

elif page == "Rates":
    from app.pages import p4_rates as rates
    rates.show()

elif page == "Commodities":
    from app.pages import p5_commodities as commodities
    commodities.show()

elif page == "ETFs":
    from app.pages import p6_etfs as etfs
    etfs.show()

elif page == "Options & Volatility":
    from app.pages import p7_options as options
    options.show()

elif page == "Alternatives":
    from app.pages import p8_alternatives as alternatives
    alternatives.show()