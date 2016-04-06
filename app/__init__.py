from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID, COMMON_PROVIDERS

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view='signin'
oid = OpenID(app,'/tmp')

from app import views, models