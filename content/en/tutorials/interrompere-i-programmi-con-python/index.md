---
title: Handling Program Interruption with Python
date: 2023-03-02 08:44:21
image: post/zoom.bomb_.shutterstock.jpg
tags:
  - python
---

Even program execution interruption can be handled as an _exception_ in Python. This way, you can react when a user presses CTRL+C.

```python
from time import sleep

for i in range(10, 0, -1):
    try:
        print(i)
        sleep(1)
    except KeyboardInterrupt:
        print(f"You stopped the countdown at -{i}...")
        quit()
print("BOOM!!!")
```