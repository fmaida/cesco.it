---
title: How to Read an RSS Feed with Python and the Feedparser Library
author: Francesco Maida
date: 2019-09-28 18:00:00
image: post/feed_rss.jpg
tags:
- python
- rss
---

Sometimes, it can be useful to keep track of updates on a website. If the website provides an RSS/Atom feed, the simplest way to do this is by reading the feed to see the latest published articles.

Thanks to an excellent and easy-to-use Python library called `feedparser`, this task can be accomplished with just a few lines of code.

## Installing the Library

To install the library, you can use `pip` from the terminal by typing:

```bash
pip install feedparser
```

## How to Use the Library

Let's now create a small script to fetch the latest news from the RSS feed of "Il Fatto Quotidiano" website:

```python
import feedparser

# Open the feed
feed = feedparser.parse("https://www.ilfattoquotidiano.it/feed/")

# For each article in the feed
for article in feed.entries:
    
    # Get the title and summary
    title = article["title"]
    summary = article["summary"]
    link = article["link"]
    
    # Print the title and summary of the article
    print("{}\n---\n{}\n\n".format(title, summary))
```

That's it. Simple, isn't it?