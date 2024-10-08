import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load data
all_data = pd.read_csv("dashboard/all_data.csv")

# Fungsi untuk membuat plot
def create_plot(data, x, y, hue, title):
    sns.countplot(data=data, x=x, hue=hue)
    plt.title(title)
    st.pyplot()

# Fungsi untuk membuat tab
def create_tab(tab_name, content):
    with st.tab(tab_name):
        content

# Bagian utama aplikasi
st.title("Dashboard Analisis Penyewaan Sepeda")

# Tab untuk spesifikasi 1 dan 2
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Pengaruh Musim Terhadap Penyewa ", "Perilaku Penyewa kasual dan terdaftar ", "Clustering"])

with tab1:
    
    # Ensure 'dteday' is in datetime format
    all_data['dteday'] = pd.to_datetime(all_data['dteday'])

    # Create a new column for year
    all_data['year'] = all_data['yr'].map({0: 2011, 1: 2012})  # Convert year code to actual year
    all_data['month'] = all_data['dteday'].dt.month_name()  # Extract month name

    # Group by month, year and user type
    monthly_user_data = all_data.groupby(['month', 'year']).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()

    # Pivot the data for plotting
    pivot_data = monthly_user_data.pivot_table(index='month', columns='year', values=['casual', 'registered'], fill_value=0)

    # Sort the months in the correct order
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                    'August', 'September', 'October', 'November', 'December']
    pivot_data = pivot_data.reindex(months_order)

    # Create line charts for casual and registered users
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

    # Plot for casual users
    for year in [2011, 2012]:
        axes[0].plot(pivot_data.index, pivot_data['casual'][year], marker='o', label=f'Year {year}')

    axes[0].set_title('Jumlah Penyewa Sepeda Casual Sepanjang Tahun Berdasarkan Bulan')
    axes[0].set_xlabel('Bulan')
    axes[0].set_ylabel('Jumlah Penyewa Casual')
    axes[0].set_xticklabels(months_order, rotation=45)
    axes[0].legend(title='Tahun')
    axes[0].grid()

    # Plot for registered users
    for year in [2011, 2012]:
        axes[1].plot(pivot_data.index, pivot_data['registered'][year], marker='o', label=f'Year {year}')

    axes[1].set_title('Jumlah Penyewa Sepeda Registered Sepanjang Tahun Berdasarkan Bulan')
    axes[1].set_xlabel('Bulan')
    axes[1].set_ylabel('Jumlah Penyewa Registered')
    axes[1].set_xticklabels(months_order, rotation=45)
    axes[1].legend(title='Tahun')
    axes[1].grid()

    # Adjust layout
    plt.tight_layout()
    
    
    # Show plot in Streamlit
    st.pyplot(fig)
    
with tab2:
    
    plot_type = st.selectbox("Choose", ["Weekday & Musim", "Workingday & Musim", "Holiday & Musim"])
    
    if plot_type == "Weekday & Musim":
        st.image("dashboard_pitc/musimdanweekday.png", caption="Weekday dan Musim")    
        long_text ='''
    1. Fluktuasi Musiman: Terdapat pola musiman yang jelas dalam jumlah penyewa. Musim Fall (Gugur) umumnya memiliki jumlah penyewa tertinggi, diikuti oleh Summer (Musim Panas). Musim Spring (Musim Semi) dan Winter (Musim Dingin) cenderung memiliki jumlah penyewa yang lebih rendah. Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda.
    2. Pola Harian:
        - Hari Kerja vs Akhir Pekan: Secara umum, jumlah penyewa pada hari kerja (Senin hingga Jumat) lebih tinggi dibandingkan akhir pekan (Sabtu dan Minggu). Ini mungkin karena banyak orang menggunakan sepeda sebagai alat transportasi untuk bekerja atau aktivitas sehari-hari lainnya.
        - Perbedaan Hari Kerja: Terdapat sedikit perbedaan jumlah penyewa di antara hari-hari kerja. Ini dipengaruhi oleh faktor-faktor seperti hari libur nasional, acara khusus, atau kondisi cuaca pada hari tersebut.

    3. Interaksi Musim dan Hari: Kombinasi antara musim dan hari dalam seminggu memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa pada akhir pekan mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.
'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)
    
    elif plot_type == "Workingday & Musim":
        st.image("dashboard_pitc/musimdanworkingday.png", caption="Workingday dan Musim")
        long_text ='''
    1. Dominasi Hari Kerja: Secara umum, jumlah penyewa pada hari kerja lebih tinggi dibandingkan akhir pekan di semua musim. Ini mengindikasikan bahwa banyak orang menggunakan sepeda sebagai alat transportasi sehari-hari untuk bekerja atau aktivitas lainnya.
    
    2. Fluktuasi Musiman: Terdapat pola musiman yang jelas dalam jumlah penyewa, baik pada hari kerja maupun akhir pekan. Musim gugur (Fall) umumnya memiliki jumlah penyewa tertinggi, diikuti oleh musim panas (Summer). Musim semi (Spring) dan musim dingin (Winter) cenderung memiliki jumlah penyewa yang lebih rendah. Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda.
    3. Interaksi Musim dan Hari Kerja: Kombinasi antara musim dan hari kerja memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa pada akhir pekan mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.
