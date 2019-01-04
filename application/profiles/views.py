from application import app, db
from flask import redirect, render_template, request, url_for
from application import admin_required
from application.auth.models import User
from application.threads.models import Thread, Post

@app.route("/profile/<user_id>/", methods = ["GET"])
def get_profile(user_id):
	user = User.query.get(user_id)
	if not user:
		return redirect(url_for('error404'))
	return render_template("profiles/profile.html", user = user)

@app.route("/promote/<user_id>/", methods = ["GET"])
@admin_required
def promote(user_id):
	user = User.query.get(user_id)
	user.admin = True
	db.session().commit()
	return redirect(url_for("get_profile", user_id = user_id))

@app.route("/demote/<user_id>/", methods = ["GET"])
@admin_required
def demote(user_id):
	user = User.query.get(user_id)
	user.admin = False
	db.session().commit()
	return redirect(url_for("get_profile", user_id = user_id))