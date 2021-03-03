from app import db
from datetime import datetime


# create the movie database table
class Movies(db.Model):
    __seachable__ = ['title', 'genres']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Text, nullable=False)
    releaseDate = db.Column(db.Text, nullable=False)
    plot = db.Column(db.Text, nullable=False)
    genres = db.Column(db.Text, nullable=False)
    certificate = db.Column(db.Text, nullable=False)
    ratingReason = db.Column(db.Text, nullable=False)
    # director = db.Column(db.Text, nullable=False)
    # actors = db.Column(db.Text, nullable=False)


    image = db.Column(db.String(150), nullable=False, default='image.jpg')

    #may want to make mutiple catgeries
    #may have to change this


    def __repr__(self):
        return '<Movie %r>' % self.title

# create the movie database table
class Screening(db.Model):
    __seachable__ = ['date']
    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.Date, nullable=False)
    theatre = db.Column(db.Text, nullable=False)
    seats = db.Column(db.Integer, nullable=False)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'),nullable=False)
    movie =  db.relationship('Movies',backref=db.backref('movie', lazy=True))

    def __repr__(self):
        return '<Screening %r>' % self.id

# create the ticket database table
class Addticket(db.Model):
    __seachable__ = ['title', 'genres']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    plot = db.Column(db.Text, nullable=False)
    genres = db.Column(db.Text, nullable=False)
    certificate = db.Column(db.Text, nullable=False)
    ratingReason = db.Column(db.Text, nullable=False)

    #seatNo = db.Column(db.Integer, nullable=False)

    #image = db.Column(db.String(150), nullable=False, default='image.jpg')

    #may want to make mutiple catgeries
    #may have to change this


    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()