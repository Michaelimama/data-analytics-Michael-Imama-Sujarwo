-- 1. Genre Paling Populer
-- Tujuan nya untuk mengetahui genre buku paling populer berdasarkan jumlah buku yang tersedia, serta melihat rata-rata rating per genre.
SELECT 
    genre, 
    COUNT(*) AS book_count, 
    AVG(rating) AS avg_rating
FROM books
GROUP BY genre
ORDER BY book_count DESC;

-- Insight --
-- a. Genre Fantasy memiliki jumlah buku terbanyak dan rating rata-rata tinggi (4.08), menunjukkan bahwa genre ini paling diminati dan berkualitas baik.
-- b. Genre lain seperti Romance, Sci-Fi, dan Dystopian juga punya rating bagus meskipun jumlah bukunya sedikit — ini bisa jadi peluang untuk menambah koleksi.
-- c. Coming-of-Age punya rating paling rendah (3.08), menandakan kurang diminati atau kualitas buku dalam genre tersebut perlu ditinjau ulang.


-- 2. Statistik segment pembaca
-- Mengukur kinerja membaca tiap pengguna, baik dari jumlah buku yang sudah dibaca maupun rata-rata persentase penyelesaian bacaan.
SELECT 
    user_id,
    COUNT(DISTINCT book_id) AS books_read,
    ROUND(AVG(completion_rate)::numeric, 2) AS avg_completion
FROM reading_progress
GROUP BY user_id
ORDER BY avg_completion DESC;

-- Insight -- 
-- a. User 20 memiliki completion rate tertinggi (55%), menandakan bahwa meskipun hanya membaca 1 buku, ia benar-benar menuntaskannya.
-- b. Pengguna dengan jumlah buku lebih banyak (2–3 buku) rata-rata punya completion rate lebih rendah (0.20–0.30) → menunjukkan kecenderungan membaca banyak buku tapi tidak sampai selesai.
-- c. Pola ini bisa digunakan untuk membuat strategi retensi pengguna — misalnya mendorong pengguna aktif dengan rekomendasi buku yang sesuai minat.

-- 3. Top active users (by number of interactions)
-- Menemukan pengguna paling aktif berdasarkan jumlah interaksi (misal klik, review, like, borrow) yang mereka lakukan pada platform.
SELECT 
    user_id,
    COUNT(*) AS total_interactions
FROM user_interactions
GROUP BY user_id
ORDER BY total_interactions DESC
LIMIT 10;

-- Insight --
-- Ada 4 pengguna paling aktif dengan 6 interaksi — bisa dianggap sebagai "power users".
-- Pengguna seperti ini cocok dijadikan target promosi, program loyalitas, atau beta tester untuk fitur baru.

-- 4. Average reading rate by user segment
-- Menganalisis tingkat penyelesaian bacaan rata-rata per segmen pengguna, guna memahami perbedaan perilaku antar kelompok pembaca.
SELECT 
    s.segment,
    COUNT(r.user_id) AS total_users,
    ROUND(AVG(r.completion_rate)::numeric, 2) AS avg_completion_segment
FROM reading_progress r
JOIN user_segments s ON r.user_id = s.user_id
GROUP BY s.segment
ORDER BY avg_completion_segment DESC;

-- Insight -- 
-- Steady Reader punya completion rate tertinggi (0.23), artinya mereka paling konsisten membaca.
-- Speed Reader justru completion rate-nya rendah (0.06) — bisa jadi mereka sering berpindah buku tanpa menyelesaikan.