from samo.config import config
from samo.core import app


if __name__ == '__main__':
    app.run(host=config['ENV']['HOST'])
