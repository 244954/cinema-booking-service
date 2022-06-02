from flask import Flask
from models.Models import db
from flask_app.config import *
from mqrabbit.RabbitChannels import RabbitChannels
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
if env == 'dev':
    app.debug = True
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_DEV
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_PROD

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['CORS_HEADERS'] = CORS_HEADERS

db.init_app(app)
rabbit_channels = RabbitChannels(db, env)
import flask_app.views  # ugly, but encouraged: https://flask.palletsprojects.com/en/2.1.x/patterns/packages/
