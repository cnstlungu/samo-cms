from samo.config import config
from samo.core import app, ENVIRONMENT


if __name__ == '__main__':
    app.run(host=config.get(ENVIRONMENT, 'HOST'))
