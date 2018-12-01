#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" wordabbreviation.py

Challenges: https://www.lintcode.com/problem/word-abbreviation/description?_from=ladder&&fromId=14
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/13/2018 4:53 PM
  __Email__ = Jeremy.Sung@osh.com

"""

## Python 2 solution:
class wordabbreviation:
  """https://www.lintcode.com/problem/word-abbreviation/description?_from=ladder&&fromId=14"""

  def abbr(self, word, size):
    if len(word) - size <= 3: return word
    return word[:size + 1] + str(len(word) - size - 2) + word[-1]

  def solve(self, dict, size):
    dlist = collections.defaultdict(list)
    for word in dict:
      dlist[self.abbr(word, size)].append(word)
    for abbr, wlist in dlist.iteritems():
      if len(wlist) == 1:
        self.dmap[wlist[0]] = abbr
      else:
        self.solve(wlist, size + 1)

  def wordsAbbreviation(self, dict):
    """
    :type dict: List[str]
    :rtype: List[str]
    """
    self.dmap = {}
    self.solve(dict, 0)
    return map(self.dmap.get, dict)




if __name__ == "__main__":

  wordabbreviation = wordabbreviation()
  dict1 = ["like", "god", "internal", "me", "internet", "interval", "intension", "face", "intrusion"]

  dict2 = ["like","god","internal","me","internet","interval","intension","face","intrusion"]
  ## Expected: ["l2e","god","internal","me","i6t","interval","inte4n","f2e","intr4n"]


  print(wordabbreviation.wordsAbbreviation(dict1))
  ## Expect: ["l2e","god","internal","me","i6t","interval","inte4n","f2e","intr4n"]