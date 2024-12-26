import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

harian_df, jam_df, rental_data = load_data()

# Menentukan rentang tanggal untuk filter
min_date = rental_data['dteday'].min()
max_date = rental_data['dteday'].max()

# Filter data berdasarkan rentang tanggal
start_date, end_date = min_date, max_date
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
if 'workingday_harian' in filtered_data and 'cnt_harian' in filtered_data:
    penyewaan_kerja_libur = filtered_data.groupby("workingday_harian")["cnt_harian"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    sns.barplot(x="workingday_harian", y="cnt_harian", data=penyewaan_kerja_libur, palette="viridis")
    plt.title("Penyewaan Sepeda: Hari Kerja vs Libur")
    plt.xlabel("Hari Kerja (1) / Libur (0)")
    plt.ylabel("Rata-rata Penyewaan Sepeda")
    plt.xticks(ticks=[0, 1], labels=["Libur", "Kerja"])
    plt.tight_layout()
    plt.show()

# Visualisasi: Pengaruh Cuaca terhadap Penyewaan Sepeda per Jam
if 'weathersit_jam' in filtered_data and 'cnt_jam' in filtered_data:
    pengaruh_cuaca = filtered_data.groupby("weathersit_jam")["cnt_jam"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="weathersit_jam", y="cnt_jam", data=pengaruh_cuaca, palette="coolwarm")
    plt.title("Statistik Penyewaan Sepeda Per Jam Berdasarkan Cuaca")
    plt.xlabel("Cuaca")
    plt.ylabel("Rata-rata Penyewaan Sepeda per Jam")
    plt.tight_layout()
    plt.show()

# Visualisasi: Data Kosong dan Duplikat
plt.figure(figsize=(8, 5))
missing_data = pd.DataFrame({
    "Dataset": ["Harian", "Jam"],
    "Missing Values": [missing_harian.sum(), missing_jam.sum()],
    "Duplicates": [duplicate_harian, duplicate_jam]
})

missing_data_melted = missing_data.melt(id_vars="Dataset", var_name="Category", value_name="Count")
sns.barplot(x="Dataset", y="Count", hue="Category", data=missing_data_melted, palette="Set2")
plt.title("Data Kosong dan Duplikat")
plt.ylabel("Jumlah")
plt.tight_layout()
plt.show()

# Informasi Dataset
print("Info Harian:")
harian_df.info()
print("\nInfo Jam:")
jam_df.info()
