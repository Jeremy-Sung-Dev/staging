#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" wordBreak.py

Challenges: https://www.lintcode.com/problem/word-break-ii/description?_from=ladder&&fromId=14
Solutions: https://www.jiuzhang.com/solution/word-break-ii/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/18/2018 12:07 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class wordBreak:

  def wordBreak(self, s, wordDict):
    pass


if __name__ == "__main__":

  wordBreak = wordBreak()

  s = "lintcode"
  dict = ["de", "ding", "co", "code", "lint"]  ## A solution is ["lint code", "lint co de"].

  print(wordBreak.wordBreak(s, dict))

