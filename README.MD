# Description

A simple CMS/blog in Flask

The application provides blogging functionality, including:
* Creating, editing and deleting blog posts
* Commenting
* Authenticating to the portal
* Managing posts, users, roles, comments and tags via an Admin Interface


## Requirements

#### Backend
For Python packages, please see the requirements.txt file.

#### Database
The development has been done with MySQL, but any database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/latest/core/engines.html)  should work with little or no adjustments.

#### Redis
The application requires Redis as its task queue.

#### Frontend
* Bootstrap 4
* [select2 library](https://select2.github.io/)


## Installation instructions

1. Install the python packages found in requirements.txt. 
I strongly recommend that you set up a python [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) for your projects.

`pip install -r requirements.txt`

2. Create a config.ini file - use config.ini.example as a starting point. Just fill in the required entries.

3. Run the management commands as follows

`python manage.py initdb` this will initialize the database (create the database objects)

*optional* `python manage.py populate` this will populate the database with play data, including an admin user (please see management section below).

4. Set an environment variable FLASK_ENV with the value of *development*

5. The final step would be starting the application by running

`python run.py`


## Management

The samo-cms/manage.py file executes basic managing tasks, including:
* initdb - initializes the databases (SQLite by default)
* create_admin - instantiates an admin user with the following credentials. Please remember to remove it as soon as the setup is complete. 
    * username="admin",
    * email="admin@example.com"
    * password="admin"
* dropdb - DROPS all tables

Usage example: 
`python manage.py initdb` &&
`python manage.py create_admin`

Also, the manage.py file is the interface to Flask-Migrate for database migrations. Commands should start with
`python manage.py migrations`, for example in order to establish an initial migration, run:
* `python manage.py migrations init`

## Credits

Samo-CMS started as a learning by doing project. The following resources, among others, proved of invaluable help:

* Reindert-Jan Ekker's course ["Introduction to the Flask Microframework"](https://github.com/gonzigonz/Pluralsight---Python-Flask-Apps) on [Pluralsight](https://www.pluralsight.com/courses/flask-micro-framework-introduction) and the boilerplate project I've built while following his course.
* Miguel Grinberg's excellent, [extensive tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) on Flask
* Realpython - great, detailed [instructions](https://realpython.com/handling-email-confirmation-in-flask/)
* Nick Janetakis' [blog](https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose)
