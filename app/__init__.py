import flask

app = flask.Flask(__name__)

from app.module.controller import *
from app.module.database import *