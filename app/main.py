import streamlit as st

# ---------------------------------------------------------
# Global page configuration
# ---------------------------------------------------------
# This sets up the dashboard's title, layout, and sidebar state.
# - page_title: Title shown in the browser tab
# - layout: "wide" gives more horizontal space for charts
# - initial_sidebar_state: "expanded" means sidebar is open by default
#   (we won't use it for navigation, but later for slicers/filters)
st.set_page_config(
    page_title="Cross-Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Data refresh on app startup
# ---------------------------------------------------------
# Each time the dashboard is launched, we run a lightweight
# refresh check. This looks at refresh_tracker.csv under
# data/processed/ and decides whether to update cached CSVs.
# - Historical datasets (FX_historical.csv) → refresh once per day
# - Snapshot datasets (FX_rate_matrix.csv, us_yields.csv, oecd_yields.csv) → refresh if older than 1 hour
# The refresh logic updates both the CSVs and the tracker timestamps.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from jobs.refresh_data import run_refresh
# Safe refresh — won’t break the app if the tracker is missing or invalid
try:
  from jobs.refresh_data import run_refresh
  run_refresh()
  st.sidebar.success("Data refreshed via tracker rules.")
except Exception as e:
  st.sidebar.warning(f"Refresh skipped: {e}")


# ---------------------------------------------------------
# Import all page modules
# ---------------------------------------------------------
# Each page is a separate Python file inside the "pages" folder.
# Every page file must define a `show()` function that renders its content.
from pages import (
    p1_overview,
    p2_equities,
    p3_fx,
    p4_rates,
    p5_commo,
    p6_etfs,
    p7_options,
    p8_alter
)

# ---------------------------------------------------------
# Custom CSS to normalize button sizes
# ---------------------------------------------------------
# Streamlit buttons normally size themselves based on text length.
# This CSS forces all buttons to have the same width and height,
# so they align neatly in the top ribbon.
st.markdown(
    """
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 3em;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Initialize session state for current page
# ---------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"


# ---------------------------------------------------------
# Top navigation ribbon
# ---------------------------------------------------------
# We create 8 equal-width columns for navigation buttons.
# Each column will contain one button corresponding to a page.
cols = st.columns(8)

# Define the mapping between button labels and page names
pages = [
    ("Overview", "Overview"),
    ("Equities", "Equities"),
    ("FX", "FX"),
    ("Rates", "Rates"),
    ("Commodities", "Commodities"),
    ("ETFs", "ETFs"),
    ("Options & Volatility", "Options & Volatility"),
    ("Alternatives", "Alternatives"),
]

# Variable to store which page is selected
page = None

# Render each button inside its column
for col, (label, name) in zip(cols, pages):
    with col:
        if st.button(label):
            st.session_state.current_page = name # Update current page on button click


# ---------------------------------------------------------
# Page routing
# ---------------------------------------------------------
# Based on the selected page, call the corresponding `show()` function.
# Each page module handles its own layout and content.

if st.session_state.current_page == "Overview":
    p1_overview.show()

elif st.session_state.current_page == "Equities":
    p2_equities.show()

elif st.session_state.current_page == "FX":
    p3_fx.show()

elif st.session_state.current_page == "Rates":
    p4_rates.show()

elif st.session_state.current_page == "Commo":
    p5_commo.show()

elif st.session_state.current_page == "ETFs":
    p6_etfs.show()

elif st.session_state.current_page == "Options & Volatility":
    p7_options.show()

elif st.session_state.current_page == "Alternatives":
    p8_alter.show()



