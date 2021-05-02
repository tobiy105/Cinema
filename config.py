#configuration file
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pdfkit

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'g8y2g3fr6g8g8yw8yg'

#path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
path_wkhtmltopdf = r"/home/andrew/flask_application/GroupProject/sep_group/app/wkhtmltopdf/bin/wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


