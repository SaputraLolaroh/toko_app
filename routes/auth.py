# routes/auth.py
# Semua rute terkait autentikasi: register, login, logout.
# Blueprint adalah cara Flask mengelompokkan rute ke dalam MODUL terpisah.

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

# Membuat Blueprint bernama "auth".
# url_prefix="/auth" artinya semua rute di file ini diawali /auth/...
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Halaman registrasi. GET = tampilkan form, POST = proses form."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        # --- Validasi input (alurnya sama seperti if/else di kursusmu) ---
        error = None
        if not username or not password:
            error = "Username dan password wajib diisi."
        elif len(password) < 6:
            error = "Password minimal 6 karakter."
        elif password != confirm:
            error = "Konfirmasi password tidak sama."
        elif User.query.filter_by(username=username).first() is not None:
            error = "Username sudah dipakai, coba yang lain."

        if error is None:
            try:
                # Password tidak pernah disimpan apa adanya (plaintext),
                # melainkan di-hash terlebih dahulu.
                user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                )
                db.session.add(user)
                db.session.commit()
                flash("Registrasi berhasil! Silakan login.", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                # Error handling: kalau ada masalah di database, batalkan.
                db.session.rollback()
                flash(f"Terjadi kesalahan: {e}", "danger")
        else:
            flash(error, "danger")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Halaman login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        # Cek apakah user ada DAN password cocok dengan hash-nya.
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Username atau password salah.", "danger")
        else:
            # Simpan id user di session (dictionary khusus milik Flask
            # yang diingat oleh browser). Inilah "status login"-nya.
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Selamat datang, {user.username}!", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Keluar: hapus data session."""
    session.clear()
    flash("Kamu sudah logout.", "info")
    return redirect(url_for("auth.login"))
