from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed

#creating the ticket form class
class Addtickets(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    category = TextAreaField('Category', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
