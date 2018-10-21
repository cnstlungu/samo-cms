from flask import url_for

from samo.models import Role


def test_roles_create():
    assert set(['Admin', 'Contributor', 'User']).issubset(Role.query.all())


def test_app(app):
    assert app.name == 'samo.core'


def test_view_index(client):
    assert client.get(url_for('index')).status_code == 200


def test_view_about(client):
    assert client.get(url_for('about')).status_code == 200
