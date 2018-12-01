#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" maxTree.py

Challenges: https://www.lintcode.com/problem/max-tree/description?_from=ladder&&fromId=4
Solutions: https://www.jiuzhang.com/solution/max-tree/#tag-highlight-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/26/2018 3:02 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import sys

class TreeNode:
  def __init__(self, val):
    self.val = val
    self.left, self.right = None, None



class maxTree:

  def maxTree(self, A):
    if not A:
      return None

    nodes = [TreeNode(num) for num in A + [sys.maxsize]]
    stack = []
    for index, num in enumerate(A + [sys.maxsize]):
      while stack and A[stack[-1]] < num:
        top = stack.pop()
        left = A[stack[-1]] if stack else sys.maxsize
        if left < num:
          nodes[stack[-1]].right = nodes[top]
        else:
          nodes[index].left = nodes[top]

      stack.append(index)

    # sys.maxsize 's left child is the maximum number
    return nodes[-1].left



if __name__ == "__main__":
  maxTree = maxTree()

  A = [2, 5, 6, 0, 3, 1]

  print(sys.maxsize)


