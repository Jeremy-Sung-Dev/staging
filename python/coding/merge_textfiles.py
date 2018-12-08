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
    # for dir in os.listdir(srcPath):
    #
    #   if "zz" in dir or dir.endswith(".zip"):
    #     continue
    #
    #   sub = srcPath + "/" + dir
    #
    #   if os.srcPath.isdir(sub):
    #     print(sub)
    #
    #   queue.append(sub)

    # queue = deque([srcPath + "/" + dir for dir in os.listdir(srcPath) if ("zz" not in dir or not dir.endswith(".zip")) and
    #                os.srcPath.isdir(srcPath + "/" + dir)])

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


  def merge_files_to_one(self, srcPath="C:/38-Git", dstPath="C:/85-Data/Subtitles"):
    """ Consolidate all subtitles into one file;
     File named as Course Name; Content segmented by sections; each section titled with subtitle filename """

    if not os.path.exists(dstPath):
      os.makedirs(dstPath)

    subdirs = [ subdir for subdir in os.listdir(srcPath) if ("zz" not in subdir or not subdir.endswith(".zip"))
                  and os.path.isdir(srcPath + "/" + subdir) ]

    for dir in subdirs:

      for srcFile in os.listdir(srcPath + '/' + dir):

        if srcFile.endswith("lang_en.srt") or "lang_en" in srcFile:

          srcCourseTitle = srcPath.strip("C:/")
          dstFile = dstPath + "/" + srcCourseTitle.replace("/","_") + "_Subtitles_All.txt"

          srcFilePath = srcPath + '/' + dir + '/' + srcFile

          with open(srcFilePath, "r") as srcf, open(dstFile, "a") as dstf:

            dstf.write(">> {} > {}:\n".format(dir, srcFile))

            for text in filter(None, (line.rstrip() for line in srcf)):

              if "-->" not in text and not text.isnumeric():
                dstf.write("{} ".format(text))

            dstf.write("\n\n")


if __name__ == "__main__":

  inst_merge_textfiles = merge_textfiles()

  # # srcPath = "C:/38-Git"
  # srcPath = "C:/zz_A1_Backup/38-Git"
  # inst_merge_textfiles.merge_files(srcPath)

  srcPath = "C:/zz_A1_Backup/38-Git"
  dstPath = "C:/85-Data/Subtitles"
  inst_merge_textfiles.merge_files_to_one(srcPath, dstPath)
  
  