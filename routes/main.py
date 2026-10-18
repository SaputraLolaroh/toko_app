# routes/main.py
# Rute utama: dashboard dan CRUD (Create, Read, Update, Delete) produk.

from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect, url_for, session, flash
)

from models import db, Product

# Blueprint untuk halaman-halaman utama (tanpa prefix).
main_bp = Blueprint("main", __name__)


def login_required(f):
    """
    DECORATOR: fungsi yang membungkus fungsi lain.
    Konsep ini mirip "fungsi sebagai variabel" dari kursusmu.
    Fungsinya: cek apakah user sudah login. Kalau belum, tendang ke halaman login.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


@main_bp.route("/")
@login_required
def dashboard():
    """Dashboard statistik inventaris milik user yang sedang login."""
    user_id = session["user_id"]

    # Ambil SEMUA produk milik user ini sebagai LIST of objek.
    products = Product.query.filter_by(user_id=user_id).all()

    # --- Statistik dengan list comprehension (dari kursusmu!) ---
    total_produk = len(products)
    total_nilai = sum([p.price * p.stock for p in products])  # nilai inventaris
    stok_menipis = [p for p in products if p.stock < 5]       # produk stok < 5
    kategori_unik = len(set([p.category for p in products]))  # set menghilangkan duplikat

    stats = {
        "total_produk": total_produk,
        "total_nilai": total_nilai,
        "stok_menipis": len(stok_menipis),
        "kategori": kategori_unik,
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        low_stock=stok_menipis,     # dikirim sebagai list ke template
        username=session["username"],
    )


# -------------------- CRUD PRODUK --------------------

@main_bp.route("/products")
@login_required
def product_list():
    """READ: tampilkan daftar produk, dengan fitur pencarian sederhana."""
    keyword = request.args.get("q", "").strip()
    query = Product.query.filter_by(user_id=session["user_id"])

    if keyword:
        # Filter: nama produk MENGANDUNG kata kunci (tidak harus sama persis).
        query = query.filter(Product.name.contains(keyword))

    products = query.order_by(Product.created_at.desc()).all()
    return render_template("products.html", products=products, keyword=keyword)


@main_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def product_add():
    """CREATE: tambah produk baru."""
    if request.method == "POST":
        # Ambil data dari form HTML.
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "Umum").strip() or "Umum"
        price = request.form.get("price", "0")
        stock = request.form.get("stock", "0")

        # Validasi & konversi tipe data (string dari form -> int).
        try:
            price = int(price)
            stock = int(stock)
            if price < 0 or stock < 0:
                raise ValueError("Harga dan stok tidak boleh negatif.")
            if not name:
                raise ValueError("Nama produk wajib diisi.")
        except ValueError as e:
            flash(f"Data tidak valid: {e}", "danger")
            return render_template("product_form.html", mode="add")

        product = Product(
            name=name, category=category,
            price=price, stock=stock,
            user_id=session["user_id"],
        )
        db.session.add(product)
        db.session.commit()
        flash("Produk berhasil ditambahkan.", "success")
        return redirect(url_for("main.product_list"))

    return render_template("product_form.html", mode="add")


@main_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def product_edit(product_id):
    """UPDATE: ubah data produk. <int:product_id> = ambil id dari URL."""
    # Ambil produk milik user ini. Kalau bukan miliknya -> 404 (aman).
    product = Product.query.filter_by(
        id=product_id, user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":
        try:
            product.name = request.form.get("name", "").strip()
            product.category = request.form.get("category", "Umum").strip() or "Umum"
            product.price = int(request.form.get("price", "0"))
            product.stock = int(request.form.get("stock", "0"))
            if not product.name:
                raise ValueError("Nama produk wajib diisi.")
            if product.price < 0 or product.stock < 0:
                raise ValueError("Harga dan stok tidak boleh negatif.")
        except ValueError as e:
            flash(f"Data tidak valid: {e}", "danger")
            return render_template("product_form.html", mode="edit", product=product)

        db.session.commit()
        flash("Produk berhasil diperbarui.", "success")
        return redirect(url_for("main.product_list"))

    return render_template("product_form.html", mode="edit", product=product)


@main_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def product_delete(product_id):
    """DELETE: hapus produk. Hanya menerima POST (lebih aman dari URL)."""
    product = Product.query.filter_by(
        id=product_id, user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(product)
    db.session.commit()
    flash("Produk berhasil dihapus.", "info")
    return redirect(url_for("main.product_list"))
