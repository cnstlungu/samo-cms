"""
This module contains the Flask Application.

"""
from flask_moment import Moment
from samo import models
from samo import views
from .core import APP
from .auth.core import AUTH
from .blog.core import BLOG
from . import admin

MOMENT = Moment(APP)
APP.register_blueprint(AUTH, url_prefix='/auth')
APP.register_blueprint(BLOG, url_prefix='/blog')
