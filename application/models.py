from application import db
from application.utils.date_format import date_to_string

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key = True, index = True)
	date_created = db.Column(db.DateTime, default = db.func.current_timestamp(), index = True)
	date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())

	def get_created(self):
		return date_to_string(self.date_created)

	def get_modified(self):
		return date_to_string(self.date_modified)