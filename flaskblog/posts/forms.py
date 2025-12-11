"""
Post-Related WTForms

This module defines Flask-WTF form class for blog post operations.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    Blog post creation/editing form.

    Fields:
        title: Required, post title (max determined by database field)
        content: Required, post content/body text
        submit: Submit button
    """

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
