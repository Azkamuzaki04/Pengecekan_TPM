# CHECKSIT Welding HMMI

Sistem inspeksi welding dengan 3 role dan 2 platform utama:

- **Petugas/User** → APK mobile
- **Admin** → Web Dashboard
- **Server** → Web Dashboard Monitoring

## Hirarki sistem

Server berada di tingkat paling atas sebagai pengelola/monitoring sistem. Admin berada di bawah Server dan mengelola operasional inspeksi. Petugas/User berada di bawah Admin dan menjalankan inspeksi melalui APK.

```text
SERVER
  │
  └── ADMIN
        │
        └── PETUGAS / USER
```

Secara teknis semua terhubung melalui Django Backend/API dan database MySQL dari XAMPP.

```text
                MySQL XAMPP
                    ▲
                    │
             Django Backend/API
                    ▲
             ┌──────┴──────┐
             │             │
          Web Admin    Web Server
             ▲
             │
          APK User
```

## Struktur

- `accounts/` login + role
- `barang/` master barang + item pemeriksaan
- `inspection/` pemeriksaan, foto NG, approval, histori
- `reports/` laporan + export Excel
- `server/` dashboard monitoring server
- `api/` API untuk APK Flutter
- `mobile_app/` source Flutter APK petugas
- `media/` gambar barang, referensi pemeriksaan, dan foto NG
- `static/` asset UI dan logo Hino

## DATABASE XAMPP / phpMyAdmin

Project menggunakan **MySQL/MariaDB XAMPP**, bukan database SQLite.

### 1. Jalankan XAMPP

Buka XAMPP Control Panel lalu hidupkan:

- **Apache**
- **MySQL**

### 2. Buat database

Buka phpMyAdmin:

`http://localhost/phpmyadmin/`

Pilih **New / Baru**, lalu buat database:

`checksit`

Collation yang disarankan:

`utf8mb4_unicode_ci`

**Jangan membuat tabel secara manual.** Django akan membuat tabel melalui migration.

### 3. Pengaturan koneksi

File:

`config/settings.py`

Bagian database:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "checksit",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

Konfigurasi di atas cocok untuk instalasi XAMPP standar yang user MySQL-nya `root` dan password-nya kosong.

Jika MySQL XAMPP Anda memakai password, ubah:

```python
"PASSWORD": "password_mysql_anda",
```

Jika port MySQL bukan 3306, ubah nilai `PORT` sesuai port di XAMPP.

### 4. Install dependency

Di terminal VS Code pada folder project:

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

### 5. Cek koneksi database

```bash
python manage.py check
```

Kemudian:

```bash
python manage.py migrate
```

Jika berhasil, tabel Django akan muncul otomatis di phpMyAdmin pada database `checksit`.

### 6. Buat akun admin

```bash
python manage.py createsuperuser
```

Lalu jalankan:

```bash
python manage.py setup_roles --password "GantiPassword!"
```

Command tersebut membuat contoh role jika akun belum ada:

- `petugas` → PETUGAS
- `admin_checksit` → ADMIN
- `server_checksit` → SERVER

Ganti password sebelum digunakan.

### 7. Jalankan web

```bash
python manage.py runserver
```

Buka:

`http://127.0.0.1:8000/`

## Jika memakai database lama

**Jangan hapus database lama.** Backup database terlebih dahulu, lalu jalankan:

```bash
python manage.py migrate
```

Migration menambahkan kebutuhan baru tanpa harus melakukan `DROP DATABASE`.

Model `Parameter` tetap dipertahankan untuk kompatibilitas database, tetapi di UI istilahnya digunakan sebagai **Item Pemeriksaan**.

Hubungan data:

```text
Barang
  └── Item Pemeriksaan (model database: Parameter)
        └── Hasil Inspeksi
```

## Gambar

- Gambar master barang → `media/barang/`
- Foto referensi item pemeriksaan → `media/parameter_reference/`
- Foto bukti NG → `media/inspection/YYYY/MM/DD/`

Database hanya menyimpan path/referensi file gambar.

## API APK

- `POST /api/auth/token/`
- `GET /api/barang/<barcode>/`
- `POST /api/inspections/`

Setelah token dibuat, APK menggunakan header:

`Authorization: Token <token>`

## Laporan Excel

Admin dapat memfilter laporan dan mengunduh file `.xlsx`. File memiliki sheet `Laporan` dan `Detail Pemeriksaan`.
