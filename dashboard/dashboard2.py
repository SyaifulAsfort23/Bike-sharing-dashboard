# dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# Helper function: Load data
@st.cache
def load_data():
    data = pd.read_csv('fixed_day.csv')
    data['dteday'] = pd.to_datetime(data['dteday'], format='%m/%d/%Y')
    return data

# Helper function: Group by season
def penyewa_by_season(data):
    return data.groupby('season')[['casual', 'registered', 'cnt']].sum().reset_index()

# Helper function: Group by weekday, workingday, holiday in each season
def penyewa_by_wday_workday_holiday(data):
    return data.groupby(['season', 'weekday', 'workingday', 'holiday'])[['casual', 'registered', 'cnt']].sum().reset_index()

# Helper function: Group by casual and registered
def penyewa_grouped_by_casual_registered(data):
    return data[['casual', 'registered', 'cnt']].groupby(['casual', 'registered']).sum().reset_index()

# Load the data
data = load_data()

# Sidebar for date filtering
st.sidebar.title("Filter Rentang Tanggal")
start_date = st.sidebar.date_input('Start date', data['dteday'].min())
end_date = st.sidebar.date_input('End date', data['dteday'].max())

filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

# Dashboard Section
st.title("Dashboard Penyewa Berdasarkan Musim dan Hari")

# Total Penyewa berdasarkan Season
st.subheader("Total Penyewa Berdasarkan Season")
season_group = penyewa_by_season(filtered_data)
st.dataframe(season_group)

# Plot Daily Orders
st.subheader("Daily Orders Plot")
plt.figure(figsize=(10, 6))
sns.lineplot(x=filtered_data['dteday'], y=filtered_data['cnt'], hue=filtered_data['season'])
plt.title("Total Orders per Day by Season")
plt.xlabel("Tanggal")
plt.ylabel("Total Penyewa")
st.pyplot(plt)

# Penyewa Berdasarkan Casual dan Registered
st.subheader("Penyewa Berdasarkan Casual dan Registered")
casual_registered_group = penyewa_grouped_by_casual_registered(filtered_data)
st.dataframe(casual_registered_group)

# Penyewa Casual berdasarkan Weekday, Workingday, & Holiday
st.subheader("Penyewa Casual Berdasarkan Weekday, Workingday, & Holiday")
wday_workday_holiday_group = penyewa_by_wday_workday_holiday(filtered_data)
casual_group = wday_workday_holiday_group[['weekday', 'workingday', 'holiday', 'casual']]
st.dataframe(casual_group)

# Penyewa Registered berdasarkan Weekday, Workingday, & Holiday
st.subheader("Penyewa Registered Berdasarkan Weekday, Workingday, & Holiday")
registered_group = wday_workday_holiday_group[['weekday', 'workingday', 'holiday', 'registered']]
st.dataframe(registered_group)

# Exploratory Lanjutan: Clustering Penyewa Casual dan Registered Berdasarkan Season
st.subheader("Clustering Penyewa Casual dan Registered Berdasarkan Season")
season_data = filtered_data[['season', 'casual', 'registered']]
kmeans = KMeans(n_clusters=3)
season_data['cluster'] = kmeans.fit_predict(season_data[['casual', 'registered']])

# Plot clustering
plt.figure(figsize=(10, 6))
sns.scatterplot(x='casual', y='registered', hue='cluster', data=season_data, palette='viridis')
plt.title("Clustering Casual & Registered")
plt.xlabel("Casual")
plt.ylabel("Registered")
st.pyplot(plt)

# Exploratory Lanjutan: Penyewa Berdasarkan Weekday, Workingday, & Holiday
st.subheader("Clustering Berdasarkan Weekday, Workingday, & Holiday")
weekday_data = filtered_data[['weekday', 'workingday', 'holiday', 'casual', 'registered']]
kmeans_weekday = KMeans(n_clusters=3)
weekday_data['cluster'] = kmeans_weekday.fit_predict(weekday_data[['casual', 'registered']])

# Plot clustering weekday
plt.figure(figsize=(10, 6))
sns.scatterplot(x='casual', y='registered', hue='cluster', data=weekday_data, palette='coolwarm')
plt.title("Clustering Berdasarkan Weekday, Workingday, & Holiday")
plt.xlabel("Casual")
plt.ylabel("Registered")
st.pyplot(plt)
