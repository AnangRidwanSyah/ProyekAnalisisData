import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from datetime import datetime

sns.set(style='dark')

# Load DataFrame
day_df = pd.read_csv("day_df_clean.csv")
hour_df = pd.read_csv("hour_df_clean.csv")

# Ubah kolom tanggal menjadi tipe datetime untuk kedua DataFrame
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

with st.sidebar:
    # Menambahkan foto
    st.image("https://media.licdn.com/dms/image/D5603AQGr8Hy4JfQFOQ/profile-displayphoto-shrink_800_800/0/1678863394592?e=1714608000&v=beta&t=1yNdAgOyMhqMpQrVc1yEYNtJ9k_4_Jk0ccpw7BE4uhc", use_column_width=True)
    
    # Informasi kontak
    st.title("Kontak")
    st.write("Nama: Anang Ridwan Syah")
    st.write("Email: anangridwan795@gmail.com")

    # Filter data
    st.title("Filter Data")
    
    # Sidebar untuk memilih rentang tanggal
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]  # Gunakan list untuk nilai awal
    )

    # Tambahkan slider untuk memilih rentang temperatur
    min_temp = day_df['temp'].min()
    max_temp = day_df['temp'].max()
    selected_temp_range = st.slider(
        label="Rentang Temperatur (Celsius)",
        min_value=min_temp,
        max_value=max_temp,
        value=(min_temp, max_temp)  # Gunakan tuple untuk nilai awal
    )

    # Pisahkan nilai minimum dan maksimum dari tuple yang dipilih
    min_selected_temp, max_selected_temp = selected_temp_range

    # Tambahkan filter untuk cuaca
    selected_weather = st.sidebar.multiselect(
    label="Pilih Kondisi Cuaca",
    options=day_df['weathersit'].unique(),  # Opsi berdasarkan nilai unik dalam kolom 'weathersit'
    default=day_df['weathersit'].unique()  # Nilai default adalah semua opsi yang tersedia
    )

    
# Konversi nilai awal menjadi datetime64[ns]
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Tambahkan header
st.markdown("<h1 style='text-align: center;'>DICODING - Proyek Analisis Data \U0001F4C8</h1>", unsafe_allow_html=True)

# Tambahkan spasi setelah header
st.markdown("<br>", unsafe_allow_html=True)

def kata_pengantar():
    st.markdown("""
    <div style="text-align: justify;">
    Selamat datang di dashboard analisis data penyewaan sepeda! 
                
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div style="text-align: justify;"> 
    Dashboard ini menyajikan visualisasi data tentang tren penggunaan sepeda berdasarkan berbagai faktor, termasuk suhu, kondisi cuaca, dan rentang waktu tertentu. Melalui visualisasi interaktif yang disediakan, Anda dapat menjelajahi pola penggunaan sepeda, memahami dampak faktor-faktor eksternal seperti suhu dan cuaca, serta mengidentifikasi tren yang mungkin memengaruhi permintaan penyewaan sepeda. Selamat menjelajahi dan semoga dashboard ini memberikan wawasan yang berharga bagi Anda!

        
    """, unsafe_allow_html=True)          
        

# Panggil fungsi kata_pengantar untuk menampilkan paragraf kata pengantar di dashboard
kata_pengantar()

st.markdown("<br>", unsafe_allow_html=True)

# Pola Penyewaan Sepeda Sepanjang Tahun
st.header("1. Pola Penyewaan Sepeda Sepanjang Tahun")
st.markdown("- Grafik Penyewa dalam Satu Bulan")

#VISUALISASI PERTANYAAN 1 - 1
def plot_monthly_rental(day_df, start_date, end_date, temp_range, selected_weather):
    # Filter DataFrame berdasarkan rentang tanggal
    filtered_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
    
    # Filter DataFrame berdasarkan rentang temperatur
    filtered_df = filtered_df[(filtered_df['temp'] >= temp_range[0]) & (filtered_df['temp'] <= temp_range[1])]

    # Filter DataFrame berdasarkan kondisi cuaca yang dipilih
    filtered_df = filtered_df[filtered_df['weathersit'].isin(selected_weather)]

    # Kelompokkan data berdasarkan bulan dan jumlahkan kolom 'cnt'
    df_by_month = filtered_df.groupby(filtered_df['dteday'].dt.to_period('M')).agg({'cnt': 'sum'})

    # Membuat subplot dengan ukuran yang telah ditentukan
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot garis chart
    ax.plot(df_by_month.index.to_timestamp(), df_by_month['cnt'], label='Jumlah Pengguna Rental Sepeda', marker='o', color='blue', linestyle='-')

    # Judul plot dan label sumbu
    ax.set_title('Jumlah Pengguna Rental Sepeda per Bulan', fontsize=16)
    ax.set_xlabel('Bulan', fontsize=14)
    ax.set_ylabel('Jumlah Pengguna', fontsize=14)

    # Menambahkan teks hover untuk setiap titik
    for x, y in zip(df_by_month.index.to_timestamp(), df_by_month['cnt']):
        ax.text(x, y, f'{int(y)}', ha='center', va='bottom')

    # Menampilkan legenda
    ax.legend()

    # Menampilkan plot
    st.pyplot(fig)

