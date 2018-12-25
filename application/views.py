from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.utils.date_format import date_to_string

@app.route("/", methods=["GET"])
def index():
	threads = Thread.query.all()

	for thread in threads:
		thread.sender = User.query.get(thread.sender_id)
		thread.time = date_to_string(thread.posting_time)
	print(type(threads))
	threads = threads[::-1]

	return render_template("index.html", threads = threads)

@app.route("/users/")
def users():
	return render_template("users.html", users = User.query.all())

@app.route("/404/")
def error404():
	return redirect(url_for("index"))