'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)
        
        
    elif plot_type == "Holiday & Musim":
        st.image("dashboard_pitc/musimdanholiday.png", caption="Holidaydan Musim")
        long_text ='''1. Musim Fall (Gugur) merupakan musim dengan jumlah penyewa tertinggi baik pada hari libur maupun bukan libur. Ini mengindikasikan bahwa cuaca atau aktivitas pada musim gugur mungkin lebih mendukung aktivitas bersepeda
        
2. Jumlah penyewa secara umum lebih tinggi pada hari-hari yang bukan libur. Ini masuk akal karena pada hari kerja, orang-orang mungkin lebih sering menggunakan sepeda untuk beraktivitas sehari-hari seperti bekerja atau bersekolah.        
3. Pada semua musim, jumlah penyewa pada hari libur lebih rendah dibandingkan hari yang bukan libur. Ini menunjukkan bahwa meskipun ada peningkatan jumlah penyewa pada hari libur, namun secara keseluruhan, aktivitas bersepeda lebih tinggi pada hari kerja.
4. Terdapat fluktuasi jumlah penyewa yang cukup signifikan antara musim. Ini mengindikasikan bahwa faktor musiman seperti cuaca, suhu, dan panjang hari memiliki pengaruh yang cukup besar terhadap minat masyarakat untuk menyewa sepeda.'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)

        
with tab3:
    plot_type = st.selectbox("Choose", [
    "Penyewa Casual by Weekday & Musim", 
    "Penyewa Casual by Workingday & Musim", 
    "Penyewa Casual by Holiday & Musim", 
    "Penyewa Registered by Weekday & Musim", 
    "Penyewa Registered by Workingday & Musim", 
    "Penyewa Registered by Holiday & Musim"
])

    if plot_type == "Penyewa Casual by Weekday & Musim":
        st.image("dashboard_pitc/casualbyweekdaynseason.png", caption="Penyewa Casual by Weekday & Musim")
        long_text ='''
    1. Fluktuasi Harian: Jumlah penyewa kasual cenderung lebih tinggi pada akhir pekan (Sabtu dan Minggu) dibandingkan hari kerja. Ini menunjukkan bahwa banyak orang menggunakan sepeda kasual untuk rekreasi atau aktivitas di luar ruangan pada akhir pekan.
    2. Pola Musiman: Terdapat perbedaan jumlah penyewa kasual di setiap musim, meskipun tidak sejelas pada visualisasi sebelumnya. Namun, secara umum, musim-musim tertentu mungkin memiliki preferensi yang berbeda terkait dengan penggunaan sepeda kasual.
    3. Interaksi Hari dan Musim: Kombinasi antara hari dalam minggu dan musim memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa kasual pada akhir pekan mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.
