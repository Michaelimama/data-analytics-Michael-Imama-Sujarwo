--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- 		PENJELASAN		--
-- Model ini terdiri dari empat tabel utama dan satu sequence. Hubungan antar tabel bersifat relasional dan analitis (tidak sepenuhnya normalized ke 3NF karena fokusnya untuk analisis, bukan transaksi). 
-- Berikut diagram konseptual sederhana:


-- users ───┬───< reading_progress >───┬─── books
--          │                          │
--          │                          │
--          ├───< user_interactions >──┘
--         	│
--          └───< user_segments >


-- Hubungan Antar Tabel (Logical Relationships)
-- | Relasi                                                | Jenis Hubungan | Keterangan                                                    |
-- | ----------------------------------------------------- | -------------- | ------------------------------------------------------------- |
-- | `books.id` → `reading_progress.book_id`               | One-to-Many    | Satu buku dapat dibaca oleh banyak pengguna.                  |
-- | `books.id` → `user_interactions.book_id`              | One-to-Many    | Satu buku dapat memiliki banyak interaksi pengguna.           |
-- | `user_segments.user_id` → `reading_progress.user_id`  | One-to-Many    | Satu pengguna memiliki banyak catatan progres baca.           |
-- | `user_segments.user_id` → `user_interactions.user_id` | One-to-Many    | Satu pengguna memiliki banyak interaksi dengan berbagai buku. |


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: books; Type: TABLE; Schema: public; Owner: postgres

CREATE TABLE public.books (
    id integer NOT NULL,
    title text,
    author text,
    genre text,
    pages integer,
    rating double precision
);
-- Berfungsi sebagai dimensi utama (dimension table) yang menyimpan metadata tentang setiap buku.
-- | Kolom      | Tipe Data          | Deskripsi                                                                                                 |
-- | ---------- | ------------------ | --------------------------------------------------------------------------------------------------------- |
-- | **id**     | `integer`          | ID unik setiap buku, menjadi **Primary Key**. Nilainya diatur otomatis melalui sequence (`books_id_seq`). |
-- | **title**  | `text`             | Judul buku.                                                                                               |
-- | **author** | `text`             | Nama pengarang.                                                                                           |
-- | **genre**  | `text`             | Kategori atau jenis buku (misal: Fantasy, Sci-Fi, Romance).                                               |
-- | **pages**  | `integer`          | Jumlah halaman buku.                                                                                      |
-- | **rating** | `double precision` | Nilai rating rata-rata buku (misal: 4.5).                                                                 |


ALTER TABLE public.books OWNER TO postgres;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- Fungsi sequence ini adalah menghasilkan nilai ID unik secara otomatis setiap kali data buku baru dimasukkan.

ALTER SEQUENCE public.books_id_seq OWNER TO postgres;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: reading_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reading_progress (
    user_id text,
    book_id integer,
    pages_read integer,
    completion_rate double precision
);
-- Ini adalah tabel fakta (fact table) yang menjembatani hubungan antara user dan books.
-- | Kolom               | Tipe Data          | Deskripsi                                                           |
-- | ------------------- | ------------------ | ------------------------------------------------------------------- |
-- | **user_id**         | `text`             | ID pengguna (relasi ke `user_segments` atau `user_interactions`).   |
-- | **book_id**         | `integer`          | ID buku yang sedang dibaca (relasi ke `books.id`).                  |
-- | **pages_read**      | `integer`          | Jumlah halaman yang sudah dibaca oleh pengguna.                     |
-- | **completion_rate** | `double precision` | Rasio penyelesaian baca: `(pages_read / pages)`, antara 0 hingga 1. |


ALTER TABLE public.reading_progress OWNER TO postgres;

--
-- Name: user_interactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_interactions (
    user_id text,
    book_id integer,
    action text,
    "timestamp" timestamp without time zone
);

-- Merekam aktivitas pengguna terhadap buku Menghubungkan user_id ke pengguna dan book_id ke buku.
-- | Kolom         | Tipe Data   | Deskripsi                                                          |
-- | ------------- | ----------- | ------------------------------------------------------------------ |
-- | **user_id**   | `text`      | ID pengguna.                                                       |
-- | **book_id**   | `integer`   | ID buku.                                                           |
-- | **action**    | `text`      | Jenis interaksi (misal: `read`, `want-to-read`, `review`, `rate`). |
-- | **timestamp** | `timestamp` | Waktu interaksi dilakukan.                                         |


ALTER TABLE public.user_interactions OWNER TO postgres;

--
-- Name: user_segments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_segments (
    user_id text,
    segment text,
    total_books_read integer
);

-- Tabel ini berfungsi untuk mengelompokkan pengguna berdasarkan perilaku membaca, user_id menghubungkan ke tabel reading_progress dan user_interactions
-- | Kolom                | Tipe Data | Deskripsi                                                 |
-- | -------------------- | --------- | --------------------------------------------------------- |
-- | **user_id**          | `text`    | ID unik pengguna (bisa menjadi relasi utama antar tabel). |
-- | **segment**          | `text`    | Nama segmen pengguna (misal: Active, Moderate, Light).    |
-- | **total_books_read** | `integer` | Jumlah total buku yang telah dibaca.                      |


ALTER TABLE public.user_segments OWNER TO postgres;

--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);



--
-- PostgreSQL database dump complete
--

