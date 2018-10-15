"""
Provides decorators to be used throughout the app.
"""
from functools import wraps

from flask import flash, redirect, url_for, current_app
from flask_login import current_user


def check_confirmed(func):
    """
    A decorator to restrict access to a given view only to email-confirmed users.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def role_required(roles=None):
    """
    A decorator to restrict access to a given view only to users view a given role.
    """
    if not roles:
        roles = ['User', 'Admin', 'Contributor']

    def decorator(func):
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            if not set(current_user.roles).intersection(roles):
                flash('Unauthorized!', 'warning')
                return redirect(url_for('index'))
            return func(*args, **kwargs)

        decorated_view.__name__ = func.__name__

        return decorated_view

    return decorator
