"""
Main Routes Module

This module defines Flask routes for main application pages:
- Home page (blog post listing)
- About page

All routes are registered under the 'main' blueprint.
"""

from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """
    Home page route - displays paginated list of blog posts.

    Posts are ordered by creation date (newest first).
    Supports pagination via 'page' query parameter.

    Query Parameters:
        page (int): Page number (default: 1, max 10 posts per page)

    Returns:
        Rendered home page template with paginated posts
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    """
    About page route.

    Returns:
        Rendered about page template
    """
    return render_template("about.html", title='About Us')