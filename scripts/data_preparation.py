#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Library Python yang dipakai saat proses/pengolahan

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random
import os


# In[4]:


# Import/Load Data Json dalam library lokal

import json

with open('/Users/macbook/Documents/Assignment Data Analytics Engineer/books.json', 'r') as f:
    data = json.load(f)
    
# Dikonversi menjadi dataframe 
df_books = pd.DataFrame(data['books'])
df_books


# In[5]:


# Informasi Mengenai dari Dtype disetiap kolom dan value pada data
df_books.info()


# In[6]:


# Informasi Mengenai Apakah terdapat Duplikat pada data
df_books.duplicated()


# In[7]:


print(df_books['id'].is_unique)      
print(df_books['title'].is_unique)  


# In[8]:


# Standarisasi format teks
df_books['title'] = df_books['title'].str.title().str.strip()
df_books['author'] = df_books['author'].str.title().str.strip()
df_books['genre'] = df_books['genre'].str.title().str.strip()
df_books['status'] = df_books['status'].str.capitalize().str.strip()
df_books


# In[9]:


# Simpan Data Books yang sudah menggunakan format CSV
df_books.to_csv("clean_books.csv", index=False)


# ## Membuat data sampel tambahan untuk interaksi pengguna dan kemajuan membaca

# In[10]:


# Load Csv books yang sudah clean
df_clean_books = pd.read_csv("clean_books.csv")
df_clean_books


# In[40]:


# Buat ID pengguna (50 user)
user_ids = list(range(1, 51))

# Buat Jumlah interaksi 
num_interactions = 150 

# jumlah data progres baca
num_progress = 100


# In[41]:


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


# In[42]:


interactions


# In[47]:


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


# In[48]:


reading_progress


# In[49]:


# Pengecekan Kualitas Data & Konsistensi kedua data yang dibuat
interactions.info()


# In[50]:


# Pengecekan Kualitas Data & Konsistensi kedua data yang dibuat
reading_progress.info()


# In[52]:


# Validasi Relasi Antar Dataset (Integrity Check)
invalid_books_interactions = interactions[~interactions["book_id"].isin(df_clean_books["id"])]
invalid_books_progress = reading_progress[~reading_progress["book_id"].isin(df_clean_books["id"])]

print("Invalid book references in interactions:", len(invalid_books_interactions))
print("Invalid book references in progress:", len(invalid_books_progress))

# Tujuan: memastikan book_id di interactions dan progress benar-benar ada di books


# In[54]:


# Validasi Logika Kolom

# Pages read tidak boleh melebihi total pages
invalid_progress = reading_progress[reading_progress["pages_read"] > reading_progress["total_pages"]]
print("Invalid pages_read entries:", len(invalid_progress))

# Tujuan: pastikan logika bisnis tidak rusak saat generate data.


# In[63]:


# Simpan data interaksi pengguna dan kemajuan baca menggunakan format CSV
interactions.to_csv("user_interactions.csv", index=False)
reading_progress.to_csv("reading_progress.csv", index=False)


# ### Transformasi Data 

# #### Hitung Metrik Turunan

# In[57]:


# Buat tanggal mulai acak
reading_progress["date_start"] = pd.to_datetime(
    np.random.choice(pd.date_range("2025-01-01", "2025-03-31"), size=len(reading_progress))
)

# Buat tanggal update antara 1–30 hari setelah mulai
reading_progress["date_last_update"] = reading_progress["date_start"] + pd.to_timedelta(
    np.random.randint(1, 30, size=len(reading_progress)), unit="D"
)

# Hitung jumlah hari aktif membaca
reading_progress["days_active"] = (
    (reading_progress["date_last_update"] - reading_progress["date_start"]).dt.days + 1
)

# Hitung kecepatan membaca (pages per hari)
reading_progress["reading_speed"] = (
    reading_progress["pages_read"] / reading_progress["days_active"]
).round(2)

# Tambahkan status penyelesaian (Completed/In Progress)
reading_progress["status"] = np.where(
    reading_progress["completion_rate"] >= 1, "Completed", "In Progress"
)
reading_progress


# #### Segmen pengguna berdasarkan perilaku membaca

# In[64]:


# Agregasi per user
user_metrics = reading_progress.groupby("user_id").agg({
    "completion_rate": "mean",
    "reading_speed": "mean"
}).reset_index()

# Tentukan segmen pengguna
def classify_user(row):
    if row["completion_rate"] >= 0.7 and row["reading_speed"] >= 20:
        return "Speed Reader"
    elif 0.3 <= row["completion_rate"] < 0.7:
        return "Steady Reader"
    elif row["completion_rate"] < 0.3:
        return "Casual Reader"
    else:
        return "Inactive"

user_metrics["segment"] = user_metrics.apply(classify_user, axis=1)
user_metrics

user_metrics.to_csv("user_segments.csv", index=False)


# #### Data Agregat untuk Dashboard

# In[61]:


# 1.Rata-rata rating & interaksi per buku
book_summary = reading_progress.groupby("book_id").agg({
    "completion_rate": "mean",
    "reading_speed": "mean"
}).reset_index()

# 2. Distribusi segmen pengguna
segment_distribution = user_metrics["segment"].value_counts().reset_index()
segment_distribution.columns = ["segment", "user_count"]

# 3. Statistik global
summary_stats = {
    "avg_completion": round(reading_progress["completion_rate"].mean(), 2),
    "avg_reading_speed": round(reading_progress["reading_speed"].mean(), 2),
    "total_users": reading_progress["user_id"].nunique(),
    "total_books": reading_progress["book_id"].nunique()
}

print("=== 📘 Book Summary ===")
display(book_summary)

print("\n=== 👥 Segment Distribution ===")
display(segment_distribution)

print("\n=== 📈 Summary Stats ===")
display(summary_stats)


# In[62]:


reading_progress

