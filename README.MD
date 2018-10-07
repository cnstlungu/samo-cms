# Description

A simple CMS/blog in Flask

Samo-CMS is a project inspired by Reindert-Jan Ekker's course ["Introduction to the Flask Microframework"](https://github.com/gonzigonz/Pluralsight---Python-Flask-Apps) on [Pluralsight](https://www.pluralsight.com/courses/flask-micro-framework-introduction) and the boilerplate project I've built while following his course.

The application has basic blogging functionality, including
* Creating, editing and deleting blog posts
* Commenting
* Authenticating to the portal
* Managing posts, users, roles, comments and tags via an Admin Interface


## Requirements

#### Python-related
See requirements.txt file.

#### Other
* Bootstrap 4
* [select2 library](https://select2.github.io/)


## Installation instructions

1. Install the python packages found in requirements.txt. 
I strongly recommend that you set up a python [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) for your projects.

`pip install -r requirements.txt`

2. Create a config.ini file - use config.ini.example as a starting point.
A default configuration to get you started would be

[ENV]
* SAMO_ENV=dev
* HOST=localhost

[DB] #leave these blank to use SQLite
* SAMO_SERVER=your_server
* SAMO_DB=your_db
* SAMO_USER=your_user
* SAMO_PASS=your_password

3. Run the management commands as follows

`python manage.py initdb` this will initialize the database (create the database objects)

`python manage.py populate` this will populate the database with play data, including an admin user (please see management section below).

4. The final step would be starting the applycation by running

`python run.py`


## Management

The app is initialized with the following credentials, as seen in manage.py.

* username="admin",
* email="test@test.com"
* password="admin"

The samo-cms/manage.py file executes basic managing tasks, including:
* initdb - initializes the databases (SQLite by default)
* populate - populates tables with test data from [here](http://www.lipsum.com/)
* dropdb - DROPS all tables

Usage example: 
`python manage.py initdb`
