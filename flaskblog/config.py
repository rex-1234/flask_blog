"""
Flask Blog Configuration Module

This module contains the configuration settings for the Flask blog application.
All configuration values are read from environment variables for security.

Configuration includes:
    - Database connection settings (SQLite)
    - Email/SMTP settings for password reset notifications (Gmail)
    - Secret key for session management and CSRF protection

Environment Variables Required:
    SECRET_KEY: Random secret key for session/CSRF (generate with secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI: Database URI (default: sqlite:///site.db)
    EMAIL_USER: Gmail address for sending password reset emails
    EMAIL_PASS: Gmail app password (not regular password due to 2FA)
"""

import os


class Config:
    """Application configuration settings loaded from environment variables."""

    SECRET_KEY = os.environ.get('SECRET_KEY')
    """Secret key for session management and CSRF token generation."""

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    """SQLAlchemy database connection URI."""

    MAIL_SERVER = 'smtp.googlemail.com'
    """SMTP server for sending emails (Gmail)."""

    MAIL_PORT = 587
    """SMTP port for TLS connection."""

    MAIL_USE_TLS = True
    """Enable TLS encryption for SMTP connection."""

    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    """Email address for authentication with SMTP server."""

    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    """App password for Gmail SMTP authentication."""