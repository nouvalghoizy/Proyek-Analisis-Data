import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Adding a title
st.title("Bike Rental Analysis")
st.write("Muhammad Nouval Ghoizy")
st.write("Bangkit ID : m179b4ky2973 ")
st.write("Bangkit Mail : m179b4ky2973@bangkit.academy ")

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Merge dataframes
bike_df = hour_df.merge(day_df, on='dteday', how='inner', suffixes=('_hour', '_day'))

# Data wrangling and exploration
# Assessing data
day_info = day_df.info()
hour_info = hour_df.info()

day_missing_values = day_df.isna().sum()
hour_missing_values = hour_df.isna().sum()

day_duplicates = day_df.duplicated().sum()
hour_duplicates = hour_df.duplicated().sum()

# Cleaning data
# No cleaning needed as per the provided code.

# Exploratory Data Analysis (EDA)
# Visualizations
# Pertanyaan 1: Bagaimana suhu rata-rata memengaruhi jumlah penyewaan sepeda?
st.write("### Pertanyaan 1: Bagaimana suhu rata-rata memengaruhi jumlah penyewaan sepeda?")
temperature_hourly = bike_df.groupby("temp")["cnt_hour"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x="temp", y="cnt_hour", data=temperature_hourly)
plt.title("Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda per Jam")
plt.xlabel("Suhu (dalam skala 0-1, dengan 1 sebagai suhu maksimal)")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda per Jam")
st.pyplot(plt)


# Pertanyaan 2: Apakah musim tertentu lebih populer untuk penyewaan sepeda?
st.write("### Pertanyaan 2: Apakah musim tertentu lebih populer untuk penyewaan sepeda?")
season_hourly = bike_df.groupby("season")["cnt_hour"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="season", y="cnt_hour", data=season_hourly)
plt.title("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda per Jam")
plt.xlabel("Musim")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda per Jam")
plt.xticks(ticks=[0, 1, 2, 3], labels=['Spring', 'Summer', 'Fall', 'Winter'])
st.pyplot(plt)


# Displaying Dataframe and other information if needed
st.subheader("Data Info")
st.write("Day DataFrame Info:", day_info)
st.write("Hour DataFrame Info:", hour_info)

st.subheader("Missing Values")
st.write("Day DataFrame Missing Values:", day_missing_values)
st.write("Hour DataFrame Missing Values:", hour_missing_values)

st.subheader("Duplicates")
st.write("Day DataFrame Duplicates:", day_duplicates)
st.write("Hour DataFrame Duplicates:", hour_duplicates)
