#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" RussianDollEnvelopes.py

Challenges: https://www.lintcode.com/problem/russian-doll-envelopes/description
Solutions:  https://www.jiuzhang.com/solution/russian-doll-envelopes/#tag-highlight-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/7/2018 3:52 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class RussianDollEnvelopes:

  def __init__(self):
    pass


  def maxEnvelopes(self, envelopes):
    # Write your code here
    height = [a[1] for a in sorted(envelopes, key = lambda x: (x[0], -x[1]))]
    dp, length = [0] * len(height), 0

    import bisect
    for h in height:
      i = bisect.bisect_left(dp, h, 0, length)
      dp[i] = h
      if i == length:
        length += 1
    return length

  def maxEnvelopes_MyFailedAttempt(self, envelopes):

    envelopes.sort()

    ## print(envelopes)
    ## return envelopes

    maxCount = 0
    lenE = len(envelopes)

    for i in range(lenE):
      envelopes[i]



if __name__ == "__main__":

  russiandollenvelopes = RussianDollEnvelopes()

  envelopes = [[5,4],[6,4],[6,7],[2,3]]  #R Expect : 3

  print(russiandollenvelopes.maxEnvelopes(envelopes))
