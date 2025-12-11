"""
Flask Blog Database Models

This module defines the database models for the Flask blog application using SQLAlchemy ORM.

Models:
    - User: Represents a blog user with authentication and profile information
    - Post: Represents a blog post created by a user

The User model includes password reset token generation and verification functionality
using itsdangerous for secure token serialization.
"""

from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature
from flask_login import UserMixin
from flask import current_app
from flaskblog import db


class User(db.Model, UserMixin):
    """
    User model representing a blog user.

    Inherits from UserMixin which provides default implementations of user authentication
    properties required by Flask-Login (is_authenticated, is_active, is_anonymous, get_id).

    Attributes:
        id (int): Primary key, unique user identifier
        username (str): Unique username (max 20 characters)
        email (str): Unique email address (max 120 characters)
        image_file (str): Filename of user's profile picture (default: 'default.jpg')
        password (str): Hashed password (bcrypt, 60 characters)
        posts (relationship): One-to-many relationship with Post model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        """
        Generate a secure password reset token with expiration.

        Uses itsdangerous URLSafeTimedSerializer to create a time-limited token
        containing the user ID. Token is valid for 30 minutes (1800 seconds) by default.

        Args:
            expires_sec (int): Token expiration time in seconds (default: 1800)

        Returns:
            str: Encrypted token containing user ID

        Example:
            token = user.get_reset_token()
            # Send token via email link: /reset_password/<token>
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """
        Verify and decode a password reset token.

        Validates that the token is authentic and hasn't expired.
        Returns the User object if token is valid, None otherwise.

        Args:
            token (str): The encrypted token to verify
            expires_sec (int): Token expiration time in seconds (default: 1800)

        Returns:
            User or None: The User object if token is valid and not expired, None otherwise

        Example:
            user = User.verify_reset_token(token_from_url)
            if user:
                # Proceed with password reset
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """String representation of User object for debugging."""
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post model representing a blog post.

    Attributes:
        id (int): Primary key, unique post identifier
        title (str): Post title (max 100 characters)
        date_posted (datetime): Timestamp when post was created (UTC timezone-aware)
        content (str): Full post content/body
        user_id (int): Foreign key linking to User model (post author)
        author (relationship): Backref to User model via user_id ForeignKey
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """String representation of Post object for debugging."""
        return f"Post('{self.title}', '{self.date_posted}')"
