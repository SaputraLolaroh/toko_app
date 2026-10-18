# Konfigurasi aplikasi Flask.
import os


def _database_url():
    # Integrasi Neon di Vercel dapat memakai salah satu nama variabel ini.
    url = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("POSTGRES_URL")
        or os.environ.get("NEON_DATABASE_URL")
    )

    if not url:
        return None

    # Paksa SQLAlchemy memakai psycopg2, yang disediakan oleh psycopg2-binary
    # di requirements.txt. Tanpa ini, SQLAlchemy bisa mencari driver psycopg v3.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # Neon menggunakan TLS; jangan menambahkan sslmode dua kali.
    if "sslmode=" not in url:
        url += "&sslmode=require" if "?" in url else "?sslmode=require"

    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "kunci-dev-lokal-ganti-ya")
    DATABASE_URL = _database_url()
    DATABASE_CONFIGURED = DATABASE_URL is not None

    # Gunakan SQLite hanya sebagai fallback agar proses build/import tidak gagal.
    # Di Vercel, app.py menolak request jika variabel Neon belum disetel.
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///toko.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True} if DATABASE_URL else {}

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("VERCEL") == "1"
