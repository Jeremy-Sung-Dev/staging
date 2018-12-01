#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" buddybitmap.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/5/2018 3:07 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class buddybitmap:

  def setbit_down(self, A, x, n):

    if x >= n:
      return

    if 2 * x + 1 <= n and A[2 * x + 1] == 0:
      A[2 * x + 1] = 1
      self.setbit_down(A, 2 * x + 1, n)

    if 2 * x + 2 <= n and A[2 * x + 2] == 0:
      A[2 * x + 2] = 1
      self.setbit_down(A, 2 * x + 2, n)


  def set_bit(self, A, pos, length):

    if not A or pos < 0 or length <= 0:
      return

    n = len(A) - 1  # last index of A

    for x in range(pos, min(n + 1, min(pos + length, 2 * pos + 1))):

      # set self
      if A[x] == 1:
        continue
      A[x] = 1

      # set descendants
      self.setbit_down(A, x, n)

      # set ancestors
      while x > 0:
        # make sure its sibling is 1, if its sibling is 0, cannot set ancestors
        if (x % 2 == 0 and A[x - 1] == 1) or (x % 2 == 1 and x < n and A[x + 1] == 1):
          A[(x - 1) >> 1 ] = 1
        x = (x - 1) >> 1


  def clear_bit(self, A, pos, length):

    if not A or pos < 0 or length <= 0:
      return

    n = len(A) - 1  # last index of A

    for x in range(pos, min(n + 1, pos + length)):
      ## x : index in A;

      # clear self
      if A[x] == 0:
        continue
      A[x] = 0

      # clear descendants
      while 2 * x + 1 <= n:
        A[2 * x + 1] = 0
        x = 2 * x + 1

      # clear ancestors
      while x > 0:
        if A[(x - 1) >> 1 ] == 0:
          break
        A[(x - 1) >> 1] = 0
        x = (x - 1) >> 1


if __name__ == "__main__":
  buddybitmap = buddybitmap()

  ## List Comprehension:
  A = [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]
  test_cases = [(x, y) for x in range(len(A)) for y in range(1, len(A) - x + 1)]
  ## [ (x, y) for x in range(12)  for y in range(1, 12 - x + 1) ]

  for each_test_case in test_cases:
    ## print(each_test_case)
    pos, length = each_test_case

    buddybitmap.set_bit(A, pos, length)

    ## print("after setting bit from {} for length: {}, A is {}".format(pos, length, A))

    buddybitmap.clear_bit(A, pos, length)
    print("after clearing bit from {} for length: {}, A is {}".format(pos, length, A))



