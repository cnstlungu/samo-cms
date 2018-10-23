from samo.config import CONFIG
from samo.core import app, ENVIRONMENT


if __name__ == '__main__':
    app.run(host=CONFIG.get('SAMO_HOST', ENVIRONMENT))
