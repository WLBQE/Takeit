from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

db = MySQL()
db.init_app(app)

from app import views, models
