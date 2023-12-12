---
title: Come leggere un feed RSS con Python e la libreria Feedparser
author: Francesco Maida
date: 2019-09-28 18:00:00
summary:
    Scrivere un semplice programma in Python per leggere un feed in formato RSS/Atom
image: post/feed_rss.jpg
tags:
    - python
    - rss
aliases:
    - "/blog/leggere-feed-rss-con-feedparser"
---
A volte potrebbe essere utile poter essere in grado di tenere sotto controllo gli aggiornamenti di un sito internet. Se il sito pubblica un feed RSS/Atom, il sistema più semplice per farlo è quello di leggere questo feed per vedere quali sono stati gli ultimi articoli pubblicati.

Grazie ad un'eccellente e semplice libreria per Python, chiamata `feedparser` questo controllo può essere effettuato con poche righe di codice.

## Installiamo la libreria

Per installare la libreria possiamo utilizzare `pip` da terminale, digitando:

```bash
pip install feedparser
```

## Come usare la libreria

Creiamo adesso un piccolo script che riporti le ultime notizie dal feed RSS del sito "Il fatto quotidiano":

```python
import feedparser

# Apriamo il feed
feed = feedparser.parse("https://www.ilfattoquotidiano.it/feed/")

# Per ogni articolo nel feed
for articolo in feed.entries:
    
    # Ottiene titolo e sommario
    titolo = articolo["title"]
    sommario = articolo["summary"]
    link = articolo["link"]
    
    # Scrive titolo e sommario dell'articolo
    print("{}\n---\n{}\n\n".format(titolo, sommario))
```

Tutto qua. Semplice, no?
