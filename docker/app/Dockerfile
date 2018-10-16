FROM python:3.6.6-jessie

RUN useradd -ms /bin/bash samo-cms

WORKDIR /home/repos/samo-cms

RUN apt-get update && apt-get -y install libmysqlclient-dev python-celery

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY samo samo
COPY migrations migrations
COPY manage.py run.py ./
COPY docker/app/entry.sh ./
RUN chmod +x entry.sh

ENV FLASK_APP samo

RUN chown -R samo-cms:samo-cms ./
USER samo-cms

EXPOSE 5000
ENTRYPOINT ["./entry.sh"]