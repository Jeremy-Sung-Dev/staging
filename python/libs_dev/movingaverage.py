#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" movingaverage.py

Challenges: https://www.lintcode.com/problem/moving-average-from-data-stream/description?_from=ladder
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/4/2018 1:23 PM
  __Modified__ = 12/18/2018 12:38 PM
  __Email__ = Jeremy.Sung@osh.com

"""

class MovingAverage:
  def __init__(self, size):
    from queue import Queue
    self.queue = Queue()
    self.size = size
    self.sum = 0.0

  def next(self, val):
    self.sum += val

    if self.queue.qsize() == self.size:
      self.sum -= self.queue.get()

    self.queue.put(val)

    return self.sum * 1.0 / self.queue.qsize()


class MovingAverage_TimeExceed:

  def __init__(self, size):
    """
    @param: size: An integer
    """
    self.size = size
    self.res = []


  def next(self, val):
    """
    @param: val: An integer
    @return:
    """
    sum = 0
    self.res.append(val)

    lenRes = len(self.res)

    if lenRes <= self.size:

      for i in range(lenRes):
        sum += self.res[i]

      return "{:.5f}".format(sum / lenRes)

    else:
      for e in self.res[ -1 : -1 - self.size : -1]:
        print(e)
        sum += e

      print(sum)

      return "{:.5f}".format(sum / self.size)  ## output.write("%.5lf\n" % (param + 0.0000000001)) TypeError: must be str, not float




class MovingAverage_Lintcode_Attempt_1:

  def __init__(self, size):
    self.size = size
    self.res = []


  def next(self, val):
    sum = 0
    self.res.append(val)

    lenRes = len(self.res)
    ## avg = 0

    if lenRes == 0 or self.size == 0:
      return 0

    if lenRes <= self.size:
      for i in range(lenRes):
        sum += self.res[i]

      # return "{:.5f}".format( sum / lenRes)
      # avg = "{:.5f}".format( sum / lenRes)
      return sum / lenRes

    else:
      for e in self.res[-1: -1 - self.size: -1]:
        sum += e

      # return "{:.5f}".format( sum / self.size)
      # avg = "{:.5f}".format( sum / self.size)
      return sum / self.size

    ## return str(avg)

  # Your MovingAverage object will be instantiated and called as such:
  # obj = MovingAverage(size)
  # param = obj.next(val)




if __name__ == "__main__":
  # # movingAverage = MovingAverage()
  # m = MovingAverage(3)
  # print(m.next(1))  # = 1   # return 1.00000
  # print(m.next(10)) # = (1 + 10) / 2 # return 5.50000
  # print(m.next(3)) # = (1 + 10 + 3) / 3 # return 4.66667
  # print(m.next(5)) # = (10 + 3 + 5) / 3 # return 6.00000

  # MovingAverage(3)
  # next(9)
  # next(3)
  # next(2)
  # next(4)
  # next(8)
  # # Expected
  # # 9.00000
  # # 6.00000
  # # 4.66667
  # # 3.00000
  # # 4.66667

  A = [1,2,3,4]
  lenA = len(A)
  for i in range(lenA):
    print("{}: {}".format(i, A.pop()))