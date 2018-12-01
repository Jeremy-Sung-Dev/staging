#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" codec.py

Challenges: https://www.lintcode.com/problem/encode-and-decode-strings/description
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/23/2018 3:04 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class codec:

  def encode(self, strs):
    """
    @param: strs: a list of strings
    @return: encodes a list of strings to a single string.
    """
    return " ".join(strs)

  def decode(self, str):
    """
    @param: str: A string
    @return: dcodes a single string to a list of strings
    """
    return str.split()






if __name__ == "__main__":
  codec = codec()

  strs = ["lint","code","love","you"]  ## string encoded_string = encode(strs)
  encoded_string = codec.encode(strs)

  print(codec.decode(encoded_string))  ## return ["lint","code","love","you"] when you call decode(encoded_string)



