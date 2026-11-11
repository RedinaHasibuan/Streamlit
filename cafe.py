import streamlit as st
import pandas as pd
import numpy as np

st.title('Peta Persebaran Pastry Cafe & Bakery 🥐')
st.write('Aplikasi interaktif untuk mengeksplorasi lokasi cafe dengan pastry terbaik!')

@st.cache_data
def load_pastry_data():
    data = pd.DataFrame({
        'Name': ['Croissant Corner', 'Artisan Bakery', 'Sweet Danish', 'Butter & Flour', 
                 'Bakehouse 99', 'The Daily Pastry', 'Flaky & Co', 'Choco Bakery'],
        'Lat': [-6.175392, -6.190000, -6.160000, -6.185000, -6.170000, -6.200000, -6.155000, -6.165000],
        'Lon': [106.827153, 106.830000, 106.810000, 106.840000, 106.800000, 106.820000, 106.835000, 106.815000],
        'Rating': [4.8, 4.2, 3.9, 4.5, 4.0, 4.7, 3.8, 4.6],
        'Avg_Price_K': [35, 50, 25, 45, 30, 60, 20, 40]
    })
    
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Memuat data pastry cafe...')
data = load_pastry_data()
data_load_state.text("Selesai memuat data! (menggunakan st.cache)")

if st.checkbox('Tampilkan data mentah'):
    st.subheader('Daftar Pastry Cafe')
    st.write(data)

st.markdown("---")

chart_data = data.set_index('name')

st.subheader('1. Distribusi Rating Cafe')
rating_counts = np.histogram(data['rating'], bins=5, range=(3.0, 5.0))[0]
st.bar_chart(rating_counts)

st.subheader('2. Tren Harga Rata-rata Pastry (Ribuan Rupiah)')
st.line_chart(chart_data['avg_price_k'])

st.subheader('3. Area Chart: Fluktuasi Harga Pastry')
st.area_chart(chart_data['avg_price_k'])

st.markdown("---")
min_rating = st.slider('Pilih Rating Minimum Cafe:', 3.0, 5.0, 4.0, step=0.1)

filtered_data = data[data['rating'] >= min_rating]

st.subheader(f'4. Peta Lokasi Cafe dengan Rating >= {min_rating}')
st.map(filtered_data)