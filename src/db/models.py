from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import flask_app


flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(flask_app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(250), unique=True, nullable=False)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    lock = db.Column(db.Boolean, nullable=False, default=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_update_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class DocMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    document_id = db.Column(db.Integer, nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    document_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(10), nullable=False)
    last_update_date = db.Column(db.DateTime, nullable=False, default=datetime.now)