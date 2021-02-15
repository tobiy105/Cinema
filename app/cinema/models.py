from app import db
from datetime import datetime


# create the ticket database table
class Addticket(db.Model):
    __seachbale__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)

    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #may want to make mutiple catgeries
    #may have to change this
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))


    def __repr__(self):
        return '<Post %r>' % self.name


# create the Categories database table
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name


db.create_all()