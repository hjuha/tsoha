# Asennusohje

## Vaaditut työvälineet

* Aloita asentamalla [Pythonin](https://www.python.org/downloads/) versio 3.5 tai uudempi.
* Tarvitset pakettienhallintajärjestelmän [pip](https://packaging.python.org/key_projects/#pip), joka asentuu todennäköisesti valmiiksi Pythonin mukana.
* Lisäksi tarvitset virtuaaliympäristöjä varten kirjaston [venv](https://docs.python.org/3/library/venv.html), joka tulee luultavimmin edellisten yhteydessä.
* Asenna [git](https://git-scm.com/downloads/)-versionhallintaohjelmisto.
* Asenna Herokun [työvälineet](https://devcenter.heroku.com/articles/heroku-cli) ja [luo tunnus](https://www.heroku.com/) palveluun.
* Lopuksi tarvitaan vielä [PostgreSQL](https://www.postgresql.org/)-tietokannanhallintajärjestelmä.

## Asennus ja ajaminen lokaalisti

Aloitetaan kloonaamalla projekti komennolla

```
git clone --recursive https://github.com/Kalakuh/tsoha
```

Luodaan kansio `venv` virtuaaliympäristöä varten komennolla

```
python3 -m venv venv
```

Aktivoidaan nyt virtuaaliympäristö käskyllä

```
source venv/bin/activate
```

Nyt kun olemme virtuaaliympäristössä, voimme asentaa ohjelmiston vaatimat riippuvuudet ajamalla komennon

```bash
pip install -r requirements.txt
```

Nyt kaikki on valmista palvelimen lokaalia käynnistämistä varten. Tehdään tämä komennolla

```bash
python3 run.py
```

Nyt palvelin on päällä. Mennään vielä selaimella osoitteeseen `http://127.0.0.1:5000/register/` ja luodaan käyttäjätunnus. Tämän jälkeen avataan tietokannanhallintasovelluksella tietokanta `application/forum.db`, ja suoritetaan seuraava SQL-komento, jossa `?` on korvattu luomasi tunnuksen käyttäjänimellä

```SQL
UPDATE Account SET admin = 0 WHERE username = '?';
```

Palvelin on nyt toiminnassa ja käyttäjätunnuksesi sen ylläpitäjä.

## Asennus ja ajaminen Herokussa

Aloitetaan kloonaamalla projekti komennolla

```bash
git clone --recursive https://github.com/Kalakuh/tsoha
```

Siirrytään luotuun kansioon, ja ajetaan komento

```bash
heroku create projektinimi
```

Missä `projektinimi` on projektiasi kuvaava nimi. Nyt tehdään seuraava komento lisätäksemme paikalliseen versiohallintaan tieto Herokusta

```bash
git remote add heroku https://git.heroku.com/projektinimi.git
```

Ja lopuksi lähetetään projekti Herokuun:

```bash
git add .
git commit -m "Initial commit"
git push heroku master
```

Hakeudutaan osoitteeseen `https://projektinimi.herokuapp.com/register/` ja luodaan käyttäjätili. Ylennetään tämä käyttäjäksi suorittamalla terminaalissa

```bash
heroku pg:psql
```

Ja ajamalla seuraava SQL-komento, jossa `?` on korvattu luomasi tunnuksen käyttäjänimellä

```SQL
UPDATE Account SET admin = TRUE WHERE username = '?';
```