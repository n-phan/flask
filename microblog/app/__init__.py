import os
import logging 

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config

application = Flask(__name__)
application.config.from_object(Config)  # File Configuration
login = LoginManager(application)       # Login Tool
login.login_view = 'login'
mail = Mail(application)                # Email Tool
db = SQLAlchemy(application)            # Database Tool
migrate = Migrate(application, db)      # Database Migration Tool

# Error notification
if not application.debug:
    # by Email
    if application.config['MAIL_SERVER']:
        auth = None
        if application.config['MAIL_USERNAME'] or application.config['MAIL_PASSWORD']:
            auth = (application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD'])
        secure = None
        if application.config['MAIL_USE_TLS']:
            secure = ()
        
        mail_handler = SMTPHandler(
            mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
            fromaddr='no-reply@' + application.config['MAIL_SERVER'],
            toaddrs=application.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        application.logger.addHandler(mail_handler)
    
    # logging
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info('Microblog startup')

from app import routes, models, errors
