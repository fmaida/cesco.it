---
title: How to Extract Text from a Web Page with Python and Newspaper
date: 2019-09-23
image: post/python_newspaper.jpg
description: 
  Learn how to extract text from a web page in minutes using Python and the Newspaper library.
tags:
- python
---

Sometimes, you might need to extract an article from a web page. If you've tried the "Reader Mode" in Firefox and Safari or used specific software like [Pocket](https://www.getpocket.com) or [Instapaper](https://www.instapaper.com), you can probably imagine what I'm talking about.

You can replicate the functionality of these tools in Python, thanks to a fantastic library called `newspaper`. Its usage is quite straightforward, and I'll explain it briefly below:

## Installation

To make the library work with Python 3.5 or higher, you first need to install some dependencies: `libxml2`, `libxslt`, `libtiff`, `libjpeg`, `webp`, and `little-cms2`. For example, on macOS, you can use the following commands to install what you need:

```sh
brew install libxml2 libxslt
brew install libtiff libjpeg webp little-cms2
```

Once you have these dependencies installed, you can proceed to install Newspaper using `pip`:

```sh
pip install newspaper3k
```

Newspaper is now installed, but not completely. In fact, if you want to use the AI functions for text analysis, you'll also need to download some certificates and dictionaries from the web that Newspaper uses for text analysis. You can use this script to install them:

```sh
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python
```

Once Newspaper and its dependencies are installed, you're finally ready to use it.

## Using Newspaper

In Python, import the library with the following command:

```python
from newspaper import Article
```

Decide on the URL of the article you want to analyze, for example:

```python
url = "http://www.ilfattoquotidiano.it/2017/08/07/google-tra-uomini-e-donne-ci-sono-differenze-biologiche-bufera-sulla-mail-dellingegnere-che-giustifica-le-disciminazioni/3780862/"
```

Then create an instance of the Article class, passing the article's URL as a parameter:

```python
article = Article(url)
```

Next, instruct the instance to download the article from the web and parse it:

```python
article.download()
article.parse()
```

If you also want to use the artificial intelligence functions to analyze the article's content and extract a summary (which rely on the `nltk` library, installed along with Newspaper), enter the command:

```python
article.nlp()
```

Now you can finally extract the information you're interested in:

```python
title = article.title       # The article's title
authors = article.authors   # An array with the article's authors
keywords = article.keywords # An array with keywords extracted from the article by AI
                            #     (remember to call article.nlp() first)
text = article.text         # The text extracted from the article
summary = article.summary   # The article's summary extracted by AI
                            #     (remember to call article.nlp() first)
```

That's it. As you can easily imagine, the most challenging part is installing the required dependencies. Otherwise, the library is very straightforward and intuitive to use.