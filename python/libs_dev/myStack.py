#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" myStack.py
Description: Implement Stack in Python
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/24/2018 3:41 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import collections


class myStack:
  """
  In a stack the element inserted last in sequence will come out first as we can remove only from the top of the stack;
  As the stack grows (as push operations occur), new stack will be added on the end of the list. 
  pop operations will manipulate that same end.
  A stack is called a “Last in, First out” or LIFO data structure; The last item added is the first to be removed.
  """

  def __init__(self):
    self.stack = []

  def isEmpty(self):
    return self.stack == []

  def push(self, item):
    self.stack.append(item)

  def pop(self):
    self.stack.pop()

  def peek(self):
    """ Use peek to look at the top(??) of the stack:
    def peek(self):
      return self.stack[0]
    """
    return self.stack[ len(self.stack) - 1 ]


  def top(self):
    if not self.stack:
      return None
    else:
      return self.stack[0]


  def size(self):
    return len(self.stack)



class myStack_using_Queue:
  """
  Implement the following operations of a stack using queues
  """

  def __init__(self):
    ## Implement Stack using collections.deque():
    self.queue = collections.deque()


  def isEmpty(self):
    if not self.queue:
      return True
    else:
      return False


  def push(self, item):
    temp = self.queue
    self.queue = collections.deque( [item] )
    self.queue.extend(temp)


  def pop(self):
    self.queue.popleft()


  def peek(self):
    """ Use peek to look at the top(??) of the stack:
    def peek(self):
      return self.stack[0]
    """
    if not self.queue:
      return None
    else:
      return self.queue[0]


  def top(self):
    if not self.queue:
      return None
    else:
      return self.queue[0]


  def size(self):
    return len(self.queue)



if __name__ == "__main__":
  myStack = myStack()


