from application import db
from application.models import Base
import application.threads as threads
from sqlalchemy.sql import text
from datetime import timedelta, date

class User(Base):
	__tablename__ = "account"

	username = db.Column(db.String(30), nullable=False)
	first_name = db.Column(db.String(30), nullable=False)
	surname = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(256), nullable=False)
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

	def is_admin(self):
		return self.admin

	@staticmethod
	def latest_threads(user_id):
		query = "SELECT Thread.id as id" \
				" FROM Thread" \
				" WHERE Thread.sender_id = :id" \
				" ORDER BY Thread.date_created DESC" \
				" LIMIT 10"
		stmt = text(query).params(id = user_id)
		res = db.engine.execute(stmt)

		results = []
		for row in res:
			results.append(threads.models.Thread.query.get(row[0]))

		return results

	def get_latest_threads(self):
		return User.latest_threads(self.id)

	@staticmethod
	def latest_posts(user_id):
		query = "SELECT Post.id as id" \
				" FROM Post" \
				" WHERE Post.sender_id = :id" \
				" ORDER BY Post.date_created DESC" \
				" LIMIT 10"
		stmt = text(query).params(id = user_id)
		res = db.engine.execute(stmt)

		results = []
		for row in res:
			results.append(threads.models.Post.query.get(row[0]))

		return results

	def get_latest_posts(self):
		return User.latest_posts(self.id)

	@staticmethod
	def active_users():
		activity_threshold = date.today() - timedelta(7)
		stmt = text("SELECT COUNT(DISTINCT Account.id) FROM Account" \
					" LEFT JOIN Post ON Post.sender_id = Account.id" \
					" WHERE Post.date_modified >= :time").params(time = activity_threshold)

		res = db.engine.execute(stmt)

		for row in res:
			if row[0] == None:
				return 0
			else:
				return row[0]
		return 0