#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" inorderTraversal.py

Challenges: https://lintcode.com/problem/binary-tree-inorder-traversal/description
Solutions:  https://www.jiuzhang.com/solution/binary-tree-inorder-traversal/#tag-highlight
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/6/2018 4:12 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class TreeNode:
  def __init__(self, val):
    self.val = val
    self.left, self.right = None, None


class inorderTraversal:

  def inorderTraversal(self, root):

    result = []

    if not root:
      return result

    stack = []
    while root:
      stack.append(root)
      root = root.left

    while stack:
      cur = stack.pop()
      result.append(cur.val)

      if cur.right:
        cur = cur.right
        while cur:
          stack.append(cur)
          cur = cur.left

    return result


if __name__ == "__main__":

  inordertraversal = inorderTraversal()

  ## bTree = {1,r'#',2,3}   ## Expect: [1,3,2]
  bTree = {1,r'#',2,3}      ## Expect: [2, 1, 3]

  print( inordertraversal.inorderTraversal(bTree) )  ## Expect:


