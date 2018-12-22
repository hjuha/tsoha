from application import app, db
from flask import redirect, render_template, request, url_for
from application.users.models import User
from application.threads.models import Thread
import hashlib

@app.route("/register/")
def register():
	return render_template("register.html")

@app.route("/register/", methods=["POST"])
def register_user(): # check user doesn't exist
	username = request.form.get("username")
	email = request.form.get("email")
	first_name = request.form.get("first_name")
	surname = request.form.get("surname")
	password = request.form.get("password")
	if username and email and first_name and surname and password and password == request.form.get("password_confirmation"):
		hashed = hashlib.sha256((username + password).encode('utf-8')).hexdigest()
		user = User(username, first_name, surname, hashed, False, email)

		db.session().add(user)
		db.session().commit()

		return redirect(url_for("index"))
	else:
		return redirect(url_for("register_user"))

@app.route("/")
def index():
	return render_template("index.html", threads = Thread.query.all())

@app.route("/users/")
def users():
	return render_template("users.html", users = User.query.all())

@app.route("/thread/new/")
def new_thread():
	return render_template("new_thread.html")

@app.route("/thread/new/", methods=["POST"])
def post_new_thread():
	topic = request.form.get("topic")
	content = request.form.get("content")
	sender_id = 1 # a placeholder value
	thread = Thread(topic, content, sender_id)

	db.session().add(thread)
	db.session().commit()

	return redirect(url_for("index"))