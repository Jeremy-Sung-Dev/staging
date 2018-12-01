#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" RemoteServer.pyllenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 7/7/2018 5:14 AM
  __Email__ = Jeremy.Sung@osh.com
  
Todo:
 - Get /etc/sysconfig/iptables
 - Create a copy
 - Update the content of the file and sftp.put it back as the same filename at the same place2018

"""

import os, re
from ldap3 import Server, Connection, SUBTREE, DEREF_ALWAYS
import bz2
import paramiko
import argparse
import pprint as pp
import Enums
from Utils import walkTrees



class RemoteServer:

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
    Return an SSH handle in order for further Remote Execuation of cmd on Remote Linux Server.

    If "sudo" is required the script need to promput user for password though:
      cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")

    Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
    """

    return self.ssh.exec_command(cmd)


  def getRemoteFile(self, filename):

    sftp = self.ssh.open_sftp()

    results_l = []
    with sftp.file(filename, 'r', -1) as file:

      for line in file:
        results_l.append(line.strip())

    sftp.close()
    return results_l


  def auditFWRule(self, filename, pattern):
    """
    Find out whether a host has an iptable rule:
     -A INPUT -m state --state NEW -m tcp -p tcp --dport 28002 -j ACCEPT
    :return:
    """

    rules_host_l = self.getRemoteFile(filename)

    Host_W_Rule_d = {}
    Host_WO_Rule_d = {}

    for rule in rules_host_l:

      if pattern in rule:
        Host_W_Rule_d[self.host] = rule
        # return {self.host : rule}
      else:
        Host_WO_Rule_d[self.host] = rule
        # return {self.host : rule}

    return Host_W_Rule_d, Host_WO_Rule_d







  def updateRemoteFile(self, filename):
    pass




