# models.py
# Model database menggunakan SQLAlchemy.
# Setiap model adalah sebuah KELAS (konsep kelas & objek dari kursusmu),
# dan setiap baris di database adalah sebuah OBJEK dari kelas tersebut.

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Objek db dibuat di sini, lalu dihubungkan ke aplikasi di app.py
# (pola ini disebut "application factory", standar di Flask).
db = SQLAlchemy()


class User(db.Model):
    """Model untuk akun pengguna."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi: satu user punya banyak produk.
    # backref="owner" membuat kita bisa menulis product.owner untuk
    # mendapatkan user pemilik produk tersebut.
    products = db.relationship("Product", backref="owner", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Product(db.Model):
    """Model untuk barang di inventaris toko."""
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default="Umum")
    price = db.Column(db.Integer, nullable=False)      # harga dalam Rupiah
    stock = db.Column(db.Integer, nullable=False, default=0)

    # Foreign key: kolom yang menghubungkan ke tabel users.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.name}>"
