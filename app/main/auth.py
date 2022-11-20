""" Auth declaration
    Includes many helpful functions for authenticate the user
    Refer to https://flask.palletsprojects.com/en/2.2.x/tutorial/views/ for usage
"""
from functools import wraps
from flask import request, redirect, url_for, session


def login_required(f):
    """Use on routes to prevent the user from accessing them unless they are logged in"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("username", None)
        if user is None:
            return redirect(url_for(".login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Use on routes to prevent the user from accessing them unless they are granted admin priveleges dev only"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_admin = session.get("admin", None)
        if is_admin is None:
            return redirect(url_for(".login"))
        return f(*args, **kwargs)

    return decorated_function
