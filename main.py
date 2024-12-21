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

# Checking for missing values
st.write("### Missing Values")
day_missing_values = day_df.isna().sum()
hour_missing_values = hour_df.isna().sum()
st.write("Day DataFrame Missing Values:", day_missing_values)
st.write("Hour DataFrame Missing Values:", hour_missing_values)

# Checking for duplicates
st.write("### Duplicates")
day_duplicates = day_df.duplicated().sum()
hour_duplicates = hour_df.duplicated().sum()
st.write("Day DataFrame Duplicates:", day_duplicates)
st.write("Hour DataFrame Duplicates:", hour_duplicates)

## 2. Cleaning Data
# As per the provided code, no cleaning is necessary, so we can skip this part or add an optional cleaning step if needed

# Exploratory Data Analysis (EDA)
st.subheader("Exploratory Data Analysis (EDA)")

# Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda per Jam
st.write("### Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda per Jam")
weather_hourly = bike_df.groupby("weathersit_hour")["cnt_hour"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="weathersit_hour", y="cnt_hour", data=weather_hourly)
plt.title("Pengaruh Cuaca terhadap Jumlah Penyewaan sepeda per Jam")
plt.xlabel("Keadaan Cuaca")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda per Jam")
plt.xticks(ticks=[0, 1, 2, 3], labels=['Springer', 'Summer', 'Fall', 'Winter'])
st.pyplot(plt)

# Pertanyaan 2: Perbedaan Jumlah Penyewaan Sepeda antara Hari Kerja dan Hari Libur
st.write("### Pertanyaan 2: Perbedaan Jumlah Penyewaan Sepeda antara Hari Kerja dan Hari Libur")
rentals_by_day_type = bike_df.groupby("workingday_day")["cnt_day"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x="workingday_day", y="cnt_day", data=rentals_by_day_type)
plt.title("Perbedaan Jumlah Penyewaan Sepeda antara Hari Kerja dan Hari Libur")
plt.xlabel("Hari Kerja(1) / Hari Libur(0)")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda")
plt.xticks(ticks=[0,1], labels=["Hari Libur", "Hari Kerja"])
st.pyplot(plt)

# Displaying Dataframe and other information if needed
st.subheader("Data Information")
st.write("### Day DataFrame (5 Rows):")
st.write(day_df.head())

st.write("### Hour DataFrame (5 Rows):")
st.write(hour_df.head())

st.write("### Merged DataFrame (5 Rows):")
st.write(bike_df.head())
