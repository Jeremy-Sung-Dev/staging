#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" myHashHeap.py

Challenges:
Solutions: https://www.jiuzhang.com/solution/sliding-window-median/#tag-highlight-lang-python

Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/21/2018 4:23 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class myHashHeap:

  def __init__(self, desc=False):
    self.hash = dict()
    self.heap = []
    self.desc = desc

  @property
  def size(self):
    return len(self.heap)

  def push(self, item):
    self.heap.append(item)
    self.hash[item] = self.size - 1
    self._sift_up(self.size - 1)

  def pop(self):
    item = self.heap[0]
    self.remove(item)
    return item

  def top(self):
    return self.heap[0]

  def remove(self, item):
    if item not in self.hash:
      return

    index = self.hash[item]
    self._swap(index, self.size - 1)

    del self.hash[item]
    self.heap.pop()

    # in case of the removed item is the last item
    if index < self.size:
      self._sift_up(index)
      self._sift_down(index)

  def _smaller(self, left, right):
    return right < left if self.desc else left < right

  def _sift_up(self, index):
    while index != 0:
      parent = index // 2
      if self._smaller(self.heap[parent], self.heap[index]):
        break
      self._swap(parent, index)
      index = parent

  def _sift_down(self, index):
    if index is None:
      return
    while index * 2 < self.size:
      smallest = index
      left = index * 2
      right = index * 2 + 1

      if self._smaller(self.heap[left], self.heap[smallest]):
        smallest = left

      if right < self.size and self._smaller(self.heap[right], self.heap[smallest]):
        smallest = right

      if smallest == index:
        break

      self._swap(index, smallest)
      index = smallest

  def _swap(self, i, j):
    elem1 = self.heap[i]
    elem2 = self.heap[j]
    self.heap[i] = elem2
    self.heap[j] = elem1
    self.hash[elem1] = j
    self.hash[elem2] = i



if __name__ == "__main__":
  myHashHeap = myHashHeap()


