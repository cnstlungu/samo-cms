"""
This module contains the core objects of the application:
the Flask (APP) object and the database object.
"""
from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_mail_sendgrid import MailSendGrid
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from samo.config import CONFIG_BY_NAME, ENVIRONMENT

APP = Flask(__name__)
APP.config.from_object('samo.config')
APP.config.from_object(CONFIG_BY_NAME[ENVIRONMENT])

csrf = CSRFProtect()
csrf.init_app(APP)

mail = MailSendGrid(APP)

celery = Celery(APP.import_name, broker=APP.config['CELERY_BROKER_URL'], backend=APP.config['CELERY_RESULT_BACKEND'])
celery.conf.update(APP.config)

DB = SQLAlchemy(APP)
DB.create_all()
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
LOGIN_MANAGER.session_protection = "strong"
LOGIN_MANAGER.login_view = "auth.login"
