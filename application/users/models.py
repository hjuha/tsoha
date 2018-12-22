from application import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(30), nullable=False)
	first_name = db.Column(db.String(30), nullable=False)
	surname = db.Column(db.String(30), nullable=False)
	password_hash = db.Column(db.String(64), nullable=False) # we will use SHA-256
	email = db.Column(db.String(100), nullable=False)

	admin = db.Column(db.Boolean, nullable=False)

	def __init__(self, username, first_name, surname, password_hash, admin, email):
		self.username = username
		self.first_name = first_name
		self.surname = surname
		self.password_hash = password_hash
		self.admin = admin
		self.email = email