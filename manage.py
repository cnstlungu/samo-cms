# -*- coding: utf-8 -*-
import datetime
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool

from samo.core import app, db
from samo.models import Role, User

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('migrations', MigrateCommand)


@manager.command
def create_admin():
    """
    Creates the admin user.

    """
    if not User.query.filter(User.username == 'admin').first():
        admin_role = Role.query.filter(Role.name == 'Admin').first_or_404()
        userone = User(username="admin", displayname="Admin", email="admin@example.com",
                       password="admin", roles=[admin_role],
                       confirmed=True, confirmed_on=datetime.datetime.utcnow())
        db.session.add(userone)
        db.session.commit()
        print('Created the Admin user.')
    else:
        raise SystemError("Admin user already exists!")


@manager.command
def initdb():
    """
    Initializes all tables as per existing models.

    """

    db.create_all()
    print('Created all tables successfully.')


@manager.command
def dropdb():
    """

    Drops the current database.

    """

    if prompt_bool("Are you sure you want drop the entire database ?"):
        db.drop_all()
        print('Dropped the database')


@manager.command
def run_test_suite():
    """

    Runs a testsuite to verify app functionality.

    """

    db.drop_all()
    print('Dropped the database')
    db.create_all()
    print('Created all tables successfully.')

    from subprocess import call
    cur_dir = os.getcwd()
    call(["python", "-m", "unittest", f"{cur_dir}/testing/test.py"])





if __name__ == '__main__':
    manager.run()
