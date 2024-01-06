#configuration file
import os
from decouple import config
import pdfkit

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'app/static/images')
WTF_CSRF_ENABLED = True

SECRET_KEY = config('SECRET_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')

path_wkhtmltopdf = "app/wkhtmltopdf/wkhtmltopdf/bin/wkhtmltopdf.exe"
# path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#path_wkhtmltopdf = "app/wkhtmltopdf/bin/wkhtmltopdf.exe" #removed a r at the start. IDK if this is correct
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
