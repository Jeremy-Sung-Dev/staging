#!C:/ProgramData/Anaconda3/python.exe
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" extract_subtitles_from_srt.py

Description:
 + Retrieve text in an .srt file; all .srt files in a directory;
 + Allow users to specify the path to the srt file interactively;
 + Allow CLI options;
 - Check in my Git repository
   - Files in zzArchives should Not be version-controlled, i.e. check in GitHub;
 - Share my work in detail in my Wordpress or GitHub, public portfolios;
 + what are the knowledge gaps I need to mitigate to make it happen? Focus on identify and solve them.

Attributes:
 __version__ = "0.0.1", __project__ = coding, __author__ = Jeremy Sung, __date__ = 12/1/2018 11:54 AM, __Email__ = jsung8@gmail.com
 - Added: Read JSON files, get a list of directories and place them in a dictionary to parse all source SRT files;
 - Added: Generated a dict of Subtitles directories and dump the dictionary to a JSON file.  dumpJSON_Paths()
"""

import os, argparse, json
import pprint as pp

class extractSubtitlesFromSRT:

  ## def __init__(self, json_input = 'C:/staging/python/txt/do_not_remove.json'):
  ##   self.json_input = json_input


  def readJSON(self, json_input = 'C:/staging/python/txt/do_not_remove.json'):

    self.json_input = json_input

    jsonF = open(self.json_input)
    jsonF_str = jsonF.read()
    self.srcPaths = json.loads(jsonF_str)


  def dumpJSON_Paths(self, path = 'C:/38-Git', json_file = ""):

    srcDirs = {}
    listSrcDirs = []

    if not os.path.exists(path):
      return

    for srcDir in os.listdir(path):

      if ".zip" in srcDir or srcDir.startswith('zz'):
        continue

      if "Subtitles" in srcDir:
        srcDir = path + '/' + srcDir
        listSrcDirs.append(srcDir)

    srcDirs["srcDirs"] = listSrcDirs

    with open(json_file, 'w') as jf:
      json.dump(srcDirs, jf)


  def extractSubtitles(self, srcFile, dstFile):

    with open(srcFile, "r") as srcf, open(dstFile, "a") as dstf:

      for text in filter(None, (line.rstrip() for line in srcf)):

        if "-->" not in text and not text.isnumeric():
          dstf.write(text + ' ')


  def extractSubtitlesFromPath(self, path = ""):

    subdirRetrieved = r'retrieved'
    dstPath = path + '/' + subdirRetrieved
    if not os.path.exists(dstPath):
      os.makedirs(dstPath)

    for srcFile in os.listdir(path):

      if srcFile.endswith("lang_en.srt") or "lang_en" in srcFile:

        dstFile = dstPath + '/' + srcFile.strip(".srt") + r".txt"
        srcFile = path + '/' + srcFile

        ## print("Source: {};\n Destination: {}".format(srcFile, dstFile))

        self.extractSubtitles(srcFile, dstFile)


  def extractSubtitlesFromPaths(self, srcPaths = ""):

    if not self.srcPaths:
      self.srcPaths = srcPaths

    for srcPath in self.srcPaths['srcDirs']:

      ## print("Source Path: {}".format(srcPath))

      if ".zip" in srcPath or srcPath.startswith('zz'):
        continue

      if "Subtitles" in srcPath:
        self.extractSubtitlesFromPath(srcPath)


if __name__ == "__main__":

  # ## Argparse Initiatives:
  # parser = argparse.ArgumentParser(prog='extract_subtitles_from_srt.py', prefix_chars='-+', description='Extract Captions from SRT file',
  #                                  add_help=True, allow_abbrev=True)
  #
  # parser.add_argument("-p","--path", default="c:/lab", help="Path to source SRT file(s)")
  # parser.add_argument("-s","--source_file", help="Source SRT Filename")
  # parser.add_argument("-d","--destination_file", help="Name of Retrieved Text File")
  # ## parser.add_argument("-p","--path", required=True, help="Path to source SRT file(s)")
  # ## parser.add_argument("-s","--source_file", choices=[3.6, 2.6], default=3.6, help="Show version")
  # ## parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # ## parser.add_argument("-V", "--verbose", action="store_true")
  # parser.add_argument("-q", "--quiet", action="store_true")
  # ## Positional:
  # # parser.add_argument('bar', help='positional bar')
  # ## Usage:  C:\staging\python\coding>python extract_subtitles_from_srt.py -p c:/lab
  #
  # args = parser.parse_args()
  #
  # if args.quiet:
  #   print(args)
  # elif args.source_file:
  #   print("Verbose - Path: {},\tSource File: {},\tDestination File: {}".format(args.path, args.source_file, args.destination_file))
  # ##
  # #########################################################################################################
  # ## Instantiate a Class object - Begin:
  # inst_aextractSubtitlesFromSRT = extractSubtitlesFromSRT()
  #
  # ## json_input = 'C:/staging/python/coding/src_subtitle_dirs.json'
  # ## inst_aextractSubtitlesFromSRT = extractSubtitlesFromSRT(json_input)
  #
  # ## path = r"c:/lab"  ## args.path
  # ##
  # ##
  # ## Individual SRT file:
  # ##
  # # source_file = r"7 - How To Succeed - lang_en.srt"
  # # destinaiton_file = source_file.strip(".srt") + r".txt"
  # #
  # # pathSourceFile, pathDestinationFile = path + source_file, path + destinaiton_file
  # #
  # ## Validation:
  # #  print("Source: {};\nDestination: {}".format(source_file, destinaiton_file))
  # #
  # # inst_aextractSubtitlesFromSRT.extractSubtitles(pathSourceFile, pathDestinationFile)
  # #
  # ##
  # ## Validation:
  # ##
  # # with open(pathDestinationFile, 'r') as dstFile:
  # #   for line in dstFile:
  # #     print(line)
  #
  # ##
  # ## Entire directory, all SRT files:
  # ##
  # ## inst_aextractSubtitlesFromSRT.extractSubtitlesFromPath(path)
  #
  # ##
  # ## Entire directory, all SRT files - CLI:
  # ##
  # ## CLI Usage: C:\staging\python\coding>python extract_subtitles_from_srt.py -p c:/lab
  # ## CLI Usage: C:\staging\python\coding>python extract_subtitles_from_srt.py -p C:\10-DataScientist\031Data_Scientist\Welcome+to+the+Data+Scientist+Nanodegree+program+Subtitles
  # ##
  # inst_aextractSubtitlesFromSRT.extractSubtitlesFromPath(args.path)
  #
  # # ##
  # # ## Debug and validation:
  # # ##
  # # subdirRetrieved = r'retrieved'
  # #
  # # ## dstPath = path + '/' + subdirRetrieved
  # # dstPath = args.path + '/' + subdirRetrieved
  # #
  # # if os.path.exists(dstPath):
  # #
  # #   for dstFile in os.listdir(dstPath):
  # #
  # #     if dstFile.endswith(".txt"):
  # #
  # #       dstFilePath = dstPath + '/' + dstFile
  # #       ## print("Filename: {}".format(dstFilePath))
  # #
  # #       with open(dstFilePath, 'r') as f:
  # #         for line in f:
  # #           print(line)
  # ##
  #########################################################################################################
  ##
  ## JSON Dump (write) - Generate a JSON file which lists all subdirs with SRT files:
  ##
  inst_aextractSubtitlesFromSRT = extractSubtitlesFromSRT()

  srcRootDir = 'C:/38-Git'
  json_file = "C:/38-Git/srcDirs.json"
  inst_aextractSubtitlesFromSRT.dumpJSON_Paths(srcRootDir, json_file)
  ##
  ## Test - JSON read:
  ##
  # json_input = r'C:/staging/python/coding/src_subtitle_dirs.json'
  json_input = json_file
  inst_aextractSubtitlesFromSRT.readJSON(json_input)

  ## pp.pprint(inst_aextractSubtitlesFromSRT.srcPaths)
  inst_aextractSubtitlesFromSRT.extractSubtitlesFromPaths()
  ##
  #########################################################################################################
  ##
