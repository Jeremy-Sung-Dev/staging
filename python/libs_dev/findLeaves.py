#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" findLeaves.py

Challenges: https://www.lintcode.com/problem/find-leaves-of-binary-tree/description?_from=ladder&&fromId=14
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/18/2018 10:37 AM
  __Email__ = Jeremy.Sung@osh.com

"""


class TreeNode:
  ## Definition of TreeNode:
  def __init__(self, val):
    self.val = val
    self.left, self.right = None, None


class findLeaves:
  ## https://www.jiuzhang.com/solution/find-leaves-of-binary-tree/#tag-other-lang-python

  def findLeaves(self, root):
    # write your code here
    ans = []
    self.depth = {}
    maxDepth = self.dfs(root)
    for i in range(1, maxDepth + 1):
      ans.append(self.depth.get(i))
    return ans


  def dfs(self, node):
    # find depth
    if node is None:
      return 0
    d = max(self.dfs(node.left), self.dfs(node.right)) + 1
    if d not in self.depth:
      self.depth[d] = []
    self.depth[d].append(node.val)
    return d









  ## My failed attempt - Not very clear in all parts:
  def findLeaves(self, root):

    root = TreeNode(root)
    result = []

    stack = [root]

    while stack:

      node = stack.pop()
      temp = []

      if node.left:
        temp.append(node.left)
      elif node.right:
        temp.append(node.right)
      else:
        result.append(node.val)

      result = temp[:]

    return result











if __name__ == "__main__":

  findLeaves = findLeaves()


