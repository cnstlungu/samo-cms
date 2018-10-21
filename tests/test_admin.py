from flask_login import login_user

from samo.admin import is_admin


def test_is_admin(create_admin_user, client):
    login_user(create_admin_user)
    assert is_admin(create_admin_user)
