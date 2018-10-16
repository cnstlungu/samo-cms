# pylint: disable=no-member
"""
This sub-module controls the views to be served by the blog blueprint.
"""

from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user

from samo.core import db
from samo.decorators import role_required
from .core import BLOG
from .forms import PostForm, CommentForm, SearchForm
from ..models import User, Post, Tag, Comment


@BLOG.route('/add', methods=['GET', 'POST'])
@role_required(roles=['Admin', 'Contributor'])
def add():
    """
    Renders a template for adding a post.
    :return: renders a template
    """
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        ptags = form.ptags.data
        title = form.title.data
        _post = Post(user=current_user, content=content, title=title, ptags=ptags, publish=True)
        db.session.add(_post)
        db.session.commit()
        flash("Stored post '{}'".format(_post.title))
        return redirect(url_for('index'))

    search = SearchForm(request.form)

    return render_template('blog/post_form.html', form=form, title="Add a post", \
                           postsearchform=search)




@BLOG.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@role_required(roles=['Admin', 'Contributor'])
def edit_post(post_id):
    """
    Renders a template for editing an existing post, given its post id
    :param post_id: int, post id of the post to be edited
    :return: renders a template
    """
    post = Post.query.get_or_404(post_id)
    if current_user != post.user and 'Admin' not in current_user.roles:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.ptags = form.ptags.data
        db.session.commit()
        flash("Edited post '{}'".format(post.title))
        return redirect(url_for('blog.author', username=current_user.username))

    search = SearchForm(request.form)

    return render_template('blog/post_form.html', form=form, title="Edit post", \
                           postsearchform=search)




@BLOG.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@role_required(roles=['Admin', 'Contributor'])
def delete_post(post_id):
    """
    Deletes a post, given its postid
    :param post_id: int, post id of the post to be deleted
    :return: renders a confirmation template
    """
    post = Post.query.get_or_404(post_id)
    if current_user != post.user and 'Admin' not in current_user.roles:
        abort(403)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Deleted post '{}'".format(post.title))
        return redirect(url_for('blog.author', username=current_user.username))
    flash("Please confirm deleting the post.", category='warning')
    return render_template('blog/confirm_delete.html', post=post, nolinks=True)


@BLOG.route('/author/<username>')
def author(username):
    """
    Returns a page with all the posts created by a given user.
    :param username: string, author to be filtered for
    :return: renders a template
    """
    _user = User.query.filter_by(username=username).first_or_404()

    search = SearchForm(request.form)

    return render_template('blog/author.html', user=_user, postsearchform=search)


@BLOG.route('/tag/<name>')
def tag(name):
    """
    Returns a page with all the posts that contain a given tag.
    :param name: string, tag name to be viewed
    :return: renders a template.
    """
    _tag = Tag.query.filter_by(name=name).first_or_404()

    search = SearchForm(request.form)

    return render_template('blog/tag.html', tag=_tag, postsearchform=search)


@BLOG.route('/post/<slug>/', methods=['GET', 'POST'])
def detail(slug):
    """
    Displays a full page with a post, given its slug (short name)
    :param slug: string, shortened name name of a post
    :return: renders a template.
    """
    post = Post.query.filter_by(slug=slug).first_or_404()

    search = SearchForm(request.form)

    if current_user.is_authenticated:

        form = CommentForm()

        if form.validate_on_submit():
            content = form.content.data
            post_id = post.id
            user_id = current_user.id
            _comment = Comment(content=content, post_id=post_id, user_id=user_id)
            db.session.add(_comment)
            db.session.commit()
            flash("Your comment was added.")
            search = SearchForm(request.form)
            return render_template('blog/detail.html', post=post, form=form, postsearchform=search)

        return render_template('blog/detail.html', post=post, form=form, postsearchform=search)

    return render_template('blog/detail.html', post=post, postsearchform=search)
