from application import db
from application.models import Base
from application.categories.models import Category, CategoryThread
import application.auth as auth
from flask_login import current_user

from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declared_attr

class ThreadBase(Base):
	__abstract__ = True

	@declared_attr
	def sender_id(self):
		return db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)

	def get_sender(self):
		return auth.models.User.query.get(self.sender_id)

	def is_deletable(self):
		return current_user.is_authenticated and (self.sender_id == current_user.get_id() or current_user.admin)


class Thread(ThreadBase):
	topic = db.Column(db.String(50), nullable = False)
	
	posts = db.relationship("Post", backref = "thread", lazy = True)
	categorythreads = db.relationship("CategoryThread", backref = "thread", lazy = True)

	def __init__(self, topic, sender_id):
		self.topic = topic
		self.sender_id = sender_id

	@staticmethod
	def search_query(contains, name, after_date, before_date, ordering, ascending, category_id):
		contains = "%" + contains.lower() + "%"
		name = "%" + name.lower() + "%"
		select = "SELECT Thread.id as id FROM Thread" \
			     " LEFT JOIN Account ON Account.id = Thread.sender_id"
		
		filters = " WHERE LOWER(Thread.topic) LIKE :contains" \
				  " AND LOWER(Account.first_name || ' ' || Account.surname) LIKE :name" \
				  " AND Thread.date_created <= :before" \
				  " AND Thread.date_created >= :after"

		category_id = int(category_id)
		if category_id:
			select += " LEFT JOIN Category_Thread ON Category_Thread.category_id = :cid"
			filters += " AND Thread.id = Category_Thread.thread_id"

		if ordering == "posts":
			select += " LEFT JOIN Post ON Post.thread_id = Thread.id"
			
			filters += " GROUP BY Thread.id" \
					   " ORDER BY COUNT(*)"
		elif ordering == "date":
			filters += " ORDER BY Thread.date_created"
		else:
			filters += " ORDER BY Thread.date_created"

		if ascending != "true":
			filters += " ASC"
		else:
			filters += " DESC"

		stmt = text(select + filters)
		if category_id:
			stmt = stmt.params(contains = contains, name = name, after = after_date, before = before_date, cid = category_id)
		else:
			stmt = stmt.params(contains = contains, name = name, after = after_date, before = before_date)
			
		res = db.engine.execute(stmt)

		results = []
		for row in res:
			results.append(Thread.query.get(row[0]))

		return results

	@staticmethod
	def number_of_replies(thread_id):
		query = "SELECT COUNT(DISTINCT Post.id)" \
				" FROM Post" \
				" WHERE Post.thread_id = :id"
		stmt = text(query).params(id = thread_id)
		res = db.engine.execute(stmt)
		return res.first()[0] - 1

	def get_number_of_replies(self):
		return Thread.number_of_replies(self.id)

	def get_categories(self):
		categories = []
		for categorythread in self.categorythreads:
			categories.append(Category.query.get(categorythread.category_id))
		return categories

class Post(ThreadBase):
	content = db.Column(db.String(1000), nullable = False)

	thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"), nullable = False)

	def __init__(self, content, sender_id, thread_id):
		self.content = content
		self.sender_id = sender_id
		self.thread_id = thread_id

	@staticmethod
	def search_query(contains, name, after_date, before_date, ordering, ascending, category_id):
		contains = "%" + contains.lower() + "%"
		name = "%" + name.lower() + "%"
		select = "SELECT Post.id as id FROM Post" \
			     " LEFT JOIN Account ON Account.id = Post.sender_id"
		
		filters = " WHERE LOWER(Post.content) LIKE :contains" \
				  " AND LOWER(Account.first_name || ' ' || Account.surname) LIKE :name" \
				  " AND Post.date_created <= :before" \
				  " AND Post.date_created >= :after"

		category_id = int(category_id)
		if category_id:
			select += " LEFT JOIN Thread ON Thread.id = Post.thread_id"
			select += " LEFT JOIN Category_Thread ON Category_Thread.category_id = :cid"
			filters += " AND Thread.id = Category_Thread.thread_id"

		filters += " ORDER BY Post.date_created"

		if ascending != "true":
			filters += " ASC"
		else:
			filters += " DESC"

		stmt = text(select + filters)
		if category_id:
			stmt = stmt.params(contains = contains, name = name, after = after_date, before = before_date, cid = category_id)
		else:
			stmt = stmt.params(contains = contains, name = name, after = after_date, before = before_date)

		res = db.engine.execute(stmt)

		results = []
		for row in res:
			results.append(Post.query.get(row[0]))

		return results

	def get_topic(self):
		return Thread.query.get(self.thread_id).topic