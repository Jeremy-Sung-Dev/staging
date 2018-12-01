#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" paintHouse.py

Challenges: https://www.lintcode.com/problem/paint-house/description
Solutions:  https://www.jiuzhang.com/solution/paint-house/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/22/2018 2:44 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class paintHouse:

  def minCost(self, costs):

    previousRed = 0
    previousBlue = 0
    previousGreen = 0

    for cost in costs:
      chooseRed = min(previousBlue, previousGreen) + cost[0]
      chooseBlue = min(previousRed, previousGreen) + cost[1]
      chooseGreen = min(previousRed, previousBlue) + cost[2]

      previousRed = chooseRed
      previousBlue = chooseBlue
      previousGreen = chooseGreen

      # ## Wrong answer:  21
      # previousRed = min(previousBlue, previousGreen) + cost[0]
      # previousBlue = min(previousRed, previousGreen) + cost[1]
      # previousGreen = min(previousRed, previousBlue) + cost[2]

    return min(previousRed, previousBlue, previousGreen)



if __name__ == "__main__":
  paintHouse = paintHouse()

  costs = [[14,2,11],[11,14,5],[14,3,10]]  ## Expect: 10

  print(paintHouse.minCost(costs))




