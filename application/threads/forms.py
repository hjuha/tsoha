from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.widgets import TextArea

class ThreadForm(FlaskForm):
	topic = StringField("Aihe", [validators.Length(min=2, max=50)])
	content = StringField("Content", [validators.Length(min=2, max=1000)], widget = TextArea())

	class Meta:
		csrf = False