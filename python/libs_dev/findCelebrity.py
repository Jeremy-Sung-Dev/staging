#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" findCelebrity.py

Challenges: https://www.lintcode.com/problem/find-the-celebrity/description?_from=ladder&&fromId=14
Solutions: https://www.jiuzhang.com/solution/find-the-celebrity/

The knows API is already defined for you.
@param a, person a
@param b, person b
@return a boolean, whether a knows b you can call Celebrity.knows(a, b)

Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/14/2018 9:43 AM
  __Email__ = Jeremy.Sung@osh.com

"""

class Celebrity:

  def knows(self, a, b):

    return True if a > b else False  ## a > b means a knows b


class findCelebrity(Celebrity):

  def findCelebrity(self, n):
    # @param {int} n a party with n people
    # @return {int} the celebrity's label or -1

    ## cel = Celebrity()

    def __init__(self):
      Celebrity.__init__(self)

    candidate = 0
    for i in range(n):
      ## if Celebrity.knows(candidate, i):  ## if i knows candidate i is No Celebrity;
      ## if cel.knows(candidate, i):  ## if i knows candidate i is No Celebrity;
      if self.knows(candidate, i):  ## if i knows candidate i is No Celebrity;
        candidate = i

    for i in range(candidate):
      ## if Celebrity.knows(candidate, i) or not Celebrity.knows(i, candidate):
      ## if cel.knows(candidate, i) or not cel.knows(i, candidate):
      if self.knows(candidate, i) or not self.knows(i, candidate):
        return -1

    for i in range(candidate + 1, n):
      ## if not Celebrity.knows(i, candidate):
      ## if not cel.knows(i, candidate):
      if not self.knows(i, candidate):
        return -1

    return candidate

if __name__ == "__main__":

  findCelebrity = findCelebrity()

  n = 2
  """
  2 ## next n * (n - 1) lines
  ## 0 knows 1
  ## 1 does not know 0
  ## return 1 ## 1 is celebrity
  """


