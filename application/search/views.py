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
		return render_template("search/search.html", categories = categories, form = form, results = [])

	categories = []
	for category in Category.query.all():
		if request.form.get("category" + str(category.id)):
			categories.append(category.id)

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

	results = Thread.search_query(contains, name, after_date, before_date, categories)

	for thread in results:
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

	results = results[::-1]

	return render_template("search/search.html", categories = categories, form = form, results = results)