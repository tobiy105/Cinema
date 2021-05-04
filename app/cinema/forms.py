from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators ,ValidationError,DateField,DateTimeField, TimeField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_wtf import FlaskForm
from .models import Movies, Screening
from _datetime import datetime
from datetime import datetime
from datetime import time

#creating the ticket form class
class Movie(Form):
    title = StringField('Title', [validators.DataRequired()])
    duration = TextAreaField('Running Time', [validators.DataRequired()])
    releaseDate = TextAreaField('Date', [validators.DataRequired()])
    plot = TextAreaField('Plot', [validators.DataRequired()])
    genres = TextAreaField('Genres', [validators.DataRequired()])
    certificate = TextAreaField('Certificate', [validators.DataRequired()])
    ratingReason = TextAreaField('Rating Reason', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])

    image = StringField('Image', [validators.DataRequired()])

    def validate_title(self, title):
        if Movies.query.filter_by(title=title.data).first():
            raise ValidationError("This title is already in use!")

#creating the screen from class
class Screen(Form):
    startTime = TimeField('Start Time', [validators.DataRequired()], default=datetime.now())
    endTime = TimeField('End Time', [validators.DataRequired()], default=datetime.now())
    date = DateField('Date', [validators.DataRequired()], default=datetime.now())
    theatre = TextAreaField('Theatre', [validators.DataRequired()])
    seats = IntegerField('Seats', [validators.DataRequired()])



#creating the ticket form class
class Tickets(Form):

    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    seatNo = IntegerField('Seat Number', [validators.DataRequired()])

    # check for the seats is not already taken
    def validate_seats(self, seatNo):
        if Screening.query.filter_by(seatNo=seatNo.data).first():
            raise ValidationError("This seat is already taken!")


#creating a form for movie search
class SearchMovieForm(Form):
    title = StringField('Title: ', [validators.DataRequired()])

