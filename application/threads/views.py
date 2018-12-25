from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread, Post
from application.threads.forms import ThreadForm, ReplyThreadForm
from flask_login import login_required, current_user

@app.route("/thread/new/", methods=["GET", "POST"])
@login_required
def post_new_thread():
	if request.method == "GET":
		return render_template("threads/new_thread.html", form = ThreadForm())
	
	form = ThreadForm(request.form)
	
	if not form.validate():
		return render_template("threads/new_thread.html", form = form)

	topic = form.topic.data
	content = form.content.data

	# while the last character of the post is a whitespace or a newline, delete it
	while content[-1] == ' ' or content[-1] == '\n':
		content = content[:-1]

	sender_id = current_user.id

	thread = Thread(topic, sender_id)

	db.session().add(thread)
	db.session().commit()

	thread_id = thread.id
	post = Post(content, sender_id, thread_id)

	db.session().add(post)
	db.session().commit()

	return redirect(url_for("index"))

@app.route("/thread/<thread_id>/", methods = ["POST"])
@login_required
def reply_thread(thread_id):
	form = ReplyThreadForm(request.form)
	try: 
		thread_id = int(thread_id)
		thread = Thread.query.get(thread_id)

		posts = Post.query.filter(Post.thread_id == thread_id)
		
		if not form.validate():
			return render_template("threads/thread.html", thread = thread, posts = posts, form = ReplyThreadForm())
	
		content = form.content.data
		# while the last character of the post is a whitespace or a newline, delete it
		while content[-1] == ' ' or content[-1] == '\n':
			content = content[:-1]

		sender_id = current_user.id

		post = Post(content, sender_id, thread_id)
		
		db.session().add(post)
		db.session().commit()

		return redirect(url_for("get_thread", thread_id = thread_id, thread = thread, posts = posts, form = ReplyThreadForm()))
	except ValueError:
		return redirect(url_for("error404"))

@app.route("/thread/<thread_id>/", methods = ["GET"])
def get_thread(thread_id):
	try: 
		thread_id = int(thread_id)
		thread = Thread.query.get(thread_id)
		
		posts = Post.query.filter(Post.thread_id == thread_id)
		posts = list(posts)
		for post in posts:
			post.sender = User.query.get(post.sender_id)
		return render_template("threads/thread.html", thread = thread, posts = posts, form = ReplyThreadForm())		
	except ValueError:
		return redirect(url_for("error404"))