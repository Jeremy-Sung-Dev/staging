#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" flattenList.py

Challenges: https://www.lintcode.com/problem/flatten-list/description?_from=ladder&&fromId=4
Solutions: https://www.jiuzhang.com/solution/flatten-list/#tag-highlight-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 10/5/2018 3:53 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class flattenList:

  def __init__(self):
    pass

  def flatten(self, nestedList):
    # @param nestedList a list, each element in the list
    # can be a list or integer, for example [1,2,[1,2]]
    # @return {int[]} a list of integer
    stack = [nestedList]
    flatten_list = []

    while stack:
      top = stack.pop()
      if isinstance(top, list):
        for elem in reversed(top):
          stack.append(elem)
      else:
        flatten_list.append(top)

    return flatten_list



if __name__ == "__main__":
  flattenList = flattenList()

  nestedList = [[1,1],2,[1,1]]
  print(flattenList.flatten(nestedList))


