#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" upsideDownBinaryTree.py

Challenges: https://www.lintcode.com/problem/binary-tree-upside-down/description?_from=ladder&&fromId=14
Solutions: https://www.jiuzhang.com/solution/binary-tree-upside-down/#tag-highlight
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/18/2018 12:25 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class TreeNode:
  def __init__(self, val):
    self.val = val
    self.left, self.right = None, None


class upsideDownBinaryTree:

  def dfs(self, curNode):

    if curNode.left is None:
      return curNode

    newHead = self.dfs(curNode.left)

    curNode.left.right = curNode
    curNode.left.left = curNode.right
    curNode.left = None
    curNode.right = None

    return newHead


  def upsideDownBinaryTree(self, root):

    rootNode = TreeNode(root)

    if rootNode is None:
      return None

    return self.dfs(rootNode)


if __name__ == "__main__":

  upsideDownBinaryTree = upsideDownBinaryTree()

  bt = {1,2,3,4,5}  ## Expected: {4,5,2,#,#,3,1}


