#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" myBigInteger.py

Challenges: https://www.lintcode.com/problem/multiply-strings/description?_from=ladder&&fromId=14
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/19/2018 5:10 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class multiplyStringsBigInteger:
  """ MyBigInteger class """

  def multiply(self, num1, num2):
    """
    Thought - Algorithm:
    Break num1 and num2 in half,

    """
    l1, l2 = len(num1), len(num2)
    l3 = l1 + l2
    res = [0 for i in range(l3)]

    for i in range(l1 - 1, -1, -1):
        carry = 0
        for j in range(l2 - 1, -1, -1):
            res[i + j + 1] += carry + int(num1[i]) * int(num2[j])
            carry = res[i + j + 1] // 10
            res[i + j + 1] %= 10
        res[i] = carry

    i = 0
    while i < l3 and res[i] == 0:
        i += 1
    res = res[i:]
    return '0' if not res else ''.join(str(i) for i in res)








if __name__ == "__main__":

  myBigInteger = multiplyStringsBigInteger()

  num1 = "123"
  num2 = "45"  ## 5535

  print(myBigInteger.multiply(num1, num2))


