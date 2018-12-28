from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.widgets import TextArea

class ThreadForm(FlaskForm):
	topic = StringField("Aihe", [validators.Length(min=1, max=50, message="Aiheen pituuden pitää olla 1-50 merkkiä")])
	content = StringField("Viesti", [validators.Length(min=1, max=1000, message="Viestin pituuden pitää olla 1-1000 merkkiä")], widget = TextArea())

	class Meta:
		csrf = False

class PostForm(FlaskForm):
	content = StringField("Vastaus", [validators.Length(min=1, max=1000, message="Viestin pituuden pitää olla 1-1000 merkkiä")], widget = TextArea())

	class Meta:
		csrf = False