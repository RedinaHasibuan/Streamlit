import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# ---------------------------------------------------------
# SETUP & CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Dashboard Clustering Pesta", layout="wide")
st.title("📊 Dashboard K-Means Text Clustering (Topik: Pesta)")
st.write("Aplikasi analisis pengelompokan tweet, frekuensi kata, dan visualisasi cluster.")

# Download NLTK Stopwords
@st.cache_resource
def load_nltk():
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_id = stopwords.words('indonesian')
    custom_stop = ['yg', 'ga', 'ngga', 'engga', 'ya', 'yaa', 'dah', 'yuk', 'amp', 'rt', 'via', 'ini', 'ada', 'di', 'pesta']
    return list(set(stop_id + custom_stop))

stop_words = load_nltk()

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('pesta_clean.csv').dropna(subset=['clean_text'])

df = load_data()

# ---------------------------------------------------------
# SIDEBAR CONTROL
# ---------------------------------------------------------
st.sidebar.header("Pengaturan Model")
k_cluster = st.sidebar.slider("Pilih Jumlah Cluster (K):", min_value=2, max_value=8, value=4)

# ---------------------------------------------------------
# PROCESS CLUSTERING
# ---------------------------------------------------------
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(df['clean_text'].astype(str))

kmeans = KMeans(n_clusters=k_cluster, random_state=42, max_iter=100, n_init=10)
kmeans.fit(X)
df['cluster'] = kmeans.labels_

score = silhouette_score(X, kmeans.labels_)

# ---------------------------------------------------------
# TABS TAMPILAN
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📌 Data & Ringkasan", "📊 Frekuensi & WordCloud", "🎯 Visualisasi Cluster (PCA)", "🔑 Top Words Cluster"])

with tab1:
    st.subheader("Data Tweet Clean")
    st.dataframe(df[['clean_text', 'cluster']].head(100), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Data Tweet", len(df))
    with col2:
        st.metric("Silhouette Score", f"{score:.4f}")

with tab2:
    col_a, col_b = st.columns(2)
    
    all_words = []
    for text in df['clean_text'].astype(str):
        words = [w for w in text.split() if w.lower() not in stop_words and len(w) > 2]
        all_words.extend(words)
        
    with col_a:
        st.subheader("10 Kata Terbanyak")
        top_words = Counter(all_words).most_common(10)
        words, counts = zip(*top_words)
        
        fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
        bars = ax_bar.bar(words, counts, color=plt.cm.tab10.colors[:len(words)])
        ax_bar.set_xticklabels(words, rotation=45)
        for bar in bars:
            yval = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center', va='bottom')
        st.pyplot(fig_bar)
        
    with col_b:
        st.subheader("WordCloud Teks")
        wc = WordCloud(width=600, height=400, background_color='black', max_words=100).generate(" ".join(all_words))
        fig_wc, ax_wc = plt.subplots(figsize=(6, 4))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)

with tab3:
    st.subheader("Scatter Plot Cluster (PCA 2D)")
    pca = PCA(n_components=2, random_state=42)
    reduced_features = pca.fit_transform(X.toarray())
    reduced_centroids = pca.transform(kmeans.cluster_centers_)
    
    fig_pca, ax_pca = plt.subplots(figsize=(8, 5))
    scatter = ax_pca.scatter(reduced_features[:, 0], reduced_features[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.6)
    ax_pca.scatter(reduced_centroids[:, 0], reduced_centroids[:, 1], marker='x', s=150, c='red', label='Centroids')
    ax_pca.set_xlabel('PCA 1')
    ax_pca.set_ylabel('PCA 2')
    fig_pca.colorbar(scatter, ax=ax_pca, label='Cluster')
    ax_pca.legend()
    ax_pca.grid(True)
    st.pyplot(fig_pca)

with tab4:
    st.subheader("Kata Kunci Utama Tiap Cluster")
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    for i in range(k_cluster):
        top_terms = [terms[ind] for ind in order_centroids[i, :8]]
        st.write(f"**Cluster {i}:** {', '.join(top_terms)}")