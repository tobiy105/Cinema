from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads#, patch_request_class

# from flask_msearch import Search
from flask_login import LoginManager

from flask_qrcode import QRcode

from flask_mail import Mail, Message
from pdfkit import pdfkit
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#Handles the passwords encyption
bcrypt = Bcrypt(app)

#Handles search
# search = Search()
# search.init_app(app)
#Handles all saved images
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
# patch_request_class(app)

# Handles all migrations.
migrate = Migrate(app, db)


#Handles all customers accounts
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please login first"



#Configures flask_mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'noreply.seproject2021@gmail.com'
app.config['MAIL_PASSWORD'] = 'softwareproject'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply.seproject2021@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Enables QRCode functionality
QRcode(app)


from app.cinema import views
from app.admin import views
from app.customers import views
from app.basket import views
from app.employee import views
from app.till import views


