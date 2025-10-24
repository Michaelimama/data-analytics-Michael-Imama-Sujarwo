# data-analytics-Michael-Imama-Sujarwo
Analytics About Books

## 📖 Deskripsi Singkat

Proyek ini bertujuan untuk menganalisis data buku dan perilaku pembaca menggunakan pendekatan data analytics berbasis Python dan SQL.
Analisis ini membantu mengidentifikasi tren buku dengan genre populer, kebiasaan membaca pengguna, top 5 buku populer, aktivitas pengguna dari waktu ke waktu, serta kemajuan membaca berdasarkan segmen pengguna.


## Struktur project mengikuti format data engineering mini-pipeline dengan tahapan:

1. ETL (Extract, Transform, Load)
2. Analisis visual & SQL query analitik
3. Dashboard statis (visualisasi akhir)


## ⚙️ Petunjuk Pengaturan (Setup Instructions)

```
data-analytics-Michael Imama Sujarwo/
├── README.md
├── data/
│   ├── raw/
│   │   └── books.json
│   ├── processed/
│   │   ├── books_clean.csv
│   │   ├── user_interactions.csv
│   │   └── reading_progress.csv
│   └── sample_data_generator.py
├── sql/
│   ├── data_model.sql
│   └── analytical_queries.sql
├── notebooks/
│   └── data_analysis.ipynb
├── dashboard/
│   ├── dashboard.html
│   └── dashboard_screenshots/
└── scripts/
    ├── data_preparation.py
    └── requirements.txt
```

## Menjalankan Project
Langkah-langkah:
1. Hasilkan data sampel -> python data/sample_data_generator.py
2. Pembersihan data (ETL) -> python scripts/data_preparation.py
3. Buka notebook analisis -> notebooks/data_analysis.ipynb
4. Lihat visualisasi -> Buka dashboard/dashboard.html di browser untuk melihat hasil visualisasi.

## 🧠 Metodologi
1. Data Collection / Generation
Menggunakan script sample_data_generator.py untuk membuat data buku dan interaksi pengguna simulatif.

2. Data Preparation (ETL)
Script data_preparation.py membersihkan data dan serta menormalisasi format kolom.
Exploratory Data Analysis (EDA)

  - Analisis distribusi genre
  - Distribusi Tingkat Penyelesaian Pembaca
  - Top 5 Buku dengan tingkat teratas
  - Aktivitas pengguna dari waktu ke waktu
  - Kemajuan membaca berdasarkan Segmen Pengguna

3. SQL Analytical Query
   
**Query pada analytical_queries.sql digunakan untuk menghitung:**
**a. Most Popular Genre**
   - Untuk mengetahui genre buku paling populer berdasarkan jumlah buku yang tersedia, serta melihat rata-rata rating per genre.
**b. User Reading Statistics**
   - Mengukur kinerja membaca tiap pengguna, baik dari jumlah buku yang sudah dibaca maupun rata-rata persentase penyelesaian bacaan.
**c. Top Active Users (by Interactions)**
   - Menemukan pengguna paling aktif berdasarkan jumlah interaksi yang mereka lakukan.
**d. Average Reading Rate by User Segment**
   - Menganalisis tingkat penyelesaian bacaan rata-rata per segmen pengguna, guna memahami perbedaan perilaku antar kelompok pembaca.

5. Visualization & Dashboard
Hasil analisis divisualisasikan dalam grafik menggunakan matplotlib / plotly, dan disajikan sebagai dashboard statis dashboard.html.


## 📊 Temuan & Rekomendasi Utama

1. Genre Fantasi mendominasi, menunjukan minat pasar tertinggi. Namun ini adalah "Zona Nyaman" yang berisiko, mungkin terjebak dalam content bubble yang kurang menarik bagi pembaca non-fiksi, membatasi potensi pertumbuhan audiens yang lebih luas.


2. Mayoritas pengguna menyelesaikan 60–80% buku yang mereka baca. Mereka bukan tidak tertarik untuk menyelesaikanya tetapi mereka merasa telah mendapat inti sari konten — tanpa harus menyelesaikan sepenuhnya.
Rekomendasi :
a. Rekomendasi konten lanjutan di 80% completion
b. Sistem reward untuk yang mencapai 100% (badges, points, akses eksklusif)
c. Survey kepuasan tepat setelah penyelesaian 100%

3. Buku Paling Teratas adalah "The Lord of the Rings" dari Genre "Fantasy" ini mencerminkan bahwasan nya pembaca tidak hanya lari dari realita — mereka mencari cerita yang membantu memahami kehidupan melalui metafora fantasi.
Rekomendasi :
Manfaatkan popularitas fantasi sebagai pintu masuk ke genre lain
Buat rekomenasi berantai:
"Jika Anda suka LOTR → coba 'Sapiens' (membangun peradaban)"
"Jika Anda suka Harry Potter → coba 'Psychology of Magic'"
Content bundling: Paket "Fantasi + Non-Fiksi Pendamping"
Serial "Dibalik Magic": Artikel tentang sains di balik konsep fantasi

4. Aktivitas membaca meningkat di awal pekan dan pada akhir pekan menunjukan Awal pekan untuk produktivitas, akhir pekan untuk kepuasan diri
Rekomendasi Strategi: Manfaatkan pola mingguan untuk membangun kebiasaan membaca yang terintegrasi dengan kehidupan pengguna

Tindakan:
a. "Monday Motivation": Konten fantasi epik untuk semangat minggu baru
b. "Weekend Wonder": Cerita pendek fantasi untuk relaksasi
c. Mid-week "Magic Break": Konten ringkat 10 menit di hari Rabu-Kamis
d. Personalized reading schedule berdasarkan historis pola baca
   
5. Segmen “Speed Reader” menunjukkan engagement tertinggi dengan 36.3%. Tidak semua pembaca cepat tercatat sebagai Speed Reader — beberapa justru masuk kategori Inactive karena cara interaksi yang berbeda.
   
Rekomendasi Strategi: Temukan dan optimasi pembaca diam yang sebenarnya sangat engaged
Tindakan:
1. Redefinisi segmentasi berdasarkan:
a. Redefinisi segmentasi berdasarkan: Completion rate, bukan hanya frekuensi login
b. Pola baca offline dan download
c. Kualitas engagement, bukan kuantitas interaksi

2. "Silent Reader VIP Program" untuk pengguna dengan completion rate tinggi tapi interaksi rendah

3. Offline reading analytics untuk memahami pola baca tersembunyi

4. Personalized re-engagement untuk "Inactive" dengan completion tinggi



