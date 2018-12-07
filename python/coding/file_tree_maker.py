#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" file_tree_maker.py

Description:
 Under construction due to : UnicodeEncodeError: 'charmap' codec can't encode characters in position 13-14: character maps to <undefined
 
Reference:
 FileTreeMaker.py - https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
 answered Sep 18 '15 at 16:01

Attributes:
  __version__ = 12/6/2018 10:29 PM, __project__ = staging, __author__ = "legendmohe", __email__ = jsungcoding@gmail.com
"""

import os
import argparse
import time


class FileTreeMaker:

  def _recurse(self, parent_path, file_list, prefix, output_buf, level):

    if len(file_list) == 0 \
      or (self.max_level != -1 and self.max_level <= level):
      return

    else:

      file_list.sort(key=lambda f: os.path.isfile(os.path.join(parent_path, f)))
      for idx, sub_path in enumerate(file_list):

        if any(exclude_name in sub_path for exclude_name in self.exn):
          continue

        full_path = os.path.join(parent_path, sub_path)
        idc = "┣━"

        if idx == len(file_list) - 1:
          idc = "┗━"

        if os.path.isdir(full_path) and sub_path not in self.exf:

          output_buf.append("%s%s[%s]" % (prefix, idc, sub_path))

          if len(file_list) > 1 and idx != len(file_list) - 1:
            # tmp_prefix = prefix + "┃  "
            tmp_prefix = prefix + u"┃  "
          else:
            # tmp_prefix = prefix + "    "
            tmp_prefix = prefix + u"    "

          self._recurse(full_path, os.listdir(full_path), tmp_prefix, output_buf, level + 1)

        elif os.path.isfile(full_path):
          output_buf.append("%s%s%s" % (prefix, idc, sub_path))

  def make(self, **args):

    # self.root = args.root
    # self.exf = args.exclude_folder
    # self.exn = args.exclude_name
    # self.max_level = args.max_level

    self.root = args["root"]
    self.exf = args["exclude_folder"]
    self.exn = args["exclude_name"]
    self.max_level = args["max_level"]

    print("root:%s" % self.root)

    buf = []
    path_parts = self.root.rsplit(os.path.sep, 1)
    buf.append("[%s]" % (path_parts[-1],))
    # self._recurse(self.root, os.listdir(self.root), "", buf, 0)
    self._recurse(self.root, os.listdir(self.root), u"", buf, 0)

    output_str = "\n".join(buf)

    # if len(args.output) != 0:
    #   with open(args.output, 'w') as of:
    #     of.write(output_str)

    if len(args["output"]) != 0:
      with open(args["output"], 'w') as of:
        of.write(output_str)
        """ return codecs.charmap_encode(input,self.errors,encoding_table)[0] 
        UnicodeEncodeError: 'charmap' codec can't encode characters in position 13-14: character maps to <undefined>"""

    return output_str


if __name__ == "__main__":

  # parser = argparse.ArgumentParser()
  # parser.add_argument("-r", "--root", help="root of file tree", default=".")
  # parser.add_argument("-o", "--output", help="output file name", default="")
  # parser.add_argument("-xf", "--exclude_folder", nargs='*', help="exclude folder", default=[])
  # parser.add_argument("-xn", "--exclude_name", nargs='*', help="exclude name", default=[])
  # parser.add_argument("-m", "--max_level", help="max level", type=int, default=-1)
  # args = parser.parse_args()

  path = "C:/38-Git"
  # path = "C:/zz_A1_Backup/38-Git"
  output_filename = "mergedSubtitles.txt"
  exclude_folder = ""
  exclude_name = ""
  max_level = 1

  args = { "root" : path , "output" : output_filename, "exclude_folder" : exclude_folder, "exclude_name" : exclude_name, "max_level" : max_level}

  inst_FileTreeMaker = FileTreeMaker()
  ## print(inst_FileTreeMaker.make(args))

  inst_FileTreeMaker.make(**args)


  