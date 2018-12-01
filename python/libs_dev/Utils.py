#!/usr/local/bin/python3.6
#!C:/staging/python/systems/Scripts/python.exe

from collections import defaultdict
import os, re
from ldap3 import Server, Connection, SUBTREE, DEREF_ALWAYS
import bz2
import paramiko
import argparse
import pprint as pp
import Enums





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


  def readLocalFile(self, filename):
    """
    Read a file in local FileSystem and return its content as a list, lines_l,
    :param filename:
    :return:
    """

    lines_l = []

    if os.path.isfile(filename):

      with open(filename, 'r', encoding="utf-8") as lines:

        for line in lines:
          if line:
            lines_l.append(line.strip())

    return lines_l



class RemoteTrees():


  def __init__(self, hostname="admin01", userid="_jsung", passwd="", privateKey="", port=22):

    self.host = hostname
    self.port = port if port else 22
    self.userid = userid
    self.passwd = passwd if passwd else ""
    self.privateKey = privateKey

    self.ssh = paramiko.SSHClient()
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if privateKey:
      self.ssh.connect(self.host, self.port, username=self.userid, key_filename=self.privateKey)
    else:
      self.ssh.connect(self.host, self.port, username=self.userid, password=self.passwd)


  def exeC(self, cmd):
    """
    Execuate cmd on remote Linux Server.
    If "sudo" is required the script need to promput user for password though:
      cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")
    Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh

    :param cmd:
    :return:
    """

    return self.ssh.exec_command(cmd)


  def readRemoteFile(self, filename):

    sftp = self.ssh.open_sftp()

    results_l = []
    with sftp.file(filename, 'r', -1) as file:

      for line in file:
        results_l.append(line.strip())

    sftp.close()
    return results_l


  def readRemote_BZ2_Messages_with_Filters(self, **kwFilters):
    """ /etc/messages-*  bz2  """

    pattern_messages = re.compile("(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*$)")
    compiled_messages = re.compile(pattern_messages)

    Included = kwFilters["Include"]
    Excluded = kwFilters["Exclude"]


    sftp = self.ssh.open_sftp()

    TimeStamps_RemoteServer_Root_Polling_l = []
    Hostnames_RemoteServer_Root_Polling_l = []
    Messages_RemoteServer_Root_Polling_l = []


    for filename in sftp.listdir("/var/log/"):

      if filename == "messages":  ## Long delay?!

        rfilePath = "/var/log/" + filename

        with sftp.file(rfilePath, 'r', -1) as messages:

          for line in messages:

            if any(term in line for term in Included):
              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))
            else:
              continue


      if filename.startswith("messages") and filename.endswith(".bz2"):

        rfilePath = "/var/log/" + filename

        with bz2.open(sftp.open(rfilePath, 'r', -1), 'rt', encoding="utf-8") as messages_bz2:

          for line in messages_bz2:

            if not line.startswith(self.LastMonth):
              continue

            # groups = compiled_messages.search(line)

            if any(term in line for term in Included):
              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))
            else:
              continue

    sftp.close()

    return TimeStamps_RemoteServer_Root_Polling_l, Hostnames_RemoteServer_Root_Polling_l, Messages_RemoteServer_Root_Polling_l






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
