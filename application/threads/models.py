from application import db
from application.models import Base
from application.categories.models import CategoryThread

from sqlalchemy.sql import text

class Thread(Base):
	topic = db.Column(db.String(50), nullable = False)
	sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)

	posts = db.relationship("Post", backref = "thread", lazy = True)
	categorythreads = db.relationship("CategoryThread", backref = "thread", lazy = True)

	def __init__(self, topic, sender_id):
		self.topic = topic
		self.sender_id = sender_id

	@staticmethod
	def search_query(contains, name, after_date, before_date, categories):
		contains = "%" + contains + "%"
		name = "%" + name + "%"
		query = "SELECT Thread.id as id" \
				" FROM Thread, Account" \
				" WHERE Account.id = Thread.sender_id" \
				" AND Thread.topic LIKE :contains" \
				" AND Account.first_name || ' ' || Account.surname LIKE :name" \
				" AND Thread.date_created <= :before" \
				" AND Thread.date_created >= :after"
		stmt = text(query).params(contains = contains, name = name, after = after_date, before = before_date)
		res = db.engine.execute(stmt)

		results = []
		for row in res:
			results.append(Thread.query.get(row[0]))

		return results

class Post(Base):
	content = db.Column(db.String(1000), nullable = False)

	sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
	thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"), nullable = False)

	def __init__(self, content, sender_id, thread_id):
		self.content = content
		self.sender_id = sender_id
		self.thread_id = thread_id

	@staticmethod
	def search_query(contains, name, after_date, before_date, categories):
		contains = "%" + contains.lower() + "%"
		name = "%" + name.lower() + "%"
		query = "SELECT Post.id as id" \
				" FROM Post, Account" \
				" WHERE Account.id = Post.sender_id" \
				" AND LOWER(Post.content) LIKE :contains" \
				" AND LOWER(Account.first_name || ' ' || Account.surname) LIKE :name" \
				" AND Post.date_created <= :before" \
				" AND Post.date_created >= :after"
		stmt = text(query).params(contains = contains, name = name, after = after_date, before = before_date)
		res = db.engine.execute(stmt)

		results = []
		for row in res:
			results.append(Post.query.get(row[0]))

		return results