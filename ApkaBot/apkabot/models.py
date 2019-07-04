from datetime import datetime, timedelta
from apkabot import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    free = db.Column(db.Float, nullable=True, default = 0)
    accounts = db.relationship('Account', backref='owner', lazy=True)

    #def __repr__(self):
    #    return f"'{self.id}','{self.username}', '{self.email}', '{self.free}', {self.accounts})"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    url = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)

    ref = db.Column(db.Integer, nullable=True)
    license = db.Column(db.DateTime, nullable=True, default = datetime.now() + timedelta(hours=3)) 

    #def __repr__(self):
    #    return f"'{self.id}',' Owner:{self.owner_id}', '{self.user_id}', L:'{self.login}', P:'{self.password}', ref:'{self.ref}', '{self.license}'"