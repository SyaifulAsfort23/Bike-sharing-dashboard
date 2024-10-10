import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt


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
with col3:
    
    st.subheader('Pengaruh Musim terhadap Penyewaan Sepeda')

    # Calculate the total bike shared during that year
    holiday_season_counts = daily_data[(daily_data['yr'] == (year_option - 2011)) & (daily_data['season'] == season_option)]['cnt'].sum()


    # Menghitung jumlah penyewa sepeda selama musim tertentu di tahun yang dipilih
    total_rentals = daily_data[(daily_data['yr'] == (year_option - 2011)) & (daily_data['season'] == season_option)]['cnt'].sum()

    # 1. Jumlah Penyewa Berdasarkan Holiday dan Season
    holiday_season_counts = daily_data.groupby(['holiday', 'season'])['cnt'].sum().reset_index()

    # Mengubah kode holiday menjadi deskripsi
    holiday_season_counts['holiday'] = holiday_season_counts['holiday'].map({0: 'No Holiday', 1: 'Holiday'})

    # Visualisasi Jumlah Penyewa Berdasarkan Holiday dan Season
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=holiday_season_counts, x='season', y='cnt', hue='holiday', ax=ax1)

    # Menyesuaikan judul dan label pada sumbu
    ax1.set_title('Jumlah Penyewa Berdasarkan Holiday dan Season')
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Jumlah Penyewa')

    # Menyesuaikan label pada sumbu x
    ax1.set_xticks([0, 1, 2, 3])
    ax1.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])

    # Menambahkan legenda
    ax1.legend(title='Hari Libur')

    # Menampilkan visualisasi
    st.pyplot(fig1)



    # 1. Jumlah Penyewa Berdasarkan Holiday dan Season
    weekday_season_counts = daily_data.groupby(['weekday', 'season'])['cnt'].sum().reset_index()

    # Visualisasi Jumlah Penyewa Berdasarkan Holiday dan Season
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weekday_season_counts, x='season', y='cnt', hue='weekday',ax=ax2)
    ax2.set_title('Jumlah Penyewa Berdasarkan Weekday dan Season')
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Jumlah Penyewa')
    ax2.set_xticks([0, 1, 2, 3])
    ax2.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    ax2.legend(title='Weexkday')
    st.pyplot(fig2)

    
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



with col1:
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