if __name__ == "__main__":

  # host = "admin01"
  # host = "mars-app91"
  # # hosts = [ "mars-app01", "oracledb01"]
  # #
  # port = 22
  # userid = 'root'
  # # privateKey_jsung = "C:/admin/id_rsa"
  # privateKey_root = "C:/admin/id_rsa_root"
  #
  # RemoteServer = RemoteServer(hostname=host, userid=userid, privateKey=privateKey_root )
  ## RemoteServer = RemoteServer(hostname=host, userid=userid, privateKey=privateKey_jsung )
  #
  # iptable_Rule = r"-A INPUT -m state --state NEW -m tcp -p tcp --dport 28002 -j ACCEPT"
  #
  # # ## Execute command on Remote Server And How to Utilize the result from Remote ExeC():
  # # stdin, stdout, stderr = RemoteServer.exeC('uptime')
  # # for line in stdout.readlines():   # Critical!!!
  # #   print(line.strip())
  #
  # ## Need to append this iptable rule at the bottom of Accept rules and right above the first Deny, Drop or Reject ones;
  #
  # path = "/etc/sysconfig/"
  # filename = "iptables"
  # pathFile = path + filename
  # # print(pathFile)
  #
  # content_l = RemoteServer.getRemoteFile(pathFile)
  # pp.pprint(content_l)
  #
  ##
  ##### =====   Audit remote server:/etc/sysconfig/iptables; Look for rule:  port 28002  ===========================
  ##
  ## Get a list of [ Hosts of MARS|WMS|Polling|Support ] from a file:
  # pathHosts = "C:/bin/hosts_mars_wms_polling"
  # walkTrees = walkTrees()
  # hosts_mars_wms_pollings_l = walkTrees.readLocalFile(filename=pathHosts)
  # ## Verify -  pp.pprint(hosts_mars_wms_pollings_l)
  #
  ## SSH port and Credential:
  # ssh_port = 22
  # userid = 'root'
  # ## privateKey_jsung = "C:/admin/id_rsa"
  # privateKey_root = "C:/admin/id_rsa_root"
  #
  # pathIPtables = "/etc/sysconfig/iptables"
  # dest_port = '28002'
  #
  # Exclude_Polling_Support_Hosts = ['polling', 'support']
  #
  # Hosts_W_Rule_l = []
  # Hosts_WO_Rule_l = []
  #
  # for host in hosts_mars_wms_pollings_l:
  #
  #   ## Exclude Pollings & Supports:
  #   if any(server in host for server in Exclude_Polling_Support_Hosts):
  #     continue
  #
  #   ## Tell which host we are:
  #   print("Host: {}".format(host))
  #
  #   ## Each remote server - create a RemoteServer object :
  #   remoteSRV = RemoteServer(hostname=host, userid=userid, privateKey=privateKey_root)
  #
  #   ## Return two dicts, one for servers w/ port 28002 and the other, w/o port 28002:
  #   Host_W_Rule_d, Host_WO_Rule_d = remoteSRV.auditFWRule(filename=pathIPtables, pattern=dest_port)
  #
  #   ## If the host has port 28002 rule in /etc/sysconfig/iptables:
  #   if Host_W_Rule_d:
  #     ## If the host has port 28002 rule in /etc/sysconfig/iptables, append to this list:
  #     Hosts_W_Rule_l.append(Host_W_Rule_d)
  #   else:
  #     ## If the host doesn't have port 28002 rule in /etc/sysconfig/iptables, append to the other list:
  #     Hosts_WO_Rule_l.append(Host_WO_Rule_d)
  #
  # ## Verify -
  # ## pp.pprint(Hosts_W_Rule_l)
  # ## pp.pprint(Hosts_WO_Rule_l)
  ##
  ##### =====  Check iptables rules on remote server :  port 28002  ===========================
  ##

  ## Get a list of [ Hosts of MARS|WMS|Polling|Support ] from a file:
  pathHosts = "C:/bin/hosts_mars_wms_polling"
  walkTrees = walkTrees()
  hosts_mars_wms_pollings_l = walkTrees.readLocalFile(filename=pathHosts)

  ## SSH port and Credential:
  ssh_port = 22
  userid = 'root'
  privateKey_root = "C:/admin/id_rsa_root"

  pathIPtables = "/etc/sysconfig/iptables"
  dest_port = '28002'

  CMD_check_iptables_avtive_rules = r"iptables -L"
  CMD_reload_iptables = r"/bin/systemctl  reload  iptables.service"

  Exclude_Polling_Support_Hosts = ['polling', 'support']

  # Server_W_Active_28002_IptablesRules_d = {}
  # Server_WO_Active_28002_IptablesRules_d = {}

  Servers_W_Active_28002_IptablesRules_l = []
  Servers_WO_Active_28002_IptablesRules_l = []

  count_all = 0
  count_w_28002 = 0
  count_wo_28002 = 0

  for host in hosts_mars_wms_pollings_l:

    ## Exclude Pollings & Supports:
    if any(server in host for server in Exclude_Polling_Support_Hosts):
      continue

    ## Tell which host we are:
    # print("Host: {}".format(host))
    count_all += 1

    ##
    Server_W_Active_28002_IptablesRules_d = {}
    Server_WO_Active_28002_IptablesRules_d = {}

    ## Each remote server - create a RemoteServer object :
    remoteSRV = RemoteServer(hostname=host, userid=userid, privateKey=privateKey_root)

    stdin, stdout, stderr = remoteSRV.exeC(cmd=CMD_check_iptables_avtive_rules)

    # Server_Active_IptablesRules_d[host] = remoteSRV.exeC(cmd=CMD_check_iptables_avtive_rules)
    #
    # ## pp.pprint(Server_Active_IptablesRules_d[host])
    # ## <paramiko.ChannelFile from <paramiko.Channel 0 (open) window=2097152 -> <paramiko.Transport at 0x20ccebe0 (cipher aes128-ctr, 128 bits) (active; 1 open channel(s))>>>)

    for line in stdout.readlines():

      if '28002' not in line:
        continue
      else:
        Server_W_Active_28002_IptablesRules_d[host] = line
        Servers_W_Active_28002_IptablesRules_l.append(Server_W_Active_28002_IptablesRules_d)
        count_w_28002 += 1
        break


    ## Hosts has Yet enabled port 28002:
    if host not in Server_W_Active_28002_IptablesRules_d:
      Server_WO_Active_28002_IptablesRules_d[host] = ""
      count_wo_28002 += 1

      ## Reload new /etc/sysconfig/iptables:
      print("Reload iptables on Host: {}".format(host))
      remoteSRV.exeC(cmd=CMD_reload_iptables)


    Servers_WO_Active_28002_IptablesRules_l.append(Server_WO_Active_28002_IptablesRules_d)

  Servers_W_Active_28002_IptablesRules_l.append(Server_W_Active_28002_IptablesRules_d)

  # Servers_WO_Active_28002_IptablesRules_l = [srv for srv in Servers_WO_Active_28002_IptablesRules_l if srv]
  Servers_WO_Active_28002_IptablesRules_l = [srv_d.keys() for srv_d in Servers_WO_Active_28002_IptablesRules_l if srv_d]

  pp.pprint(Servers_W_Active_28002_IptablesRules_l)
  pp.pprint(Servers_WO_Active_28002_IptablesRules_l)
  print("Total: {}, Hosts enabled: {}, Hosts yet enabled: {}".format(count_all, count_w_28002, count_wo_28002))

  ##
  ##### =====  --------------------------------------------------------------------  ===========================
  ##