# Panggil fungsi untuk menggambar plot
plot_monthly_rental(day_df, start_date, end_date, selected_temp_range, selected_weather)


st.markdown("- Grafik Penyewa dalam Satu Hari")

#VISUALISASI PERTANYAAN 1 - 2
def plot_daily_rental(hour_df, start_date, end_date, temp_range, selected_weather):
    # Filter DataFrame berdasarkan rentang tanggal
    filtered_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]
    # Filter DataFrame berdasarkan rentang temperatur
    filtered_df = filtered_df[(filtered_df['temp'] >= temp_range[0]) & (filtered_df['temp'] <= temp_range[1])]
    # Filter DataFrame berdasarkan kondisi cuaca yang dipilih
    filtered_df = filtered_df[filtered_df['weathersit'].isin(selected_weather)]
    
    # Kelompokkan data berdasarkan hari dan jumlahkan kolom 'cnt'
    df_by_day = filtered_df.groupby(filtered_df['dteday']).agg({'cnt': 'sum'})

    # Membuat subplot dengan ukuran yang telah ditentukan
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot garis chart tanpa marker
    ax.plot(df_by_day.index, df_by_day['cnt'], label='Jumlah Pengguna Rental Sepeda', color='orange', linestyle='-')

    # Judul plot dan label sumbu
    ax.set_title('Jumlah Pengguna Rental Sepeda per Hari', fontsize=16)
    ax.set_xlabel('Tanggal', fontsize=14)
    ax.set_ylabel('Jumlah Pengguna', fontsize=14)

    # Menampilkan legenda
    ax.legend()

    # Menampilkan plot
    st.pyplot(fig)

# Panggil fungsi untuk menggambar plot
plot_daily_rental(hour_df, start_date, end_date, selected_temp_range, selected_weather)


st.markdown("- Grafik Perbandingan Rata-Rata")

#VISUALISASI PERTANYAAN 1 - 3
# Filter DataFrame berdasarkan rentang tanggal
filtered_day_df_visualisasi3 = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
filtered_hour_df_visualisasi3 = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]

# Filter DataFrame berdasarkan rentang temperatur
filtered_day_df_visualisasi3 = filtered_day_df_visualisasi3[(filtered_day_df_visualisasi3['temp'] >= min_selected_temp) & (filtered_day_df_visualisasi3['temp'] <= max_selected_temp)]
filtered_hour_df_visualisasi3 = filtered_hour_df_visualisasi3[(filtered_hour_df_visualisasi3['temp'] >= min_selected_temp) & (filtered_hour_df_visualisasi3['temp'] <= max_selected_temp)]

# Filter DataFrame berdasarkan kondisi cuaca yang dipilih
filtered_day_df_visualisasi3 = filtered_day_df_visualisasi3[filtered_day_df_visualisasi3['weathersit'].isin(selected_weather)]
filtered_hour_df_visualisasi3 = filtered_hour_df_visualisasi3[filtered_hour_df_visualisasi3['weathersit'].isin(selected_weather)]

monthly_mean_visualisasi3 = filtered_day_df_visualisasi3.groupby(filtered_day_df_visualisasi3['dteday'].dt.to_period('M')).agg({'cnt': 'sum'})['cnt'].mean()
daily_mean_visualisasi3 = filtered_hour_df_visualisasi3.groupby(filtered_hour_df_visualisasi3['dteday']).agg({'cnt': 'sum'})['cnt'].mean()

# Kelompokkan data per bulan
df_by_month_visualisasi3 = filtered_day_df_visualisasi3.groupby(filtered_day_df_visualisasi3['dteday'].dt.to_period('M')).agg({'cnt': 'sum'})

# Kelompokkan data per hari
df_by_day_visualisasi3 = filtered_hour_df_visualisasi3.groupby(filtered_hour_df_visualisasi3['dteday']).agg({'cnt': 'sum'})

# Membuat subplot dengan ukuran yang telah ditentukan
fig_visualisasi3, ax_visualisasi3 = plt.subplots(2, 1, figsize=(16, 12), sharex=True)

# Plot garis chart per bulan dengan marker bulatan
ax_visualisasi3[0].plot(df_by_month_visualisasi3.index.to_timestamp(), df_by_month_visualisasi3['cnt'], label='Bulanan', color='blue', linestyle='-', marker='o')
ax_visualisasi3[0].axhline(y=monthly_mean_visualisasi3, color='red', linestyle='--', label='Rata-rata Bulanan')

