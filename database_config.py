import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'


app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app)
