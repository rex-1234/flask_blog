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

    """Secret key for session management and CSRF token generation."""
    SECRET_KEY = os.environ.get('SECRET_KEY')

    """SQLAlchemy database connection URI."""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///site.db'
    )

    """SMTP server for sending emails (Gmail)."""
    MAIL_SERVER = 'smtp.googlemail.com'

    """SMTP port for TLS connection."""
    MAIL_PORT = 587

    """Enable TLS encryption for SMTP connection."""
    MAIL_USE_TLS = True

    """Email address for authentication with SMTP server."""
    MAIL_USERNAME = os.environ.get('EMAIL_USER')

    """App password for Gmail SMTP authentication."""
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