# Menambahkan keterangan angka di setiap titik data
for x, y in zip(df_by_month_visualisasi3.index.to_timestamp(), df_by_month_visualisasi3['cnt']):
    ax_visualisasi3[0].text(x, y, f'{int(y)}', ha='center', va='bottom')

# Menambahkan keterangan angka di garis rata-rata bulanan
ax_visualisasi3[0].text(df_by_month_visualisasi3.index[-1].to_timestamp(), monthly_mean_visualisasi3, f'Rata-rata: {int(monthly_mean_visualisasi3)}', ha='left', va='bottom', fontweight='bold')

ax_visualisasi3[0].set_title('Jumlah Pengguna Rental Sepeda per Bulan (2011-2012)')
ax_visualisasi3[0].set_ylabel('Jumlah Pengguna')
ax_visualisasi3[0].legend()

# Plot garis chart per hari
ax_visualisasi3[1].plot(df_by_day_visualisasi3.index, df_by_day_visualisasi3['cnt'], label='Harian', color='orange', linestyle='-')
ax_visualisasi3[1].axhline(y=daily_mean_visualisasi3, color='red', linestyle='--', label='Rata-rata Harian')

# Menambahkan keterangan angka di garis rata-rata harian
ax_visualisasi3[1].text(df_by_day_visualisasi3.index[-1], daily_mean_visualisasi3, f'Rata-rata: {int(daily_mean_visualisasi3)}', ha='right', va='bottom', fontweight='bold')

ax_visualisasi3[1].set_title('Jumlah Pengguna Rental Sepeda per Hari (2011-2012)')
ax_visualisasi3[1].set_xlabel('Tanggal')
ax_visualisasi3[1].set_ylabel('Jumlah Pengguna')
ax_visualisasi3[1].legend()

# Menampilkan plot
ax_visualisasi3[1].grid(False)  # Matikan grid di subplot kedua
plt.tight_layout()

# Tampilkan plot menggunakan Streamlit
st.pyplot(fig_visualisasi3)

# Dampak Suhu dan Cuaca dalam Penyewaan Sepeda
st.header("2. Dampak Suhu dan Cuaca dalam Penyewaan Sepeda")
st.markdown("- Grafik Pengaruh Temperatur terhadap Jumlah Pengguna")

## VISUALISASI PERTANYAAN 2 - 1 
# Filter DataFrame berdasarkan rentang tanggal, temperatur, dan cuaca
filtered_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
filtered_df = filtered_df[(filtered_df['temp'] >= min_selected_temp) & (filtered_df['temp'] <= max_selected_temp)]
filtered_df = filtered_df[filtered_df['weathersit'].isin(selected_weather)]

# Scatter plot: Temperatur vs Jumlah Pengguna setelah difilter
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(filtered_df['temp'], filtered_df['cnt'], color='blue', alpha=0.5)  # Menggunakan kolom 'temp' dan 'cnt'
ax.set_title('Scatter Plot: Temperatur vs Jumlah Pengguna')
ax.set_xlabel('Temperatur (C)')
ax.set_ylabel('Jumlah Pengguna')
ax.grid(False)

# Menampilkan plot di Streamlit
st.pyplot(fig)


st.markdown("- Grafik Pengaruh Cuaca terhadap Jumlah Pengguna")

## VISUALISASI PERTANYAAN 2 - 2
# Filter DataFrame berdasarkan rentang tanggal
filtered_df_visualisasi2 = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]

# Filter DataFrame berdasarkan rentang temperatur
filtered_df_visualisasi2 = filtered_df_visualisasi2[(filtered_df_visualisasi2['temp'] >= min_selected_temp) & (filtered_df_visualisasi2['temp'] <= max_selected_temp)]

# Filter DataFrame berdasarkan kondisi cuaca yang dipilih
filtered_df_visualisasi2 = filtered_df_visualisasi2[filtered_df_visualisasi2['weathersit'].isin(selected_weather)]

# Tentukan warna untuk setiap kondisi cuaca
weather_colors = {
    'Clear/Partly Cloudy': 'blue',
    'Misty/Cloudy': 'green',
    'Light Snow/Rain': 'red'
}

# Membuat line plot setelah difilter
plt.figure(figsize=(12, 6))
for weather_situation, group_data in filtered_df_visualisasi2.groupby('weathersit'):
    plt.plot(group_data['dteday'], group_data['cnt'], label=f"Weather: {weather_situation}", color=weather_colors[weather_situation])

plt.title('Tren Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Pengguna')
plt.legend()
plt.grid(False)
plt.tight_layout()

# Menampilkan plot menggunakan st.pyplot()
st.pyplot(plt)
