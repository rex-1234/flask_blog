"""
Error Handlers Module

This module defines error handlers for common HTTP errors:
- 404 Not Found
- 403 Forbidden
- 500 Internal Server Error

All handlers are registered under the 'errors' blueprint using @app_errorhandler
which makes them apply to the entire Flask application.
"""

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    Handle 404 Not Found errors.

    Args:
        error: The exception object from Flask

    Returns:
        Tuple of (rendered error page, HTTP status code 404)
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    Handle 403 Forbidden errors.

    Typically raised when user tries to access/modify a resource they don't own.

    Args:
        error: The exception object from Flask

    Returns:
        Tuple of (rendered error page, HTTP status code 403)
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """
    Handle 500 Internal Server Error.

    Generic error handler for unexpected server errors.

    Args:
        error: The exception object from Flask

    Returns:
        Tuple of (rendered error page, HTTP status code 500)
    """
    return render_template('errors/500.html'), 500
