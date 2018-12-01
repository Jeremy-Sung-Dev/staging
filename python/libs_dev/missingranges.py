#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" MissingRanges.py

Challenges:  https://www.lintcode.com/problem/missing-ranges/description?_from=ladder
Solutions:  https://www.jiuzhang.com/solution/missing-ranges/#tag-other-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/7/2018 4:42 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class MissingRanges:

  def findMissingRanges(self, nums, lower, upper):
    """
    Ref. https://github.com/kamyu104/LeetCode/blob/master/Python/missing-ranges.py
    """

    def getRange(lower, upper):
      if lower == upper:
        return "{}".format(lower)
      else:
        return "{}->{}".format(lower, upper)

    ranges = []
    pre = lower - 1

    for i in range(len(nums) + 1):
      if i == len(nums):
        cur = upper + 1
      else:
        cur = nums[i]
      if cur - pre >= 2:
        ranges.append(getRange(pre + 1, cur - 1))

      pre = cur

    return ranges




  def findMissingRanges_II_Buggy(self, nums, lower, upper):
    ## https://www.jiuzhang.com/solution/missing-ranges/#tag-other-lang-python

    missing = []
    nums = [lower - 1] + nums + [upper + 1]
    ## nums = [lower - 1] + nums + [upper + 1] ## Wrong Answer

    for i in range(1, len(nums)):
      l = nums[i - 1]
      h = nums[i]

      if l + 1 > upper or h - 1 > upper:
        continue

      if h - 1 >= 2:
        if h - 1 == 2:
          missing.append( str(l + 1))
        else:
          missing.append( str(l + 1) + "->" + str(h - 1))

    return missing




  # def findMissingRanges_myAttempt_I(self, nums, lower, upper):
  #
  #   missing_nums = []
  #
  #   for curr in range(lower, upper + 1):
  #
  #     if curr not in nums:
  #       missing_nums.append(curr)
  #
  #   return missing_nums




if __name__ == "__main__":

  missingranges = MissingRanges()

  nums = [0, 1, 3, 50, 75]
  lower = 0
  upper = 99

  nums1 = [2147483647]
  lower1 = 0
  upper1 = 2147483647  ## Expected:  ["0->2147483646"]

  nums2 = [0,1,3,50,75]
  lower2 = 0
  upper2 = 99

  nums4 = []
  lower4 = 1
  upper4 = 1


  ## print(missingranges.findMissingRanges(nums, lower, upper))   ## ["2", "4->49", "51->74", "76->99"]
  ## print(missingranges.findMissingRanges(nums1, lower1, upper1))   ## ["2", "4->49", "51->74", "76->99"]
  ## print(missingranges.findMissingRanges(nums2, lower2, upper2))   ## Expected: ["2","4->49","51->74","76->99"]
  print(missingranges.findMissingRanges(nums4, lower4, upper4))   ## ["2", "4->49", "51->74", "76->99"]

