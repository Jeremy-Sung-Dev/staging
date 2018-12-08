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


  # def extractSubtitles_Embedded_Filename_as_SectionTitle(self, srcFile, dstFile):
  #
  #   with open(srcFile, "r") as srcf, open(dstFile, "a") as dstf:
  #
  #     for text in filter(None, (line.rstrip() for line in srcf)):
  #
  #       if "-->" not in text and not text.isnumeric():
  #         dstf.write(text + ' ')


  def merge_files_to_one(self, srcPath="C:/38-Git", dstPath="C:/85-Data/Subtitles"):
    """ Consolidate all subtitles into one file in c:/10-Udacity/SUbtitles; Filename will be the name of the course;
    Each subtitle will be separated by the name of its subtitle filename; """

    if not os.path.exists(dstPath):
      os.makedirs(dstPath)

    ## subdirs = [ srcPath + "/" + subdir for subdir in os.listdir(srcPath) if ("zz" not in subdir or not subdir.endswith(".zip"))
    ##               and os.path.isdir(srcPath + "/" + subdir) ]
    subdirs = [ subdir for subdir in os.listdir(srcPath) if ("zz" not in subdir or not subdir.endswith(".zip"))
                  and os.path.isdir(srcPath + "/" + subdir) ]

    for dir in subdirs:

      ## srcDirPath = srcPath + '/' + dir

      for srcFile in os.listdir(srcPath + '/' + dir):

        if srcFile.endswith("lang_en.srt") or "lang_en" in srcFile:

          srcCourseTitle = srcPath.strip("C:/")
          dstFile = dstPath + "/" + srcCourseTitle.replace("/","_") + "_Subtitles_All.txt"

          srcFilePath = srcPath + '/' + dir + '/' + srcFile
          # srcFilePath = dir + '/' + srcFile

          ## print("Source: {};\n Destination: {}".format(srcFile, dstFile))

          with open(srcFilePath, "r") as srcf, open(dstFile, "a") as dstf:

            dstf.write(">> {} > {}:\n".format(dir, srcFile))

            for text in filter(None, (line.rstrip() for line in srcf)):

              if "-->" not in text and not text.isnumeric():
                dstf.write("{} ".format(text))

            dstf.write("\n\n")




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



    # queue = [ dir for dir in os.listdir(srcPath) if os.srcPath.isdir(dir) ]
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
    #   ## if os.srcPath.isdir(dir) and "retrieved" in dir:
    #   if os.srcPath.isdir(dir):
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
    #     srcFile = srcPath + '/' + srcFile
    #
    #     ## print("Source: {};\n Destination: {}".format(srcFile, dstFile))
    #
    #     self.extractSubtitles(srcFile, dstFile)






if __name__ == "__main__":
  inst_merge_textfiles = merge_textfiles()
  # # srcPath = "C:/38-Git"
  # srcPath = "C:/zz_A1_Backup/38-Git"
  # inst_merge_textfiles.merge_files(srcPath)

  srcPath = "C:/zz_A1_Backup/38-Git"
  dstPath = "C:/85-Data/Subtitles"
  inst_merge_textfiles.merge_files_to_one(srcPath, dstPath)
  
  