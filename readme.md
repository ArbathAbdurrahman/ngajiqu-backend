# NgajiQu API
Selamat datang di dokumentasi resmi NgajiQu API. Ini adalah layanan backend yang dirancang untuk mendukung aplikasi NgajiQu, sebuah platform digital yang berfokus untuk memudahkan para ustadz dan santri dalam mencatat dan memantau progres mengaji.

API ini dibangun menggunakan Django dan Django REST Framework, serta dilengkapi dengan dokumentasi interaktif Swagger (OpenAPI) yang dibuat secara otomatis untuk mempermudah proses pengembangan dan integrasi.

## Teknologi yang Digunakan
- Backend: Python 3.9+

- Framework: Django 5.2, Django REST Framework 3.x

- Database: PostgreSQL (direkomendasikan untuk produksi), SQLite3 (untuk pengembangan)

- Autentikasi: Simple JWT (JSON Web Token)

- Dokumentasi API: drf-spectacular (Generator skema OpenAPI 3)

- Manajemen Environment: Python Virtual Environment (venv), python-dotenv

## Prasyarat
Sebelum memulai, pastikan perangkat lunak berikut sudah terpasang di sistem Anda:

- Python 3.11 atau versi yang lebih baru

- PIP (Package Installer for Python)

- Git

## Panduan Instalasi
Ikuti langkah-langkah berikut untuk menyiapkan lingkungan pengembangan di mesin lokal Anda.

### 1. Clone Repositori

```bash
git clone https://github.com/[NAMA_PENGGUNA_ANDA]/ngajiqu-api.git
cd ngajiqu-api
```

### 2. Buat dan Aktifkan Virtual Environment
Ini akan mengisolasi dependensi proyek Anda.

```bash
# Untuk Windows
python -m venv venv
.\venv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependensi
Semua pustaka yang dibutuhkan tercantum dalam file requirements.txt.

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variables
Salin file .env.example menjadi .env. File ini digunakan untuk menyimpan konfigurasi sensitif.

```bash
cp .env.example .env
```

Kemudian, buka file `.env` dan sesuaikan nilainya.

```env
# Wajib diubah dengan kunci rahasia yang unik dan kuat
SECRET_KEY='ganti-dengan-secret-key-anda-yang-aman'

# Ubah ke False saat masuk ke lingkungan produksi
DEBUG=True

# Konfigurasi database (contoh untuk SQLite)
DATABASE_URL='sqlite:///db.sqlite3'

# Contoh untuk PostgreSQL:
# DATABASE_URL='postgres://user:password@host:port/dbname'
```

### 5. Jalankan Migrasi Database
Perintah ini akan membuat tabel-tabel yang dibutuhkan oleh aplikasi di database Anda.

```bash
python manage.py migrate
```

### 6. Buat Superuser (Admin)
Akun ini akan memiliki akses penuh ke Django Admin.

```bash
python manage.py createsuperuser
```

Ikuti petunjuk untuk membuat username, email, dan password.

### 7. Menjalankan Server
Setelah instalasi selesai, Anda dapat menjalankan server pengembangan lokal dengan perintah:

```bash
python manage.py runserver
```

Secara default, API akan dapat diakses di http://127.0.0.1:8000/.