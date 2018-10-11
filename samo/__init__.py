"""
This module contains the Flask Application.

"""
from flask_moment import Moment

from samo import logger
from samo import models
from samo import views
from . import admin
from .auth.core import AUTH
from .blog.core import BLOG
from .core import APP

MOMENT = Moment(APP)
APP.register_blueprint(AUTH, url_prefix='/auth')
APP.register_blueprint(BLOG, url_prefix='/blog')
