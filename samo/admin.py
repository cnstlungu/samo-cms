# pylint: disable=too-few-public-methods
"""
This module defines the admin interface of the web application.


"""

from flask import redirect, url_for
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_login import current_user

from samo.core import app, db
from samo.decorators import role_required
from samo.models import User, Post, Tag, Comment, Role


def is_admin(user):
    if user.is_authenticated:
        return 'Admin' in user.roles
    return False



class CustomAdminIndexView(AdminIndexView):
    """
    Creates the Custom admin Index View
    """


    @expose('/')
    @role_required(roles=['Admin'])
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super(CustomAdminIndexView, self).index()


ADMIN = Admin(app, index_view=CustomAdminIndexView(), template_mode='bootstrap3')


class PostAdmin(sqla.ModelView):
    """
    Defines the Post administration page
    """
    form_excluded_columns = ('slug',)
    form_columns = ('title', 'user', 'content', 'tags', 'publish', 'comments')
    column_list = ('title', 'date', 'user', 'tags', 'publish')
    column_searchable_list = ('title', 'content')

    def is_accessible(self):
        """
        Function to check if user has access to certain page
        :return: True if accessible, False if not
        """
        return is_admin(current_user)


ADMIN.add_view(PostAdmin(Post, db.session, name='Posts'))


class TagAdmin(sqla.ModelView):
    """
    Defines the Tag administration page
    """

    def is_accessible(self):
        """
        Function to check if user has access to certain page
        :return: True if accessible, False if not
        """
        return is_admin(current_user)


ADMIN.add_view(TagAdmin(Tag, db.session, name='Tags'))


class CommentAdmin(sqla.ModelView):
    """
    Defines the Comment administration page
    """
    column_list = ('comment_user', 'date', 'content', 'posts')
    form_columns = ('comment_user', 'date', 'content', 'posts')
    columns_searchable = ('content')

    def is_accessible(self):
        """
        Function to check if user has access to certain page
        :return: True if accessible, False if not
        """
        return is_admin(current_user)


ADMIN.add_view(CommentAdmin(Comment, db.session, name='Comments'))


class UserAdmin(sqla.ModelView):
    """
    Defines the Comment administration page
    """

    def is_accessible(self):
        """
        Function to check if user has access to certain page
        :return: True if accessible, False if not
        """
        return is_admin(current_user)

    column_labels = dict(displayname='Display Name', )
    form_excluded_columns = ('posts', 'comments')
    column_searchable_list = ('username', 'email', 'displayname')


ADMIN.add_view(UserAdmin(User, db.session, name='Users'))


class RoleAdmin(sqla.ModelView):
    """
    Defines the Comment administration page
    """

    def is_accessible(self):
        """
        Function to check if user has access to certain page
        :return: True if accessible, False if not
        """
        return is_admin(current_user)

    column_labels = dict(name='Name', )
    form_excluded_columns = ('users',)
    column_searchable_list = ('name', 'description')


ADMIN.add_view(RoleAdmin(Role, db.session, name='Roles'))

ADMIN.add_link(MenuLink(name='Back', url='/'))
