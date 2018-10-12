# pylint: disable=too-few-public-methods
"""
This module defines the parameters and objects for the Deployment Environments.
"""

import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

ENVIRONMENT = config['ENV']['SAMO_ENV']


class Config:
    """
    Defines the parent Config class.
    """
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = config['QUEUE']['CELERY_BROKER_URL']
    CELERY_RESULT_BACKEND = config['QUEUE']['CELERY_RESULT_BACKEND']
    MAIL_SENDGRID_API_KEY = config['MAIL']['MAIL_SENDGRID_API_KEY']


class DevelopmentConfig(Config):
    """
    Defines a Development Environment Configuration.
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')


class TestingConfig(Config):
    """
    Defines a Testing Environment Configuration.
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _pass = config['DB']['SAMO_PASS']
    _server = config['DB']['SAMO_SERVER']
    _db = config['DB']['SAMO_DB']
    _user = config['DB']['SAMO_USER']

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}?charset=utf8mb4'.format(_user, _pass, _server, _db)


class ProductionConfig(Config):
    """
    Defines a Production Environment Configuration.
    """
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _pass = config['DB']['SAMO_PASS']
    _server = config['DB']['SAMO_SERVER']
    _db = config['DB']['SAMO_DB']
    _user = config['DB']['SAMO_USER']

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(_user, _pass, _server, _db)


CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
