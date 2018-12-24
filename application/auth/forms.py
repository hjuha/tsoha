from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField

class LoginForm(FlaskForm):
	username = StringField("Käyttäjänimi")
	password = PasswordField("Salasana")
	
	class Meta:
		csrf = False
  
class RegisterForm(FlaskForm):
	username = StringField("Käyttäjänimi")
	email = StringField("Sähköposti")
	first_name = StringField("Etunimi")
	surname = StringField("Sukunimi")
	password = PasswordField("Salasana")
	password_confirmation = PasswordField("Salasana uudelleen")

	class Meta:
		csrf = False