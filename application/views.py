from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.utils.date_format import date_to_string
from application import admin_required
from flask_login import current_user
from application.categories.models import Category

@app.route("/", methods=["GET"])
def index():
	threads = Thread.query.all()

	for thread in threads:
		thread.sender = User.query.get(thread.sender_id)
		thread.posted = date_to_string(thread.date_created)
		thread.deletable = False
		thread.categories = []

		if current_user.is_authenticated:
			user = User.query.get(current_user.get_id())
			if user.is_admin() or user.id == thread.sender_id:
				thread.deletable = True

		for categorythread in thread.categorythreads:
			thread.categories.append(Category.query.get(categorythread.category_id))

	threads = threads[::-1]

	return render_template("index.html", threads = threads)

@app.route("/users/")
@admin_required
def users():
	return render_template("users.html", users = User.query.all())

@app.route("/404/")
def error404():
	return render_template("404.html")

@app.errorhandler(404)
def on404(e):
	return render_template("404.html")