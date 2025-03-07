import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    hour_df = pd.read_csv("data/hour.csv")
    
    # Konversi kolom dteday ke datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Tambahkan kolom nama untuk kategori
    weather_map = {1: 'Cerah/Sedikit awan', 2: 'Berkabut/Berawan', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
    holiday_map = {0: 'Bukan Hari Libur', 1: 'Hari Libur'}
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    
    day_df['weathersit_name'] = day_df['weathersit'].map(weather_map)
    day_df['holiday_name'] = day_df['holiday'].map(holiday_map)
    day_df['season_name'] = day_df['season'].map(season_map)
    
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Sidebar
st.sidebar.title("Bike Sharing Dashboard")
# st.sidebar.image("https://img.freepik.com/free-vector/city-bike-rental-abstract-concept-illustration_335657-3789.jpg", width=200)

# Menu navigasi
menu = st.sidebar.radio(
    "Pilih Analisis:",
    ["Beranda", "Faktor yang Mempengaruhi Penyewaan", "Analisis Waktu Optimal", "Pengaruh Cuaca", "Time Series Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Proyek Analisis Data**
- Nama: Ummam Hoerussifa
- Email: ummamhoerussifa@gmail.com
- ID Coding Camp: M299D5Y2175
""")

# Beranda
if menu == "Beranda":
    st.title("🚲 Dashboard Analisis Data Bike Sharing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tentang Dataset")
        st.write("""
        Dataset Bike Sharing berisi informasi tentang penyewaan sepeda harian dan per jam 
        selama periode 2011-2012. Dataset ini mencakup informasi tentang kondisi cuaca, 
        musim, hari libur, dan faktor lain yang mungkin mempengaruhi jumlah penyewaan sepeda.
        """)
        
        st.subheader("Pertanyaan Analisis")
        st.write("""
        1. Faktor apa yang paling mempengaruhi jumlah penyewaan sepeda?
        2. Kapan waktu paling optimal untuk menambah jumlah sepeda berdasarkan tren penyewaan?
        3. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
        """)
    
    with col2:
        # Tampilkan ringkasan statistik
        st.subheader("Ringkasan Data")
        
        # Metrik utama
        total_rentals = day_df['cnt'].sum()
        avg_daily_rentals = day_df['cnt'].mean()
        max_daily_rentals = day_df['cnt'].max()
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Penyewaan", f"{total_rentals:,}")
        col_b.metric("Rata-rata Harian", f"{avg_daily_rentals:.0f}")
        col_c.metric("Penyewaan Maksimum", f"{max_daily_rentals:,}")
        
        # Grafik tren penyewaan selama periode data
        st.subheader("Tren Penyewaan Sepeda")
        fig = px.line(day_df, x='dteday', y='cnt', title='Jumlah Penyewaan Sepeda Harian')
        fig.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penyewaan')
        st.plotly_chart(fig, use_container_width=True)

# Faktor yang Mempengaruhi Penyewaan
elif menu == "Faktor yang Mempengaruhi Penyewaan":
    st.title("Faktor yang Mempengaruhi Jumlah Penyewaan Sepeda")
    
    # Korelasi antara variabel numerik dan jumlah penyewaan
    st.subheader("Korelasi antara Variabel dan Jumlah Penyewaan")
    
    # Pilih kolom numerik yang relevan
    numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
    corr = day_df[numeric_cols].corr()
    
    # Heatmap korelasi
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    
    st.write("""
    **Interpretasi:**
    - Temperatur (temp) dan temperatur yang dirasakan (atemp) memiliki korelasi positif tertinggi dengan jumlah penyewaan.
    - Kelembaban (hum) memiliki korelasi negatif dengan jumlah penyewaan.
    - Kecepatan angin (windspeed) memiliki korelasi negatif lemah dengan jumlah penyewaan.
    """)
    
    # Scatter plot untuk melihat hubungan antara temperatur dan jumlah penyewaan
    st.subheader("Hubungan antara Temperatur dan Jumlah Penyewaan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(day_df, x='temp', y='cnt', 
                         trendline='ols', 
                         title='Temperatur vs Jumlah Penyewaan')
        fig.update_layout(xaxis_title='Temperatur (Normalized)', 
                          yaxis_title='Jumlah Penyewaan')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(day_df, x='hum', y='cnt', 
                         trendline='ols', 
                         title='Kelembaban vs Jumlah Penyewaan')
        fig.update_layout(xaxis_title='Kelembaban (Normalized)', 
                          yaxis_title='Jumlah Penyewaan')
        st.plotly_chart(fig, use_container_width=True)
    
    # Pengaruh musim terhadap penyewaan
    st.subheader("Pengaruh Musim Terhadap Jumlah Penyewaan")
    
    # Agregasi data berdasarkan musim
    season_agg = day_df.groupby('season_name')['cnt'].agg(['mean', 'sum']).reset_index()
    season_agg = season_agg.sort_values('mean', ascending=False)
    
    fig = px.bar(season_agg, x='season_name', y='mean', 
                 title='Rata-rata Penyewaan Berdasarkan Musim',
                 color='season_name',
                 text_auto='.0f')
    fig.update_layout(xaxis_title='Musim', yaxis_title='Rata-rata Penyewaan')
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    **Interpretasi:**
    - Musim Fall (Gugur) memiliki rata-rata penyewaan tertinggi.
    - Musim Spring (Semi) memiliki rata-rata penyewaan terendah.
    """)

# Analisis Waktu Optimal
elif menu == "Analisis Waktu Optimal":
    st.title("Waktu Optimal untuk Menambah Jumlah Sepeda")
    
    # Analisis berdasarkan bulan
    st.subheader("Penyewaan Berdasarkan Bulan")
    
    # Konversi bulan dari angka ke nama
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    day_df['month_name'] = day_df['mnth'].map(month_names)
    
    # Agregasi data berdasarkan bulan
    monthly_agg = day_df.groupby('mnth').agg({
        'cnt': ['mean', 'sum'],
        'month_name': 'first'
    }).reset_index()
    monthly_agg.columns = ['month_num', 'mean', 'sum', 'month_name']
    monthly_agg = monthly_agg.sort_values('month_num')
    
    # Plot rata-rata penyewaan per bulan
    fig = px.bar(monthly_agg, x='month_name', y='mean', 
                 title='Rata-rata Penyewaan Sepeda per Bulan',
                 color='mean',
                 text_auto='.0f')
    fig.update_layout(xaxis_title='Bulan', yaxis_title='Rata-rata Penyewaan')
    st.plotly_chart(fig, use_container_width=True)
    
    # Analisis berdasarkan hari dalam seminggu
    st.subheader("Penyewaan Berdasarkan Hari dalam Seminggu")
    
    # Konversi hari dari angka ke nama
    day_names = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 
                 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    day_df['day_name'] = day_df['weekday'].map(day_names)
    
    # Agregasi data berdasarkan hari
    daily_agg = day_df.groupby('weekday').agg({
        'cnt': ['mean', 'sum'],
        'day_name': 'first'
    }).reset_index()
    daily_agg.columns = ['weekday', 'mean', 'sum', 'day_name']
    daily_agg = daily_agg.sort_values('weekday')
    
    # Plot rata-rata penyewaan per hari
    fig = px.bar(daily_agg, x='day_name', y='mean', 
                 title='Rata-rata Penyewaan Sepeda per Hari',
                 color='mean',
                 text_auto='.0f')
    fig.update_layout(xaxis_title='Hari', yaxis_title='Rata-rata Penyewaan')
    st.plotly_chart(fig, use_container_width=True)
    
    # Analisis berdasarkan jam (dari dataset hour)
    st.subheader("Penyewaan Berdasarkan Jam")
    
    # Agregasi data berdasarkan jam
    hourly_agg = hour_df.groupby('hr')['cnt'].mean().reset_index()
    
    # Plot rata-rata penyewaan per jam
    fig = px.line(hourly_agg, x='hr', y='cnt', 
                  title='Rata-rata Penyewaan Sepeda per Jam',
                  markers=True)
    fig.update_layout(xaxis_title='Jam', yaxis_title='Rata-rata Penyewaan')
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    **Interpretasi:**
    - Bulan Juni hingga September memiliki rata-rata penyewaan tertinggi, dengan puncaknya di bulan September.
    - Hari kerja (Senin-Jumat) memiliki pola penyewaan yang relatif stabil, sementara akhir pekan memiliki pola yang berbeda.
    - Terdapat dua puncak penyewaan dalam sehari: pagi hari (sekitar jam 8) dan sore hari (sekitar jam 17-18), 
      yang menunjukkan pola penggunaan untuk perjalanan ke dan dari tempat kerja.
    """)

# Pengaruh Cuaca
elif menu == "Pengaruh Cuaca":
    st.title("Pengaruh Kondisi Cuaca Terhadap Jumlah Penyewaan Sepeda")
    
    # Pengaruh kondisi cuaca
    st.subheader("Pengaruh Kondisi Cuaca")
    
    # Agregasi data berdasarkan kondisi cuaca
    weather_agg = day_df.groupby('weathersit_name')['cnt'].agg(['mean', 'count']).reset_index()
    weather_agg = weather_agg.sort_values('mean', ascending=False)
    
    # Plot rata-rata penyewaan berdasarkan kondisi cuaca
    fig = px.bar(weather_agg, x='weathersit_name', y='mean', 
                 title='Rata-rata Penyewaan Berdasarkan Kondisi Cuaca',
                 color='weathersit_name',
                 text_auto='.0f')
    fig.update_layout(xaxis_title='Kondisi Cuaca', yaxis_title='Rata-rata Penyewaan')
    st.plotly_chart(fig, use_container_width=True)
    
    # Box plot untuk melihat distribusi penyewaan berdasarkan kondisi cuaca
    st.subheader("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
    
    fig = px.box(day_df, x='weathersit_name', y='cnt', 
                 title='Distribusi Penyewaan Berdasarkan Kondisi Cuaca',
                 color='weathersit_name')
    fig.update_layout(xaxis_title='Kondisi Cuaca', yaxis_title='Jumlah Penyewaan')
    st.plotly_chart(fig, use_container_width=True)

# Time Series Analysis
elif menu == "Time Series Analysis":
    st.title("Time Series Analysis")
    
    # Pengaruh musim terhadap penyewaan
    st.subheader("Pengaruh Musim Terhadap Jumlah Penyewaan")
    
    # Agregasi data berdasarkan musim
    season_agg = day_df.groupby('season_name')['cnt'].agg(['mean', 'sum']).reset_index()
    season_agg = season_agg.sort_values('mean', ascending=False)
    
    fig = px.bar(season_agg, x='season_name', y='mean', 
                 title='Rata-rata Penyewaan Berdasarkan Musim',
                 color='season_name',
                 text_auto='.0f')
    fig.update_layout(xaxis_title='Musim', yaxis_title='Rata-rata Penyewaan')
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("""
    **Interpretasi:**
    - Bulan Juni hingga September memiliki rata-rata penyewaan tertinggi, dengan puncaknya di bulan September.
    - Hari kerja (Senin-Jumat) memiliki pola penyewaan yang relatif stabil, sementara akhir pekan memiliki pola yang berbeda.
    - Terdapat dua puncak penyewaan dalam sehari: pagi hari (sekitar jam 8) dan sore hari (sekitar jam 17-18), 
      yang menunjukkan pola penggunaan untuk perjalanan ke dan dari tempat kerja.
    """)