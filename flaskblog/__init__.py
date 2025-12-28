"""
Flask Blog Application Factory

This module implements the application factory pattern for creating and configuring
the Flask blog application. It initializes all extensions (SQLAlchemy, Bcrypt, Mail, LoginManager)
and registers blueprints for different modules (users, posts, main, errors).

The create_app function should be called from run.py to instantiate the application.

Modules:
    - config: Configuration settings
    - auth: Authentication setup with Flask-Login
    - users.routes: User registration, login, account management
    - posts.routes: Post creation, editing, deletion
    - main.routes: Main pages (home, about)
    - errors.handlers: Error page handlers
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
"""SQLAlchemy ORM instance for database operations."""

bcrypt = Bcrypt()
"""Bcrypt instance for password hashing."""

mail = Mail()
"""Flask-Mail instance for sending emails (password reset notifications)."""


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    This factory function creates a Flask app instance, initializes all extensions,
    registers blueprints, and sets up Flask-Login user loader.

    The function uses the factory pattern to allow creation of multiple app instances
    with different configurations (useful for testing).

    Args:
        config_class: Configuration class to use (default: Config from config.py)

    Returns:
        Flask: Configured Flask application instance

    Example:
        app = create_app()
        app.run(debug=True)
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Import and init login manager
    from flaskblog.auth import login_manager
    login_manager.init_app(app)

    # Register blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app