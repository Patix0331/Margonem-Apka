from datetime import datetime
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
    accounts = db.relationship('Account', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}')"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    license = db.Column(db.DateTime, nullable=True, default = datetime.utcnow)

    def __repr__(self):
        return f"Account('owner:{self.owner_id}', '{self.id}', '{self.url}'"