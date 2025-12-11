"""
User Routes Module

This module defines Flask routes for user-related operations:
- Registration and account creation
- Login and logout
- Account management and profile updates
- User posts browsing
- Password reset functionality

All routes are registered under the 'users' blueprint.
"""

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (
    RegisterationForm, LoginForm, UpdateAccountForm,
    RequestResetForm, ResetPasswordForm
)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    User registration route.

    GET: Display registration form
    POST: Process registration form submission

    Creates a new user account with hashed password.
    Redirects authenticated users to home page.

    Returns:
        GET: Rendered registration form template
        POST: Redirect to login page on success, or re-render form with errors
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    User login route.

    GET: Display login form
    POST: Process login form submission

    Authenticates user credentials and creates session.
    Redirects authenticated users to home page.
    Supports 'remember me' functionality for persistent sessions.

    Returns:
        GET: Rendered login form template
        POST: Redirect to 'next' page (if specified) or home page on success
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """
    User logout route.

    Clears user session and redirects to login page.

    Returns:
        Redirect to login page
    """
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    User account management route.

    GET: Display account form with current user information
    POST: Update user account (username, email, profile picture)

    Requires: User must be logged in (@login_required)

    Returns:
        GET: Rendered account form with profile picture
        POST: Redirect to account page on success, or re-render form with errors
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    """
    Display all posts by a specific user.

    Shows paginated list of posts for the specified user.

    Args:
        username (str): Username to retrieve posts for

    Returns:
        Rendered user posts page with paginated posts

    Raises:
        404: If user doesn't exist
    """
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Password reset request route.

    GET: Display password reset request form
    POST: Send password reset email to user

    User enters email to receive reset link.
    Redirects authenticated users to home page.

    Returns:
        GET: Rendered password reset request form
        POST: Redirect to login page after sending email
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset the password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    Password reset via token route.

    GET: Display password reset form (if token is valid)
    POST: Process new password submission

    Verifies token before allowing password reset.
    Token expires after 30 minutes.

    Args:
        token (str): Password reset token from email link

    Returns:
        GET: Rendered password reset form (if token valid)
        POST: Redirect to login page on success

    Raises:
        Warning flash: If token is invalid or expired
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
