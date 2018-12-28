from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CategoryForm(FlaskForm):
	name = StringField("Nimi", [validators.Length(min=1, max=25, message="Kategorian nimen pitää olla 2-25 merkkiä")])

	class Meta:
		csrf = False