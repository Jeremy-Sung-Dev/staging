#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" convertBST_to_GreaterTreepy

Challenges: https://www.lintcode.com/problem/convert-bst-to-greater-tree/description?_from=ladder&&fromId=14
Solutions:  https://www.jiuzhang.com/solution/convert-bst-to-greater-tree/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/18/2018 11:12 AM
  __Email__ = Jeremy.Sung@osh.com

"""


class TreeNode:
  ## Definition of  TreeNode:
  def __init__(self, val):
    self.val = val
    self.left, self.right = None, None

class convertBST_to_GreaterTree:

  ## Ref: https://www.jiuzhang.com/solution/convert-bst-to-greater-tree/#tag-highlight-lang-python

  def convertBST(self, root):
    self.sum = 0
    self.helper(root)
    return root

  def helper(self, root):
    if root is None:
      return
    if root.right:
      self.helper(root.right)

    self.sum += root.val
    root.val = self.sum
    if root.left:
      self.helper(root.left)



if __name__ == "__main__":
  convertBST_to_Greater_Tree = convertBST_to_GreaterTree()

  ## {5,2,13}  ## Expected: {18,20,13}


