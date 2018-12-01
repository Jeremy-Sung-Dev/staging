#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" myQueue.py
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/24/2018 4:56 PM
  __Email__ = Jeremy.Sung@osh.com

"""

from collections import deque


class myQueue:
  """ Implement using List[] """

  def __init__(self):
    self.items = []

  def isEmpty(self):
    return self.items == []

  def enqueue(self, item):
    self.items.insert(0, item)  ## O(N) !!

  def dequeue(self):
    return self.items.pop()  ## O(1)


  def size(self):
    return len(self.items)







if __name__ == "__main__":
  myQueue = myQueue()


