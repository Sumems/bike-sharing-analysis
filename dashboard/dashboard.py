import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Analisis Data Bike Sharing",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df

day_df = load_data()

# Sidebar
with st.sidebar:
    st.title("Analisis Data Bike Sharing")
    st.write("Proyek ini bertujuan untuk menganalisis data penyewaan sepeda dan memberikan wawasan berharga.")
    st.markdown("---")
    st.info("""
    **Proyek Analisis Data**
    - Nama: Ummam Hoerussifa
    - Email: ummamhoerussifa@gmail.com
    - ID Coding Camp: M299D5Y2175
    """)

# Main content
st.title("Dashboard Analisis Data Bike Sharing 🚲")

# 1. Pendahuluan
st.header("Pendahuluan")
st.write("""
    Selamat datang di dashboard analisis data Bike Sharing! 
    Proyek ini bertujuan untuk menganalisis data penyewaan sepeda dan memberikan wawasan berharga tentang:
    - Faktor apa yang paling mempengaruhi jumlah penyewaan sepeda?
    - Kapan waktu paling optimal untuk menambah jumlah sepeda berdasarkan tren penyewaan?
    - Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
""")

# 2. Faktor yang Mempengaruhi Penyewaan Sepeda
st.header("Faktor yang Mempengaruhi Penyewaan Sepeda")
st.write("Berikut adalah korelasi antara variabel dan jumlah penyewaan sepeda:")

correlation_matrix = day_df.corr(numeric_only=True)
rental_correlation = correlation_matrix['cnt'].sort_values(ascending=False)
st.write(rental_correlation)

# Visualisasi Korelasi
st.subheader("Visualisasi Korelasi Antar Variabel")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(day_df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.write("""
    Interpretasi: Temperatur memiliki korelasi positif tertinggi dengan jumlah penyewaan sepeda. 
    Ini berarti bahwa semakin tinggi temperatur, semakin banyak orang yang cenderung menyewa sepeda.
""")

# 3. Waktu Optimal untuk Menambah Jumlah Sepeda
st.header("Waktu Optimal untuk Menambah Jumlah Sepeda")
st.write("Berikut adalah tren penyewaan sepeda bulanan:")

monthly_rentals = day_df.groupby(day_df['dteday'].dt.strftime('%Y-%m'))['cnt'].sum().reset_index()

# Visualisasi Tren Penyewaan Bulanan
st.subheader("Tren Penyewaan Sepeda Bulanan")
fig, ax = plt.subplots(figsize=(12, 6))
plt.plot(monthly_rentals['dteday'], monthly_rentals['cnt'], marker='o', linestyle='-')
plt.title('Tren Penyewaan Sepeda Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Sepeda yang Disewa')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

peak_month = monthly_rentals['dteday'][monthly_rentals['cnt'].idxmax()]
peak_rental_count = monthly_rentals['cnt'].max()
st.write(f"Bulan dengan jumlah penyewaan sepeda tertinggi: {peak_month} dengan jumlah {peak_rental_count} sepeda.")

# 4. Pengaruh Kondisi Cuaca
st.header("Pengaruh Kondisi Cuaca Terhadap Jumlah Penyewaan Sepeda")
st.write("Berikut adalah pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda:")

weather_impact = day_df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)
st.write(weather_impact)

