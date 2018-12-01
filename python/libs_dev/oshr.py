#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe
# -*- coding: utf-8 -*-
""" Oshr.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/2/2018 11:23 AM
  __Email__ = Jeremy.Sung@osh.com
  
Ref.
 - https://stackoverflow.com/questions/10745138/python-paramiko-ssh
"""

import argparse
import paramiko
import pprint as pp



class Oshr:
  """
  ## cmd = 'cat /etc/sudoers'
  ## If "sudo" is required the script need to promput user for password though:
  # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")

  """

  def __init__(self, **kwargs):

    # self.hostname = kwargs["hostname"] if "hostname" in kwargs else ""
    # self.hostnames = kwargs["hostnames"] if "hostnames" in kwargs else []

    self.port = kwargs["port"] if "port" in kwargs else 22
    self.userid = kwargs["userid"] if "userid" in kwargs else ""
    self.password = kwargs["password"] if "password" in kwargs else ""
    self.privateKey = kwargs["privateKey"] if "privateKey" in kwargs else ""

    ## self.commands = kwargs["commands"]


  def Connect(self, hostname="", port=22, userid="", password="", privateKey=""):
    ## Establish SSH session:

    self.ssh = paramiko.SSHClient()
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # if not self.hostname and not self.hostnames:
    #   print("Host: {} is empty or invalid. Please provide a valid hostname.".format(hostname))
    #   self.hostname = 'admin01'
    #   return

    ## if self.privateKey and self.hostname:
    if self.privateKey:
      self.ssh.connect(hostname, port, username=userid, key_filename=privateKey)
    else:
      self.ssh.connect(hostname, port, username=userid, password=password)



  def oshr(self, **kwargs):

    self.hostname = kwargs["hostname"] if "hostname" in kwargs else ""
    self.hostnames = kwargs["hostnames"] if "hostnames" in kwargs else []
    self.commands = kwargs["commands"]

    result_l = []

    if self.hostnames:

      for host in self.hostnames:

        result_l.append(host + ' :\n')

        self.Connect(hostname=host, port=self.port, userid=self.userid, privateKey=self.privateKey)



        for cmd in self.commands:

          stdin, stdout, stderr = self.ssh.exec_command(cmd)
          # stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_unsubscribed_all)
          ## stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_unregistered)

          for line in stdout.readlines():
            # if '^#' in line or '^$' in line:
            #   continue
            result_l.append("{}".format(line))

      self.ssh.close()

    elif self.hostname:

      result_l.append(self.hostname + ' :\n')
      self.Connect(hostname=self.hostname, port=self.port, userid=self.userid, privateKey=self.privateKey)

      for cmd in self.commands:

        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        # stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_unsubscribed_all)
        ## stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_unregistered)

        for line in stdout.readlines():
          # if '^#' in line or '^$' in line:
          #   continue
          result_l.append("{}".format(line))

    else:
      print("Host is empty or invalid. Please provide a valid hostname.")

    self.ssh.close()

    pp.pprint(result_l)

    # self.ssh.close()
    # return result_l


if __name__ == "__main__":

  ## Worked!  Similar to Oshr.pl;

  ## Argparse Initiatives:
  ## Allow interaction with console:

  parser = argparse.ArgumentParser(prog='oshr.py', prefix_chars='-+', description='util to execute Linux commands remotely',
                                   add_help=True, allow_abbrev=True)

  parser.add_argument("-C", "--command", required=True, help="Linux command to execute on remote host")
  # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # parser.add_argument("-C", "--command", action="store_true", help="Linux command to execute")
  ## Positional:
  # parser.add_argument('bar', help='positional bar')
  parser.add_argument("-l", "--Log", default="C:/staging/python/pilot", help="Show content in reportPath")
  # pp.pprint(parser)

  args = parser.parse_args()
  # pp.pprint(args)

  ## Have to execute with "python" in front!!
  ## C:\staging\python\pilot>python dev_oshr.py --command date
  ## Namespace(command='date', reportPath='C:/staging/python/pilot')

  ## Doesn't work:
  ## C:\staging\python\pilot> dev_oshr.py --command date  # unable to recognize "--command date"

  ##
  ### print("Command: {},\tReport: {}".format(args.command, args.Log))
  ##
  ## print(args.command)
  ## print("Command: {}".format(args.command))
  ## pp.pprint(args.command)
  ## result_l = auditSC_LocalAdminAccess.exeC(args.co)

  # pp.pprint(result_l)

  # ###############################################################################################

  ## hostname = 'wms-wmosapp91'  # wms-app91.orchard.osh
  ## hostnames = ['10.1.19.21', 'wms-app91', 'wmsci-db91']
  ## hostnames = ['10.1.19.21', '10.1.19.20']
  hostnames = ['wms-app01']


  # cmd_date = "date"
  # cmd_cat_release = "cat /etc/*release"
  # cmd_ifconfig_a = "ifconfig -a"
  # ## cmd_cat_release = 'cat /etc/*release'
  # ## cmd_shutdown = "shutdown -P 2"
  # # cmd_unsubscribed_all = 'subscription-manager unsubscribe --all'
  # # cmd_unregistered = 'subscription-manager unregister'

  cmd = args.command
  print("Command: {},\tReport: {}".format(cmd, args.Log))

  port = 22
  userid = 'root'

  privateKey_root = "C:/admin/id_rsa_root"

  # kwargs = { "hostnames" : hostnames,
  #            "port" : 22,
  #            "userid" : "root",
  #            "privateKey" : "C:/admin/id_rsa_root",
  #            "commands" : [cmd_date, cmd_cat_release, cmd_ifconfig_a]}

  kwargs = { "hostnames" : hostnames,
             "port" : 22,
             "userid" : "root",
             "privateKey" : "C:/admin/id_rsa_root",
             "commands" : [cmd]}

  oshr1 = Oshr(**kwargs)


  oshr1.oshr(**kwargs)



