"""
Flask-Login Authentication Module

This module configures Flask-Login for user authentication and session management.
It defines the login manager instance and the user loader callback required by Flask-Login.

This module is separate from __init__.py to avoid circular import issues since it depends
on the User model from models.py.
"""

from flask_login import LoginManager
from flaskblog.models import User

login_manager = LoginManager()
"""LoginManager instance for handling user authentication and sessions."""

login_manager.login_view = 'users.login'
"""Redirect to login page when unauthenticated user accesses protected route."""

login_manager.login_message_category = 'info'
"""Bootstrap alert category for login requirement messages (info, danger, success, etc)."""


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database by ID.

    This callback is required by Flask-Login. It's called to populate the
    current_user proxy object when a user session is active.

    Args:
        user_id (str): The user ID from the session, passed as string

    Returns:
        User or None: User object if found, None if user doesn't exist

    Note:
        user_id is passed as a string by Flask-Login and must be converted to int
        for database query.
    """
    return User.query.get(int(user_id))