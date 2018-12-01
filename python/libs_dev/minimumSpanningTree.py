#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" minimumSpanningTree.py

Challenges: https://www.lintcode.com/problem/minimum-spanning-tree/description?_from=ladder&&fromId=4
Solutions: https://www.jiuzhang.com/solution/minimum-spanning-tree/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/20/2018 11:14 AM
  __Email__ = Jeremy.Sung@osh.com

"""

import pprint as pp

class Connection:
  ## Definition for a Connection
  def __init__(self, city1, city2, cost):
    self.city1, self.city2, self.cost = city1, city2, cost

  def __repr__(self):
    return "{} {} {}".format(self.city1, self.city2, self.cost)

  def __str__(self):
    return "{} {} {}".format(self.city1, self.city2, self.cost)



class minimumSpanningTree:

  def lowestCost(self, connections):
    """
    Ref. https://www.jiuzhang.com/solution/minimum-spanning-tree/#tag-other-lang-python
    Build graph, clarify connectivities among all cities;
    Confirm all cities are scanned; Are they all connected? If not return [].
    If all connected, take min Cost and involved lists;

    開始動手，基本算法思想有嗎？夠熟練？
    """
    connections.sort(key = lambda x: (x.cost, x.city1, x.city2))
    self.ans = []
    self.root_city, self.count = {}, 0
    for c in connections:
      city1, city2= c.city1, c.city2
      if city1 not in self.root_city:
        self.root_city[city1] = city1
        self.count += 1
      if city2 not in self.root_city:
        self.root_city[city2] = city2
        self.count += 1
      self.union(c)

    if self.count == 1:
      return self.ans
    else:
      return []


  def union(self, c):
    root_a, root_b = self.find(c.city1), self.find(c.city2)
    if root_a != root_b:
      self.root_city[root_a] = root_b
      self.count -= 1
      self.ans.append(c)


  def find(self, city):
    path = []
    while city != self.root_city[city]:
      path.append(city)
      city = self.root_city[city]
    for c in path:
      self.root_city[c] = city
    return city






if __name__ == "__main__":

  minimumSpanningTree = minimumSpanningTree()

  connections_raw1 = [["Acity", "Bcity", 1], ["Acity", "Ccity", 2], ["Bcity", "Ccity", 3]]
  connections_raw2 = [["Acity","Bcity",1], ["Bcity","Ccity",2], ["Acity","Ccity",2]]

  connections1 = [ Connection(*item) for item in connections_raw1 ]
  connections2 = [Connection(*item) for item in connections_raw2]
  ## print( connections1 )

  ## print( minimumSpanningTree.lowestCost(connections1)  )  ## Expect: ["Acity","Bcity",1], ["Acity","Ccity",2]
  print( minimumSpanningTree.lowestCost(connections2)  )  ## Expect: ["Acity","Bcity",1], ["Acity","Ccity",2]
