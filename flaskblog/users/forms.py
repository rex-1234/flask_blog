"""
User-Related WTForms

This module defines Flask-WTF form classes for user-related operations:
registration, login, account updates, and password reset.

Each form includes built-in validation using WTForms validators.
Custom validators check for duplicate usernames/emails in the database.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegisterationForm(FlaskForm):
    """
    User registration form.

    Fields:
        username: Required, 2-20 characters, must be unique
        email: Required, valid email format, must be unique
        password: Required, must match confirm_password
        confirm_password: Required, must equal password field
        submit: Submit button
    """

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Custom validator to check if username already exists.

        Args:
            username: The username field from the form

        Raises:
            ValidationError: If username is already taken
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """
        Custom validator to check if email already exists.

        Args:
            email: The email field from the form

        Raises:
            ValidationError: If email is already registered
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    User login form.

    Fields:
        email: Required, valid email format
        password: Required
        remember: Optional checkbox to remember login across sessions
        submit: Submit button
    """

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    Account update form for changing username, email, and profile picture.

    Fields:
        username: Required, 2-20 characters, must be unique (unless same as current)
        email: Required, valid email format, must be unique (unless same as current)
        picture: Optional profile picture upload (jpg, png only)
        submit: Submit button
    """

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Update Info!')

    def validate_username(self, username):
        """
        Custom validator to check if new username already exists.

        Allows user to keep their current username without error.

        Args:
            username: The username field from the form

        Raises:
            ValidationError: If new username is already taken by another user
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """
        Custom validator to check if new email already exists.

        Allows user to keep their current email without error.

        Args:
            email: The email field from the form

        Raises:
            ValidationError: If new email is already registered to another user
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """
    Password reset request form.

    User enters their email to request a password reset link.
    Form validates that the email exists in the database.

    Fields:
        email: Required, valid email format, must exist in database
        submit: Submit button
    """

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """
        Custom validator to check if email exists in database.

        Args:
            email: The email field from the form

        Raises:
            ValidationError: If no user account exists with the given email
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """
    Password reset form.

    User sets a new password after clicking link from reset email.
    New password must match confirmation password.

    Fields:
        password: Required, new password
        confirm_password: Required, must match password
        submit: Submit button
    """

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset Password')
