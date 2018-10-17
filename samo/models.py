# pylint: disable=no-member,too-few-public-methods
"""
This module defines the Models for the Object used in the application.

"""
import re
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import desc, event
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import observes
from werkzeug.security import check_password_hash, generate_password_hash

from samo.core import db

TAGS = db.Table('post_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Post(db.Model):
    """
    Defines the Post object.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.UnicodeText(140))
    slug = db.Column(db.UnicodeText(200))
    content = db.Column(db.UnicodeText())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=TAGS, backref='posts')
    comments = db.relationship('Comment', backref='posts', cascade="all, delete-orphan")
    publish = db.Column(db.Boolean)

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


class Tag(db.Model):
    """
    Defines the Tag object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

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


class Comment(db.Model):
    """
    Defines the Comment object.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    content = db.Column(db.UnicodeText())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    hidden = db.Column(db.Boolean, default=False)

    @staticmethod
    def all():
        """
        Returns all the comments.
        :return:
        """
        return Comment.query.all()

    def __str__(self):
        return self.comment_user.displayname + ' : ' + self.content

    def __repr__(self):
        return self.comment_user.displayname + ' : ' + self.content


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))  # pylint: disable=invalid-name


class User(db.Model, UserMixin):
    """
    Defines the User object.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    displayname = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment_user', lazy='dynamic')
    password_hash = db.Column(db.String(120))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

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


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role '{}'>".format(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __hash__(self):
        return hash(self.name)


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)  # auto incrementing
    logger = db.Column(db.String(100))  # the name of the logger. (e.g. myapp.views)
    level = db.Column(db.String(100))  # info, debug, or error?
    trace = db.Text(db.String(4096))  # the full traceback printout
    msg = db.Column(db.String(4096))  # any custom log you may have included
    created_at = db.Column(db.DateTime, default=db.func.now())  # the current timestamp

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])


@event.listens_for(Role.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):  # pylint: disable=unused-argument
    db.session.add(Role(name='Admin', description='admin'))
    db.session.add(Role(name='Contributor', description='contributor'))
    db.session.add(Role(name='User', description='regular user'))
    db.session.commit()


@db.event.listens_for(Role, "after_insert")
def get_default_role(*args, **kwargs):  # pylint: disable=unused-argument
    return Role.query.filter(Role.name == 'User').first_or_404()
