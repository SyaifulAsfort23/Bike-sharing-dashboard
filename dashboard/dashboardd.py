import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

st.set_page_config(
    page_title='Bike Sharing Dashboard',
    layout='centered'
)

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

# Helper function: Load data
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/fixed_day.csv')
    data['dteday'] = pd.to_datetime(data['dteday'], format='%Y-%m-%d')  # Ensure correct date parsing
    return data  # Return the DataFrame

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
st.title("Dashboard Bike Share")

# Total Penyewa berdasarkan Season
st.subheader("Total Penyewa Berdasarkan Season")
season_group = penyewa_by_season(filtered_data)
st.dataframe(season_group)

# Bar Plot yang Dibagi Berdasarkan Casual dan Registered
st.subheader("Visualisasi Total Penyewa Berdasarkan Season (Casual dan Registered)")
season_group_melted = season_group.melt(id_vars="season", value_vars=["casual", "registered"], 
                                        var_name="Penyewa", value_name="Jumlah")

plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='Jumlah', hue='Penyewa', data=season_group_melted)
plt.title("Total Penyewa Berdasarkan Season (Casual dan Registered)")
plt.xlabel("Season")
plt.ylabel("Total Penyewa")
st.pyplot(plt)

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

# Scatter Plot Casual dan Registered
st.subheader("Visualisasi Penyewa Berdasarkan Casual dan Registered (Scatter Plot)")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='casual', y='registered', data=casual_registered_group)
plt.title("Scatter Plot Casual vs Registered")
plt.xlabel("Casual")
plt.ylabel("Registered")
st.pyplot(plt)

st.subheader("Visualisasi Total Penyewa Berdasarkan Casual dan Registered (Bar Plot)")
casual_registered_total = casual_registered_group[['casual', 'registered']].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='index', y=0, data=casual_registered_total)
plt.title("Bar Plot Total Casual dan Registered")
plt.xlabel("Kategori")
plt.ylabel("Jumlah Penyewa")
st.pyplot(plt)

# Membuat group data
wday_workday_holiday_group = penyewa_by_wday_workday_holiday(filtered_data)

# Membagi visualisasi ke dalam 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Penyewa Casual Berdasarkan Workingday")
    workingday_group = wday_workday_holiday_group.groupby('workingday').agg({
        'casual': 'sum'
    }).reset_index()
    st.dataframe(workingday_group)
    # Bar plot untuk workingday
    plt.figure(figsize=(5, 4))
    sns.barplot(x='workingday', y='casual', data=workingday_group)
    plt.title("Penyewa Casual Berdasarkan Workingday")
    st.pyplot(plt)

with col2:
    st.subheader("Penyewa Casual Berdasarkan Weekday")
    weekday_group = wday_workday_holiday_group.groupby('weekday').agg({
        'casual': 'sum'
    }).reset_index()
    st.dataframe(weekday_group)
    # Bar plot untuk weekday
    plt.figure(figsize=(5, 4))
    sns.barplot(x='weekday', y='casual', data=weekday_group)
    plt.title("Penyewa Casual Berdasarkan Weekday")
    st.pyplot(plt)

with col3:
    st.subheader("Penyewa Casual Berdasarkan Holiday")
    holiday_group = wday_workday_holiday_group.groupby('holiday').agg({
        'casual': 'sum'
    }).reset_index()
    st.dataframe(holiday_group)
    # Bar plot untuk holiday
    plt.figure(figsize=(5, 4))
    sns.barplot(x='holiday', y='casual', data=holiday_group)
    plt.title("Penyewa Casual Berdasarkan Holiday")
    st.pyplot(plt)

# Bar plot dengan 3 kategori sekaligus (Workingday, Weekday, Holiday)
st.subheader("Visualisasi Penyewa Casual Berdasarkan Weekday, Workingday, & Holiday")
casual_group_melted = wday_workday_holiday_group.melt(
    id_vars="weekday", value_vars=["workingday", "holiday"],
    var_name="Kategori", value_name="Jumlah Casual"
)

plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='Jumlah Casual', hue='Kategori', data=casual_group_melted)
plt.title("Penyewa Casual Berdasarkan Weekday, Workingday, & Holiday")
plt.xlabel("Weekday")
plt.ylabel("Total Penyewa Casual")
st.pyplot(plt)

# Penyewa Casual berdasarkan Weekday, Workingday, & Holiday
st.subheader("Penyewa Casual Berdasarkan Weekday, Workingday, & Holiday")
wday_workday_holiday_group = penyewa_by_wday_workday_holiday(filtered_data)
casual_group = wday_workday_holiday_group[['weekday', 'workingday', 'holiday', 'casual']]
st.dataframe(casual_group)

# Bar Plot Penyewa Casual Berdasarkan Weekday, Workingday, & Holiday
st.subheader("Visualisasi Penyewa Casual Berdasarkan Weekday, Workingday, & Holiday")
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='casual', hue='workingday', data=casual_group)
plt.title("Penyewa Casual Berdasarkan Weekday dan Workingday")
plt.xlabel("Weekday")
plt.ylabel("Total Penyewa Casual")
st.pyplot(plt)

# Penyewa Registered berdasarkan Weekday, Workingday, & Holiday
st.subheader("Penyewa Registered Berdasarkan Weekday, Workingday, & Holiday")
registered_group = wday_workday_holiday_group[['weekday', 'workingday', 'holiday', 'registered']]
st.dataframe(registered_group)

# Bar Plot Penyewa Registered Berdasarkan Weekday, Workingday, & Holiday
st.subheader("Visualisasi Penyewa Registered Berdasarkan Weekday, Workingday, & Holiday")
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='registered', hue='workingday', data=registered_group)
plt.title("Penyewa Registered Berdasarkan Weekday dan Workingday")
plt.xlabel("Weekday")
plt.ylabel("Total Penyewa Registered")
st.pyplot(plt)

# Exploratory Lanjutan: Clustering Penyewa Casual dan Registered Berdasarkan Season
st.subheader("Clustering Penyewa Casual dan Registered Berdasarkan Season")

# Drop rows with NaN values
filtered_data = filtered_data.dropna()

# Prepare data for clustering
cluster_data = filtered_data[['casual', 'registered']]
kmeans = KMeans(n_clusters=3)  # Adjust the number of clusters as necessary
cluster_labels = kmeans.fit_predict(cluster_data)

# Add cluster labels to the data
filtered_data['cluster'] = cluster_labels

# Plot the clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x='casual', y='registered', hue='cluster', data=filtered_data, palette='deep')
plt.title("Clustering Penyewa Casual dan Registered")
plt.xlabel("Casual")
plt.ylabel("Registered")
st.pyplot(plt)

# Keterangan tentang Clustering
st.write("Clustering menggunakan KMeans untuk membedakan pola penyewa casual dan registered berdasarkan season.")

# Footer
st.sidebar.markdown("Developed by [SYAIFUL]")
