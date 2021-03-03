from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators , ValidationError, DateField, DateTimeField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from .models import Movies, Screening
import datetime

#creating the ticket form class
class Movie(Form):
    title = StringField('Title', [validators.DataRequired()])
    duration = TextAreaField('Running Time', [validators.DataRequired()])
    releaseDate = TextAreaField('Date', [validators.DataRequired()])
    plot = TextAreaField('Plot', [validators.DataRequired()])
    genres = TextAreaField('Genres', [validators.DataRequired()])
    certificate = TextAreaField('Certificate', [validators.DataRequired()])
    ratingReason = TextAreaField('Rating Reason', [validators.DataRequired()])

    image = StringField('Image', [validators.DataRequired()])

    confirm = TextAreaField('Are you happy with movie details (Yes/No)', [validators.DataRequired()])

    def validate_title(self, title):
        if Movies.query.filter_by(title=title.data).first():
            raise ValidationError("This title is already in use!")

#creating the screen from class
class Sceen(Form):
    startTime = DateTimeField('Start Time', [validators.DataRequired()], default=datetime.now())
    endTime = DateTimeField('End Time', [validators.DataRequired()], default=datetime.now())
    date = DateField('Date', [validators.DataRequired()], default=datetime.now())
    theatre = TextAreaField('Theatre', [validators.DataRequired()])
    seats = IntegerField('Seats', [validators.DataRequired()])



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

    # seatNo = IntegerField('Seat Number', [validators.DataRequired()])
    #
    # # check for the seats is not already taken
    # def validate_seats(self, seatNo):
    #     if Screening.query.filter_by(seatNo=seatNo.data).first():
    #         raise ValidationError("This seat is already taken!")




#creating a form for movie search
class SearchMovieForm(Form):
    title = StringField('Title: ', [validators.DataRequired()])

