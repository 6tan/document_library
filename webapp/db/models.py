from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
from app import flask_app


flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(flask_app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    lock = db.Column(db.Boolean, nullable=False, default=False)
    version = db.Column(db.Integer, nullable=False)
    participants = db.Column(db.ARRAY(db.Integer), server_default="{}")
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_update_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
