import streamlit as st
import pandas as pd
import altair as alt

DAY_PATH = 'data/day.csv'
HOUR_PATH = 'data/hour.csv'

st.set_page_config(
    page_title='Bike Sharing Dashboard',
    layout='wide'
)

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Load data
daily_data = load_data(DAY_PATH)
hourly_data = load_data(HOUR_PATH)

# Sidebar options
st.sidebar.title("Bike Sharing Dashboard")

# Fix season columns format
daily_data['season'] = daily_data['season'].replace({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
hourly_data['season'] = hourly_data['season'].replace({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})

# Adjust the hour format
hourly_data['hr'] += 1

year_option = st.sidebar.selectbox(
    'Select Year',
    (2011, 2012)
)

season_option = st.sidebar.selectbox(
    'Select Season',
    ('Winter', 'Spring', 'Summer', 'Fall')
)

# Create columns for the dashboard layout
col1, col2 = st.columns((1, 2), gap='medium')

# Column 1: Pengaruh Musim terhadap Penyewaan Sepeda
with col1:
    st.subheader('Pengaruh Musim terhadap Penyewaan Sepeda')
    
    # Data pengaruh musim terhadap penyewaan sepeda
    seasonal_rentals = daily_data[daily_data['yr'] == (year_option - 2011)].groupby('season')['cnt'].mean().reset_index()
    
    # Plotting data penyewaan sepeda per musim
    chart = alt.Chart(seasonal_rentals).mark_bar().encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('cnt:Q', title='Average Daily Rentals'),
        tooltip=['season', 'cnt']
    ).properties(
        title='Average Daily Bike Rentals per Season'
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("""
        **Kesimpulan:** Dari data ini, kita bisa melihat bagaimana musim tertentu mempengaruhi jumlah penyewaan sepeda harian.
        Hal ini bisa digunakan untuk memaksimalkan promosi dan penawaran khusus pada musim yang lebih rendah untuk meningkatkan pendapatan.
    """)

# Column 2: Perilaku Penyewa Casual dan Registered
with col2:
    st.subheader('Perilaku Penyewa Casual dan Registered')

    # Data penyewa casual dan registered
    user_behavior = daily_data[daily_data['yr'] == (year_option - 2011)].groupby('season')[['casual', 'registered']].mean().reset_index()
    
    # Plotting data penyewa casual vs registered per musim
    chart = alt.Chart(user_behavior).mark_bar().encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('value:Q', title='Average Daily Rentals'),
        color=alt.Color('variable:N', title='User Type'),
        tooltip=['season', 'value', 'variable']
    ).transform_fold(
        ['casual', 'registered'],
        as_=['variable', 'value']
    ).properties(
        title='Average Daily Rentals by Casual and Registered Users per Season'
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("""
        **Kesimpulan:** Data ini menunjukkan perbedaan perilaku antara penyewa casual dan registered di setiap musim. 
        Dengan informasi ini, kita bisa merencanakan strategi untuk mengonversi pengguna casual menjadi pelanggan tetap.
    """)
