#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" merge_textfiles.py

Description: Merge Subtitles Text files

Attributes:
  __version__ = 12/6/2018 4:13 PM, __project__ = staging, __author__ = Jeremy Sung, __email__ = jsungcoding@gmail.com
"""

import os, argparse
from collections import deque
import pprint as pp

class merge_textfiles:

  def merge_files(self, path = "C:/38-Git"):
    """ Merge Texts into retrieved subdir for each Lesson."""

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
    """ Extract Texts from SRTs and Merge into a file for a course;
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

  ## Argparse Initiatives:
  parser = argparse.ArgumentParser(prog='merge_textfiles.py', prefix_chars='-+', description='Extract text from SRTs and Merge',
                                   add_help=True, allow_abbrev=True)

  parser.add_argument("-sp","--srcPath", default="c:/zz_A1_Backup/38-Git", help="Path to source SRT file(s)")
  ## parser.add_argument("-s","--source_file", help="Source SRT Filename")
  parser.add_argument("-dp","--dstPath", help="Path to the destination file for final retrieved texts")
  ## parser.add_argument("-p","--srcPath", required=True, help="Path to source SRT file(s)")
  ## parser.add_argument("-s","--source_file", choices=[3.6, 2.6], default=3.6, help="Show version")
  ## parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  ## parser.add_argument("-V", "--verbose", action="store_true")
  parser.add_argument("-q", "--quiet", action="store_true")
  ## Positional:
  # parser.add_argument('bar', help='positional bar')
  ## Usage:  C:\staging\python\coding>python extract_subtitles_from_srt.py -p c:/lab

  args = parser.parse_args()

  # if args.quiet:
  #   print(args)
  # elif args.srcPath:
  #   print("Verbose - Source Path: {},\tDestination File: {}".format(args.srcPath, args.dstPath))
  #   ## print("Verbose - Path: {},\tSource File: {},\tDestination File: {}".format(args.srcPath, args.source_file, args.destination_file))

  inst_merge_textfiles = merge_textfiles()

  # ##
  # ## Merge all Subtitles Text files in a lesson to a retrieved subdir ;
  # ##
  # # srcPath = "C:/38-Git"
  # srcPath = "C:/zz_A1_Backup/38-Git"
  # inst_merge_textfiles.merge_files(srcPath)

  ##
  ## Extract SRTs and Merge to a file in destination for a course.
  ## CLI : C:\Users\Jeremy Sung>python c:\staging\python\coding\merge_textfiles.py --srcPath "C:/zz_A1_Backup/38-Git" --dstPath "C:/85-Data/Subtitles"
  ##
  srcPath = args.srcPath if args.srcPath else "C:/zz_A1_Backup/38-Git1"
  dstPath = args.dstPath if args.dstPath else "C:/85-Data/Subtitles1"
  inst_merge_textfiles.merge_files_to_one(srcPath, dstPath)
  
  