"""
Post Routes Module

This module defines Flask routes for blog post operations:
- Creating new posts
- Viewing individual posts
- Updating existing posts
- Deleting posts

All routes are registered under the 'posts' blueprint.
Some routes require user authentication (@login_required).
"""

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Create a new blog post route.

    GET: Display post creation form
    POST: Save new post to database

    Requires: User must be logged in (@login_required)

    Returns:
        GET: Rendered post creation form
        POST: Redirect to home page on success
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)


@posts.route("/post/<post_id>")
def post(post_id):
    """
    View a specific blog post.

    Args:
        post_id (int): ID of post to display

    Returns:
        Rendered post view template

    Raises:
        404: If post doesn't exist
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    Update an existing blog post.

    GET: Display post edit form with current post data
    POST: Save changes to post

    Requires: User must be logged in (@login_required)
    Requires: Current user must be post author (checked via abort(403))

    Args:
        post_id (int): ID of post to update

    Returns:
        GET: Rendered post edit form
        POST: Redirect to post view page on success

    Raises:
        403: If current user is not the post author
        404: If post doesn't exist
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, post=post)


@posts.route("/post/<post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Delete a blog post.

    POST-only route for security (prevents accidental deletion via GET).

    Requires: User must be logged in (@login_required)
    Requires: Current user must be post author (checked via abort(403))

    Args:
        post_id (int): ID of post to delete

    Returns:
        Redirect to home page after deletion

    Raises:
        403: If current user is not the post author
        404: If post doesn't exist
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
