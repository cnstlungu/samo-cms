# -*- coding: utf-8 -*-

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool

from samo.core import APP, DB
from samo.models import User, Post, Tag, Comment, Role, roles_users
from testing import DUMMY_CONTENT

manager = Manager(APP)
migrate = Migrate(APP, DB)

manager.add_command('migrations', MigrateCommand)

os.environ["SAMO_ENV"] = "dev"


@manager.command
def populate():
    """
    Populates the database with placeholder content for functional testing purposes.

    """

    DB.create_all()

    roleone = Role(name='Admin', description='root user')
    roletwo = Role(name='Contributor', description='reqular user')
    userone = User(username="admin", displayname="admin", email="admin@test.com", password="admin")
    usertwo = User(username="user", displayname="user", email="user@test.com", password="user")

    DB.session.add(userone)
    DB.session.add(usertwo)
    DB.session.add(roleone)
    DB.session.add(roletwo)

    DB.session.commit()

    DB.session.execute(roles_users.insert().values([(1, 1), (2, 2)]))

    for x, i in enumerate(DUMMY_CONTENT):
        tag = Tag(name=i['lang_name'])
        DB.session.add(tag)

        post = Post(content=i['content'] * 3, title=i['title'], user=usertwo, tags=[tag], publish=True)
        DB.session.add(post)

        comment = Comment(name=i['name'], content=i['comm_content'], email='test'+str(x+1)+'@test.com', post_id=x + 1)
        DB.session.add(comment)

    DB.session.commit()

    print('Populated the database with test data.')


@manager.command
def initdb():
    """
    Initializez all tables as per existing model.

    """

    DB.create_all()
    print('Created all tables successfully.')


@manager.command
def dropdb():
    """

    Drops the current database.

    """

    if prompt_bool("Are you sure you want drop the entire database ?"):
        DB.drop_all()
        print('Dropped the database')


@manager.command
def run_test_suite():
    """

    Runs a testsuite to verify app functionality.

    """

    DB.drop_all()
    print('Dropped the database')
    DB.create_all()
    print('Created all tables successfully.')

    from subprocess import call
    cur_dir = os.getcwd()
    call(["python", "-m", "unittest", f"{cur_dir}/testing/test.py"])





if __name__ == '__main__':
    manager.run()
