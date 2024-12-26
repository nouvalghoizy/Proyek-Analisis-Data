import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca dataset
def load_data():
    harian = pd.read_csv("day.csv")
    jam = pd.read_csv("hour.csv")

    # Konversi 'dteday' ke datetime
    harian['dteday'] = pd.to_datetime(harian['dteday'])
    jam['dteday'] = pd.to_datetime(jam['dteday'])

    # Menggabungkan dataset
    rental = jam.merge(harian, on='dteday', how='inner', suffixes=('_jam', '_harian'))
    return harian, jam, rental

# Load data
harian_df, jam_df, rental_data = load_data()

# Streamlit layout
st.title("Analisis Data Penyewaan Sepeda")

# Menentukan rentang tanggal untuk filter
min_date = rental_data['dteday'].min()
max_date = rental_data['dteday'].max()

st.sidebar.header("Filter Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date)

# Filter data berdasarkan rentang tanggal
filtered_data = rental_data[
    (rental_data['dteday'] >= pd.to_datetime(start_date)) &
    (rental_data['dteday'] <= pd.to_datetime(end_date))
]

# Eksplorasi Data Awal (menggunakan data terfilter)
missing_harian = harian_df.isnull().sum()
missing_jam = jam_df.isnull().sum()

duplicate_harian = harian_df.duplicated().sum()
duplicate_jam = jam_df.duplicated().sum()

# Visualisasi: Perbedaan Penyewaan antara Hari Kerja dan Hari Libur
st.header("Penyewaan Sepeda: Hari Kerja vs Libur")
if 'workingday_harian' in filtered_data and 'cnt_harian' in filtered_data:
    penyewaan_kerja_libur = filtered_data.groupby("workingday_harian")["cnt_harian"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="workingday_harian", y="cnt_harian", data=penyewaan_kerja_libur, palette="viridis", ax=ax)
    ax.set_title("Penyewaan Sepeda: Hari Kerja vs Libur")
    ax.set_xlabel("Hari Kerja (1) / Libur (0)")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Libur", "Kerja"])
    st.pyplot(fig)

# Visualisasi: Pengaruh Cuaca terhadap Penyewaan Sepeda per Jam
st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda per Jam")
if 'weathersit_jam' in filtered_data and 'cnt_jam' in filtered_data:
    pengaruh_cuaca = filtered_data.groupby("weathersit_jam")["cnt_jam"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="weathersit_jam", y="cnt_jam", data=pengaruh_cuaca, palette="coolwarm", ax=ax)
    ax.set_title("Statistik Penyewaan Sepeda Per Jam Berdasarkan Cuaca")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda per Jam")
    st.pyplot(fig)

# Visualisasi: Data Kosong dan Duplikat
st.header("Data Kosong dan Duplikat")
fig, ax = plt.subplots(figsize=(8, 5))
missing_data = pd.DataFrame({
    "Dataset": ["Harian", "Jam"],
    "Missing Values": [missing_harian.sum(), missing_jam.sum()],
    "Duplicates": [duplicate_harian, duplicate_jam]
})

missing_data_melted = missing_data.melt(id_vars="Dataset", var_name="Category", value_name="Count")
sns.barplot(x="Dataset", y="Count", hue="Category", data=missing_data_melted, palette="Set2", ax=ax)
ax.set_title("Data Kosong dan Duplikat")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

# Informasi Dataset
st.header("Informasi Dataset")
st.subheader("Info Harian")
st.text(harian_df.info(buf=None))
st.subheader("Info Jam")
st.text(jam_df.info(buf=None))
