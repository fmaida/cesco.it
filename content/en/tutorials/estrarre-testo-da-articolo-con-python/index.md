---
title: Come estrarre i testi di una pagina web con Python e Newspaper
date: 2019-09-23
image: post/python_newspaper.jpg
description: 
  Come estrarre i testi di un articolo di una pagina web 
  in pochi minuti, utilizzando python e la libreria newspaper.
tags:
- python
---
A volte potremmo aver bisogno di estrapolare un articolo da una pagina web. Se avete provato la modalità articolo di Firefox e Safari, o se avete utilizzato software specifici come [Pocket](https://www.getpocket.com) o [Instapaper](https://www.instapaper.com) credo che possiate immaginare quello di cui vi voglio parlare.

Possiamo replicare le funzionalità di questi software in Python, grazie ad una fantastica libreria chiamata `newspaper`.
Il suo utilizzo è piuttosto semplice, eccolo descritto in breve:

## Installazione

Per installare la libreria in modo che funzioni con Python 3.5 o superiori, avrò innanzitutto bisogno di installare alcune dipendenze: `libxml2`, `libxslt`, `libtiff`, `libjpeg`, `webp` e `little-cms2`.  
Ad esempio su macOS utilizzo questi due comandi per installare tutto quello di cui ho bisogno:

```sh
brew install libxml2 libxslt
brew install libtiff libjpeg webp little-cms2
```

una volta installate queste dipendenze posso procedere ad installare newspaper utilizzando `pip`:

```sh
pip install newspaper3k
```

Newspaper è ora installato, ma non del tutto. Infatti, se desidero utilizzare le funzioni di IA per l'analisi dei testi degli articoli avrò anche bisogno di scaricare alcuni certificati e dizionari dal web che servono a Newspaper per effettuare l'analisi dei testi.
Per installarle posso utilizzare questo script:

```sh
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python
```

Una volta installato newspaper e le sue dipendenze, sono finalmente pronto ad utilizzarlo.


Utilizzo di newspaper
---------------------

Da Python importo la libreria con il comando

```python
from newspaper import Article
```

Decido qual'è l'URL con l'articolo che voglio analizzare, ad esempio:

```python
url = "http://www.ilfattoquotidiano.it/2017/08/07/google-tra-uomini-e-donne-ci-sono-differenze-biologiche-bufera-sulla-mail-dellingegnere-che-giustifica-le-disciminazioni/3780862/"
```

creo quindi un'istanza della classe Article, passandogli come parametro l'URL all'articolo che voglio importare:

```python
articolo = Article(url)
```

Quindi chiedo all'istanza di scaricare l'articolo dal web e di analizzarlo:

```python
articolo.download()
articolo.parse()
```

Se voglio anche utilizzare le funzioni di intelligenza artificiale che analizzano il contenuto dell'articolo e ne estraggono il riassunto (che si basano sulla libreria `nltk` installata assieme a newspaper), devo digitare il comando:

```python
articolo.nlp()
```

Ora posso finalmente estrarre le informazioni che mi interessano:

```python
titolo = articolo.title      # Il titolo dell'articolo
autori = articolo.authors    # Un array con gli autori dell'articolo
parole = articolo.keywords   # Un array con le parole chiave 
                             #     dell'articolo estratte dall'IA
                             #     ( prima devo richiamare articolo.nlp() )
testo = articolo.text        # Il testo estrapolato dall'articolo
sommario = articolo.summary  # Il sommario dell'articolo 
                             #     estratto dall'IA 
                             #     ( prima devo richiamare articolo.nlp() )
```

Tutto qui. Come potete facilmente immaginare, la difficoltà maggiore è soltanto quella di installare le dipendenze richieste. Per il resto, la libreria è veramente semplice ed intuitiva da utilizzare.