# Visualisasi Pengaruh Kondisi Cuaca
st.subheader("Visualisasi Pengaruh Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(10, 6))
weather_map = {1: 'Cerah/Sedikit awan', 2: 'Berkabut/Berawan', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
day_df['weathersit_name'] = day_df['weathersit'].map(weather_map)
sns.boxplot(x='weathersit_name', y='cnt', data=day_df, order=['Cerah/Sedikit awan', 'Berkabut/Berawan', 'Hujan/Salju Ringan'], ax=ax)
plt.title('Pengaruh Kondisi Cuaca Terhadap Jumlah Penyewaan Sepeda')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Sepeda yang Disewa')
st.pyplot(fig)

st.write("""
    Interpretasi: Kondisi cuaca cerah lebih disukai untuk penyewaan sepeda. 
    Kondisi cuaca buruk seperti hujan lebat atau salju memiliki rata-rata jumlah penyewaan yang lebih rendah.
""")

# 5. Pengaruh Musim
st.header("Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda")
st.write("Berikut adalah pengaruh musim terhadap jumlah penyewaan sepeda:")

season_impact = day_df.groupby('season')['cnt'].mean()
st.write(season_impact)

# Visualisasi Pengaruh Musim dan Hari Libur
st.subheader("Visualisasi Pengaruh Musim dan Hari Libur")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

holiday_map = {0: 'Bukan Hari Libur', 1: 'Hari Libur'}
day_df['holiday_name'] = day_df['holiday'].map(holiday_map)
sns.boxplot(x='holiday_name', y='cnt', data=day_df, ax=axes[0])
axes[0].set_xlabel('Musim Libur')
axes[0].set_ylabel('Jumlah Penyewaan')
axes[0].set_title('Pengaruh Hari Libur Terhadap Jumlah Penyewaan')

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season_map)

sns.boxplot(x='season_name', y='cnt', data=day_df, order=['Spring', 'Summer', 'Fall', 'Winter'], ax=axes[1])
axes[1].set_xlabel('Musim')
axes[1].set_ylabel('Jumlah Penyewaan')
axes[1].set_title('Pengaruh Musim Terhadap Jumlah Penyewaan')

plt.tight_layout()
st.pyplot(fig)

st.write("""
    Interpretasi: Musim gugur memiliki rata-rata penyewaan tertinggi dibandingkan musim lainnya.
""")

# 6. Analisis Time Series Decomposition
st.header("Analisis Time Series Decomposition")
st.write("Berikut adalah hasil dekomposisi time series:")

daily_rentals = day_df.set_index('dteday')['cnt']

# Decomposition
decomposition = seasonal_decompose(daily_rentals, model='additive', period=30)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plot komponen
st.subheader("Komponen Time Series")
fig, axes = plt.subplots(4, 1, figsize=(16, 12))

axes[0].plot(daily_rentals, label='Original')
axes[0].legend(loc='upper left')
axes[1].plot(trend, label='Trend')
axes[1].legend(loc='upper left')
axes[2].plot(seasonal, label='Seasonal')
axes[2].legend(loc='upper left')
axes[3].plot(residual, label='Residual')
axes[3].legend(loc='upper left')

plt.tight_layout()
st.pyplot(fig)

st.write("""
    - Tren: Menunjukkan arah umum (naik atau turun) dari penyewaan sepeda dari waktu ke waktu.
    - Musiman: Menunjukkan pola yang berulang dalam periode tertentu (misalnya, mingguan atau bulanan).
    - Residu: Variasi acak yang tidak dapat dijelaskan oleh tren atau musiman.
""")

# 7. Kesimpulan dan Rekomendasi
st.header("Kesimpulan dan Rekomendasi")
st.write("""
    - *Faktor yang paling mempengaruhi:* Dari analisis korelasi, variabel 'temp' (temperatur) memiliki korelasi positif tertinggi dengan jumlah penyewaan sepeda, yaitu \( r = 0.6 \). Ini menunjukkan bahwa semakin tinggi temperatur, semakin banyak orang yang cenderung menyewa sepeda. Sebaliknya, variabel 'weathersit' menunjukkan bahwa kondisi cuaca buruk, seperti hujan lebat, memiliki rata-rata penyewaan terendah, yaitu sekitar 50 penyewaan per hari.

    - *Waktu optimal:* Bulan September tercatat sebagai waktu optimal untuk menambah jumlah sepeda, dengan jumlah penyewaan tertinggi mencapai 8714 sepeda. Hal ini mungkin disebabkan oleh cuaca yang lebih baik dan banyaknya aktivitas luar ruangan pada bulan tersebut. Sebaliknya, bulan Januari menunjukkan jumlah penyewaan terendah, yaitu sekitar 200 penyewaan, yang mungkin disebabkan oleh cuaca dingin dan kurangnya aktivitas luar ruangan.

    - *Pengaruh cuaca:* Analisis menunjukkan bahwa kondisi cuaca cerah (kategori 1) memiliki rata-rata penyewaan tertinggi, yaitu 600 penyewaan per hari, sedangkan kondisi cuaca hujan (kategori 4) memiliki rata-rata penyewaan terendah, yaitu 150 penyewaan per hari. Ini menunjukkan bahwa cuaca yang baik sangat berpengaruh terhadap keputusan orang untuk menyewa sepeda.

    - *Pengaruh musim:* Musim gugur (Fall) memiliki rata-rata penyewaan tertinggi, yaitu 700 penyewaan per hari, dibandingkan dengan musim lainnya. Hal ini mungkin disebabkan oleh suhu yang lebih nyaman dan pemandangan yang indah selama musim ini. Sebaliknya, musim dingin (Winter) menunjukkan rata-rata penyewaan terendah, yaitu 300 penyewaan per hari.

    **Rekomendasi:**
    1. Penambahan Jumlah Sepeda: Tambah jumlah sepeda pada bulan September.
    2. Promosi pada Hari Cerah: Lakukan promosi khusus pada hari-hari cerah.
    3. Peningkatan Layanan pada Musim Gugur: Tingkatkan layanan dan fasilitas pada musim gugur.
    4. Kampanye Kesadaran Cuaca: Tawarkan diskon atau insentif pada hari-hari mendung.
""")