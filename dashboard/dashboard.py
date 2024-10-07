import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scikit-learn 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

sns.set(style='dark')

st.write("Current Working Directory:", os.getcwd())

# Load dataset day_df dan hour_df
day_df = pd.read_csv('dashboard/all_data.csv')

# Sidebar for navigation
st.sidebar.title("Bike Sharing Dashboard")
option = st.sidebar.selectbox("Select Dashboard Section", ['Overview', 'Casual vs Registered Behavior', 'Clustering Analysis'])

# Dashboard Title
st.title("Bike Sharing Data Analysis Dashboard")

if option == 'Overview':
    st.header("Data Overview")
    
    # Display summary statistics
    st.subheader('Summary Statistics')
    st.write(day_df.describe())
    
    # Show metrics for casual, registered, and total rentals
    total_rentals = day_df['cnt'].sum()
    total_casual = day_df['casual'].sum()
    total_registered = day_df['registered'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rentals", f"{total_rentals / 1000:.2f}K")
    col2.metric("Total Casual Rentals", f"{total_casual / 1000:.2f}K")
    col3.metric("Total Registered Rentals", f"{total_registered / 1000:.2f}K")
    
    st.write("This dashboard provides insights into the bike-sharing dataset, including seasonal effects and customer behavior.")

if option == 'Casual vs Registered Behavior':
    st.header('Perbandingan Penyewa Kasual dan Terdaftar')

    # Add dropdown to select season
    selected_season = st.selectbox('Pilih Musim', ['Spring', 'Summer', 'Fall', 'Winter'])
    season_map = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    filtered_data = day_df[day_df['season'] == season_map[selected_season]]
    
    # Add metrics for casual and registered rentals in the selected season
    casual_season_sum = filtered_data['casual'].sum()
    registered_season_sum = filtered_data['registered'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Casual Rentals", f"{casual_season_sum / 1000:.2f}K")
    col2.metric("Registered Rentals", f"{registered_season_sum / 1000:.2f}K")

    st.write(f"Data untuk {selected_season}")
    st.write(filtered_data[['casual', 'registered', 'cnt']])
    
    # Create a bar plot for casual vs registered users
    fig, ax = plt.subplots()
    sns.barplot(x='weekday', y='cnt', hue='holiday', data=filtered_data, ax=ax)
    ax.set_title(f'Perbandingan Penyewa Berdasarkan Weekday untuk {selected_season}')
    ax.set_ylabel('Jumlah Penyewa (ribuan)')
    st.pyplot(fig)
    
    # Add insights or recommendations
    st.subheader("Insights and Recommendations")
    st.write("""
    - **Casual users** tend to rent more on holidays and weekends, while **registered users** are more consistent across the weekdays.
    - To convert casual users to registered users, we recommend offering special deals on weekdays.
    """)

if option == 'Clustering Analysis':
    st.header("Clustering Analysis")

    # Prepare data for clustering
    clustering_data = day_df[['casual', 'registered', 'cnt', 'temp', 'atemp', 'hum', 'windspeed']]
    scaler = StandardScaler()
    clustering_data_scaled = scaler.fit_transform(clustering_data)

    # K-Means Clustering
    st.subheader("K-Means Clustering")
    num_clusters = st.slider("Select number of clusters", min_value=2, max_value=10, value=3)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    day_df['cluster'] = kmeans.fit_predict(clustering_data_scaled)

    # Display cluster centroids
    st.subheader(f"Cluster Centers (n={num_clusters})")
    centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=clustering_data.columns)
    st.write(centroids)

    # Visualize clusters
    fig, ax = plt.subplots()
    sns.scatterplot(x=day_df['temp'], y=day_df['cnt'], hue=day_df['cluster'], palette='Set2', ax=ax)
    ax.set_title('Clustering of Rentals Based on Temperature')
    st.pyplot(fig)

    # Cluster Insights
    st.subheader("Cluster Insights")
    for i in range(num_clusters):
        st.write(f"Cluster {i+1}:")
        st.write(day_df[day_df['cluster'] == i].describe().T)

