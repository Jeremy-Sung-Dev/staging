#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" validWordAbbreviation.py

Challenges: https://www.lintcode.com/problem/valid-word-abbreviation/description
Solutions: https://www.jiuzhang.com/solution/valid-word-abbreviation/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/23/2018 2:10 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class validWordAbbreviation:

  def validWordAbbreviation(self, word, abbr):

    i, n = 0, "0"
    for c in abbr:
      if c.isdigit():
        if n == c:
          return False
        n += c
      else:
        i += int(n)
        if i >= len(word) or word[i] != c:
          return False
        i += 1
        n = '0'

    return i + int(n) == len(word)



  def validWordAbbreviation_MyAttempt(self, word, abbr):
    """
    Start with abbr;
     when char is alphabet, match it with the char at same position;
     when char is numeric, match it with length of buffer;

    :param word:
    :param abbr:
    :return:
    """

    buffer = []
    lenAbbr = len(abbr)
    count = 0

    for i in range(lenAbbr):
      count += i
      if abbr[i].isalpha() and abbr[i] == word[count][i]:

        buffer = []
        continue
      else:
        buffer.append(word[count])




if __name__ == "__main__":
  validWordAbbreviation = validWordAbbreviation()

  word = "internationalization"
  abbr = "i12iz4n"

  print( validWordAbbreviation.validWordAbbreviation(word, abbr) )


