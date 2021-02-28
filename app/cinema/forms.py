from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed

#creating the ticket form class
class Addtickets(Form):
    title = StringField('Title', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    time = TextAreaField('Running Time', [validators.DataRequired()])
    date = TextAreaField('Date', [validators.DataRequired()])
    plot = TextAreaField('Plot', [validators.DataRequired()])
    genres = TextAreaField('Genres', [validators.DataRequired()])
    certificate = TextAreaField('Certificate', [validators.DataRequired()])
    ratingReason = TextAreaField('Rating Reason', [validators.DataRequired()])

    #image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'Images only please'])




#creating a form for movie search
class MovieForm(Form):
    title = StringField('Title: ', [validators.DataRequired()])

