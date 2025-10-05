from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, db
from ..utils import validate_username, validate_password

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)

# -----------------------------
# Registration Route
# -----------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))  # Redirect to home

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validation
        if not validate_username(username):
            flash("Username must be at least 5 letters (A-Z, a-z)")
            return render_template('register.html', username=username)
        if not validate_password(password):
            flash("Password must be at least 5 characters with letters, numbers and one of $ % * @")
            return render_template('register.html', username=username)

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return render_template('register.html', username=username)

        # Save user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# -----------------------------
# Login Route
# -----------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid password")  # Keep username filled
            return render_template('login.html', username=username)

        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for('home.dashboard'))

    return render_template('login.html')


# -----------------------------
# Logout Route
# -----------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))


# -----------------------------
# Home / Dashboard Route
# -----------------------------
@login_required
@home_bp.route('/home')
def dashboard():
    return render_template('home.html')

