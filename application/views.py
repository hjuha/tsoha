from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.utils.date_format import date_to_string
from application import admin_required
from flask_login import current_user
from application.categories.models import Category

THREADS_PER_PAGE = 10

@app.route("/", methods=["GET"])
def index():
	threads = Thread.query.all()
	threads = threads[::-1]

	page_id = 1
	last_page_id = len(threads) // THREADS_PER_PAGE
	if len(threads) % THREADS_PER_PAGE != 0:
		last_page_id += 1

	display_threads = threads[0:THREADS_PER_PAGE]

	return render_template("index.html", threads = display_threads, page_id = page_id, last_page_id = last_page_id)

@app.route("/<page_id>/", methods=["GET"])
def index_by_page_id(page_id):
	page_id = int(page_id)
	begin = (page_id - 1) * THREADS_PER_PAGE
	end = page_id * THREADS_PER_PAGE

	threads = Thread.query.all()
	threads = threads[::-1]

	last_page_id = len(threads) // THREADS_PER_PAGE
	if len(threads) % THREADS_PER_PAGE != 0:
		last_page_id += 1

	display_threads = threads[begin:end]

	return render_template("index.html", threads = display_threads, page_id = page_id, last_page_id = last_page_id)

@app.route("/users/")
@admin_required
def users():
	return render_template("users.html", users = User.query.all())

@app.route("/404/")
def error404():
	return render_template("404.html")

@app.errorhandler(500)
def on500(e):
	return render_template("404.html")

@app.errorhandler(404)
def on404(e):
	return render_template("404.html")