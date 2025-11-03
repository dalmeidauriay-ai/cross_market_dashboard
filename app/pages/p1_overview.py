import streamlit as st

def show():
    st.title("🌍 Market Overview")

    tab1, tab2, tab3, tab4 = st.tabs(["Indexes", "Macro", "Commodities", "FX Matrix"])

    with tab1:
        st.write("Global indexes go here...")

    with tab2:
        st.write("Macro indicators go here...")

    with tab3:
        st.write("Commodities overview goes here...")

    with tab4:
        st.write("FX matrix goes here...")