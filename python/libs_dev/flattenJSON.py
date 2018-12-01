#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" flattenJSON.py

Challenges: https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
Solutions:
Description: Flatten a JSON objects file

Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 10/5/2018 3:20 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class flattenJSON:

  def __init__(self):
    pass

  def flatten_json(self, y):

    out = {}

    def flatten(x, name=''):

      if type(x) is dict:
        for a in x:
          flatten(x[a], name + a + '_')

      elif type(x) is list:
        i = 0
        for a in x:
          flatten(a, name + str(i) + '_')
          i += 1

      else:
        out[name[:-1]] = x

    flatten(y)
    return out





if __name__ == "__main__":
  flattenJSON = flattenJSON()


