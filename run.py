from samo.core import APP as app
from flask_wtf.csrf import CSRFProtect
from samo.config import config
import logging
import os

logging.basicConfig(filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.log'), level=logging.DEBUG)

csrf = CSRFProtect()

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(host=config['ENV']['HOST'])
