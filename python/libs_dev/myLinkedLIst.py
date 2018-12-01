#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" myLinkedList.py
Description: My Linked List
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/24/2018 3:42 PM
  __Email__ = Jeremy.Sung@osh.com

"""

class Node:
  def __init__(self, data=None, next_node=None):
    self.data = data
    self.next = next_node

  # def getNext(self):
  #   return self.next


class myLinkedList:

  def __init__(self, head=None):
    self.head = head


  def size(self):
    current = self.head
    count = 0
    while current:
      count += 1
      current = current.next
    return count


  def insert(self, data):
    """ Insert a new node to the Head"""
    newNode = Node(data)
    newNode.next = self.head
    self.head = newNode


  def add_Tail(self, data):

    current = self.head

    while current:
      previous = current
      current = current.next

    previous.next = Node(data)



  def search(self, data):
    current = self.head
    found = False

    ## while current and found is False:
    while current and not found:
      if current.data == data:
        found = True
      else:
        current = current.next

    if current is None:
      raise ValueError("Data not in list")

    return current


  def delete(self, data):

    current = self.head
    previous = None
    found = False

    ## while current and found is False:
    while current and not found:
      if current.data == data:
        found = True
      else:
        previous = current
        current = current.next

    if current is None:
      raise ValueError("Data not in list")

    if previous is None:
      self.head = current.next
    else:
      previous.next = current.next





if __name__ == "__main__":
  myLinkedLIst = myLinkedList()


