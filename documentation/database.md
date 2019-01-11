# Tietokanta

## Tietokantataulut

Kaikki taulut sisältävät niiden tunnisteluvun, luomispäivän ja muokkauspäivän.

### Account

Taulu sisältää yleistä tietoa käyttäjästä, mukaan lukien tämän käyttäjänimen ja salasanan tiivisteen.

```SQL
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	username VARCHAR(30) NOT NULL, 
	first_name VARCHAR(30) NOT NULL, 
	surname VARCHAR(30) NOT NULL, 
	password VARCHAR(256) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	admin BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	CHECK (admin IN (0, 1))
);
```

### Thread

Viestiketjut sisältävät aiheen ja tiedon lähettäjästä.

```SQL
CREATE TABLE thread (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	topic VARCHAR(50) NOT NULL, 
	sender_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sender_id) REFERENCES account (id)
);
```

### Post

Viesti sisältää viestin sisällön ja tunnisteen lähettäjästä ja viestiketjusta. 

```SQL
CREATE TABLE post (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	content VARCHAR(1000) NOT NULL, 
	thread_id INTEGER NOT NULL, 
	sender_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(thread_id) REFERENCES thread (id), 
	FOREIGN KEY(sender_id) REFERENCES account (id)
);
```

### Category

Kategoria sisältää kategorian nimen.

```SQL
CREATE TABLE category (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(25) NOT NULL, 
	PRIMARY KEY (id)
);
```

### Category_Thread

KategoriaViestiketju on liitostaulu joka sisältää viitteen kategoriaan ja viestiketjuun.

```SQL
CREATE TABLE category_thread (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	category_id INTEGER NOT NULL, 
	thread_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES category (id), 
	FOREIGN KEY(thread_id) REFERENCES thread (id)
);
```

### Vote

Ääni sisältää tiedon, onko ääni positiivinen (1) vai negatiivinen (-1), ja käyttäjän ja viestiketjun viitteen.

```SQL
CREATE TABLE vote (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	sender_id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	value INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sender_id) REFERENCES account (id), 
	FOREIGN KEY(post_id) REFERENCES post (id)
);
```

### Indeksit

Ohjelmakoodin puolella kaikki tietokantataulut perivät taulun, joka sisältää sarakkeet `id`, `date_created` ja `date_modified`, joten tämän takia joitakin ylimääräisiä indeksejä syntyy ohjelmistolle.

* Kaikkien taulujen `id`-sarakkeet, sillä tämä nopeuttaa useampia tauluja käyttäviä kyselyitä.
* Kaikkien taulujen `date_created`-sarakkeet, sillä hakutuloksia voidaan järjestää mm. luomisajan mukaan.
* Taulujen `Post` ja `Thread` sarakkeet `sender_id` monitauluisten kyselyiden nopeuttamiseksi.
* Taulun `Post` sarake `thread_id`, sillä tätä käytetään vastausten määrän laskuun.
* Taulun `Category_Thread` sarakkeet `thread_id` ja `sender_id`, joita käytetään kategorioiden ja viestiketjujen liittämiseen.
* Taulun `Vote` sarakkeet `post_id` ja `sender_id`, joita käytetään viestin äänimäärän laskemiseen ja tuplaäänestämisen estämiseen.

## Normalisointi

Tietokanta on toisessa normalimuodossa, mutta ei kolmannessa, sillä `Account`-taulu sisältää mm. transitiivisen riippuvuuden `id` -> `username` -> `first_name`. Kuitenkin käytännöllisyyden ja kyselyiden nopeuden vuoksi katsottiin järkevämmäksi, että tätä ei normalisoida kolmanteen normaalimuotoon.

## Tietokantakaavio

![tietokantakaavio](https://github.com/Kalakuh/tsoha/blob/master/documentation/relation_diagram.png "Tietokantakaavio")