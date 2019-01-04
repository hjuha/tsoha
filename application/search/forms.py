from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators
from wtforms.widgets import TextArea

class SearchForm(FlaskForm):
	contains = StringField("Sisältää tekstin")
	name = StringField("Kirjoittajan nimi")
	after_date = DateField("Kirjoitettu jälkeen", format='%d.%m.%Y')
	before_date = DateField("Kirjoitettu ennen", format='%d.%m.%Y')
	
	class Meta:
		csrf = False