#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" mergeAccounts.py

Challenges: https://www.lintcode.com/problem/accounts-merge/description?_from=ladder&&fromId=4
Solutions: https://www.jiuzhang.com/solution/accounts-merge/
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/20/2018 10:04 AM
  __Email__ = Jeremy.Sung@osh.com

"""


class mergeAccounts:

  def accountsMerge(self, accounts):
    self.initialize(len(accounts))
    email_to_ids = self.get_email_to_ids(accounts)

    # union
    for email, ids in email_to_ids.items():
      root_id = ids[0]
      for id in ids[1:]:
        self.union(id, root_id)

    id_to_email_set = self.get_id_to_email_set(accounts)

    merged_accounts = []
    for user_id, email_set in id_to_email_set.items():
      merged_accounts.append([
        accounts[user_id][0],
        *sorted(email_set),
      ])
    return merged_accounts

  def get_id_to_email_set(self, accounts):
    id_to_email_set = {}
    for user_id, account in enumerate(accounts):
      root_user_id = self.find(user_id)
      email_set = id_to_email_set.get(root_user_id, set())
      for email in account[1:]:
        email_set.add(email)
      id_to_email_set[root_user_id] = email_set
    return id_to_email_set

  def get_email_to_ids(self, accounts):
    email_to_ids = {}
    for i, account in enumerate(accounts):
      for email in account[1:]:
        email_to_ids[email] = email_to_ids.get(email, [])
        email_to_ids[email].append(i)
    return email_to_ids

  def initialize(self, n):
    self.father = {}
    for i in range(n):
      self.father[i] = i

  def union(self, id1, id2):
    self.father[self.find(id1)] = self.find(id2)

  def find(self, user_id):
    path = []
    while user_id != self.father[user_id]:
      path.append(user_id)
      user_id = self.father[user_id]

    for u in path:
      self.father[u] = user_id

    return user_id



  # ## My Attempt - Thought I -
  # def __init__(self):
  #   self.email_name_d = {}
  #
  #
  # def checkMerge(self):
  #   ## When an email is found exist in self.email_name_d, trace to its owner (name), merge related email
  #   ## to this owner and eliminate all related email:name dictionary in self.email_name_d;
  #   ## And, continue
  #   pass
  #
  #
  #
  # def accountsMerge(self, accounts):
  #   """
  #   for each Name, each email as key and the user name as value; store these dictionaries for each account
  #   when an email finds a match, retrieve the owner's name (value)
  #   the owner's name may have duplicate entries but as different person
  #     Verify this is the same person by checking whether candidates do own the email address
  #     True and merge emails if both name and one of email presents in both accounts;
  #     remove candidate account so avoid redundant comparison on other email
  #
  #   """
  #   ## lenAcc = len(accounts)
  #
  #   ## email_name_d = {}
  #
  #   for account in accounts:
  #
  #     name = accounts[0]
  #     for email in account[1:]:
  #
  #       if email not in self.email_name_d:
  #         self.email_name_d[email] = name
  #
  #       else:
  #
  #         self.checkMerge()


if __name__ == "__main__":

  mergeAccounts = mergeAccounts()

  accounts = [
  ["John", "johnsmith@mail.com", "john00@mail.com"],
  ["John", "johnnybravo@mail.com"],
  ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
  ["Mary", "mary@mail.com"]
  ]

  print(mergeAccounts.accountsMerge(accounts))




