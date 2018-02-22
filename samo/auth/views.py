# pylint: disable=no-member
"""
This sub-module controls the views to be served by the auth blueprint.
"""
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user

from samo.core import DB
from . import AUTH
from .forms import LoginForm, SignupForm
from ..models import User


@AUTH.route("/login", methods=["GET", "POST"])
def login():
    """
    Processes user login
    :return: renders template
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('blog.user',
                                                                username=user.username))
        flash('Incorrect username or password.')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("auth/login.html", form=form)


@AUTH.route("/logout")
def logout():
    """
    Logs out user
    :return: template, redirects to page
    """
    logout_user()
    return redirect(url_for('index'))


@AUTH.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Processes the signup form
    :return: renders template
    """
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        DB.session.add(user)
        DB.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('auth.login'))
    return render_template("auth/signup.html", form=form)
