from application import db
from application.models import Base

class Vote(Base):
	sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False, index = True)
	post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable = False, index = True)
	value = db.Column(db.Integer, nullable = False)

	def __init__(self, value, post_id, sender_id):
		self.value = value
		self.sender_id = sender_id
		self.post_id = post_id