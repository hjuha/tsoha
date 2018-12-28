from application import db
from application.models import Base

class Category(Base):
	name = db.Column(db.String(25), nullable = False)
	categorythreads = db.relationship("CategoryThread", backref = "category", lazy = True)

	def __init__(self, name):
		self.name = name

class CategoryThread(Base):
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable = False)
	thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"), nullable = False)

	def __init__(self, category_id, thread_id):
		self.category_id = category_id
		self.thread_id = thread_id