#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" readNCharsGivenRead4_II.py

Challenges: https://www.lintcode.com/problem/read-n-characters-given-read4-ii-call-multiple-times/description?_from=ladder
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 9/10/2018 2:20 PM
  __Email__ = Jeremy.Sung@osh.com

"""


# def read4(buf):
#   """
#   The read4 API is already defined for you.
#   @param buf a list of characters
#   @return an integer
#   you can call Reader.read4(buf)
#   """
#
#   global file_content
#   i = 0
#
#   while i < len(file_content) and i < 4:
#     buf[i] = file_content[i]
#     i += 1
#
#   if len(file_content) > 4:
#     file_content = file_content[4:]
#   else:
#     file_content = ""
#
#   return i



class readNCharsGivenRead4_II:



  def read4(self, buf):
    """
    The read4 API is already defined for you.
    @param buf a list of characters
    @return an integer
    you can call Reader.read4(buf)
    """

    global file_content
    i = 0

    while i < len(file_content) and i < 4:
      buf[i] = file_content[i]
      i += 1

    if len(file_content) > 4:
      file_content = file_content[4:]
    else:
      file_content = ""

    return i



  def __init__(self):
      self.left = []

  def read(self, buf, n):
    count, reads = 0, [''] * 4

    if self.left:
      while count < min(n, len(self.left)):
        buf[count] = self.left[count]
        count += 1

      self.left = self.left[count:]

    while count < n:
      size = read4(reads)
      if not size:
        break

      length = min(n - count, size)
      self.left = reads[length : size]

      for i in xrange(length):
        buf[count] = reads[i]
        count += 1

    return count


  # def __init__(self):
  #   self.__buf4 = [''] * 4
  #   self.__i4 = 0
  #   self.__n4 = 0
  #
  #
  # def read_B(self, buf, n):
  #   i = 0
  #   while i < n:
  #     if self.__i4 < self.__n4:  # Any characters in buf4.
  #       buf[i] = self.__buf4[self.__i4]
  #       i += 1
  #       self.__i4 += 1
  #     else:
  #       self.__n4 = self.read4(self.__buf4)  # Read more characters.
  #       if self.__n4:
  #         self.__i4 = 0
  #       else:  # Buffer has been empty.
  #         break
  #
  #   return i


  def read_A(self, buf, n):
    """Ref. https://github.com/kamyu104/LeetCode/.../Python/read-n-characters-given-read4.py"""

    read_bytes = 0
    buff = [''] * 4

    ## for i in range(n / 4 + 1):
    for i in range(n >> 2 + 1):

      ## size = Reader.read4(buff)
      size = self.read4(buff)

      if size:
        size = min(size, n - read_bytes)
        buf[read_bytes: read_bytes + size] = buff[:size]
        read_bytes += size
      else:
        break

    return read_bytes





if __name__ == "__main__":
  readNCharsGivenRead4_II = readNCharsGivenRead4_II()

  buf = "filetestbuffer"
  print(readNCharsGivenRead4_II.read(buf, 6))
  print(readNCharsGivenRead4_II.read(buf, 5))
  print(readNCharsGivenRead4_II.read(buf, 4))


