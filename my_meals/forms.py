from wtforms import TextField, PasswordField, validators
from flask.ext.wtf import Form

from models import User

class Unique(object):
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'Already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise validators.ValidationError(self.message)


class MemberForm(Form):
    username = TextField('Username', [validators.Required(), Unique(User, User.username)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
