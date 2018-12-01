#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" slidingWindowMedian.py

Challenges: https://www.lintcode.com/problem/sliding-window-median/description?_from=ladder&&fromId=4
Solutions: https://www.jiuzhang.com/solution/sliding-window-median/#tag-highlight-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/21/2018 10:38 AM
  __Email__ = Jeremy.Sung@osh.com

"""

from myHashHeap import myHashHeap

class slidingWindowMedian:

  def medianSlidingWindow(self, nums, k):
    if not nums or len(nums) < k:
      return []

    self.maxheap = myHashHeap(desc=True)
    self.minheap = myHashHeap()

    for i in range(0, k - 1):
      self.add((nums[i], i))

    medians = []
    for i in range(k - 1, len(nums)):
      self.add((nums[i], i))
      # print(self.maxheap.heap, self.median, self.minheap.heap)
      medians.append(self.median)
      self.remove((nums[i - k + 1], i - k + 1))
      # print(self.maxheap.heap, self.median, self.minheap.heap)

    return medians

  def add(self, item):
    if self.maxheap.size > self.minheap.size:
      self.minheap.push(item)
    else:
      self.maxheap.push(item)

    if self.maxheap.size == 0 or self.minheap.size == 0:
      return

    if self.maxheap.top() > self.minheap.top():
      self.maxheap.push(self.minheap.pop())
      self.minheap.push(self.maxheap.pop())

  def remove(self, item):
    self.maxheap.remove(item)
    self.minheap.remove(item)
    if self.maxheap.size < self.minheap.size:
      self.maxheap.push(self.minheap.pop())

  @property
  def median(self):
    return self.maxheap.top()[0]



if __name__ == "__main__":

  slidingWindowMedian = slidingWindowMedian()

  nums1 = [1,2,7,8,5]
  k1 = 3
  nums2 = [1,2,7,7,2]
  k2 = 3
  nums3 = [10]
  k3 = 1

  nums4 = [1,2,7,7,2]
  k4 = 1

  ## print(slidingWindowMedian.medianSlidingWindow(nums1, k1))  ## Expect: [2,7,7]? [2,7,8]
  ## print(slidingWindowMedian.medianSlidingWindow(nums2, k2)) ## Expect: [2,7,7]
  ## print(slidingWindowMedian.medianSlidingWindow(nums3, k3)) ## Expect: [10]
  print(slidingWindowMedian.medianSlidingWindow(nums4, k4)) ## Expect: [1,2,7,7,2]


