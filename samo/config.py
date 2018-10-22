# pylint: disable=too-few-public-methods
"""
This module defines the parameters and objects for the Deployment Environments.
"""

import configparser
import os


class ConfigReader():
    _config = None
    _source = None

    def __init__(self, source='env', filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')):
        self._source = source
        if self._source == 'file':
            self._config = configparser.ConfigParser()  # pylint: disable=invalid-name
            self._config.read(filename)
        elif self._source == 'env':
            pass
        else:
            raise NotImplementedError

    def get(self, key, environment):

        if self._source == 'file' and environment:
            try:
                return self._config.get(environment, key)
            except KeyError:
                pass
        elif self._source == 'env':
            return os.environ[key]


config = ConfigReader()

ENVIRONMENT = os.environ['FLASK_ENV']
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Defines the parent Config class.
    """
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = config.get('SAMO_CELERY_BROKER_URL', ENVIRONMENT)
    CELERY_RESULT_BACKEND = config.get('SAMO_CELERY_RESULT_BACKEND', ENVIRONMENT)
    MAIL_SENDGRID_API_KEY = config.get('SAMO_MAIL_SENDGRID_API_KEY', ENVIRONMENT)
    MAIL_DEFAULT_SENDER = config.get('SAMO_MAIL_DEFAULT_SENDER', ENVIRONMENT)
    SECURITY_PASSWORD_SALT = config.get('SAMO_SECURITY_PASSWORD_SALT', ENVIRONMENT)


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
    _dbtype = config.get('SAMO_DB_TYPE', ENVIRONMENT)
    _pass = config.get('SAMO_DB_PASS', ENVIRONMENT)
    _server = config.get('SAMO_DB_SERVER', ENVIRONMENT)
    _db = config.get('SAMO_DB_NAME', ENVIRONMENT)
    _user = config.get('SAMO_DB_USER', ENVIRONMENT)

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
    _dbtype = config.get('SAMO_DB_TYPE', ENVIRONMENT)
    _pass = config.get('SAMO_DB_PASS', ENVIRONMENT)
    _server = config.get('SAMO_DB_SERVER', ENVIRONMENT)
    _db = config.get('SAMO_DB_NAME', ENVIRONMENT)
    _user = config.get('SAMO_DB_USER', ENVIRONMENT)

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
