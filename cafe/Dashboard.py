import streamlit as st

st.set_page_config(
    page_title="Coffee Shop Sales",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Coffee Shop Sales Dashboard")

st.markdown("""
Dashboard sederhana untuk mengeksplorasi dan memvisualisasikan
data penjualan coffee shop.

Silakan pilih halaman:
- Data Explorer
- Visualization
""")