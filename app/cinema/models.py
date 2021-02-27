from app import db
from datetime import datetime


# create the ticket database table
class Addticket(db.Model):
    __seachbale__ = ['name', 'desc']
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

    #image = db.Column(db.String(150), nullable=False, default='image.jpg')

    #may want to make mutiple catgeries
    #may have to change this


    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()