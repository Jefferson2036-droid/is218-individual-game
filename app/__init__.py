"""Flask application factory for Arena Climb."""

import os

from dotenv import load_dotenv
from flask import Flask, redirect, session, url_for
from flask_login import current_user

from .extensions import csrf, db, login_manager
from .game.progression import rank_name, stars_needed
from .models import User
from .views.auth import auth_bp
from .views.play import play_bp
from .views.results import results_bp

load_dotenv()


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Base configuration
    secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production-123456789")
    database_url = os.environ.get("DATABASE_URL", "sqlite:///arena.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_TIME_LIMIT=None,
    )

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.sign_in"
    login_manager.login_message = "Please sign in to access this page."

    @login_manager.user_loader
    def load_user(user_id):
        user = db.session.get(User, int(user_id))
        if user is None:
            return None
        # Verify session auth_version matches user's auth_version
        if session.get("auth_version") != user.auth_version:
            return None
        return user

    # Context processors for Jinja templates
    @app.context_processor
    def utility_processor():
        return {
            "rank_name": rank_name,
            "stars_needed": stars_needed,
        }

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(results_bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("play.play_screen"))
        return redirect(url_for("auth.sign_in"))

    # Auto-create tables for local/dev environments
    with app.app_context():
        db.create_all()

    return app
