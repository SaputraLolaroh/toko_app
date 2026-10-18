# Inventaris Toko

Aplikasi web sederhana untuk mengelola stok dan data produk toko. Pengguna dapat membuat akun, masuk, lalu mengelola produk miliknya melalui dashboard.

## Fitur
- Registrasi, login, dan logout.
- Dashboard ringkas berisi statistik inventaris.
- Tambah, lihat, edit, hapus, dan cari produk.
- Database SQLite untuk penggunaan lokal dan PostgreSQL (Neon) untuk deployment.

## Teknologi
Python, Flask, SQLAlchemy, Bootstrap 5, dan PostgreSQL.

## Menjalankan secara lokal
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Di Windows, aktifkan lingkungan virtual dengan `venv\\Scripts\\activate`. Kemudian buka http://127.0.0.1:5000.

## Deployment
Aplikasi dapat di-deploy ke Vercel. Atur environment variables berikut pada pengaturan proyek:
- `SECRET_KEY`: kunci rahasia aplikasi.
- `DATABASE_URL`: connection string database PostgreSQL dari Neon.

Pastikan variabel lingkungan telah diatur sebelum menggunakan aplikasi di lingkungan produksi.
