from application import db

class Thread(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	topic = db.Column(db.String(50), nullable=False)
	content = db.Column(db.String(1000), nullable=False)
	sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	posting_time = db.Column(db.DateTime, default=db.func.current_timestamp())

	def __init__(self, topic, content, sender_id):
		self.topic = topic
		self.content = content
		self.sender_id = sender_id