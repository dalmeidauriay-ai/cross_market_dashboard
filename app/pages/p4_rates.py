import streamlit as st
import pandas as pd

def show():
    st.title("📉 Rates")

    st.write("This page displays yield curves for selected countries.")

    # Sidebar slicer for country selection
    country = st.sidebar.selectbox(
        "Select Country",
        ["USA", "Germany", "Japan", "UK"]
    )

    # Example maturities and dummy yields (replace with real data later)
    maturities = ["1Y", "2Y", "5Y", "10Y", "30Y"]
    yields = {
        "USA": [5.1, 4.8, 4.3, 4.0, 3.9],
        "Germany": [3.2, 3.0, 2.7, 2.5, 2.4],
        "Japan": [0.1, 0.2, 0.3, 0.5, 0.8],
        "UK": [4.5, 4.3, 4.0, 3.8, 3.7],
    }

    df = pd.DataFrame({
        "Maturity": maturities,
        "Yield": yields[country]
    })

    st.line_chart(df.set_index("Maturity"))