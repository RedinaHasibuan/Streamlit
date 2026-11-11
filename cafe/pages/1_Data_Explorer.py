import streamlit as st
import pandas as pd
import time

st.title("📊 Coffee Shop Data Explorer")
DATA_URL = "https://raw.githubusercontent.com/siglimumuni/Datasets/master/Coffee%20Shop%20Sales.csv"

# Progress Bar
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Loading Data... {i + 1}%")
    bar.progress(i + 1)
    time.sleep(0.01)

latest_iteration.empty()
bar.empty()

# Load Data
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data = load_data()
st.success("Data berhasil dimuat!")

# Nampilin Raw Data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

# Informasi Dataset
st.subheader("Informasi Dataset")
st.write("Jumlah baris:", data.shape[0])
st.write("Jumlah kolom:", data.shape[1])

# Nama Kolom
st.subheader("Nama Kolom")
st.write(data.columns.tolist())

# Statistik
st.subheader("Statistik Deskriptif")
st.write(data.describe())