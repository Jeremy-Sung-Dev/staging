#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe

# -*- coding: utf-8 -*-
""" keepServiceLive.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "0.1.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 8/9/2018 12:38 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import paramiko


class keepServiceLive:

  def __init__(self, **kwargs):

    self.services = kwargs['services']
    self.hostnames = kwargs['hostnames'] if "hostnames" in kwargs else []  ## expect a list of hosts

    self.port = kwargs["port"] if "port" in kwargs else 22
    self.userid = kwargs["userid"] if "userid" in kwargs else ""
    self.password = kwargs["password"] if "password" in kwargs else ""
    self.privateKey = kwargs["privateKey"] if "privateKey" in kwargs else ""


  def Connect(self, hostname="", port=22, userid="", password="", privateKey=""):

    ## Establish SSH session:
    self.ssh = paramiko.SSHClient()
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if self.privateKey:
      self.ssh.connect(hostname, port, username=userid, key_filename=privateKey)
    else:
      self.ssh.connect(hostname, port, username=userid, password=password)



  def keepservicelive_in_host(self, hostname=""):

    ## rssh = Oshr(**kwargs)

    result_l = []

    process = "java"
    service = "openfire"
    cmd_chkProcess = "ps -ef"
    cmd_chkService = "service " + service + " status"
    cmd_startService = "service " + service + " start"

    self.Connect(hostname=hostname, port=self.port, userid=self.userid, privateKey=self.privateKey)

    result_l = []

    cntRestart = 0

    stdin, stdout, stderr = self.ssh.exec_command(cmd_chkProcess)

    for line in stdout.readlines():

      if "openfire" in line:
        result_l.append(line)

    if result_l:
      print("Openfire is alive.")
    else:
      print("Openfire died.")
      print("Attempt to restart the service...")

      self.ssh.exec_command(cmd_startService)
      cntRestart += 1

      self.keepservicelive_in_host(hostname)

    self.ssh.close()

    print("Restart attempt(s): {}".format(cntRestart))



  def keepservicelive_in_hosts(self):

    if self.hostnames:

      for host in self.hostnames:
        self.keepservicelive_in_host(host)

    else:
      print("Host {} is empty or invalid. Please provide a valid hostname.".format(self.hostnames))



if __name__ == "__main__":

  privateKey_root_Windows = "C:/admin/id_rsa_root"
  privateKey_root_Linux = "/root/.ssh/id_rsa"

  service = "openfire"
  cmd_chkService = "service " + service + " status"
  cmd_startService = "service " + service + " start"

  kwargs = { "services" : ["openfire"],
             "hostnames" : {"admin01.orchard.osh"},
             "port" : 22,
             "userid" : "root",
             "password" : None,
             ## "privateKey" : privateKey_root_Windows,
             "privateKey" : privateKey_root_Linux,
             "commands" : [cmd_chkService, cmd_startService] }

  hostname = 'admin01.orchard.osh'


  keepServiceLive = keepServiceLive(**kwargs)
  keepServiceLive.keepservicelive_in_host(hostname)




