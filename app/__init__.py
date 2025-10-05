import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # base dir of this file (app/)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # absolute paths to project-level templates and static folders
    template_folder = os.path.abspath(os.path.join(BASE_DIR, '..', 'templates'))
    static_folder = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder
    )

    # config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join(BASE_DIR, '..', 'database', 'guess_game.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."

    # avoid circular imports by importing models and blueprints inside app context
    with app.app_context():
        from . import models  # noqa: F401

        # register blueprints
        from .routes.auth import auth_bp, home_bp  # import home_bp
        from .routes.game import game_bp
        from .routes.admin import admin_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)  # register home_bp for /home
        app.register_blueprint(game_bp)
        app.register_blueprint(admin_bp)

        # user loader for flask-login
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            try:
                return User.query.get(int(user_id))
            except Exception:
                return None

        # create DB tables if they don't exist
        db.create_all()

    return app
