from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, db
from ..utils import validate_password
import re

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)

# -----------------------------
# Registration Route
# -----------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Username validation: letters + spaces, at least 5 letters ignoring spaces
        if len(re.sub(r'[^A-Za-z]', '', username)) < 5 or not re.match(r'^[A-Za-z ]+$', username):
            flash("Username must have at least 5 letters (A-Z, a-z) and can include spaces.", "error")
            return render_template('register.html', username=username)

        # Password validation
        if not validate_password(password):
            flash("Password must be at least 5 characters with letters, numbers and one of $ % * @", "error")
            return render_template('register.html', username=username)

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!", "error")
            return render_template('register.html', username=username)

        # Save user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html', username="")

# -----------------------------
# Login Route
# -----------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    username = ""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Invalid username", "error")
            username = ""  # clear username if invalid
        elif not check_password_hash(user.password_hash, password):
            flash("Invalid password", "error")
            # Keep username if it exists
        else:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home.dashboard'))

        # Always clear password field
        return render_template('login.html', username=username)

    return render_template('login.html', username="")

# -----------------------------
# Logout Route
# -----------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))

# -----------------------------
# Home / Dashboard Route
# -----------------------------
@login_required
@home_bp.route('/home')
def dashboard():
    return render_template('home.html')

# -----------------------------
# Landing Page Route
# -----------------------------
@home_bp.route('/')
def landing():
    if current_user.is_authenticated:
        # Show Start Game and Logout for logged-in users
        return render_template('landing.html', logged_in=True)
    else:
        # Show Login and Register for non-logged-in users
        return render_template('landing.html', logged_in=False)

