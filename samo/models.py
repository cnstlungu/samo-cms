# pylint: disable=no-member,too-few-public-methods
"""
This module defines the Models for the Object used in the application.

"""
import re
from datetime import datetime

from flask_login import UserMixin
from flask_security import RoleMixin
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import observes
from werkzeug.security import check_password_hash, generate_password_hash

from samo.core import DB

TAGS = DB.Table('post_tag',
                DB.Column('tag_id', DB.Integer, DB.ForeignKey('tag.id')),
                DB.Column('post_id', DB.Integer, DB.ForeignKey('post.id')))

class Post(DB.Model):
    """
    Defines the Post object.
    """
    id = DB.Column(DB.Integer, primary_key=True)
    date = DB.Column(DB.DateTime, default=datetime.utcnow)
    title = DB.Column(DB.UnicodeText(140))
    slug = DB.Column(DB.UnicodeText(200))
    content = DB.Column(DB.UnicodeText())
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))
    tags = DB.relationship('Tag', secondary=TAGS, backref='posts')
    comments = DB.relationship('Comment', backref='posts', cascade="all, delete-orphan")
    publish = DB.Column(DB.Boolean)

    @observes('title')
    def compute_slug(self, title):
        """
        Computes the slug - shortened version of the title.
        :param title:  string, title to be shortened
        :return: string, resulting slug
        """
        self.slug = re.sub(r'[^\w]+', '-', title.lower())

    @staticmethod
    def newest(num):
        """
        Returns latest n posts.
        :param num: int, number of post to be returned.
        :return: n Post(s)
        """
        return Post.query.order_by(desc(Post.date)).limit(num)

    @property
    def ptags(self):
        """
        Returns a comma-separated list of available tags.
        :return:
        """
        return ",".join([t.name for t in self.tags])

    @ptags.setter
    def ptags(self, string):
        if string:

            self.tags = [Tag.get_or_create(name) for name in string.split(',')]

        else:
            self.tags = []

    def __repr__(self):
        return "<Post '{}': '{}'>".format(self.title, self.date)


class Tag(DB.Model):
    """
    Defines the Tag object.
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        """
        Gets or creates a tag with a given name.
        :param name: string, name of the tag to be found or created if it doesn't exist.
        :return:  Tag
        """
        try:
            return Tag.query.filter_by(name=name).one()
        except NoResultFound:
            return Tag(name=name)

    @staticmethod
    def all():
        """
        Returns all the tags.
        :return: Tag(s)
        """
        return Tag.query.all()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Comment(DB.Model):
    """
    Defines the Comment object.
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120))
    date = DB.Column(DB.DateTime, default=datetime.utcnow, nullable=False)
    email = DB.Column(DB.String(120))
    content = DB.Column(DB.UnicodeText())
    post_id = DB.Column(DB.Integer, DB.ForeignKey('post.id'), nullable=False)

    @staticmethod
    def all():
        """
        Returns all the comments.
        :return:
        """
        return Comment.query.all()

    def __str__(self):
        return self.name + ' : ' + self.content

    def __repr__(self):
        return self.name + ' : ' + self.content


roles_users = DB.Table('roles_users',
                       DB.Column('user_id', DB.Integer(), DB.ForeignKey('user.id')),
                       DB.Column('role_id', DB.Integer(), DB.ForeignKey('role.id')))

class User(DB.Model, UserMixin):
    """
    Defines the User object.
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(80), unique=True)
    displayname = DB.Column(DB.String(120), unique=True)
    email = DB.Column(DB.String(120), unique=True)
    posts = DB.relationship('Post', backref='user', lazy='dynamic')
    password_hash = DB.Column(DB.String(120))
    roles = DB.relationship('Role', secondary=roles_users,
                            backref=DB.backref('users', lazy='dynamic'))

    @property
    def password(self):
        """
        Raises an attribute error if password field is trying to be modified
        :return:
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """
        Sets the password
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks password hash
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        """
        Returns user by username.
        :param username: username to be retrieved
        :return: User
        """
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Role(DB.Model, RoleMixin):
    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(80), unique=True)
    description = DB.Column(DB.String(255))

    def __repr__(self):
        return "<Role '{}'>".format(self.name)

    def __str__(self):
        return self.name
