import streamlit as st
import pandas as pd
import altair as alt

day_shape = 'fixed_day.csv'
hour_shape = 'hour.csv'

st.set_page_config(
    page_title='Bike Sharing Dashboard',
    layout='wide'
)

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Load data
daily_data = load_data(day_shape)
hour_data = load_data(hour_shape)


# Changes Season format
daily_data['season'] = daily_data['season'].replace({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
hour_data['season'] = hour_data['season'].replace({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})

# Sidebar options
st.sidebar.title("Bike Sharing Dashboard")


# Adjust the hour format
hour_data['hr'] += 1

year_option = st.sidebar.selectbox(
    'Select Year',
    (2011, 2012)
)

season_option = st.sidebar.selectbox(
    'Select Season',
    ('Winter', 'Spring', 'Summer', 'Fall')
)

day_option = st.sidebar.selectbox(
    'Select Hour',
    tuple(range(1,25))
)

# Create columns for the dashboard layout
col1, col2, col3 = st.columns((2, 2, 3), gap='medium')

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
    
    # Reshape data for Altair-friendly format
    user_behavior = pd.melt(user_behavior, id_vars=['season'], value_vars=['casual', 'registered'], 
                            var_name='User Type', value_name='Average Rentals')

    # Plotting data penyewa casual vs registered per musim
    chart = alt.Chart(user_behavior).mark_bar().encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('Average Rentals:Q', title='Average Daily Rentals'),
        color=alt.Color('User Type:N', title='User Type'),
        tooltip=['season', 'Average Rentals', 'User Type']
    ).properties(
        title='Average Daily Rentals by Casual and Registered Users per Season'
    )
    st.altair_chart(chart, use_container_width=True)
    st.markdown("""
        **Kesimpulan:** Data ini menunjukkan perbedaan perilaku antara penyewa casual dan registered di setiap musim. 
        Dengan informasi ini, kita bisa merencanakan strategi untuk mengonversi pengguna casual menjadi pelanggan tetap.
    """)


with col3:
    st.subheader('Total Bike Shared')

    # Calculate the total bike shared during that year
    total_bikes_shared = daily_data[daily_data['yr'] == (year_option - 2011)]['cnt'].sum()
    total_bikes_shared_season = daily_data[(daily_data['yr'] == (year_option - 2011)) & (daily_data['season'] == season_option)]['cnt'].sum()

    # Draw the total year & season
    total_year, total_season = st.columns(2)
    total_year.metric(label='Total Year', value=f"{total_bikes_shared / 1_000_000:.1f}M")
    total_season.metric(label='Total Season', value=f"{total_bikes_shared_season / 1_000:.1f}K")

    st.subheader('Peak & Low')
    max_day = daily_data[daily_data['yr'] == (year_option - 2011)]['cnt'].max()
    min_day = daily_data[daily_data['yr'] == (year_option - 2011)]['cnt'].min()
    max_hour = hour_data[hour_data['yr'] == (year_option - 2011)]['cnt'].max()
    min_hour = hour_data[hour_data['yr'] == (year_option - 2011)]['cnt'].min()

    daymax, daymin, hourmax, hourmin = st.columns(4, gap='small')
    daymax.metric(label='Peak Day', value=max_day)
    daymin.metric(label='Lowest Day', value=min_day)
    hourmax.metric(label='Peak Hour', value=max_hour)
    hourmin.metric(label='Lowest Hour', value=min_hour)

    # Weather occurrence during those year & season
    st.subheader('Weather Occurrences')
    # Draw the total year & season
    clear, mist, light, heavy = st.columns(4, gap='small')
    # Extract counts for each weather condition
    counts = {
        'Clear/Cloudy': 0,
        'Mist': 0,
        'Light Rain/Snow': 0,
        'Heavy Rain/Snow': 0
    }

    # Calculate total occurences of each weather
    total_weather = hour_data[(hour_data['yr'] == (year_option - 2011)) & 
    (hour_data['season'] == season_option) & (hour_data['hr'] == day_option)].groupby('weathersit').size().reset_index(name='count')

    # Fill the counts dictionary based on occurrences
    for index, row in total_weather.iterrows():
        if row['weathersit'] in counts:
            counts[row['weathersit']] = row['count']
    
    # Display the metrics in the respective columns
    clear.metric(label='Clear/Cloudy', value=counts['Clear/Cloudy'])
    mist.metric(label='Mist', value=counts['Mist'])
    light.metric(label='Light Rain/Snow', value=counts['Light Rain/Snow'])
    heavy.metric(label='Heavy Rain/Snow', value=counts['Heavy Rain/Snow'])

    st.subheader('Working Day')
    working_day = hour_data[(hour_data['yr'] == (year_option - 2011)) & (hour_data['season'] == season_option) & (hour_data['hr'] == day_option)].groupby('workingday')['cnt'].mean().reset_index()
    # Create a pie/donut chart using Altairx
    chart = alt.Chart(working_day).mark_arc(innerRadius=50).encode(
        color=alt.Color(field='workingday', type='nominal', title='Working Day'),
        theta=alt.Theta(field='cnt', type='quantitative', title='Average Bikes Shared'),
        tooltip=['cnt', 'workingday']
    ).properties(
        title='Working Day Comparison'
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)