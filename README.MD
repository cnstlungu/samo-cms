# Description

A simple CMS/blog in Flask

Samo-CMS is a learning-by-doing project, inspired by Reindert-Jan Ekker's course ["Introduction to the Flask Microframework"](https://github.com/gonzigonz/Pluralsight---Python-Flask-Apps) on [Pluralsight](https://www.pluralsight.com/courses/flask-micro-framework-introduction) and the boilerplate project I've built while following his course.

The application has basic blogging functionality, including
* Creating posts and assigning tags
* Commenting
* Authenticating to the portal
* Managing posts, users, comments and tags via an Admin Interface


## Requirements

### Python-related
See requirements file.

### Other
* Bootstrap 4
* [select2 library](https://select2.github.io/)


## Installation instructions

After installing the necessary Python packages, execute samo-cms/run.py.

Usage example: 

`python3 run.py`


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
`python3 manage.py initdb`
