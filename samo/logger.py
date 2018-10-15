import logging
import traceback

from samo.core import db
from samo.models import Log


class SQLAlchemyHandler(logging.Handler):

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


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)

ch = SQLAlchemyHandler()  # pylint: disable=invalid-name
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # pylint: disable=invalid-name
ch.setFormatter(formatter)

loggers = [logger, logging.getLogger('werkzeug'), logging.getLogger('sqlalchemy'), \
           logging.getLogger('flask.app')]  # pylint: disable=invalid-name

for l in loggers:
    l.addHandler(ch)
