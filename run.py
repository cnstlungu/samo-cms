from flask_wtf.csrf import CSRFProtect

from samo.config import config
from samo.core import APP as app

csrf = CSRFProtect()

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(host=config['ENV']['HOST'])
