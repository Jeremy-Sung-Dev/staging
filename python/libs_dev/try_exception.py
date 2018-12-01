#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" try_exception.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/4/2018 7:58 AM
  __Email__ = Jeremy.Sung@osh.com

"""


class pureStorage:

  def __init__(self):
    pass


if __name__ == "__main__":
  # pureStorage = pureStorage()

  num = 'a'

  try:

    ## intNum = int(num)  ## ValueError...
    if num.isdigit():
      print(num)
    # else:
    #   print("Nah!")

    # if num.isdecimal():
    #   print(num)
    # else:
    #   print("Nah!")

  except ValueError as ve:
    print("Value Error: {0}".format(ve))



