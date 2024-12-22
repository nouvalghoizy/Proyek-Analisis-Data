import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Analisis Rental Sepeda - Dataset Bike Sharing")
st.write("Analisis oleh: Muhammad Nouval Ghoizy")
st.write("Bangkit ID: m179b4ky2973 | Email: m179b4ky2973@bangkit.academy")

# Membaca dataset
harian_df = pd.read_csv("day.csv")
jam_df = pd.read_csv("hour.csv")

# Menggabungkan dataset
rental_data = jam_df.merge(harian_df, on='dteday', how='inner', suffixes=('_jam', '_harian'))

# Eksplorasi Data Awal
info_harian = harian_df.info()
info_jam = jam_df.info()

missing_harian = harian_df.isnull().sum()
missing_jam = jam_df.isnull().sum()

duplicate_harian = harian_df.duplicated().sum()
duplicate_jam = jam_df.duplicated().sum()

# Visualisasi: Perbedaan Penyewaan antara Hari Kerja dan Hari Libur
penyewaan_kerja_libur = rental_data.groupby("workingday_harian")["cnt_harian"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x="workingday_harian", y="cnt_harian", data=penyewaan_kerja_libur)
plt.title("Penyewaan Sepeda: Hari Kerja vs Libur")
plt.xlabel("Hari Kerja (1) / Libur (0)")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.xticks(ticks=[0, 1], labels=["Libur", "Kerja"])
st.pyplot(plt)

# Visualisasi: Pengaruh Cuaca terhadap Penyewaan Sepeda per Jam
pengaruh_cuaca = rental_data.groupby("weathersit_jam")["cnt_jam"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="weathersit_jam", y="cnt_jam", data=pengaruh_cuaca)
plt.title("Pengaruh Cuaca terhadap Penyewaan per Jam")
plt.xlabel("Kategori Cuaca")
plt.ylabel("Rata-rata Penyewaan Sepeda per Jam")
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])
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
