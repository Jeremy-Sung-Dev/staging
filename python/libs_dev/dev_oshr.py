#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dev_oshr.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = Dev
  __author__ = Jeremy Sung
  __date__ = 6/26/2018 1:27 PM
  __Email__ = Jeremy.Sung@osh.com

Ref.
  https://stackoverflow.com/questions/10745138/python-paramiko-ssh

Todo:
 - Need to add parallel or hyper-threading

"""

import argparse
import paramiko
import pprint as pp

class dev_oshr:

  def __init__(self, host="", port=22, userid="", passwd="", privateKey=""):
    self.hostname = host
    self.port = port if port else 22
    self.userid = userid
    self.passwd = passwd if passwd else ""
    self.privateKey = privateKey

    self.ssh = paramiko.SSHClient()
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if privateKey:
      self.ssh.connect(self.hostname, self.port, username=self.userid, key_filename=self.privateKey)
    else:
      self.ssh.connect(self.hostname, self.port, username=self.userid, password=self.passwd)


  def exeC(self, cmd):
    """
    Can run any Linux commands as root@admin01;
    even for those require sudo privilege, such as "cat /etc/sudoers"
    :param cmd:
    :return:
    """

    stdin, stdout, stderr = self.ssh.exec_command(cmd) # Here we only take the output. Can use stdin or stderr

    result_l = []

    for line in stdout.readlines():
      if '^#' in line or '^$' in line:
        continue

      result_l.append(line)

    self.ssh.close()
    return result_l



if __name__ == "__main__":

  # server = '10.1.19.21'  # wms-app91.orchard.osh
  # server = '10.1.2.210'  # wms-wmosapp01.orchard.osh
  # server = '10.1.19.8'  # mars-app91.orchard.osh
  hostname = '10.1.3.177'  # admin01.orchard.osh
  port = 22
  userid = 'root'

  privateKey_root = "C:/admin/id_rsa_root"

  pilotSSH = dev_oshr(host=hostname, port=port, userid=userid, privateKey=privateKey_root)

  # cmd_sudoers = 'cat /etc/sudoers'
  # cmd_passwd = 'cat /etc/passwd'
  ## If "sudo" is required the script need to promput user for password though:
  # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")
  # cmd = 'cat /var/log/secure | head -30'
  # cmd = "server; cat /etc/*release; date"
  # result_l = auditSC_LocalAdminAccess.exeC(cmd)
  # result_l = auditSC_LocalAdminAccess.exeC(cmd_sudoers)


  ## Argparse Initiatives:
  parser = argparse.ArgumentParser(prog='dev_oshr.py', prefix_chars='-+', description='util to execute Linux commands',
                                   add_help=True, allow_abbrev=True)
  parser.add_argument("-C", "--command", required=True, help="Linux command to execute")
  # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # parser.add_argument("-C", "--command", action="store_true", help="Linux command to execute")
  ## Positional:
  # parser.add_argument('bar', help='positional bar')
  # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # pp.pprint(parser)

  args = parser.parse_args()
  # pp.pprint(args)

  ## Have to execute with "python" in front!!
  ## C:\staging\python\pilot>python dev_oshr.py --command date
  ## Namespace(command='date', reportPath='C:/staging/python/pilot')

  ## Doesn't work:
  ## C:\staging\python\pilot> dev_oshr.py --command date  # unable to recognize "--command date"


  # print(args.command)
  # print("Command: {}".format(args.command))
  # print("Command: {},\tReport: {}".format(args.command, args.report))
  # pp.pprint(args.command)

  result_l = pilotSSH.exeC(args.command)
  # result_l = auditSC_LocalAdminAccess.exeC(args.co)

  pp.pprint(result_l)