'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)

    elif plot_type == "Penyewa Casual by Workingday & Musim":
        st.image("dashboard_pitc/casualbyworkingdaynseason.png", caption="Penyewa Casual by Workingday & Musim")
        long_text ='''
  1. Dominasi Hari Libur: Secara umum, jumlah penyewa kasual pada hari libur (non-working day) lebih tinggi dibandingkan hari kerja. Ini mengindikasikan bahwa banyak orang menggunakan sepeda kasual untuk rekreasi atau aktivitas di luar ruangan pada akhir pekan.

    2. Fluktuasi Musiman: Terdapat perbedaan jumlah penyewa kasual di setiap musim. Musim gugur (fall) dan musim panas (summer) umumnya memiliki jumlah penyewa kasual yang lebih tinggi dibandingkan musim semi (spring) dan musim dingin (winter). Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda kasual.

    3. Interaksi Hari dan Musim: Kombinasi antara hari kerja dan musim memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa kasual pada akhir pekan mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)


    elif plot_type == "Penyewa Casual by Holiday & Musim":
        st.image("dashboard_pitc/casualbyholidaynseason.png", caption="Penyewa Casual by Holiday & Musim")
        long_text ='''
   1.  Dominasi Hari Libur: Secara umum, jumlah penyewa kasual pada hari libur (Holiday) lebih tinggi dibandingkan hari kerja (No Holiday). Ini mengindikasikan bahwa banyak orang menggunakan sepeda kasual untuk rekreasi atau aktivitas di luar ruangan pada akhir pekan atau hari libur.

    2. Fluktuasi Musiman: Terdapat perbedaan jumlah penyewa kasual di setiap musim. Musim gugur (Fall) dan musim panas (Summer) umumnya memiliki jumlah penyewa kasual yang lebih tinggi dibandingkan musim semi (Spring) dan musim dingin (Winter). Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda kasual.

    3. Interaksi Hari Libur dan Musim: Kombinasi antara hari libur dan musim memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa kasual pada hari libur mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)


    elif plot_type == "Penyewa Registered by Weekday & Musim":
        st.image("dashboard_pitc/registeredbyweekdaynseason.png", caption="Penyewa Registered by Weekday & Musim")
        long_text ='''
   1. Fluktuasi Harian: Jumlah penyewa registered cenderung lebih tinggi pada akhir pekan (Sabtu dan Minggu) dibandingkan hari kerja. Ini mengindikasikan bahwa banyak pengguna terdaftar menggunakan sepeda untuk rekreasi atau aktivitas di luar ruangan pada akhir pekan.
    2. Pola Musiman: Terdapat perbedaan jumlah penyewa registered di setiap musim. Musim gugur (Fall) dan musim panas (Summer) umumnya memiliki jumlah penyewa registered yang lebih tinggi dibandingkan musim semi (Spring) dan musim dingin (Winter). Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda.
    3. Interaksi Hari dan Musim: Kombinasi antara hari dalam minggu dan musim memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa registered pada akhir pekan mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)


    elif plot_type == "Penyewa Registered by Workingday & Musim":
        st.image("dashboard_pitc/registeredbyworkingdaynseason.png", caption="Penyewa Registered by Workingday & Musim")
        long_text ='''

   1.  Dominasi Hari Libur: Secara umum, jumlah penyewa registered pada hari libur (non-working day) lebih tinggi dibandingkan hari kerja. Ini mengindikasikan bahwa banyak pengguna terdaftar menggunakan sepeda untuk rekreasi atau aktivitas di luar ruangan pada akhir pekan.

    2. Fluktuasi Musiman: Terdapat perbedaan jumlah penyewa registered di setiap musim. Musim gugur (fall) dan musim panas (summer) umumnya memiliki jumlah penyewa registered yang lebih tinggi dibandingkan musim semi (spring) dan musim dingin (winter). Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda.

    3. Interaksi Hari dan Musim: Kombinasi antara hari kerja dan musim memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa registered pada akhir pekan mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.
