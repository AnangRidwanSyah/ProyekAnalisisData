# Proyek Analisis Data

## Proyek Akhir Dicoding Course: Belajar Analisis Data dengan Python

## Deskripsi
Proyek ini menggambarkan eksplorasi dan analisis dari [Bike Sharing Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view) dengan tujuan menyajikan informasi yang relevan dan wawasan yang berguna terkait dengan tren penggunaan sepeda. Proyek ini juga mencakup penyesuaian tampilan dashboard dan penanganan kesalahan yang mungkin timbul selama pengembangan. Melalui langkah-langkah ini, proyek bertujuan untuk memberikan pemahaman yang lebih dalam tentang pola penggunaan sepeda berdasarkan faktor-faktor tertentu.

## Struktur Direktori 
- **Bike_Sharing_Dataset**: Direktori ini berisi raw data dan data yang sudah diolah untuk digunakan dalam analisis, dalam format .csv.
- **dashboard.py**: File ini digunakan untuk melakukan generate dashboard hasil visualisasi menggunakan streamlit.
- **FP_Analisis_Data_Dicoding.ipynb**: File ini digunakan untuk melakukan tahap analisis data mulai dari Data Wrangling, Exploratory Data Analysis (EDA), dan Visualization & Explanatory Analysis.

## Cara Instalasi

1. Clone repository ini ke komputer lokal Anda menggunakan perintah berikut:

   ```shell
   git clone https://github.com/AnangRidwanSyah/ProyekAnalisisData.git
   ```
2. Set Up Environment:
   ```shell
   conda create --name main-ds python=3.9
   conda activate main-ds
   pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
   ```
3. Run Streamlit Dashboard dari CMD:
   ```shell
   cd \{Folder_File_Penyimpanan}
   streamlit run dashboard.py
   ```
## Tampilan Dashboard
![image](https://github.com/AnangRidwanSyah/ProyekAnalisisData/assets/112993686/cb5731f8-899d-4a19-80fe-1c871512bf42)

