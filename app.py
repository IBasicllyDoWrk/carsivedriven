from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
import secrets
import sqlite3

from forms import RegistrationForm, LoginForm, CarForm, ProfileUpdateForm
from db import init_db, get_db

# Initialize app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# CSRF Protection
csrf = CSRFProtect(app)
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Secure session cookies
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=20)
)

# HTTPS security headers
Talisman(app, content_security_policy=None)

# Rate limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Initialize database
init_db()

# --- Routes ---

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        name = form.name.data
        age = form.age.data
        location = form.location.data

        try:
            with get_db() as db:
                db.execute(
                    "INSERT INTO users (username, password, name, age, location) VALUES (?, ?, ?, ?, ?)",
                    (username, password, name, age, location)
                )
                db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("100 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session.permanent = True
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@limiter.limit("30 per minute")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cars = db.execute("SELECT * FROM cars WHERE user_id = ?", (session["user_id"],)).fetchall()
    return render_template("dashboard.html", cars=cars)

@app.route("/add", methods=["GET", "POST"])
def add_car():
    if "user_id" not in session:
        return redirect(url_for("login"))
    form = CarForm()
    if form.validate_on_submit():
        data = (
            session["user_id"],
            form.make.data,
            form.model.data,
            form.model_year.data,
            form.engine.data,
            form.transmission.data
        )
        db = get_db()
        db.execute("INSERT INTO cars (user_id, make, model, model_year, engine, transmission) VALUES (?, ?, ?, ?, ?, ?)", data)
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_car.html", form=form)

@app.route("/edit/<int:car_id>", methods=["GET", "POST"])
def edit_car(car_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    car = db.execute("SELECT * FROM cars WHERE id = ? AND user_id = ?", (car_id, session["user_id"])).fetchone()
    if not car:
        flash("Car not found.", "error")
        return redirect(url_for("dashboard"))
    form = CarForm(data=car)
    if form.validate_on_submit():
        db.execute("""
            UPDATE cars 
            SET make=?, model=?, model_year=?, engine=?, transmission=?
            WHERE id=? AND user_id=?
        """, (
            form.make.data,
            form.model.data,
            form.model_year.data,
            form.engine.data,
            form.transmission.data,
            car_id,
            session["user_id"]
        ))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("edit_car.html", form=form, car_id=car_id)

@app.route("/delete/<int:car_id>", methods=["POST"])
def delete_car(car_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    db.execute("DELETE FROM cars WHERE id = ? AND user_id = ?", (car_id, session["user_id"]))
    db.commit()
    flash("Car deleted successfully", "success")
    return redirect(url_for("dashboard"))

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    with get_db() as db:
        user = db.execute(
            "SELECT username, name, age, location FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        total_cars = db.execute(
            "SELECT COUNT(*) FROM cars WHERE user_id = ?",
            (user_id,)
        ).fetchone()[0]
        newest_car = db.execute(
            "SELECT * FROM cars WHERE user_id = ? ORDER BY model_year DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        oldest_car = db.execute(
            "SELECT * FROM cars WHERE user_id = ? ORDER BY model_year ASC LIMIT 1",
            (user_id,)
        ).fetchone()

    return render_template("profile.html", user=user, total_cars=total_cars,
                           newest_car=newest_car, oldest_car=oldest_car)

@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    db = get_db()

    user = db.execute(
        "SELECT name, age, location FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    form = ProfileUpdateForm(data=user)

    if form.validate_on_submit():
        db.execute(
            "UPDATE users SET name = ?, age = ?, location = ? WHERE id = ?",
            (form.name.data, form.age.data, form.location.data, user_id)
        )
        db.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    return render_template("update_profile.html", form=form)

@app.route("/delete_profile", methods=["POST"])
def delete_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    db = get_db()
    user_id = session["user_id"]
    
    db.execute("DELETE FROM cars WHERE user_id = ?", (user_id,))
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    
    session.clear()
    flash("Your profile has been deleted.", "success")
    return redirect(url_for("register"))

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port=5000)
