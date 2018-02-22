# pylint: disable=unused-argument
"""
Handles views to be served by the app.

"""
from flask import render_template
from sqlalchemy import desc
from samo.core import APP, LOGIN_MANAGER
from samo.models import User, Post, Tag


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """
    Gets user given a certain user_id
    :param user_id:
    :return: User
    """
    return User.query.get(int(user_id))


@APP.route('/index', defaults={'page': 1})
@APP.route("/page/<int:page>/", methods=["GET", "POST"])
@APP.route('/', defaults={'page': 1})
def index(page):
    """
    Displays a given page or the index (first) page.

    :param page: page to display
    :return: html template
    """

    posts = Post.query.filter(Post.publish).order_by(desc(Post.date)).paginate(page, 3)
    return render_template('index.html', posts=posts)


@APP.route('/about')
def about():
    """
    Renders the about page.

    :return: html template
    """
    return render_template('about.html')


@APP.errorhandler(403)
def forbidden(error):
    """
    Renders 403 error.

    :return: html template
    """
    return render_template('403.html'), 403


@APP.errorhandler(404)
def page_not_found(error):
    """
    Renders 404 error.

    :return: html template
    """
    return render_template('404.html'), 404


@APP.errorhandler(500)
def internal_server_error(error):
    """
    Renders 500 error.

    :return: html template
    """
    return render_template('500.html'), 500


@APP.context_processor
def inject_tags():
    """
    Makes all the tags available in JS.

    :return: void
    """

    return dict(all_tags=Tag.all)
