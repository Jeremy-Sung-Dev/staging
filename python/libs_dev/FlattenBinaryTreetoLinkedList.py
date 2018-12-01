#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" FlattenBinaryTreetoLinkedList.py

Challenges: https://www.lintcode.com/problem/flatten-binary-tree-to-linked-list/description?_from=ladder&&fromId=4
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 10/5/2018 4:06 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class TreeNode:
  def __init__(self, val):
    self.val = val
    self.left, self.right = None, None


class FlattenBinaryTreetoLinkedList:

  def __init__(self):
    pass

  def flatten(self, root):
    """
    @param root: a TreeNode, the root of the binary tree
    @return: nothing
    """

    rootNode = TreeNode(root)

    queue = [rootNode]
    result = []

    while queue:

      head = queue.pop()
      result.append(head.val)

      if head.left:
        queue.append(head.left)
      elif head.right:
        queue.append(head.right)




if __name__ == "__main__":
  FlattenBinaryTreetoLinkedList = FlattenBinaryTreetoLinkedList()


