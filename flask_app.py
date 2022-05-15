from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app
from app.controllers import *
from app.models import *

app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app)
db.create_all()
db.session.commit()
