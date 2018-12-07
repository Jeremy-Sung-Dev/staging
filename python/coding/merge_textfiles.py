#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" merge_textfiles.py

Description: Merge Subtitles Text files

Attributes:
  __version__ = 12/6/2018 4:13 PM, __project__ = staging, __author__ = Jeremy Sung, __email__ = jsungcoding@gmail.com
"""

import os
from collections import deque
import pprint as pp

class merge_textfiles:

  def merge_files(self, path = "C:/38-Git"):

    if not os.path.exists(path):
      print("{} does not exist.".format(path))
      return

    queue = deque()
    for dir in os.listdir(path):

      if "zz" in dir or dir.endswith(".zip"):
        continue

      sub = path + "/" + dir

      # if os.path.isdir(sub):
      #   print(sub)

      queue.append(sub)

    ## pp.pprint(queue)




    # queue = [ dir for dir in os.listdir(path) if os.path.isdir(dir) ]
    # print(queue)

    # for i in queue:
    #   print(i)

    # while queue:
    #
    #
    #   entry = queue.
    #
    #   for
    # for dir in os.listdir(Path):
    #
    #   ## if os.path.isdir(dir) and "retrieved" in dir:
    #   if os.path.isdir(dir):
    #     queue.append(dir)
    #
    #     for file in dir:
    #
    #       ## print("Source Path: {}".format(srcPath))
    #
    #       if "Subtitles" in srcPath:
    #         self.extractSubtitlesFromPath(srcPath)
    #
    #
    #     dstFile = dstPath + '/' + srcFile.strip(".srt") + r".txt"
    #     srcFile = path + '/' + srcFile
    #
    #     ## print("Source: {};\n Destination: {}".format(srcFile, dstFile))
    #
    #     self.extractSubtitles(srcFile, dstFile)






if __name__ == "__main__":
  inst_merge_textfiles = merge_textfiles()
  path = "C:/38-Git"
  inst_merge_textfiles.merge_files(path)
  
  