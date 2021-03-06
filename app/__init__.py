from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_sslify import SSLify
# from flask_migrate import Migrate

app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
# sslify=SSLify(app)
# migrate=Migrate(app,db)

from .models import Sisi

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    sisi=Sisi.query.get(user_id)
    return sisi

from . import views
