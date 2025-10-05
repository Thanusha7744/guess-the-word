import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Create instance folder (for DB)
    instance_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'instance'))
    os.makedirs(instance_path, exist_ok=True)

    # Create Flask app
    app = Flask(
        __name__,
        instance_path=instance_path,
        template_folder=os.path.abspath(os.path.join(BASE_DIR, '..', 'templates')),
        static_folder=os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))
    )

    # Secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

    # Database configuration (SQLite stored in instance folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'guess_game.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.game import game_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(admin_bp)

    # User loader
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app