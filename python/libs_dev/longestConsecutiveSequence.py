#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" longestConsecutiveSequence.py

Challenges:  https://www.lintcode.com/problem/longest-consecutive-sequence/description?_from=ladder&&fromId=14
Solutions:  https://www.jiuzhang.com/solution/longest-consecutive-sequence/#tag-highlight-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/17/2018 6:35 PM
  __Email__ = Jeremy.Sung@osh.com

"""


## class longestConsecutiveSequence:


# O(n)
class longestConsecuritveSequence_Sol_N:
  """
  @param num, a list of integer
  @return an integer
  """

  def longestConsecutive(self, num):
    # write your code here
    dict = {}

    for x in num:
      dict[x] = 1

    ans = 0

    for x in num:
      if x in dict:
        len = 1
        del dict[x]
        l = x - 1
        r = x + 1
        while l in dict:
          del dict[l]
          l -= 1
          len += 1
        while r in dict:
          del dict[r]
          r += 1
          len += 1
        if ans < len:
          ans = len

    return ans

# O(nlogn)
class longestConsecuritveSequence_Sol_NlogN:
  # @param num, a list of integer
  # @return an integer
  def longestConsecutive(self, num):
    num.sort()
    l = num[0]
    ans = 1
    tmp = 1
    for n in num:
      if (n - l == 0):
        continue;
      elif (n - l == 1):
        tmp += 1
      else:
        if tmp > ans:
          ans = tmp
        tmp = 1
      l = n
    if tmp > ans:
      ans = tmp
    return ans

if __name__ == "__main__":
  longestConsecutiveSequence = longestConsecuritveSequence_Sol_N()

  input = [0]  # Expected output: 1


