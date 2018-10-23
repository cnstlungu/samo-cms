# pylint: disable=no-member
"""
This sub-module controls the views to be served by the auth blueprint.
"""
import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from samo.core import db
from . import AUTH
from .confirmation_email import send_email
from .forms import LoginForm, SignupForm
from .token import generate_confirmation_token, confirm_token
from ..models import User, get_default_role, Post, Comment


@AUTH.route("/login", methods=["GET", "POST"])
def login():
    """
    Processes user login
    :return: renders template
    """
    form = LoginForm()
    if form.validate_on_submit():
        _user = User.get_by_username(form.username.data)
        if _user is not None and _user.check_password(form.password.data):
            login_user(_user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(_user.username), category='success')
            return redirect(request.args.get('next') or url_for('blog.author',
                                                                username=_user.username))
        flash('Incorrect username or password.', category='danger')
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
        _user = User(email=form.email.data,
                     username=form.username.data,
                     displayname=form.display_name.data,
                     password=form.password.data,
                     confirmed=False,
                     roles=[get_default_role()])
        db.session.add(_user)
        db.session.commit()

        token = generate_confirmation_token(_user.email)

        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"

        send_email.delay(recipients=_user.email, subject=subject, template=html)

        login_user(_user)

        flash('A confirmation email has been sent via email.', 'success')

        return redirect(url_for("auth.unconfirmed"))

    return render_template("auth/signup.html", form=form)


@login_required
@AUTH.route('/confirm/<token>')
def confirm_email(token):
    """
    Confirms the email sent for user verification, using the token provided
    :param token:
    :return: flask message depending on the outcome
    """
    try:
        email = confirm_token(token)
    except Exception:  # pylint: disable=broad-except
        flash('The confirmation link is invalid or has expired.', 'danger')
    _user = User.query.filter_by(email=email).first_or_404()
    if _user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        _user.confirmed = True
        _user.confirmed_on = datetime.datetime.utcnow()
        db.session.add(_user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))


@AUTH.route('/resend')
@login_required
def resend_confirmation():
    """
    Sends a confirmation email using an async task
    :return: renders a html template
    """
    if current_user.confirmed:
        flash('Your account is already confirmed!', 'warning')
        return redirect('index')
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email.delay(recipients=current_user.email, subject=subject, template=html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@AUTH.route('/unconfirmed')
@login_required
def unconfirmed():
    """
    A route for unconfirmed users
    :return: renders a html template
    """
    if current_user.confirmed:
        flash('Your account is already confirmed!', 'warning')
        return redirect('index')
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html')


@AUTH.route('/user/<username>')
def user(username):
    """
    Dispays a user personal profile. Some information (role, date joined) is only
    visible to the user, whereas other (posts, comments) is public
    :rtype: renders a html template
    """
    _user = User.query.filter_by(username=username).first_or_404()
    _posts = Post.query.filter(Post.user_id == _user.id).all()
    _comments = Comment.query.filter(Comment.user_id == _user.id).all()

    return render_template('auth/user.html', user=_user, posts=_posts, comments=_comments)
