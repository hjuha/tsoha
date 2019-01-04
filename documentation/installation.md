# Asennusohje

## Vaaditut työvälineet

* Aloita asentamalla [Pythonin](https://www.python.org/downloads/) versio 3.5 tai uudempi.
* Tarvitset pakettienhallintajärjestelmän [pip](https://packaging.python.org/key_projects/#pip), joka asentuu todennäköisesti valmiiksi Pythonin mukana.
* Lisäksi tarvitset virtuaaliympäristöjä varten kirjaston [venv](https://docs.python.org/3/library/venv.html), joka tulee luultavimmin edellisten yhteydessä.
* Asenna [git](https://git-scm.com/downloads/)-versionhallintaohjelmisto.
* Lopuksi tarvitaan vielä [PostgreSQL](https://www.postgresql.org/)-tietokannanhallintajärjestelmä.

## Asennus

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

Nyt kaikki on valmista palvelimen käynnistämistä varten. Tehdään tämä komennolla

```bash
python3 run.py
```

Nyt palvelin on päällä. Mennään vielä selaimella osoitteeseen `/register/` ja luodaan käyttäjätunnus. Tämän jälkeen avataan tietokannanhallintasovelluksella tietokanta `application/forum.db`, ja suoritetaan seuraava SQL-komento, jossa `?` on korvattu luomasi tunnuksen käyttäjänimellä

```SQL
UPDATE Account SET admin = TRUE WHERE username = '?';
```

Palvelin on nyt toiminnassa ja käyttäjätunnuksesi sen ylläpitäjä.
