import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from babel.numbers import format_currency
sns.set(style='dark')

st.write("Current Working Directory:", os.getcwd())

# Load dataset day_df dan hour_df
day_df = pd.read_csv('dashboard/all_data.csv')



# Sidebar for navigation
st.sidebar.title("Bike Sharing Dashboard")
option = st.sidebar.selectbox("Select Dashboard Section", ['Overview', 'Casual vs Registered Behavior'])

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

def load_data():
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df['total'] = day_df['casual'] + day_df['registered']
    return day_df

day_df = load_data()

# 2. Menghitung RFM
today = day_df['dteday'].max()

rfm_df = day_df.groupby('instant').agg({
    'dteday': lambda x: (today - x.max()).days,  # Recency
    'total': 'sum'  # Frequency
}).rename(columns={'dteday': 'recency', 'total': 'frequency'})

rfm_df['monetary'] = rfm_df['frequency']  # Misalnya, setiap penyewaan dihargai sama


# Subheader for best customer based on RFM parameters
st.subheader("Best Customer Based on RFM Parameters")

# Display average recency, frequency, and monetary
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO')
    st.metric("Average Monetary", value=avg_monetary)

# Display bar charts for top 5 customers by recency, frequency, and monetary
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9"] * 5

sns.barplot(y="recency", x="instant", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer ID", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="instant", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer ID", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="instant", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer ID", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

# Additional Section: Best Time for Promotion (Day/Season Analysis)
st.subheader("Best Day or Season for Promotion")

# Grouping data by season and weekday to calculate total rentals and monetary value
day_df['total_monetary'] = day_df['cnt'] * 10  # Assume each rental costs 10 units of currency
seasonal_data = day_df.groupby('season').agg({'cnt': 'sum', 'total_monetary': 'sum'}).reset_index()
weekday_data = day_df.groupby('weekday').agg({'cnt': 'sum', 'total_monetary': 'sum'}).reset_index()

# Display metrics for best season and day based on rentals and monetary value
best_season = seasonal_data.loc[seasonal_data['cnt'].idxmax()]
best_weekday = weekday_data.loc[weekday_data['cnt'].idxmax()]

col1, col2 = st.columns(2)

with col1:
    st.metric(f"Best Season for Promotion", value=f"Season {int(best_season['season'])}")
    st.metric(f"Rentals in Best Season", value=f"{int(best_season['cnt'])} rentals")
    st.metric(f"Total Revenue in Best Season", value=f"${int(best_season['total_monetary'])}")

with col2:
    st.metric(f"Best Day for Promotion", value=f"Weekday {int(best_weekday['weekday'])}")
    st.metric(f"Rentals on Best Day", value=f"{int(best_weekday['cnt'])} rentals")
    st.metric(f"Total Revenue on Best Day", value=f"${int(best_weekday['total_monetary'])}")

# Visualization of Rentals and Revenue by Season and Weekday
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

# Barplot for Rentals and Revenue by Season
sns.barplot(x='season', y='cnt', data=seasonal_data, palette='Blues', ax=ax1)
ax1.set_title('Total Rentals by Season')
ax1.set_ylabel('Rentals')

sns.barplot(x='season', y='total_monetary', data=seasonal_data, palette='Greens', ax=ax2)
ax2.set_title('Total Revenue by Season')
ax2.set_ylabel('Revenue')

st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023')

