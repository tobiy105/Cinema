from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Employee


# creating the Customer Registration form class
class EmployeeRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(),
                                            validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Employee.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")

    def validate_email(self, email):
        if Employee.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


# creating the Customer Login form class
class EmployeeLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])



















