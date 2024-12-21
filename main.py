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

# Make sure 'dteday' is in datetime format
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

# Create 'weekday' column (0=Monday, 6=Sunday)
bike_df['weekday'] = bike_df['dteday'].dt.weekday

# Check the first few rows to ensure 'weekday' was created correctly
st.write(bike_df.head())

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

# Pertanyaan 1: Bagaimana hari dalam seminggu memengaruhi jumlah penyewaan sepeda?
# Group by weekday to analyze bike rental per weekday
weekday_rentals = bike_df.groupby("weekday")["cnt_hour"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x="weekday", y="cnt_hour", data=weekday_rentals)
plt.title("Pengaruh Hari dalam Seminggu terhadap Jumlah Penyewaan Sepeda per Jam")
plt.xlabel("Hari dalam Seminggu")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda per Jam")
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
st.pyplot(plt)

# Pertanyaan 2: Apakah ada perbedaan jumlah penyewaan sepeda antara jam sibuk dan non-sibuk?
# Defining busy hours (7-9 AM and 4-6 PM)
bike_df['busy_hour'] = bike_df['hr'].apply(lambda x: 'Sibuk' if (7 <= x <= 9) or (16 <= x <= 18) else 'Non-Sibuk')

# Group by busy_hour to analyze bike rental during busy vs non-busy hours
busy_hour_rentals = bike_df.groupby("busy_hour")["cnt_hour"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x="busy_hour", y="cnt_hour", data=busy_hour_rentals)
plt.title("Perbandingan Jumlah Penyewaan Sepeda pada Jam Sibuk dan Non-Sibuk")
plt.xlabel("Jam Sibuk / Non-Sibuk")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda per Jam")
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
