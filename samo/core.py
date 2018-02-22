"""
This module contains the core objects of the application:
the Flask (APP) object and the database object.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from samo.config import CONFIG_BY_NAME, ENVIRONMENT

APP = Flask(__name__)
APP.config.from_object('samo.config')
APP.config.from_object(CONFIG_BY_NAME[ENVIRONMENT])

DB = SQLAlchemy(APP)
DB.create_all()
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
LOGIN_MANAGER.session_protection = "strong"
LOGIN_MANAGER.login_view = "auth.login"
