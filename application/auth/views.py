from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import RegisterForm, LoginForm

@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/login/", methods = ["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("auth/login.html", form = LoginForm())

	form = LoginForm(request.form)

	username = form.username.data
	password = form.password.data

	user = User.query.filter_by(username = username, password = password).first()

	if not user:
		return render_template("auth/login.html", form = form, error = "Virheellinen käyttäjänimi tai salasana")

	login_user(user)

	return redirect(url_for("index"))

@app.route("/register/", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("auth/register.html", form = RegisterForm())

	form = RegisterForm(request.form)

	username = form.username.data
	email = form.email.data
	first_name = form.first_name.data
	surname = form.surname.data
	password = form.password.data
	password_confirmation = form.password_confirmation.data;

	if form.validate() and password == password_confirmation:
		user = User(username, first_name, surname, password, False, email)

		db.session().add(user)
		db.session().commit()

		login_user(user)

		return redirect(url_for("index"))
	else:
		if password == password_confirmation:
			return render_template("auth/register.html", form = form)
		else:
			return render_template("auth/register.html", form = form, password_error = "Salasanat eivät täsmää")
