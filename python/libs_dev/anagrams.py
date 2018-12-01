#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" anagrams.py

Challenges:
  https://www.lintcode.com/problem/valid-anagram/description?_from=ladder&&fromId=14
  https://www.lintcode.com/problem/find-all-anagrams-in-a-string/description?_from=ladder&&fromId=14
 Group Anagrams:  https://www.lintcode.com/problem/group-anagrams/description


Solutions:
  https://www.jiuzhang.com/solution/valid-anagram/#tag-other

 Group Anagrams:  https://www.jiuzhang.com/solution/group-anagrams/


Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/12/2018 12:21 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import string
from collections import defaultdict

class anagrams:

  def validAnagram(self, s, t):
    """
    Time Complexity: O(N)
    Space Complexity: O(1)
    """

    dicS = {ch: 0 for ch in string.printable}
    dicT = {ch: 0 for ch in string.printable}

    for char in t:
      dicT[char] += 1

    for char in s:

      dicS[char] += 1

      if char in t:
        dicT[char] -= 1
        dicS[char] -= 1

    return dicS == dicT


  def validAnagram_RunTimeError(self, s, t):
    """
    Runtime Error:
    Input  "happy new year"   "n ahwryeypp ea"
    Expected   true
    Traceback (most recent call last): File "/code/Main.py", line 70, in ans = solution.anagram(s, t) File "/code/Solution.py", line 34, in anagram dicT[char] += 1 KeyError: ' '

    ## Corner cases: White space - \t, spaces, etc.
    ## Upper & lower cases??

    Time Complexity: O(N)
    Space Complexity: O(1)
    """

    dicS = { ch:0 for ch in string.ascii_lowercase }
    dicT = { ch:0 for ch in string.ascii_lowercase }

    for char in t:
      dicT[char] += 1

    for char in s:

      dicS[char] += 1

      if char in t:
        dicT[char] -= 1
        dicS[char] -= 1

    return dicS == dicT


  def validAnagram_Worked(self, s, t):
    """
    Time Complexity: O(N)
    Space Complexity: O(N)
    """

    dicS = { }
    dicT = {}

    for char in t:

      if char not in dicT:
        dicT[char] = 1
      else:
        dicT[char] += 1

    for char in s:

      if char not in dicS:
        dicS[char] = 1
      else:
        dicS[char] += 1

      if char in t:
        if char not in dicT:
          dicT[char] = 0
        else:
          dicT[char] -= 1

        dicS[char] -= 1

    return dicS == dicT



  def findAnagrams(self, s, p):
    """

    :param s:
    :param p:
    :return:
    """
    pass


  def anagramMappings(self, A, B):
    """
    https://www.lintcode.com/problem/find-anagram-mappings/description
    :param A:
    :param B:
    :return:
    """

    p = []
    lenA = len(A)
    for i in range(lenA):
      for j in range(lenA - 1, -1, -1):
        if A[i] == B[j]:
          p.append(j)
          break

    return p

    ## return [ j for i in range(lenA) for j in range(lenA) if A[i] == B[j]]






  def groupAnagrams(self, strs):
    """
    copy & paste :
    Ref: https://www.lintcode.com/problem/group-anagrams/description

    @param strs: the given array of strings
    @return: The anagrams which have been divided into groups
    """

    hash_word = defaultdict(list)
    for word in strs:
      hash = ''.join(sorted(word))
      hash_word[hash].append(word)

    return [sorted(v) for k, v in hash_word.iteritems()]



if __name__ == "__main__":

  # import string
  # ## print(string.ascii_letters)  ## abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
  # print(string.ascii_lowercase)  ## abcdefghijklmnopqrstuvwxyz

  anagrams = anagrams()

  # S = ["abcd", "ab"]
  # T = ["dcab", "ac"]
  #
  # s1 = "abcd"
  # t1 = "dcab"
  #
  # s2 = "ab"
  # t2 = "ac"
  #
  # s3 = "aacc"
  # t3 = "ccac"
  #
  # s4 = "az"
  # t4 = "by"
  #
  #
  # # ## print( [anagrams.validAnagram(s,t) for s in S for t in T] )  ## [True, False, False, False]
  # # print(anagrams.validAnagram(s1, t1))  ## Expect: True
  # # print(anagrams.validAnagram(s2, t2)) ## Expect: False
  # # print(anagrams.validAnagram(s3, t3))    ## Expect: False
  # print(anagrams.validAnagram(s4, t4))  ## Expect: False

  ##
  ## 813. Find Anagram Mappings
  ##
  A1 = [12, 28, 46, 32, 50]
  B1 = [50, 12, 32, 46, 28]  ## Return [1, 4, 3, 2, 0]

  A2= [84, 8, 0, 84, 0, 84]
  B2= [84, 84, 8, 0, 0, 84]  ## [5,2,4,5,4,5] or [0, 2, 3, 0, 3, 0]
  print(anagrams.anagramMappings(A2, B2))





  # ##
  # ## Group Anagrams Test Cases:
  # ##
  # strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
  # print(anagrams.groupAnagrams(strs))
  # """ Expected Return:
  # [
  #     ["ate", "eat","tea"],
  #     ["nat","tan"],
  #     ["bat"]
  # ]
  # """
