#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" surroundedRegions.py

Challenges: https://www.lintcode.com/problem/surrounded-regions/description?_from=ladder&&fromId=14
Solutions: https://www.jiuzhang.com/solution/surrounded-regions/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/18/2018 5:15 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class surroundedRegions:

  def surroundedRegions(self, board):
    """
    @param: board: board a 2D board containing 'X' and 'O'
    @return: nothing
    """

    if not any(board):
      return

    n, m = len(board), len(board[0])
    q = [ij for k in range(max(n, m)) for ij in ((0, k), (n - 1, k), (k, 0), (k, m - 1))]
    while q:
      i, j = q.pop()
      if 0 <= i < n and 0 <= j < m and board[i][j] == 'O':
        board[i][j] = 'W'
        q += (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)

    board[:] = [['XO'[c == 'W'] for c in row] for row in board]

if __name__ == "__main__":
  surroundedRegions = surroundedRegions()

  input = ["XXXX","XOOX","XXOX","XOXX"]  ## Output: ["XXXX","XXXX","XXXX","XOXX"]


