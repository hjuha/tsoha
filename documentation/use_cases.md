# Käyttötapaukset

Ohjelmassa on kolme käyttäjäryhmää: kirjautumaton käyttäjä, (kirjautunut) käyttäjä ja ylläpitäjä. Käyttäjä voi tehdä kaiken mitä kirjautunut käyttäjä voi tehdä, ja vastaavasti ylläpitäjä voi tehdä kaiken mitä käyttäjä voi tehdä.

## Etusivu

* Kirjautumaton käyttäjä näkee etusivulla viimeisimmät viestiketjut
```SQL
SELECT * FROM Thread;
```
* Kirjautumaton käyttäjä näkee etusivulla käyttäjien, aktiivisten käyttäjien, viestiketjujen ja viestien määrän
```SQL
SELECT COUNT(Accout.id) FROM Account;

SELECT COUNT(DISTINCT Account.id) FROM Account
	LEFT JOIN Post ON Post.sender_id = Account.id
	WHERE Post.date_modified >= ?;

SELECT COUNT(Thread.id) FROM Thread;

SELECT COUNT(Post.id) FROM Post;
```

## Käyttäjä

* Kirjautumaton käyttäjä voi luoda käyttäjätunnuksen
```SQL
INSERT INTO Account(date_created, date_modified, username, first_name, surname, password, email, admin) VALUES(?, ?, ?, ?, ?, ?, ?, FALSE);
```
* Kirjautumaton käyttäjä voi kirjautua sisään käyttäjätunnuksellaan
```SQL
SELECT * FROM Account WHERE Account.username = ? AND Account.password = ?;
```
* Käyttäjä voi kirjautua ulos käyttäjätunnukseltaan

## Käyttäjäsivu

* Kirjautumaton käyttäjä voi katsoa käyttäjien käyttäjäsivuja
```SQL
SELECT * FROM Account WHERE Account.id = ?;
```
* Kirjautumaton käyttäjä voi nähdä käyttäjän viimeisimmät viestiketjut ja viestit tämän käyttäjäsivulla
```SQL
SELECT Thread.id as id
	FROM Thread
	WHERE Thread.sender_id = ?
	ORDER BY Thread.date_created DESC
	LIMIT 10;

SELECT Post.id as id
	FROM Post
	WHERE Post.sender_id = ?
	ORDER BY Post.date_created DESC
	LIMIT 10;
```
* Kirjautumaton käyttäjä näkee tunnuksen iän ja luotujen viestien ja viestiketjujen määrän käyttäjän käyttäjäsivulla
```SQL
SELECT COUNT(Thread.id) FROM Thread WHERE Thread.sender_id = ?;

SELECT COUNT(Post.id) FROM Post WHERE Post.sender_id = ?;
```
* Ylläpitäjä voi tehdä muista käyttäjistä ylläpitäjiä näiden käyttäjäsivulla
```SQL
UPDATE Account SET admin = TRUE WHERE username = ?;
```
* Ylläpitäjä voi poistaa muiden käyttäjien ylläpito-oikeudet näiden käyttäjäsivulla
```SQL
UPDATE Account SET admin = FALSE WHERE username = ?;
```

## Viestiketju

* Kirjautumaton käyttäjä voi lukea viestiketjuja
```SQL
SELECT * FROM Thread WHERE id = ?;

SELECT * FROM Post WHERE Post.thread_id = ?;
```
* Käyttäjä voi luoda viestiketjun
```SQL
INSERT INTO Thread(date_created, date_modified, topic, sender_id) VALUES(?, ?, ?, ?);
```
* Käyttäjä voi poistaa oman viestiketjunsa
```SQL
DELETE FROM Thread WHERE id = ?;
```
* Käyttäjä voi lisätä oman viestiketjunsa eri kategorioihin
```SQL
INSERT INTO Category_Thread(date_created, date_modified, category_id, thread_id) VALUES(?, ?, ?, ?);
```
* Käyttäjä voi lisätä viestin viestiketjuun
```SQL
INSERT INTO Post(date_created, date_modified, content, thread_id, sender_id) VALUES(?, ?, ?, ?, ?);
```
* Käyttäjä voi muokata oman viestiketjunsa aihetta
```SQL
UPDATE Thread SET topic = ? WHERE id = ?;
```
* Ylläpitäjä voi muokata viestiketjun aihetta
```SQL
UPDATE Thread SET topic = ? WHERE id = ?;
```
* Ylläpitäjä voi poistaa viestiketjun
```SQL
DELETE FROM Thread WHERE id = ?;
```

## Viesti

* Kirjautumaton käyttäjä voi avata viestin sivun painamalla viestiketjussa sen aikaleimaa
```SQL
SELECT * FROM Post WHERE id = ?;
```
* Kirjautumaton käyttäjä näkee viestissä äänten yhteissumman
```SQL
SELECT SUM(Vote.value) FROM Vote
	WHERE Vote.post_id = ?;
```
* Käyttäjä voi muokata omaa viestiään
```SQL
UPDATE Post SET content = ? WHERE id = ?;
```
* Käyttäjä voi poistaa oman viestinsä
```SQL
DELETE FROM Post WHERE id = ?;
```
* Käyttäjä voi äänestää pitääkö viestistä
```SQL
INSERT INTO Vote(date_created, date_modified, sender_id, post_id, value) VALUES(?, ?, ?, ?, ?);
```
* Käyttäjä näkee viestissä oman äänensä
```SQL
SELECT value FROM Post WHERE sender_id = ? AND post_id = ?;
```
* Ylläpitäjä voi muokata viestejä
```SQL
UPDATE Post SET content = ? WHERE id = ?;
```
* Ylläpitäjä voi poistaa viestejä
```SQL
DELETE FROM Post WHERE id = ?;
```

## Kategoria

* Ylläpitäjä voi luoda kategorioita
```SQL
INSERT INTO Category(date_created, date_modified, name) VALUES(?, ?, ?);
```
* Ylläpitäjä voi muuttaa kategorian nimeä
```SQL
UPDATE Category SET name = ? WHERE id = ?;
```
* Ylläpitäjä voi poistaa kategorioita
```SQL
DELETE FROM Category WHERE id = ?;
```

## Haku

* Kirjautumaton käyttäjä voi hakea viestiketjuja sisällön, ajan, kirjoittajan ja kategorian perusteella
```
Kysely rakennetaan dynaamisesti
```
* Kirjautumaton käyttäjä voi hakea viestejä sisällön, ajan, kirjoittajan ja kategorian perusteella
```
Kysely rakennetaan dynaamisesti
```
* Kirjautumaton käyttäjä voi järjestää hakutulokset ajan tai vastausten määrän perusteella
```
Kysely rakennetaan dynaamisesti
```
* Kirjautumaton käyttäjä voi järjestää hakutulokset käänteiseen järjestykseen niin halutessaan
```
Kysely rakennetaan dynaamisesti
```