from flask import Flask

app = Flask(__name__)

def sanitize_for_js(text):
	text = text.replace("\\", "\\u005C")
	text = text.replace("&", "\\u0026")
	text = text.replace("`", "\\u0060")
	text = text.replace("<", "\\u003C")
	text = text.replace(">", "\\u003E")
	text = text.replace("'", "\\u0027")
	text = text.replace("\"", "\\u0022")
	return text

app.jinja_env.filters['sanitize_for_js'] = sanitize_for_js

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
	app.config["SQLALCHEMY_ECHO"] = True
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Ole hyvä ja kirjaudu käyttääksesi sivustoa."

from functools import wraps
from flask import url_for, redirect

def admin_required(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		if not current_user:
			return login_manager.unauthorized()

		if not current_user.is_authenticated:
			return login_manager.unauthorized()

		if not current_user.is_admin():
			return redirect(url_for("index"))
		
		return fn(*args, **kwargs)
	return decorated_view

from application import views

from application.auth import views
from application.auth import models
from application.auth.models import User

from application.threads import views
from application.threads import models

from application.categories import views
from application.categories import models

from application.search import views

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

db.create_all()