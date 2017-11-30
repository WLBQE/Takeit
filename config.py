import os
basedir = os.path.abspath(os.path.dirname(__file__))

MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'password'
MYSQL_DATABASE_DB = 'TakeIt'
MYSQL_DATABASE_HOST = 'localhost'

EVENT_PICTURE = os.path.join(basedir, 'app/static/event_picture')
USER_PICTURE = os.path.join(basedir, 'app/static/user_picture')
DEFAULT_USER_PIC = os.path.join(USER_PICTURE, 'default_avatar.png')
DEFAULT_EVENT_PIC = os.path.join(EVENT_PICTURE, 'default_cover_picture.png')

TEST = True

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)
