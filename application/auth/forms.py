from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
	username = StringField("Käyttäjänimi")
	password = PasswordField("Salasana")
	
	class Meta:
		csrf = False
  
class RegisterForm(FlaskForm):
	username = StringField("Käyttäjänimi", [validators.Length(min=3, max=15, message="Käyttäjänimen pituuden pitää olla 3-15 merkkiä")])
	email = StringField("Sähköposti", [validators.Email(message="Virheellinen sähköpostiosoite")])
	first_name = StringField("Etunimi", [validators.Length(min=2, max=25, message="Etunimen pituuden pitää olla 2-25 merkkiä")])
	surname = StringField("Sukunimi", [validators.Length(min=2, max=25, message="Sukunimen pituuden pitää olla 2-25 merkkiä")])
	password = PasswordField("Salasana", [validators.Length(min=8, message="Salasanan tulee olla vähintään 8 merkkiä"),
										  validators.Regexp(".*[0-9].*[a-z].*[A-Z].*|.*[0-9].*[A-Z].*[a-z].*|.*[a-z].*[0-9].*[A-Z].*|.*[a-z].*[A-Z].*[0-9].*|.*[A-Z].*[0-9].*[a-z].*|.*[A-Z].*[0-9].*[a-z].*", message="Salasanassa tulee olla pieniä ja isoja kirjaimia sekä numeroita")])
	password_confirmation = PasswordField("Salasana uudelleen")

	class Meta:
		csrf = False