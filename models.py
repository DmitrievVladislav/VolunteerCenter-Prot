from datetime import datetime
from flask_login import UserMixin
from database_config import db


class User(UserMixin, db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_lvl = db.Column(db.Integer)
    username = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(30), unique=False)
    surname = db.Column(db.String(30), unique=False)
    midname = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(50), unique=False)
    phone = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(100))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
