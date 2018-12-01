#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" factorcombinations.py

Challenges: https://www.lintcode.com/problem/factor-combinations/description
Solutions: http://blog.ystanzhang.com/2015/10/lc-factor-combinations_5.html
  https://www.jiuzhang.com/solution/factor-combinations/#tag-other-lang-java
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 10/25/2018 1:20 PM
  __Email__ = Jeremy.Sung@osh.com

"""
import copy

class factorcombinations:

  def dfs(self, n, subset, start, result):

    while start * start <= n:

      if n % start == 0:
        result.append(subset + [start, n //start ])
        self.dfs(n//start, subset + [start], start, result)

      start += 1

    return result


  def getFactors(self, n):

    result = []
    self.dfs(n, [], 2, result)

    return result



if __name__ == "__main__":
  factorcombinations = factorcombinations()

  ## nums = [1, 37, 12, 32]
  nums = [24]

  for num in nums:
    print("Num: {} Factor Combinations: {}".format(num, factorcombinations.getFactors(num)))

  ## input: 1     output: []
  ## input: 37    output:  []
  ## input: 12    output:  [[2, 6], [2, 2, 3], [3, 4]]
  ## input: 32    output:  [[2, 16],[2, 2, 8],[2, 2, 2, 4],[2, 2, 2, 2, 2],[2, 4, 4],[4, 8]]

