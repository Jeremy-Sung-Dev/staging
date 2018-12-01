#!/usr/local/bin/python3.6
#!C:/staging/python/systems/Scripts/python.exe

import os
from collections import defaultdict
# import pprint as pp

class walkTrees:


  def listFiles(self, startPath, bSubTree=True):
    """
    Ref: https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    :param startPath:
    :return:
    """

    # fsStructure = defaultdict(list)
    # directories_l, files_l = [], []

    files_l = []
    for path, dirs, files in os.walk(startPath, topdown = True):

      level = path.replace(startPath, '').count(os.sep)
      indent = ' ' * 2 * (level)
      # print('{}{}/'.format(indent, os.path.basename(path)))
      subindent = ' ' * 2 * (level + 1)

      for f in files:
        # print('{}{}'.format(subindent, f))
        files_l.append(f)

      # Do not search sub-tree next level
      if not bSubTree:
        break

    return files_l
    # return reportPath, directories_l, files_l



if __name__ == "__main__":

  utils = walkTrees()

  # startPath = "C:/staging"

  # reportPath, directories_l, files_l = utils.listFiles(startPath)

  # utils.listFiles(startPath)

  ## print the last directory:
  # print(reportPath)

  ## multi-dimensional list, i.e. list of lists:
  ## A DFS style of directory in hierarchical; list of lists:
  # print(directories_l)
  # pp.pprint(directories_l)

  ## a flat list of files in a folder:
  # print(files_l)

  path = r"C:/staging/python/pilot/"
  utils.listFiles(path)
