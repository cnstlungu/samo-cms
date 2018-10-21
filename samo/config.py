# pylint: disable=too-few-public-methods
"""
This module defines the parameters and objects for the Deployment Environments.
"""

import configparser
import os

config = configparser.ConfigParser()  # pylint: disable=invalid-name
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

ENVIRONMENT = os.environ['FLASK_ENV']
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Defines the parent Config class.
    """
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = config.get(ENVIRONMENT, 'CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = config.get(ENVIRONMENT, 'CELERY_RESULT_BACKEND')
    MAIL_SENDGRID_API_KEY = config.get(ENVIRONMENT, 'MAIL_SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = config.get(ENVIRONMENT, 'MAIL_DEFAULT_SENDER')
    SECURITY_PASSWORD_SALT = config.get(ENVIRONMENT, 'SECURITY_PASSWORD_SALT')


class NoDBDevelopmentConfig(Config):
    """
    Defines a Development Environment Configuration.
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')


class DevelopmentConfig(Config):
    """
    Defines a Testing Environment Configuration.
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _dbtype = config.get(ENVIRONMENT, 'DB_TYPE')
    _pass = config.get(ENVIRONMENT, 'DB_PASS')
    _server = config.get(ENVIRONMENT, 'DB_SERVER')
    _db = config.get(ENVIRONMENT, 'DB_NAME')
    _user = config.get(ENVIRONMENT, 'DB_USER')

    SQLALCHEMY_DATABASE_URI = None

    if _dbtype == 'mysql':
        SQLALCHEMY_DATABASE_URI = f'mysql://{_user}:{_pass}@{_server}/{_db}?charset=utf8mb4'
    elif _dbtype == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')
    else:
        SQLALCHEMY_DATABASE_URI = f'{_dbtype}://{_user}:{_pass}@{_server}/{_db}'


class DockerTestingConfig(Config):
    """
    Defines a Docker Testing Environment Configuration.
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    _dbtype = config.get(ENVIRONMENT, 'DB_TYPE')
    _pass = config.get(ENVIRONMENT, 'DB_PASS')
    _server = config.get(ENVIRONMENT, 'DB_SERVER')
    _db = config.get(ENVIRONMENT, 'DB_NAME')
    _user = config.get(ENVIRONMENT, 'DB_USER')

    SQLALCHEMY_DATABASE_URI = None

    if _dbtype == 'mysql':
        SQLALCHEMY_DATABASE_URI = f'mysql://{_user}:{_pass}@{_server}/{_db}?charset=utf8mb4'
    elif _dbtype == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')
    else:
        SQLALCHEMY_DATABASE_URI = f'{_dbtype}://{_user}:{_pass}@{_server}/{_db}'


CONFIG_BY_NAME = dict(
    development=DevelopmentConfig,
    dockertesting=DockerTestingConfig,
    nodb=NoDBDevelopmentConfig
)
