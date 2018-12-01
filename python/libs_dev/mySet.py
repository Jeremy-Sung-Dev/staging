#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" mySet.py

Description: Make set data structure with
 add, remove, clear, lookup(contains), and
 iterator in constant time... iterator can be O(size)

Reference: https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch05s18.html
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/5/2018 5:24 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import string


class mySet:
  """
  Ref. https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch05s18.html
  """

  def __init__(self, *args):
    self._dict = {}
    for arg in args:
      self.add(arg)


  def __repr__(self):
    elems = map(repr, self._dict.keys(  ))
    elems.sort(  )
    return "%s(%s)" % (self.__class__.__name__, string.join(elems, ', '))


  def extend(self, *args):
    """ Add several items at once. """
    for arg in args:
      self.add(arg)


  def add(self, item):
    """ Add one item to the set. """
    self._dict[item] = item


  def remove(self, item):
    """ Remove an item from the set. """
    del self._dict[item]


  def clear(self):
    pass



  def contains(self, item):
    """ Lookup - Check whether the set contains a certain item. """
    return self._dict.has_key(item)

    self.__contains__ = contains

  ## High-performance membership test for Python 2.0 and later
  ## __contains__ = contains

  def __getitem__(self, index):
    """ Support the 'for item in set:' protocol. """
    return self._dict.keys(  )[index]


  def __iter__(self):
    """ Better support of 'for item in set:' via Python 2.2 iterators """
    return iter(self._dict.copy(  ))


  def __len__(self):
    """ Return the number of items in the set """
    return len(self._dict)


  def items(self):
    """ Return a list containing all items in sorted order, if possible """
    result = self._dict.keys( )
    try: result.sort( )
    except: pass

    return result


  def __copy__(self):
    return mySet(self)



if __name__ == "__main__":

  myset = mySet()


