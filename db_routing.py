from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask import Flask

app = Flask('Jarvis', static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'Radius'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_authenticated

    def get_id(self):
        return self.id


class Trigger(db.Model):
    __tablename__ = 'Triggers'
    id = db.Column(db.Integer, primary_key=True)
    triggername = db.Column(db.String(80), unique=True, nullable=False)
    trigger_def = db.Column(db.String(200))


class Action(db.Model):
    __tablename__ = 'Actions'
    id = db.Column(db.Integer, primary_key=True)
    actionname = db.Column(db.String(80), unique=True, nullable=False)
    action_def = db.Column(db.String(200))


class Scenario(db.Model):
    __tablename__ = 'Scenarios'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('Users.id'))
    trigger_id = db.Column(db.Integer, ForeignKey('Triggers.id'))
    trigger_args = db.Column(db.String(200))
    action_id = db.Column(db.Integer, ForeignKey('Actions.id'))
    action_args = db.Column(db.String(200))


def add_user(user_name, passw_hash):
    if not find_user(user_name):
        new_user = User(username=user_name, password=passw_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    else:
        print('Логин занят')
        return False


def find_user(id=None, username=None):
    if id:
        return User.query.filter_by(id=id).first()
    if username:
        return User.query.filter_by(username=username).first()


# def get_trigers():
