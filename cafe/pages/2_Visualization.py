import streamlit as st
import pandas as pd

st.title("📈 Coffee Shop Visualization")
DATA_URL = "https://raw.githubusercontent.com/siglimumuni/Datasets/master/Coffee%20Shop%20Sales.csv"

# Load Data
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data = load_data()

# 1. PENJUALAN BERDASARKAN KATEGORI
st.subheader("Jumlah Penjualan Berdasarkan Kategori Produk")
category_sales = data.groupby("product_category")["transaction_qty"].sum()
st.bar_chart(category_sales)

# 2. PENJUALAN BERDASARKAN LOKASI TOKO
st.subheader("Jumlah Penjualan Berdasarkan Lokasi Toko")
location_sales = data.groupby("store_location")["transaction_qty"].sum()
st.bar_chart(location_sales)

# 3. FILTER JUMLAH TRANSAKSI
st.subheader("Filter Jumlah Transaksi")
min_qty = int(data["transaction_qty"].min())
max_qty = int(data["transaction_qty"].max())

qty = st.slider(
    "Pilih jumlah produk minimum",
    min_qty,
    max_qty,
    min_qty
)

filtered_data = data[data["transaction_qty"] >= qty]
st.write("Jumlah data:", len(filtered_data))
st.dataframe(filtered_data)

# 4. PENJUALAN BERDASARKAN TANGGAL
st.subheader("Jumlah Penjualan Berdasarkan Tanggal")
data["transaction_date"] = pd.to_datetime(
    data["transaction_date"]
)
daily_sales = data.groupby("transaction_date")["transaction_qty"].sum()

st.line_chart(daily_sales)