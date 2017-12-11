from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
from flask_images import Images

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
images = Images(app)

db = MySQL()
db.init_app(app)

from app import views, models
