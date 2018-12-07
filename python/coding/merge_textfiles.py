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

    # queue = deque()
    # for dir in os.listdir(path):
    #
    #   if "zz" in dir or dir.endswith(".zip"):
    #     continue
    #
    #   sub = path + "/" + dir
    #
    #   if os.path.isdir(sub):
    #     print(sub)
    #
    #   queue.append(sub)

    # queue = deque([path + "/" + dir for dir in os.listdir(path) if ("zz" not in dir or not dir.endswith(".zip")) and
    #                os.path.isdir(path + "/" + dir)])

    queue = deque( path + "/" + dir for dir in os.listdir(path) if ("zz" not in dir or not dir.endswith(".zip")) and
                   os.path.isdir(path + "/" + dir) )

    ## pp.pprint(queue)
    ## print(queue.popleft())

    # while queue:
    #   subdir = queue.popleft()

    for dir in queue:

      for subdir in os.listdir(dir):

        # mergedFileName = subdir + "_mergedSubtitles"

        if "retrieved" in subdir and os.path.isdir(dir + '/' + subdir):

          mergedFileName = dir + '/' + subdir + '/' + "mergedSubtitles.txt"

          for src in os.listdir(dir + '/' + subdir):
            srcFile = dir + '/' + subdir + '/' + src

            with open(srcFile, "r") as srcf, open(mergedFileName, "a") as mergedf:

              for text in filter(None, (line.rstrip() for line in srcf)):

                if "-->" not in text and not text.isnumeric():
                  mergedf.write(text + ' ')

        # for srcFile in os.listdir(subdir):
        #
        #   if srcFile.endswith("lang_en.srt") or "lang_en" in srcFile:
        #
        #     # dstFile = dir + '/' + srcFile.strip(".srt") + r".txt"
        #     srcFile = dir + '/' + subdir + '/' + srcFile
        #
        #     ## print("Source: {};\n Destination: {}".format(srcFile, dstFile))
        #
        #     # self.extractSubtitles(srcFile, dstFile)
        #     with open(srcFile, "r") as srcf, open(mergedFileName, "a") as mergedf:
        #
        #       for text in filter(None, (line.rstrip() for line in srcf)):
        #
        #         if "-->" not in text and not text.isnumeric():
        #           mergedf.write(text + ' ')



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
  # path = "C:/38-Git"
  path = "C:/zz_A1_Backup/38-Git"
  inst_merge_textfiles.merge_files(path)
  
  