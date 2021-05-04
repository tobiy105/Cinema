from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError, IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Employee


#creating the Admin Registration form class
class EmployeeRegisterForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

#creating the Admin Login form class
class EmployeeLoginFrom(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

class PayWithCashForm(Form):
    n50 = IntegerField('Amount of £50 notes')
    n20 = IntegerField('Amount of £20 notes')
    n10 = IntegerField('Amount of £10 notes')
    n5 = IntegerField('Amount of £5 notes')
    c200 = IntegerField('Amount of £2 coins')
    c100 = IntegerField('Amount of £1 coins')
    c50 = IntegerField('Amount of 50p coins')
    c20 = IntegerField('Amount of 20p coins')
    c10 = IntegerField('Amount of 10p coins')
    c5 = IntegerField('Amount of 5p coins')
    c2 = IntegerField('Amount of 2p coins')
    c1 = IntegerField('Amount of 1p coins')
    submit = SubmitField('Pay')