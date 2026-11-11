import streamlit as st
import joblib
import os
import numpy as np 

# Fungsi untuk memuat file model dari folder models
def load_prediction_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file), "rb"))
    return loaded_model

def main():
    st.title("Prediksi Pendapatan Coffee Shop")

    # Membuat kotak header
    html_templ = """
    <div style="background-color:#726E6D;padding:10px;">
    <h3 style="color:white">Estimasi Pendapatan Harian Menggunakan Regresi Linier</h3>
    </div>
    """
    st.markdown(html_templ, unsafe_allow_html=True)

    # Membuat menu di samping
    activity = ["Prediksi Pendapatan", "Apa itu Regresi?"]
    choice = st.sidebar.selectbox("Menu", activity)

    # Halaman Utama
    if choice == 'Prediksi Pendapatan':
        st.subheader("Simulasi Pendapatan Harian")
        
        # Slider input sesuai Pilihan 2 (Jumlah Transaksi Harian)
        transactions = st.slider("Berapa perkiraan jumlah transaksi hari ini?", 10, 1000, 300)

        if st.button("Proses Prediksi"):
            # Memuat model yang sudah kamu buat di Colab
            regressor = load_prediction_model("models/linear_regression_coffee.pkl")
            transactions_reshaped = np.array(transactions).reshape(-1, 1)
            
            # Melakukan prediksi pendapatan
            predicted_revenue = regressor.predict(transactions_reshaped)
            
            st.success(f"Estimasi total pendapatan toko untuk {transactions} transaksi harian adalah: ${predicted_revenue[0][0]:.2f}")

    # Halaman Info
    elif choice == 'Apa itu Regresi?':
        st.subheader("Tentang Regresi Linier")
        st.write("Regresi Linier Sederhana ini digunakan untuk memprediksi nilai total pendapatan harian toko berdasarkan estimasi jumlah struk/transaksi yang masuk.")

if __name__ == '__main__':
    main()