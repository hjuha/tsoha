from application import app, db
from flask import redirect, render_template, request, url_for
from application.auth.models import User
from application.threads.models import Thread
from application.threads.forms import ThreadForm
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
	sender_id = current_user.id
	thread = Thread(topic, content, sender_id)

	db.session().add(thread)
	db.session().commit()

	return redirect(url_for("index"))