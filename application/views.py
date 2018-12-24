from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread
from application.threads.forms import ThreadForm

@app.route("/")
def index():
	threads = Thread.query.all()

	for thread in threads:
		thread.sender = User.query.get(thread.sender_id)

	return render_template("index.html", threads = threads)

@app.route("/users/")
def users():
	return render_template("users.html", users = User.query.all())