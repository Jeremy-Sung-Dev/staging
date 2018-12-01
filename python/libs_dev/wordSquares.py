#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" wordSquares.py

Challenges: https://www.lintcode.com/problem/word-squares/description?_from=ladder&&fromId=14
Solutions: https://www.jiuzhang.com/solution/word-squares/#tag-highlight-lang-python
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/18/2018 3:04 PM
  __Email__ = Jeremy.Sung@osh.com

"""


class TrieNode:
  def __init__(self):
    self.children = {}
    self.is_word = False
    self.word_list = []


class Trie:
  def __init__(self):
    self.root = TrieNode()

  def add(self, word):
    node = self.root
    for c in word:
      if c not in node.children:
        node.children[c] = TrieNode()
      node = node.children[c]
      node.word_list.append(word)
    node.is_word = True

  def find(self, word):
    node = self.root
    for c in word:
      node = node.children.get(c)
      if node is None:
        return None
    return node

  def get_words_with_prefix(self, prefix):
    node = self.find(prefix)
    return [] if node is None else node.word_list

  def contains(self, word):
    node = self.find(word)
    return node is not None and node.is_word



class wordSquares:

  def wordSquares(self, words):
    """
    @param: words: a set of words without duplicates
    @return: all word squares
    """
    trie = Trie()
    for word in words:
      trie.add(word)

    squares = []
    for word in words:
      self.search(trie, [word], squares)

    return squares


  def search(self, trie, square, squares):
    n = len(square[0])
    curt_index = len(square)
    if curt_index == n:
      squares.append(list(square))
      return

    # Pruning, it's ok to remove it, but will be slower
    for row_index in range(curt_index, n):
      prefix = ''.join([square[i][row_index] for i in range(curt_index)])
      if trie.find(prefix) is None:
        return

    prefix = ''.join([square[i][curt_index] for i in range(curt_index)])
    for word in trie.get_words_with_prefix(prefix):
      square.append(word)
      self.search(trie, square, squares)
      square.pop()  # remove the last word


  ####
  ## My initial attempt:
  #
  # def wordSquares(self, words):
  #   """
  #   @param: words: a set of words without duplicates
  #   @return: all word squares
  #   """
  #
  #   rowWords = len(words)
  #   colWords = len(words[0])
  #
  #   i, j = 0, 0
  #   results = []
  #   count = 0
  #
  #   while i < rowWords and j < colWords:
  #
  #     if words[i][j] != words[j][i]:
  #       return False
  #     i += 1
  #     j += 1
  #
  #
  #
  #   return True
  #
  #
  #
  # def isWordSquare(self, words):
  #
  #   rowWords = len(words)
  #   colWords = len(words[0])
  #
  #
  #
  #   i, j = 0, 0
  #
  #   while i < rowWords and j < colWords:
  #
  #     if words[i][j] != words[j][i]:
  #       return False
  #
  #     i += 1
  #     j += 1
  #
  #   return True







if __name__ == "__main__":

  wordSquares = wordSquares()

  words1 = ["ball", "area", "lead", "lady"]

  words2 = ["area","lead","wall","lady","ball"]  ## [["ball","area","lead","lady"],["wall","area","lead","lady"]]

  words3 = ["abat","baba","atan","atal"]

  print(wordSquares.wordSquares(words1))
  ## print(wordSquares.wordSquares(words2))
  print(wordSquares.wordSquares(words3))

