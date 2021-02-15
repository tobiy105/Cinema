from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

import  os

from flask_msearch import Search
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#Handles the passwords encyption
bcrypt = Bcrypt(app)

#Handles search
search = Search()
search.init_app(app)
#Handles all saved images
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

# Handles all migrations.
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

#Handles all customers accounts
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"

from app.admin import views
from app.customers import views
from app.basket import views
from app.cinema import views


