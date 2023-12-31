from app import db
from datetime import datetime
from datetime import time

# create the movie database table
class Movies(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Text, nullable=False)
    releaseDate = db.Column(db.Text, nullable=False)
    plot = db.Column(db.Text, nullable=False)
    genres = db.Column(db.Text, nullable=False)
    certificate = db.Column(db.Text, nullable=False)
    ratingReason = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    image = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Movie %r>' % self.title

# create the movie database table
class Screening(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    theatre = db.Column(db.Text, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),nullable=False)
    movie = db.relationship('Movies',backref=db.backref('movie', lazy=True))

    def __repr__(self):
        return '<Screening %r>' % self.id

# create the ticket database table
class Ticket(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    seatNo = db.Column(db.Integer, nullable=False)
    taken = db.Column(db.Boolean, default=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable=False)
    screen = db.relationship('Screening', backref=db.backref('screen', lazy=True))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return '<Post %r>' % self.id
