#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" LoadBalancer.py

Challenges: https://www.lintcode.com/problem/load-balancer/description?_from=ladder&&fromId=14
Solutions: https://www.jiuzhang.com/solution/load-balancer/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/14/2018 11:08 AM
  __Email__ = Jeremy.Sung@osh.com

"""

import random

class LoadBalancer:

  def __init__(self):
    ## self.server_id = 0
    ## self.servers = set()
    ## self.servers = {}
    self.servers = []
    self.count = 0


  def add(self, server_id):
    """
    @param: server_id: add a new server to the cluster
    @return: nothing
    """

    if server_id not in self.servers:
      self.servers.append(server_id)
      self.count += 1


  def remove(self, server_id):
    """
    @param: server_id: server_id remove a bad server from the cluster
    @return: nothing
    """
    try:

      if server_id in self.servers:
        self.count -= 1
        ## del self.servers[server_id]
        self.servers.remove(server_id)
      else:
        print("Server: {} not in the list".format(server_id))

    except IndexError as e:
      print(e.__cause__)


  def pick(self):
    """
    @return: pick a server in the cluster randomly with equal probability
    """
    # scale =

    ## ranIndex = random.randrange(0, self.count + 1, 1) ## IndexError: list index out of range
    ranIndex = random.randrange(0, self.count, 1)

    ## print(self.servers[ranIndex])
    return self.servers[ranIndex]







if __name__ == "__main__":
  loadbalancer = LoadBalancer()
  # # num = int(random.random() * 10)
  # # print(num)
  # ranindex = random.randrange(0, 20, 1)
  # print(ranindex)
  loadbalancer.add(1)
  loadbalancer.add(2)
  loadbalancer.add(3)

  loadbalancer.pick() ## >> 1 // the return value is random, it can be either 1, 2, or 3.
  loadbalancer.pick() ## >> 2
  loadbalancer.pick() ## >> 1
  loadbalancer. pick() ## >> 3

  loadbalancer.remove(1)

  loadbalancer.pick() ## >> 2
  loadbalancer.pick() ## >> 3
  loadbalancer.pick() ## >> 3

