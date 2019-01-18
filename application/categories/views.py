from application import app, db
from flask import redirect, render_template, request, url_for
from application import admin_required
from application.categories.models import Category, CategoryThread
from application.categories.forms import CategoryForm

@app.route("/categories/", methods=["GET"])
@admin_required
def get_categories():
	categories = Category.query.all()
	form = CategoryForm()
	return render_template("categories/categories.html", categories = categories, form = form)

@app.route("/add_category/", methods=["POST"])
@admin_required
def add_category():
	form = CategoryForm(request.form)

	if not form.validate():
		return render_template("categories/categories.html", categories = Category.query.all(), form = form)

	name = form.name.data

	category = Category(name)

	db.session().add(category)
	db.session().commit()

	return redirect(url_for("get_categories"))

@app.route("/edit_category/<category_id>/", methods=["POST"])
@admin_required
def edit_category(category_id):
	form = CategoryForm(request.form)

	if not form.validate():
		return render_template("categories/categories.html", categories = Category.query.all(), form = form)

	category = Category.query.get(int(category_id))
	
	category.name = form.name.data
	db.session().commit()

	return redirect(url_for("get_categories"))

@app.route("/delete_category/<category_id>/")
@admin_required
def delete_category(category_id):
	category = Category.query.get(int(category_id))
	for categorythread in category.categorythreads:
		db.session().delete(categorythread)
	db.session().delete(category)
	db.session().commit()
	return redirect(url_for("get_categories"))