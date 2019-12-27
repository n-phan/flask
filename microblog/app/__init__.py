from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

application = Flask(__name__)
application.config.from_object(Config)  # File Configuration
db = SQLAlchemy(application)            # Database Tool
migrate = Migrate(application, db)      # Database Migration Tool
login = LoginManager(application)       # Login Tool
login.login_view = 'login'

from app import routes, models