#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" longestAbsoluteFilePath.py

Challenges: https://www.lintcode.com/problem/longest-absolute-file-path/description
Solutions: https://www.jiuzhang.com/solution/longest-absolute-file-path/#tag-highlight
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/23/2018 3:42 PM
  __Email__ = Jeremy.Sung@osh.com

Thoughts:
 Tree
 Should have no infinite loop by ignorant symlinks

"""

import re


class longestAbsoluteFilePath:

  def lengthLongestPath(self, input):

    if not input:
      return 0

    ans = 0
    sum = [0 for z in range(len(input) + 1)]

    for str in input.split("\n"):

      level = str.count('\t') + 1
      leng = 0

      if "." in str:  ## isFile: True
        leng = len(str.strip("\t"))
        ans = max(ans, sum[level - 1] + leng)

      else:
        ## leng = len(str.strip()) + 1  ## For Dir, add 1 to its length for "/"
        leng = len(str.strip("\t")) + 1  ## For Dir, add 1 to its length for "/"
        sum[level] = sum[level - 1] + leng

    return ans


  def lengthLongestPath_Staging_Worked(self, input):
    """
    @param input: an abstract file system
    @return: return the length of the longest absolute path to file
    """
    # if len(input) == 0:
    #   return 0
    if not input:
      return 0

    ans = 0
    sum = [0 for z in range(len(input))]

    for str in input.split("\n"):

      ## print("String: {} ".format(str))

      level = str.count('\t') + 1
      ## leng = len(str.strip())+ (level - 1)
      leng = 0

      ## if str.count(".") > 0:
      if "." in str:  ## isFile: True
        ## print("Before - ans: {}, Level: {}, leng: {}, sum[{}]: {}".format(ans, level, leng, level, sum[level]))
        ## leng = len(str.strip())
        leng = len(str.strip("\t"))
        ans = max(ans, sum[level - 1] + leng)
        ## print(" After - ans: {}, Level: {}, leng: {}, sum[{}]: {}".format(ans, level, leng, level, sum[level]))
      else:
        ## print("Dir Before - leng: {}".format(leng))
        ## leng = len(str.strip()) + 1  ## For Dir, add 1 to its length for "/"
        leng = len(str.strip("\t")) + 1  ## For Dir, add 1 to its length for "/"
        sum[level] = sum[level - 1] + leng
        ## print("Dir After - ans: {}, Level: {}, leng: {}, sum[{}]: {}".format(ans, level, leng, level, sum[level]))

    return ans



if __name__ == "__main__":
  longestAbsoluteFilePath = longestAbsoluteFilePath()

  input = "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext"   ## return 20
  input2 = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"  ## return : 32
  ## input10 = "dir.txt\n"  ## File at root dir
  input111 = "file01.txt"   ## File at root dir
  ## # Invalid: input11 = "file01.txt\n\tfile11.txt"  ## Missing a subdir in path!  \n\t can never go after a filename;
  input12 = "dir\n\tfile01.txt\n\tsubdir1\n\t\tfile.txt"  ## Same as input.  Expect 20
  input13 = "a"
  input14 = "dir\n file.txt"

  # print(longestAbsoluteFilePath.lastIndexOf(input, "\t"))

  # print(longestAbsoluteFilePath.lengthLongestPath(input))  # Expect : 20
  # print(longestAbsoluteFilePath.lengthLongestPath(input2)) # Expect : 32
  # ## print(longestAbsoluteFilePath.lengthLongestPath(input10)) # Expect : 20
  ## print(longestAbsoluteFilePath.lengthLongestPath(input111)) # Expect : 10
  ## print(longestAbsoluteFilePath.lengthLongestPath(input12)) # Expect : 20
  ## print(longestAbsoluteFilePath.lengthLongestPath(input13)) # Expect : 0
  print(longestAbsoluteFilePath.lengthLongestPath(input14)) # Expect : 9
