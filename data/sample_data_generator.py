#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Library Python yang dipakai saat proses/pengolahan

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
import os


# In[ ]:


# Buat Data Buku
books = [
    {"book_id": 1, "title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "rating": 4.3, "pages": 688},
    {"book_id": 2, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 4.9, "pages": 1216},
    {"book_id": 3, "title": "Harry Potter", "author": "J.K. Rowling", "genre": "Fantasy", "rating": 4.7, "pages": 309}
]

# Simpan ke JSON
with open('data/raw/books.json', 'w') as f:
    json.dump(books, f, indent=4)


# Bagian kode membuat sebuah daftar (list) berisi tiga buku fiktif dengan informasi penting seperti book_id, title, author, genre, rating, dan pages.
# 
# a. Kolom book_id berfungsi sebagai identitas unik untuk setiap buku.
# b. title dan author menyimpan judul dan nama penulis buku.
# c. genre menunjukkan kategori atau jenis bacaan (misalnya Sci-Fi atau Fantasy).
# d. rating menggambarkan penilaian rata-rata pembaca terhadap buku tersebut.
# e. pages menandakan jumlah halaman, yang nantinya dapat digunakan untuk menghitung progres membaca.
# 
# Setelah data buku dibuat, langkah berikutnya adalah menyimpan data tersebut dalam format JSON menggunakan modul json.

# In[3]:


# Buat ID pengguna (50 user)
user_ids = list(range(1, 51))

# Buat Jumlah interaksi 
num_interactions = 150 

# jumlah data progres baca
num_progress = 100


# Bagian ini menyiapkan parameter dasar simulasi:
# 
# a. user_ids → membuat daftar pengguna dengan ID 1–50, artinya ada 50 pengguna unik.
# b. num_interactions → menentukan bahwa akan dibuat 150 baris data interaksi pengguna (setiap baris mewakili satu aksi seperti melihat buku, mencari buku, atau memberi rating).
# c.num_progress → menentukan jumlah baris data kemajuan membaca (100 catatan pengguna terkait buku yang sedang atau sudah dibaca)

# In[ ]:


# Buat Data Interaksi Pengguna

num_interaction = 150  # jumlah baris interaksi
interactions = pd.DataFrame({
    "user_id": random.choices(user_ids, k=num_interactions),
    "book_id": random.choices(df_clean_books["id"], k=num_interactions),
    "action": random.choices(["view", "search", "rate"], weights=[0.5, 0.3, 0.2], k=num_interactions),
    "timestamp": [(datetime.now() - timedelta(days=random.randint(0, 60),
                                hours=random.randint(0, 23),
                                minutes=random.randint(0, 59))
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    for _ in range(num_interactions)
]})


# Bagian ini membuat DataFrame interactions berisi data aktivitas pengguna terhadap buku, dengan kolom:
# 
# a. user_id → ID pengguna yang melakukan interaksi (dipilih acak dari 1–50).
# 
# b. book_id → ID buku dari daftar df_clean_books yang sudah dibersihkan.
# 
# c. action → jenis interaksi pengguna, dipilih secara acak dengan bobot probabilitas:
# 
# d. view (melihat buku) → 50% kemungkinan
# 
# e. search (mencari buku) → 30% kemungkinan
# 
# f.rate (memberi rating) → 20% kemungkinan
# 
# g.timestamp → waktu terjadinya interaksi, dibangkitkan acak dalam rentang 60 hari terakhir, untuk mensimulasikan aktivitas nyata pengguna dari waktu ke waktu.

# In[ ]:


# Buat Data kemajuan membaca (halaman yang dibaca, status penyelesaian)

num_progress = 100  # jumlah baris data progres
reading_progress = pd.DataFrame({
    "user_id": random.choices(user_ids, k=num_progress),
    "book_id": random.choices(df_clean_books["id"], k=num_progress),
})

# Ambil total halaman dari data buku
book_page_map = dict(zip(df_clean_books["id"], df_clean_books["pages"]))
reading_progress["total_pages"] = reading_progress["book_id"].map(book_page_map)

# Tambahkan kolom pages_read (0 s.d. total_pages)
reading_progress["pages_read"] = reading_progress["total_pages"].apply(lambda x: random.randint(0, x))

# Hitung tingkat penyelesaian (completion_rate numerik)
reading_progress["completion_rate"] = (
    reading_progress["pages_read"] / reading_progress["total_pages"]
).round(2)

reading_progress = reading_progress[[
    "user_id", "book_id", "pages_read", "total_pages", "completion_rate"
]]


# Membangun untuk dataset reading_progress, yang merekam hubungan antara pengguna dan buku yang sedang mereka baca.
# 
# Setiap baris mewakili satu buku yang sedang dibaca oleh seorang pengguna.
# 
# Data awal ini belum memiliki informasi seberapa jauh mereka membaca.
# 
# Tujuan: Menyiapkan struktur data untuk menambahkan metrik kemajuan membaca di langkah berikutnya.
