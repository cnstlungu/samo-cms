"""
This module contains the core objects of the application:
the Flask (app) object and the database object.
"""
from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_mail_sendgrid import MailSendGrid
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from samo.config import CONFIG_BY_NAME, ENVIRONMENT

app = Flask(__name__)  # pylint: disable=invalid-name
app.config.from_object('samo.config')
app.config.from_object(CONFIG_BY_NAME[ENVIRONMENT])


@app.template_filter('intersect')
def intersect(a, b):
    return set(a).intersection(b)

csrf = CSRFProtect()  # pylint: disable=invalid-name
csrf.init_app(app)

mail = MailSendGrid(app)  # pylint: disable=invalid-name

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], \
                backend=app.config['CELERY_RESULT_BACKEND'])  # pylint: disable=invalid-name
celery.conf.update(app.config)

db = SQLAlchemy(app)  # pylint: disable=invalid-name
db.create_all()
login_manager = LoginManager()  # pylint: disable=invalid-name
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
