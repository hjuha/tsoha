# Toteutusdokumentti

Ohjelmisto toteutettiin käyttäen Pythonille tehtyä web-kehystä Flaskia. Sivujen muotoilu toteutettiin Jinja2:lla, tietokantaoperaatiot SQLAlchemy:llä, useimmat kaavakkeet WTForms:lla ja salasanojen salaus bcrypt:llä.

## Dokumentaation vastaavuus toteutukseen

Kaikki dokumentoidut ominaisuudet on implementoitu, ja vastaavasti kaikki, mikä on implementoitu, on myös dokumentoitu.

## Puutteet ja rajoitteet

* Viestiketjujen olisi hyvä ilmaista käyttäjälle, mikäli niissä on lukemattomia viestejä. Mahdollisesti käyttäjä voisi myös saada erillisen ilmoituksen, mikäli viestiketjuun, johon hän on vastannut, on tullut uusia viestejä.
* Viesteihin olisi käytännöllistä saada muotoilukieli, jolla niitä voisi muotoilla ja jolla niihin voisi liittää linkkejä ja kuvia.
* Hyödyllinen ominaisuus olisi myös mahdollistaa vastaaminen yksittäiseen viestiin.
* Käyttäjälle mahdollisuus omien tietojensa muuttamiseen ja salasanan palauttamiseen tarvitaan.