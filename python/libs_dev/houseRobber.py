#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" houseRobber.py

Challenges: https://www.lintcode.com/problem/house-robber/description
Solutions: https://www.jiuzhang.com/solution/house-robber/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/22/2018 3:18 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class houseRobber:

  def houseRobber(self, A):
    if not A:
      return 0
    if len(A) <= 2:
      return max(A)

    f = [0] * 3
    f[0], f[1] = A[0], max(A[0], A[1])

    for i in range(2, len(A)):
      f[i % 3] = max(f[(i - 1) % 3], f[(i - 2) % 3] + A[i])

    return f[(len(A) - 1) % 3]


if __name__ == "__main__":

  houseRobber = houseRobber()

  A = [3, 8, 4]

  print(houseRobber.houseRobber(A))


