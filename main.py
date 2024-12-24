import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Analisis Rental Sepeda - Dataset Bike Sharing")
st.write("Analisis oleh: Muhammad Nouval Ghoizy")
st.write("Bangkit ID: m179b4ky2973 | Email: m179b4ky2973@bangkit.academy")

# Sidebar untuk filter interaktif
st.sidebar.header("Filter Data")

# Membaca dataset
@st.cache_data
def load_data():
    harian = pd.read_csv("day.csv")
    jam = pd.read_csv("hour.csv")
    
    # Konversi 'dteday' ke datetime
    harian['dteday'] = pd.to_datetime(harian['dteday'])
    jam['dteday'] = pd.to_datetime(jam['dteday'])
    
    # Menggabungkan dataset
    rental = jam.merge(harian, on='dteday', how='inner', suffixes=('_jam', '_harian'))
    return harian, jam, rental

harian_df, jam_df, rental_data = load_data()

# Menentukan rentang tanggal untuk filter
min_date = rental_data['dteday'].min()
max_date = rental_data['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if isinstance(start_date, tuple) or isinstance(end_date, tuple):
    start_date, end_date = start_date
elif isinstance(start_date, pd.Timestamp):
    start_date = start_date.to_pydatetime().date()
    end_date = end_date.to_pydatetime().date()

# Filter data berdasarkan rentang tanggal
filtered_data = rental_data[
    (rental_data['dteday'] >= pd.to_datetime(start_date)) &
    (rental_data['dteday'] <= pd.to_datetime(end_date))
]

# Eksplorasi Data Awal (menggunakan data terfilter)
info_harian = harian_df.info()
info_jam = jam_df.info()

missing_harian = harian_df.isnull().sum()
missing_jam = jam_df.isnull().sum()

duplicate_harian = harian_df.duplicated().sum()
duplicate_jam = jam_df.duplicated().sum()

# Visualisasi: Perbedaan Penyewaan antara Hari Kerja dan Hari Libur
penyewaan_kerja_libur = filtered_data.groupby("workingday_harian")["cnt_harian"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x="workingday_harian", y="cnt_harian", data=penyewaan_kerja_libur, palette="viridis")
plt.title("Penyewaan Sepeda: Hari Kerja vs Libur")
plt.xlabel("Hari Kerja (1) / Libur (0)")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.xticks(ticks=[0, 1], labels=["Libur", "Kerja"])
st.pyplot(plt)

# Visualisasi: Pengaruh Cuaca terhadap Penyewaan Sepeda per Jam
pengaruh_cuaca = filtered_data.groupby("weathersit_jam")["cnt_jam"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="weathersit_jam", y="cnt_jam", data=pengaruh_cuaca, palette="coolwarm")
plt.title("Statistik Penyewaan Sepeda Per Jam Berdasarkan Cuaca")
plt.xlabel("Hour")
plt.ylabel("Rata-rata Penyewaan Sepeda per Jam")
st.pyplot(plt)

# Menampilkan Informasi Dataset
st.subheader("Informasi Dataset")
st.write("Info Harian:", info_harian)
st.write("Info Jam:", info_jam)

st.subheader("Nilai Kosong")
st.write("Harian - Nilai Kosong:", missing_harian)
st.write("Jam - Nilai Kosong:", missing_jam)

st.subheader("Data Duplikat")
st.write("Harian - Duplikat:", duplicate_harian)
st.write("Jam - Duplikat:", duplicate_jam)
