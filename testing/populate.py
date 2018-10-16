import datetime

from samo.core import db
from samo.models import User, Post, Tag, Comment, Role
from . import DUMMY_CONTENT


def load_dummy_data():
    """
    Populates the database with placeholder content for functional testing purposes.

    """

    db.create_all()

    admin_role = Role.query.filter(Role.name == 'Admin').first_or_404()
    contributor_role = Role.query.filter(Role.name == 'Contributor').first_or_404()
    userone = User(username="admin_testing", displayname="admin_testing", email="admin_testing@example.com",
                   password="admin", roles=[admin_role],
                   confirmed=True, confirmed_on=datetime.datetime.utcnow())
    usertwo = User(username="user_testing", displayname="user_testing", email="user_testing@example.com",
                   password="user", roles=[contributor_role], confirmed=True, confirmed_on=datetime.datetime.utcnow())

    db.session.add(userone)
    db.session.add(usertwo)

    db.session.commit()

    for x, i in enumerate(DUMMY_CONTENT):
        tag = Tag(name=i['lang_name'])
        db.session.add(tag)

        post = Post(content=i['content'] * 3, title=i['title'], user=usertwo, tags=[tag], publish=True)
        db.session.add(post)

        comment = Comment(comment_user=userone, content=i['comm_content'], post_id=x + 1)
        db.session.add(comment)

    db.session.commit()

    print('Populated the database with test data.')
