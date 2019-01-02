from application import app, db
from flask import redirect, render_template, request, url_for
from application.categories.models import Category
from application.search.forms import SearchForm
from datetime import datetime, date, timedelta
from application.threads.models import Thread, Post
from application.auth.models import User
from application.utils.date_format import date_to_string
from flask_login import current_user

@app.route("/search/", methods=["GET", "POST"])
def search():
	if request.method == "GET":
		categories = Category.query.all()
		form = SearchForm()
		return render_template("search/search.html", categories = categories, form = form, results = [], type = "None")

	categories = []
	for category in Category.query.all():
		if request.form.get("category" + str(category.id)):
			categories.append(category.id)

	query_type = request.form.get("type")

	form = SearchForm(request.form)

	contains = form.contains.data
	name = form.name.data
	after_date = form.after_date.data
	before_date = form.before_date.data

	if not after_date:
		after_date = date(1900, 1, 1)
	if not before_date:
		before_date = date.today()

	before_date += timedelta(1)
	results = []

	if query_type == "thread":
		results = Thread.search_query(contains, name, after_date, before_date, categories)

		for thread in results:
			thread.sender = User.query.get(thread.sender_id)
			thread.posted = date_to_string(thread.date_created)
			thread.deletable = False
			thread.categories = []

			for categorythread in thread.categorythreads:
				thread.categories.append(Category.query.get(categorythread.category_id))
	elif query_type == "post":
		results = Post.search_query(contains, name, after_date, before_date, categories)

		for post in results:
			post.sender = User.query.get(post.sender_id)
			post.posted = date_to_string(post.date_created)
			post.modified = date_to_string(post.date_modified)
			post.thread_topic = Thread.query.get(post.thread_id).topic

	results = results[::-1]

	return render_template("search/search.html", categories = Category.query.all(), form = form, results = results, type = query_type)