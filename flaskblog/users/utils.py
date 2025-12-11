"""
User Utility Functions

This module contains utility functions for user operations including:
- Profile picture handling (upload, resize, storage)
- Email notifications (password reset emails)
"""

import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    """
    Save and process user-uploaded profile picture.

    Generates a random filename to avoid conflicts, resizes the image to 200x200px,
    and saves it to the profile_pics directory.

    Args:
        form_picture (FileStorage): Picture file from form submission

    Returns:
        str: Filename of saved picture (random_hex.ext)

    Example:
        filename = save_picture(form.picture.data)
        user.image_file = filename
        db.session.commit()
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fname)

    # Resize the image before saving
    output_size = (200, 200)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fname


def send_reset_email(user):
    """
    Send password reset email to user.

    Generates a secure reset token, creates an email message with reset link,
    and sends it via configured SMTP server (Gmail).

    The email contains a unique token-based URL that expires after 30 minutes.

    Args:
        user (User): User object to send reset email to

    Returns:
        None

    Raises:
        Exception: If mail server is not configured or email fails to send

    Example:
        user = User.query.filter_by(email='user@example.com').first()
        send_reset_email(user)
    """
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    msg.body = f'''To reset your password, visit the following link:
                {url_for('users.reset_token', token=token, _external=True)}

                If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)