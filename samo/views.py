# pylint: disable=unused-argument
"""
Handles views to be served by the app.

"""
from flask import render_template, request
from sqlalchemy import desc

from samo.blog.forms import SearchForm
from samo.core import app, login_manager, db
from samo.models import User, Post, Tag


@login_manager.user_loader
def load_user(user_id):
    """
    Gets user given a certain user_id
    :param user_id:
    :return: User
    """
    return User.query.get(int(user_id))


@app.route('/index', defaults={'page': 1})
@app.route("/page/<int:page>/", methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"], defaults={'page': 1})
def index(page):
    """
    Displays a given page or the index (first) page.

    :param page: page to display
    :return: html template
    """

    posts = Post.query.filter(Post.publish).order_by(desc(Post.date)).paginate(page, 3)

    search = SearchForm(request.form)

    if request.method == 'POST':

        term = search.data['search']

        results = Post.query.filter(Post.content.like(f'%{term}%')).order_by(desc(Post.date))

        return render_template('results.html', posts=results, postsearchform=search)

    return render_template('index.html', posts=posts, postsearchform=search)


@app.route('/about')
def about():
    """
    Renders the about page.

    :return: html template
    """

    search = SearchForm(request.form)

    return render_template('about.html', postsearchform=search)


@app.errorhandler(403)
def forbidden(error):
    """
    Renders 403 error.

    :return: html template
    """
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    """
    Renders 404 error.

    :return: html template
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Renders 500 error.

    :return: html template
    """
    return render_template('500.html'), 500


@app.context_processor
def inject_tags():
    """
    Makes all the tags available in JS.

    :return: void
    """

    return dict(all_tags=Tag.all, tag_stats=list(
        db.session.query(Tag.name, db.func.count(Post.id)).outerjoin(Post, Tag.posts). \
            group_by(Tag.name).having(db.func.count(Post.id) > 0). \
            order_by(db.func.count(Post.id).desc()).all()))
