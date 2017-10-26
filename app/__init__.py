from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

db = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'TakeIt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db.init_app(app)

from app import views, models
