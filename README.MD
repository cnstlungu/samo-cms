# Description
[![Build Status](https://travis-ci.org/cnstlungu/samo-cms.svg?branch=master)](https://travis-ci.org/cnstlungu/samo-cms)

<img src="http://flask.pocoo.org/static/logo/flask.svg" height="75px"/>

<img src="https://www.docker.com/sites/default/files/vertical.png" height="75px"/>

<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" height="75px"/>

<img src="http://download.redis.io/logocontest/82.png" height="75px"/>

<br>
<br>


A Flask CMS/blog 

The application provides blogging functionality, including:
* Creating, editing and deleting blog posts
* Commenting
* Authenticating to the portal
* Managing posts, users, roles, comments and tags via an Admin Interface


## Requirements

#### Platform
The application is designed to be run under Linux (built with Ubuntu 18.04 LTS). For Windows users, use the Docker deployment option or  adjust the steps from source accordingly.

#### Backend
For  required Python packages, please see the [requirements.txt](requirements.txt) file.

#### Database
The testing has been done with [MySQL](https://www.mysql.com/), but any database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/latest/core/engines.html)  should work with little to no adjustments.

#### Redis
The application requires [Redis](https://redis.io) as its task queue.

#### Frontend
* [Bootstrap 4](https://getbootstrap.com/)
* [select2 library](https://select2.github.io/)

## Installation instructions

### Option A: Docker (pick this if you're using Windows)

1. Ensure you have [docker CE](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/) installed.

2. Change directory to the folder containing the source
`cd samo-cms`

3. Set up the environment variables mentioned in *dockerfile-compose.yml. 

Run the following command to compose the docker containers

`docker-compose up`

4. The application will be available at [http://localhost:8000](http://localhost:8000)


### Option B: From Source

1. Install the python packages found in requirements.txt. 
I strongly recommend that you set up a python [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) for your projects.

`pip install -r requirements.txt`

2. Set up Redis

For a quick an easy set-up, use Docker as follows:

`docker pull redis:latest`

`docker run --name redis -p 6379:6379 --network samo-network -d redis`, assuming a [bridge network](https://docs.docker.com/network/bridge/#differences-between-user-defined-bridges-and-the-default-bridge) samo-network has been created


3. Set up a MySQL server. 

Again, for a quick set-up, use Docker as follows:

`docker pull mysql:latest`

`docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=$SAMO_DB_PASS -d mysql:latest`

Create a database named 'samo'.


4. Configure the environment variables as follows:
* FLASK_ENV=development
* all the environment variables mentioned in config.ini.example 

5. Run the management commands as follows

`python manage.py initdb` this will initialize the database (create the database objects)

`python manage.py create_admin` this will create an admin user with the following credentials. Please remember to remove it as soon as the setup is complete. 
    * username="admin",
    * email="admin@example.com"
    * password="admin"

6. Run the Celery Worker

        cd ./samo-cms/
        source venv/bin/activate
        celery worker -A samo.core.celery --loglevel=info


6. The final step would be starting the application by running

`python run.py`


## Management

The samo-cms/manage.py file executes basic managing tasks, including:
* initdb - initializes the databases
* create_admin - creates an admin user with the following credentials. Please remember to remove it as soon as the setup is complete. 
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

Samo-CMS started as a learning by doing project. The following resources, among others, proved of great help:

* Reindert-Jan Ekker's course ["Introduction to the Flask Microframework"](https://github.com/gonzigonz/Pluralsight---Python-Flask-Apps) on [Pluralsight](https://www.pluralsight.com/courses/flask-micro-framework-introduction) and the boilerplate project I've built while following his course.
* Miguel Grinberg's excellent, [extensive tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) on Flask
* Realpython - great, detailed [instructions](https://realpython.com/handling-email-confirmation-in-flask/)
* Nick Janetakis' [blog](https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose)
