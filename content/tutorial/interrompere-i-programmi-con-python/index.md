---
title: Gestire l'interruzione di un programma con Python
date: 2023-03-02 08:44:21
image: post/zoom.bomb_.shutterstock.jpg
tags:
  - python
aliases:
  - "/blog/2023-03-02-gestire-interruzione-del-programma-python"
---

Anche l'interruzione dell'esecuzione del vostro programma può essere gestito come un'_eccezione_ in Python. In questo modo potete reagire quando un utente preme CTRL+C.

```python
from time import sleep   

for i in range(10, 0, -1):     
    try:
        print(i)
        sleep(1)
    except KeyboardInterrupt:
        print(f"Hai fermato la bomba a -{i}...")
        quit()
print("BOOM!!!") 
```
