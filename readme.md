# 🚲 Analisis Data Bike Sharing: Menjelajahi Tren Penyewaan Sepeda

Selamat datang di repositori analisis data Bike Sharing! Proyek ini bertujuan untuk memenuhi kelas Analisis Data dengan Python pada Coding Camp by DBS Foundation dalam menganalisis data penyewaan sepeda dan memberikan wawasan berharga tentang faktor-faktor yang memengaruhi penyewaan, waktu optimal untuk menambah jumlah sepeda, dan pengaruh kondisi cuaca.

## 🎯 Tujuan Proyek

Proyek ini bertujuan untuk menjawab pertanyaan-pertanyaan berikut:

1.  Faktor apa yang paling mempengaruhi jumlah penyewaan sepeda?
2.  Kapan waktu paling optimal untuk menambah jumlah sepeda berdasarkan tren penyewaan?
3.  Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?

## 🛠️ Teknologi yang Digunakan

*   **Python:** Bahasa pemrograman utama yang digunakan dalam proyek ini.
*   **Pandas:** Library untuk manipulasi dan analisis data. (notebook.ipynb:28-30)
*   **Matplotlib & Seaborn:** Library untuk visualisasi data. (notebook.ipynb:28-30)
*   **Statsmodels:** Library untuk analisis time series. (notebook.ipynb:31-32)
*   **Streamlit:** Framework untuk membuat aplikasi web interaktif.
*   **Plotly:** Library untuk membuat visualisasi interaktif.

## 🚀 Cara Menjalankan Aplikasi

1.  Klon repositori ini:

    ```bash
    git clone https://github.com/sumems/bike-sharing-analysis.git
    ```

2.  Arahkan ke direktori proyek:

    ```bash
    cd bike-sharing-analysis
    ```

3.  Instal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

4.  Jalankan aplikasi Streamlit:

    ```bash
    streamlit run dashboard/dashboard.py
    ```

## 📊 Hasil Analisis

### Faktor yang Mempengaruhi Penyewaan Sepeda

Analisis korelasi menunjukkan bahwa **temperatur** memiliki korelasi positif tertinggi dengan jumlah penyewaan sepeda. Ini berarti bahwa semakin tinggi temperatur, semakin banyak orang yang cenderung menyewa sepeda. (notebook.ipynb:1003-1007)

### Waktu Optimal untuk Menambah Jumlah Sepeda

Bulan **September** adalah waktu optimal untuk menambah jumlah sepeda berdasarkan tren penyewaan tertinggi. (notebook.ipynb:954-958)

### Pengaruh Kondisi Cuaca

Kondisi cuaca **cerah** lebih disukai untuk penyewaan sepeda. Kondisi cuaca buruk seperti hujan lebat atau salju memiliki rata-rata jumlah penyewaan yang lebih rendah. (notebook.ipynb:1097-1105)

### Pengaruh Musim

Musim **gugur** memiliki rata-rata penyewaan tertinggi dibandingkan musim lainnya. (notebook.ipynb:1118-1128)

## 📈 Time Series Decomposition

Analisis time series decomposition memberikan wawasan tentang tren, musiman, dan residu dalam data penyewaan sepeda. (notebook.ipynb:1163-1187)

*   **Tren:** Menunjukkan arah umum (naik atau turun) dari penyewaan sepeda dari waktu ke waktu.
*   **Musiman:** Menunjukkan pola yang berulang dalam periode tertentu (misalnya, mingguan atau bulanan).
*   **Residu:** Variasi acak yang tidak dapat dijelaskan oleh tren atau musiman.