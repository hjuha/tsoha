from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CategoryForm(FlaskForm):
	name = StringField("Nimi", [validators.Length(min=2, max=20, message="Kategorian nimen pitää olla 2-25 merkkiä")])

	class Meta:
		csrf = False