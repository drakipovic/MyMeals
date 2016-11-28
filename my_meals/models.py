from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from main import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(50))
    role = db.Column(db.String(15))
    meals = db.relationship('Meal', backref='user', lazy='dynamic')

    def __init__(self, username, password, role):
        self.username = username
        self.password_hash = self._set_password(password)
        self.role = role

    def __iter__(self):
        yield 'id', self.user_id
        yield 'username', self.username
        yield 'role', self.role
    
    def _set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

class Meal(db.Model):
    __tablename__ = 'meals'

    meal_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    text = db.Column(db.Text)
    calories = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    def __iter__(self):
        yield 'id', self.meal_id
        yield 'date', datetime.strftime(self.timestamp, "%m/%d/%Y")
        yield 'time', datetime.strftime(self.timestamp, "%-H:%M")
        yield 'text', self.text
        yield 'calories', self.calories

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
