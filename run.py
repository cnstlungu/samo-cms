from samo.core import APP as app
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()
if __name__ == '__main__':
    csrf.init_app(app)
    app.run()

