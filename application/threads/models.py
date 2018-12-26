from application import db
from application.models import Base

class Thread(Base):
	topic = db.Column(db.String(50), nullable = False)
	sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)

	posts = db.relationship("Post", backref = "thread", lazy = True)

	def __init__(self, topic, sender_id):
		self.topic = topic
		self.sender_id = sender_id

class Post(Base):
	content = db.Column(db.String(1000), nullable = False)

	sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
	thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"), nullable = False)

	def __init__(self, content, sender_id, thread_id):
		self.content = content
		self.sender_id = sender_id
		self.thread_id = thread_id