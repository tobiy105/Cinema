from config import SQLALCHEMY_DATABASE_URI
from app import app, db

# Creates all the tables and the database.

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

