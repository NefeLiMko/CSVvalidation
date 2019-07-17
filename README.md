# Chat_test
# Overview
Django chat

# Requirements

    Python 3.6.7
    celery==4.3.0
    Django==2.2.3
    rabbitmq-server
    postgresql


# Install
```
$ git clone https://github.com/NefeLiMko/CSVvalidation
```

# Usage

Example:
```
$ pip install pipenv
$ cd CSVvalidation
$ pipenv shell
$ pip install -r requirements.txt
$ cd CSVvalidation
  change settings.py for your user and database or create your databse and user as in example:
        'NAME': 'test',
        'USER' : 'nefelim',
        'PASSWORD' : 'password'
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

open the website and input
http://127.0.0.1:8000/
```
