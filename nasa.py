import streamlit as st
import pandas as pd
import numpy as np

# 1. SET TITLE
st.title('Distribusi Jatuhnya Meteorit di Bumi (NASA)')

# 2. SET CONSTANT & URL
DATA_URL = 'https://raw.githubusercontent.com/datasets/meteorite-landings/master/data/meteorite-landings.csv'

# 2.1 Buat Fungsi Load Data dengan Cache
@st.cache_data
def load_data(nrows):
    # Membaca data
    data = pd.read_csv(DATA_URL, nrows=nrows)
    
    # Mengubah nama kolom menjadi huruf kecil
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    
    # Mengubah nama kolom koordinat untuk st.map
    data.rename(columns={'reclat': 'lat', 'reclong': 'lon', 'mass (g)': 'mass'}, inplace=True)
    
    # Menghapus data yang tidak memiliki koordinat atau massa
    data = data.dropna(subset=['lat', 'lon', 'mass'])
    return data

# 2.2 Eksekusi Load Data
data_load_state = st.text('Loading data...')
data = load_data(5000) # Ambil 5000 baris pertama untuk kelancaran
data_load_state.text("Done! (using st.cache)")

# 3. Checkbox untuk Raw Data
if st.checkbox('Show raw data'):
    st.subheader('Raw data Meteorit')
    st.write(data)

# 4. Filter dengan Slider
st.subheader('Filter Berdasarkan Massa Meteorit (Gram)')
mass_to_filter = st.slider('Minimal Massa (Gram)', 0, 50000, 1000)
filtered_data = data[data['mass'] >= mass_to_filter]

# 5. Visualisasi Bar Chart (Jumlah meteor per kelas klasifikasi)
st.subheader('Distribusi Berdasarkan Kelas Meteorit')
# Menghitung jumlah masing-class pada data yang difilter
class_count = filtered_data['recclass'].value_counts().head(10) 
st.bar_chart(class_count)

# 6. Visualisasi Peta
st.subheader(f'Peta Sebaran Meteorit (Massa >= {mass_to_filter} g)')
st.map(filtered_data)