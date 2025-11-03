import streamlit as st

def show():
    st.title("📈 Equities")

    # Sidebar slicer
    stock = st.sidebar.selectbox(
        "Choose a stock:",
        ["AAPL", "MSFT", "GOOG", "AMZN"]
    )

    st.write(f"You selected: {stock}")
    st.line_chart([1, 2, 3, 4])  # placeholder chart