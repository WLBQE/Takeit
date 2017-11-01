import os
basedir = os.path.abspath(os.path.dirname(__file__))

MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'password'
MYSQL_DATABASE_DB = 'TakeIt'
MYSQL_DATABASE_HOST = 'localhost'

TEST = True

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)
