#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" numDecodings.py

Challenges: https://www.lintcode.com/problem/decode-ways/description
Solutions: https://www.jiuzhang.com/solution/decode-ways/#tag-other-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/22/2018 3:54 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class numDecodings:

  def numDecodings(self, s):
    N = len(s)

    def check1(d):
      if ord('1') <= ord(d) <= ord('9'):
        return 1
      else:
        return 0

    def check2(d1, d2):
      if d1 == '0':
        return 0
      elif 1 <= int(d1 + d2) <= 26:
        return 1
      else:
        return 0

    if N == 0:
      return 0
    if N == 1:
      return check1(s[0])
    if N == 2:
      return check1(s[0]) * check1(s[1]) + check2(s[0], s[1])

    dp = ['?'] * N
    dp[0] = check1(s[0])
    dp[1] = check1(s[0]) * check1(s[1]) + check2(s[0], s[1])

    for i in range(2, N):
      dp[i] = check1(s[i]) * dp[i - 1] + check2(s[i - 1], s[i]) * dp[i - 2]

    return dp[-1]

if __name__ == "__main__":
  numDecodings = numDecodings()


