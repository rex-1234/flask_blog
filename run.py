"""
Flask Blog Application Entry Point

This module initializes and runs the Flask blog application.
It creates the Flask app instance using the application factory pattern
and starts the development server with debug mode enabled.

Environment Variables:
    SECRET_KEY: Secret key for session management and CSRF protection
    SQLALCHEMY_DATABASE_URI: Database connection URI
    EMAIL_USER: Email account for password reset notifications
    EMAIL_PASS: Email account password/app password

Usage:
    python run.py
    or
    uv run run.py
"""

from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)