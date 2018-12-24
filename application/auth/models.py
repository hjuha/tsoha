from application import db

class User(db.Model):
	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	username = db.Column(db.String(30), nullable=False)
	first_name = db.Column(db.String(30), nullable=False)
	surname = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(100), nullable=False)

	admin = db.Column(db.Boolean, nullable=False)

	threads = db.relationship("Thread", backref = __tablename__, lazy = True)
	posts = db.relationship("Post", backref = __tablename__, lazy = True)

	def __init__(self, username, first_name, surname, password, admin, email):
		self.username = username
		self.first_name = first_name
		self.surname = surname
		self.password = password
		self.admin = admin
		self.email = email

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True