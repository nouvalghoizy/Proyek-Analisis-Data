import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit app title
st.title("Bike Rental Analysis")
st.write("Muhammad Nouval Ghoizy")
st.write("Bangkit ID : m179b4ky2973 ")
st.write("Bangkit Mail : m179b4ky2973@bangkit.academy ")

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Merge dataframes
bike_df = hour_df.merge(day_df, on='dteday', how='inner', suffixes=('_hour', '_day'))

# Pertanyaan 1: Bagaimana suhu rata-rata memengaruhi jumlah penyewaan sepeda?
avg_temp_rentals = bike_df.groupby("temp_hour")["cnt_hour"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x="temp_hour", y="cnt_hour", data=avg_temp_rentals)
plt.title("Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda")
plt.xlabel("Suhu Normalisasi")
plt.ylabel("Rata-rata Penyewaan Sepeda per Jam")
plt.grid()
st.pyplot(plt)

# Pertanyaan 2: Apakah musim tertentu lebih populer untuk penyewaan sepeda?
season_rentals = day_df.groupby("season")["cnt"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x="season", y="cnt", data=season_rentals)
plt.title("Penyewaan Sepeda Berdasarkan Musim")
plt.xlabel("Musim")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.xticks(ticks=[0, 1, 2, 3], labels=["Spring", "Summer", "Fall", "Winter"])
st.pyplot(plt)

# Pertanyaan 3: Bagaimana distribusi penyewaan sepeda berdasarkan jam dalam sehari?
hourly_distribution = hour_df.groupby("hr")["cnt"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="hr", y="cnt", data=hourly_distribution)
plt.title("Distribusi Penyewaan Sepeda Berdasarkan Jam")
plt.xlabel("Jam")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.grid()
st.pyplot(plt)

# Display data info
st.subheader("Data Info")
st.write("Day DataFrame Head:")
st.write(day_df.head())

st.write("Hour DataFrame Head:")
st.write(hour_df.head())

st.write("Bike DataFrame Head:")
st.write(bike_df.head())
