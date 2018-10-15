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
from .core import app

MOMENT = Moment(app)
app.register_blueprint(AUTH, url_prefix='/auth')
app.register_blueprint(BLOG, url_prefix='/blog')
