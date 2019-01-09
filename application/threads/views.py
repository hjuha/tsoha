from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread, Post
from application.threads.forms import ThreadForm, PostForm
from flask_login import login_required, current_user
from application.utils.date_format import date_to_string
from application.categories.models import Category, CategoryThread

def trim_end(msg):
	# remove last character as long as it's whitespace or newline
	while len(msg) > 1 and (msg[-1] == ' ' or msg[-1] == '\n'):
		msg = msg[:-1]
	return msg

@app.route("/thread/new/", methods=["GET", "POST"])
@login_required
def post_new_thread():
	if request.method == "GET":
		return render_template("threads/new_thread.html", form = ThreadForm(), categories = Category.query.all())
	
	categories = []
	for category in Category.query.all():
		if request.form.get("category" + str(category.id)):
			categories.append(category.id)

	form = ThreadForm(request.form)
	
	if not form.validate():
		return render_template("threads/new_thread.html", form = form, categories = Category.query.all())

	topic = form.topic.data

	content = trim_end(form.content.data)

	sender_id = current_user.id

	thread = Thread(topic, sender_id)

	db.session().add(thread)
	db.session().commit()

	thread_id = thread.id
	post = Post(content, sender_id, thread_id)

	for category_id in categories:
		categorythread = CategoryThread(category_id, thread_id)
		db.session().add(categorythread)

	db.session().add(post)
	db.session().commit()

	return redirect(url_for("index"))

@app.route("/thread/<thread_id>/", methods = ["POST"])
@login_required
def reply_thread(thread_id):
	form = PostForm(request.form)
	try: 
		thread_id = int(thread_id)
		thread = Thread.query.get(thread_id)

		posts = Post.query.filter(Post.thread_id == thread_id)
		
		if not form.validate():
			return redirect(url_for("get_thread", thread_id = thread_id))
	
		content = trim_end(form.content.data)

		sender_id = current_user.id

		post = Post(content, sender_id, thread_id)
		
		db.session().add(post)
		db.session().commit()

		return redirect(url_for("get_thread", thread_id = thread_id))
	except ValueError:
		return redirect(url_for("error404"))

@app.route("/edit_post/<post_id>/", methods = ["POST"])
@login_required
def edit_post(post_id):
	form = PostForm(request.form)
	post = Post.query.get(post_id)
	thread = Thread.query.get(post.thread_id)
	if not form.validate():
		return redirect(url_for('get_thread', thread_id = thread.id))
	
	content = trim_end(form.content.data)

	if current_user.is_authenticated:
		user = User.query.get(current_user.get_id())
		if user.is_admin() or user.id == post.sender_id:
			post.content = content
			db.session().commit()

	return redirect(url_for('get_thread', thread_id = thread.id))

@app.route("/delete_post/<post_id>/")
@login_required
def delete_post(post_id):
	post = Post.query.get(post_id)
	thread = Thread.query.get(post.thread_id)
	if current_user.is_authenticated:
		user = User.query.get(current_user.get_id())
		if user.is_admin() or user.id == post.sender_id:
			db.session().delete(post)
			db.session().commit()

	return redirect(url_for('get_thread', thread_id = thread.id))

@app.route("/thread/<thread_id>/", methods = ["GET"])
def get_thread(thread_id):
	try:
		thread_id = int(thread_id)
		thread = Thread.query.get(thread_id)

		# sort by date_created
		thread.posts.sort(key = (lambda post : post.date_created))
		
		return render_template("threads/thread.html", thread = thread, form = PostForm())		
	except ValueError:
		return redirect(url_for("error404"))

@app.route("/delete_thread/<thread_id>/", methods = ["GET"])
def delete_thread(thread_id):
	try: 
		thread_id = int(thread_id)
		thread = Thread.query.get(thread_id)

		if current_user.is_authenticated:
			user = User.query.get(current_user.get_id())
			if user.is_admin() or user.id == thread.sender_id:
				for categorythread in thread.categorythreads:
					db.session().delete(categorythread)
				posts = Post.query.filter(Post.thread_id == thread_id)
				for post in posts:
					db.session().delete(post)
					
				db.session().delete(thread)
				db.session().commit()

		return redirect(url_for("index"))
	except ValueError:
		return redirect(url_for("error404"))