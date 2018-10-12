from samo.config import config
from samo.core import APP as app


if __name__ == '__main__':
    app.run(host=config['ENV']['HOST'])
