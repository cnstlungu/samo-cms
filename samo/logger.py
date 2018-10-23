# pylint: disable-msg=C0103
"""
Provides the handler and logger necessary for piping the logs into the database.
"""

import logging
import traceback

from samo.core import db
from samo.models import Log


class SQLAlchemyHandler(logging.Handler):
    """
    Logging handler for SQLAlchemy
    """

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'], )
        db.session.add(log)
        db.session.commit()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = SQLAlchemyHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

loggers = [logger, logging.getLogger('werkzeug'), logging.getLogger('sqlalchemy'), \
           logging.getLogger('flask.app')]

for l in loggers:
    l.addHandler(ch)
