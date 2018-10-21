import os

import pytest
from splinter import Browser
from sqlalchemy.exc import OperationalError

from samo.core import app as flask_app
from samo.core import db
from samo.models import User, Post, Role

os.environ["PATH"] += ':' + r'/home/dev/assets/chromedriver_linux64'


@pytest.fixture
def app():
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="module", autouse=True)
def init_db():
    db.session.commit()
    try:
        db.drop_all()
    except OperationalError:
        pass
    db.create_all()


@pytest.fixture(scope="module", autouse=True)
def create_admin_user(init_db):
    role = Role.query.filter(Role.name == 'admin').first()
    user = User(username="test_admin", displayname="test_admin", email="test_admin@example.com", password="test",
                roles=[role])
    db.session.add(user)
    db.session.commit()
    return user
    db.session.delete()


@pytest.fixture(scope="module", autouse=True)
def create_contrib_user(init_db):
    role = Role.query.filter(Role.name == 'contributor').first()
    user = User(username="test_contrib", displayname="test_contrib", email="test_contributor@test.com", password="test",
                roles=[role])
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="module", autouse=True)
def create_post_edit(init_db, create_contrib_user):
    post = Post(title="DummyTitle02", content="Hello test", user=create_contrib_user, publish=True)
    db.session.add(post)
    db.session.commit()
    yield post


@pytest.fixture(scope="module", autouse=True)
def create_post_delete(init_db, create_contrib_user):
    post = Post(title="DummyTitle03", content="Hello test", user=create_contrib_user, publish=True)
    db.session.add(post)
    db.session.commit()
    yield post


@pytest.fixture()
def browser(init_db):
    browser = Browser('firefox', headless=False)
    yield browser
    browser.quit()