'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)


    elif plot_type == "Penyewa Registered by Holiday & Musim":
        st.image("dashboard_pitc/registeredbyholidaynseason.png", caption="Penyewa Registered by Holiday & Musim")
        long_text ='''
    1. Dominasi Hari Libur: Secara umum, jumlah penyewa registered pada Kerja(No Holiday) jauh lebih tinggi dibandingkan di hari Libur (Holiday). Ini mengindikasikan bahwa banyak pengguna terdaftar menggunakan sepeda untuk rekreasi atau aktivitas di luar ruangan pada akhir pekan atau hari libur.

    2. Fluktuasi Musiman: Terdapat perbedaan jumlah penyewa registered di setiap musim. Musim gugur (Fall) dan musim panas (Summer) umumnya memiliki jumlah penyewa registered yang lebih tinggi dibandingkan musim semi (Spring) dan musim dingin (Winter). Ini menunjukkan bahwa faktor cuaca dan aktivitas musiman sangat mempengaruhi minat masyarakat untuk menyewa sepeda.

    3. Interaksi Hari Libur dan Musim: Kombinasi antara hari libur dan musim memberikan pola yang lebih kompleks. Misalnya, pada musim panas, jumlah penyewa registered pada hari libur mungkin lebih tinggi dibandingkan musim dingin karena cuaca yang lebih mendukung untuk beraktivitas di luar ruangan.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)


        
    
# Isi tab 3: Clustering
with tab4:
    plot_type = st.selectbox("Choose", [
    "Cluster Penyewa by Musim", 
    "Cluster Perilaku Penyewa Weekday", 
    "Cluster Perilaku Penyewa Workingday", 
    "Cluster Perilaku Penyewa Holiday"
])

    if plot_type == "Cluster Penyewa by Musim":
        st.image("dashboard_pitc/cluster_sewa_by_season.png")
        long_text ='''
    
    1. Segmentasi Pasar:
        - Musim Puncak: Terdapat cluster yang menunjukkan jumlah penyewaan yang sangat tinggi pada suhu tertentu. Ini mengindikasikan musim puncak dalam bisnis penyewaan sepeda. Perusahaan dapat mempersiapkan diri dengan meningkatkan jumlah sepeda yang tersedia dan mungkin menawarkan promo khusus selama musim puncak.
        - Musim Sepi: Sebaliknya, ada juga cluster yang menunjukkan jumlah penyewaan yang lebih rendah. Perusahaan dapat memanfaatkan periode ini untuk melakukan perawatan rutin pada sepeda atau menawarkan paket promosi khusus untuk menarik pelanggan.
    2. Strategi Harga:
        - Harga Dinamis: Perusahaan dapat menerapkan strategi harga yang dinamis berdasarkan musim dan suhu. Misalnya, menaikkan harga sewa selama musim puncak dan memberikan diskon pada musim sepi.
    3. Perencanaan Inventaris:
        - Prediksi Permintaan: Dengan memahami pola penyewaan pada setiap cluster, perusahaan dapat lebih akurat dalam memprediksi permintaan sepeda di masa mendatang dan mengatur inventaris secara lebih efisien.
        - Lokasi Stasiun Sepeda: Perusahaan dapat mengoptimalkan lokasi stasiun sepeda berdasarkan pola penggunaan pada setiap cluster. Misalnya, menempatkan lebih banyak sepeda di area yang populer selama musim puncak.
    4. Pengembangan Produk:
        - Aksesori Musim Dingin: Jika ada cluster yang menunjukkan penggunaan sepeda yang cukup tinggi meskipun pada suhu rendah, perusahaan dapat mempertimbangkan untuk menyediakan aksesori tambahan seperti sarung tangan, topi, atau jaket untuk menarik lebih banyak pelanggan.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)
            
    elif plot_type == "Cluster Perilaku Penyewa Weekday":
        st.image("dashboard_pitc/cluster_perilaku_wekday.png")
        long_text ='''
    
    - Cluster pertama cenderung memiliki jumlah penyewa reguler dan casual yang lebih tinggi.
    - Cluster kedua memiliki jumlah penyewaan yang lebih rendah.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)
            
            
    elif plot_type == "Cluster Perilaku Penyewa Workingday":
        st.image("dashboard_pitc/cluster_perilaku_workingday.png")
        long_text ='''
    - Pola serupa dengan weekday, namun dengan jumlah penyewaan reguler yang lebih tinggi. Ini menunjukkan bahwa pada hari kerja, sebagian besar pengguna adalah pengguna reguler yang mungkin menggunakan sepeda untuk commuting.
'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)
            
            
    elif plot_type == "Cluster Perilaku Penyewa Holiday":
        st.image("dashboard_pitc/cluster_perilaku_holiday.png")
        long_text ='''
        
    - Jumlah penyewa casual cenderung lebih tinggi dibandingkan hari kerja, menunjukkan bahwa banyak orang menyewa sepeda untuk rekreasi pada hari libur.
    - Ada kemungkinan adanya beberapa cluster yang mewakili area wisata atau taman yang populer.

'''
        with st.container():
            st.markdown("**Dari hasil visualsisasi diatas dapat dilihat bahwa :**")
            st.markdown(long_text)

            
            
    
    
