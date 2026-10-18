# app.py
# FILE UTAMA: pabrik aplikasi (application factory).

import os
from flask import Flask

from config import Config
from models import db
from routes.auth import auth_bp
from routes.main import main_bp


def create_app():
    """Fungsi yang membuat dan mengatur objek aplikasi Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Jangan biarkan variabel Neon yang belum disetel membuat proses import/build gagal.
    # Pada Vercel, tampilkan pesan yang jelas saat ada request, bukan memakai SQLite diam-diam.
    @app.before_request
    def require_production_database():
        if os.environ.get("VERCEL") == "1" and not app.config.get("DATABASE_CONFIGURED"):
            return (
                "Konfigurasi database belum tersedia. Tambahkan DATABASE_URL "
                "(connection string PostgreSQL Neon) di Vercel > Settings > Environment Variables.",
                503,
            )
        return None

    # Membuat tabel bila database tersedia. Kegagalan koneksi tidak boleh mematikan import;
    # periksa Runtime Logs jika tabel tidak dapat dibuat.
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            db.session.rollback()
            app.logger.exception("Gagal membuat tabel database saat inisialisasi.")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
