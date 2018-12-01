#!/usr/lib/anaconda3/bin/python
# -*- coding: utf-8 -*-
""" auditSoxCompliance_ServerLocal.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "2.0.2"
  __project__ = Prod
  __author__ = Jeremy Sung
  __date__ = 6/27/2018 11:31 AM
  __Email__ = Jeremy.Sung@osh.com

"""

import os, re
import Enums
import pandas as pd
import openpyxl
import bz2
import paramiko
import pprint as pp
import argparse


class auditSoxCompliance_ServerLocal:

  def __init__(self, hostname="admin01", userid="root", passwd="", privateKey="", port=22, reportPath=""):
    """

    :param hostname:
    :param port:
    :param userid:
    :param passwd:
    :param privateKey:
    :param reportPath:
    """

    self.hostname = hostname
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


    if not os.path.isfile(reportPath):
      self.wb2 = openpyxl.Workbook()
      self.wb2.save(reportPath)

    self.reportPath = reportPath

    self.wb2 = pd.ExcelWriter(self.reportPath, engine='openpyxl')
    self.book = openpyxl.load_workbook(self.reportPath)
    self.wb2.book = self.book

    self.DateTime = Enums.DateTime
    self.LastMonth = Enums.LastMonth

    self.CMD_passwd_shadow = r'date && cat /etc/passwd | grep -v "nologin" | grep -v "false" && cat /etc/shadow | grep -v ":!" | grep -v ":\*" | cut -d ":" -f 1'
    self.CMD_sudoers = r'date && cat /etc/sudoers | grep -v "^#" | grep -v "^$"'

    self.CMD_root_access_wms = r'sudo cat /var/log/secure-* /var/log/secure | grep `date +"%b" --date="1 month ago"` | grep -v "rfuser\|disconnect\|pam_unix" | grep -v "subsystem request for sftp" > access.log'
    self.CMD_root_access_mars = r'sudo cat /var/log/secure-* /var/log/secure | grep `date +"%b" --date="1 month ago"` | grep -v "rfuser\|disconnect\|pam_unix" | grep -v "subsystem request for sftp \| marssftp from 10.1.1.63"'
    self.CMD_Oracle_access_mars = r'sudo cat /var/log/secure-* /var/log/secure | grep `date +"%b" --date="1 month ago"` | grep sudo | grep USER=oracle'

    self.CMD_root_access_polling = r'sudo bzcat /var/log/messages-*.bz2 | grep `date +"%b" --date="1 month ago"` | grep "sudo\|sshd" | grep root | grep -v "nagios" && sudo cat /var/log/messages | grep `date +"%b" --date="1 month ago"` | grep "sudo\|sshd" | grep root | grep -v "nagios" '
    self.CMD_informix_access_polling = r'sudo bzcat /var/log/messages-*.bz2 | grep `date +"%b" --date="1 month ago"` | grep sudo | grep informix && sudo cat /var/log/messages | grep `date +"%b" --date="1 month ago"` | grep sudo | grep informix '


  def exeC(self, cmd):

    stdin, stdout, stderr = self.ssh.exec_command(cmd)

    result_l = []

    for line in stdout.readlines():
      if '^#' in line or '^$' in line:
        continue
      result_l.append(line)

    self.ssh.close()
    return result_l


  def scanLocalAdminAccounts_RemoteServer_SingleFile(self, filename, excludedPhrases):

    sftp = self.ssh.open_sftp()

    results_l = []
    with sftp.file(filename, 'r', -1) as file:

      for entry in file:

        if entry.startswith("#"):
          continue

        if any(term in entry for term in excludedPhrases):
          continue

        results_l.append(entry.strip())

    sftp.close()
    return results_l


  def scanPasswdShadow_RemoteServer(self):
    """
    Default: Inspeact Three Local Account DB and sudoer files: /etc/passwd, shadow or sudoers
    """

    Excluded_passwd = ('nologin', 'false')
    Excluded_shadow = (':!', ':*')

    resPasswordShadow_RemoteServer_l = self.scanLocalAdminAccounts_RemoteServer_SingleFile("/etc/passwd", Excluded_passwd)

    if resPasswordShadow_RemoteServer_l:
      resPasswordShadow_RemoteServer_l.extend( [ x.split(":")[0] for x in self.scanLocalAdminAccounts_RemoteServer_SingleFile("/etc/shadow", Excluded_shadow) ] )

    return resPasswordShadow_RemoteServer_l


  def scanSudoers_RemoteServer(self):
    """
    Default: Inspeact Three Local Account DB and sudoer files: /etc/passwd, shadow or sudoers
    """

    file_sudoers = "/etc/sudoers"
    Excluded_sudoers = ('^#', '^$')

    sftp = self.ssh.open_sftp()

    results_l = []
    with sftp.file(file_sudoers, 'r', -1) as sudoers:

      for entry in sudoers:

        if not entry.startswith("#"):

          if "\\" in entry:
            if '"'in entry:
              results_l.append(entry.strip().strip("\\").strip('"'))
            else:
              results_l.append(" " * 45 + entry.strip().strip("\\"))
          else:
            results_l.append(entry.strip())

    sftp.close()
    return [x for x in results_l if x]



  def scanHostAccess_RemoteServer_VarLogSecure_Generic(self, **kwFilters):
    """ /etc/secure and /etc/secure.* """

    pattern = re.compile("(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*$)")
    compiled = re.compile(pattern)

    Excluded = kwFilters["Exclude"]

    sftp = self.ssh.open_sftp()

    TimeStamps_RemoteServer_l = []
    Hostnames_RemoteServer_l = []
    Messages_RemoteServer_l = []

    for filename in sftp.listdir("/var/log/"):

      if filename.startswith("secure"):

        rfilePath = "/var/log/" + filename

        with sftp.file(rfilePath, 'r', -1) as secures:


          for line in secures:

            if not line.startswith(self.LastMonth):
              continue

            if any(term in line for term in Excluded):
              continue

            groups = compiled.search(line)

            TimeStamps_RemoteServer_l.append(groups.group(1).strip())
            Hostnames_RemoteServer_l.append(groups.group(2).strip())
            Messages_RemoteServer_l.append(groups.group(3))


    sftp.close()
    return TimeStamps_RemoteServer_l, Hostnames_RemoteServer_l, Messages_RemoteServer_l



  def scanHostAccess_RemoteServer_VarLogSecures(self, **kwFilters):
    """ /etc/secure-*   """

    pattern_messages = re.compile("(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*$)")
    compiled_messages = re.compile(pattern_messages)

    Included_All = kwFilters["Include_All"]
    Included_Any = kwFilters["Include_Any"]
    Excluded = kwFilters["Exclude"]

    sftp = self.ssh.open_sftp()

    TimeStamps_RemoteServer_Root_Polling_l = []
    Hostnames_RemoteServer_Root_Polling_l = []
    Messages_RemoteServer_Root_Polling_l = []

    for filename in sftp.listdir("/var/log/"):

      if filename.startswith("secure"):

        rfilePath = "/var/log/" + filename

        with sftp.file(rfilePath, 'r', -1) as secure:

          for line in secure:

            if not line.startswith(self.LastMonth):
              continue

            if any(item in line for item in Excluded):
              continue


            if Included_Any and any(term in line for term in Included_Any):
              if Included_All and all(term in line for term in Included_All):
                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            elif Included_All and all(term in line for term in Included_All):
              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            else:
              continue

    sftp.close()
    return TimeStamps_RemoteServer_Root_Polling_l, Hostnames_RemoteServer_Root_Polling_l, Messages_RemoteServer_Root_Polling_l



  def scanHostAccess_RemoteServer_VarLogMessages_BZ2_Polling(self, **kwFilters):
    """ /etc/messages-*  bz2  """

    pattern_messages = re.compile("(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*$)")
    compiled_messages = re.compile(pattern_messages)

    Included_All = kwFilters["Include_all"]
    Included_Any = kwFilters["Include_any"]
    Excluded = kwFilters["Exclude"]

    sftp = self.ssh.open_sftp()

    TimeStamps_RemoteServer_Root_Polling_l = []
    Hostnames_RemoteServer_Root_Polling_l = []
    Messages_RemoteServer_Root_Polling_l = []

    visitedFiles_s = set()

    for filename in sftp.listdir("/var/log/"):

      if filename in visitedFiles_s:
        print("File has checked: {} ".format(filename))
        break

      if not filename.startswith("messages"):
        continue

      elif not filename.endswith(".bz2"):
        continue

      else:

        print("File - messageXXXXX.bz2: {} ".format(filename))

        visitedFiles_s.add(filename)

        rfilePath = "/var/log/" + filename

        with bz2.open(sftp.open(rfilePath, 'r', -1), 'rt', encoding="utf-8") as messages_bz2:

          for line in messages_bz2:

            if not line.startswith(self.LastMonth):
              continue

            if any(item in line for item in Excluded):
              continue

            if Included_Any and any(term in line for term in Included_Any):

              if Included_All and all(term in line for term in Included_All):

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            elif Included_All and all(term in line for term in Included_All):

              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            else:
              continue

    for filename in sftp.listdir("/var/log/"):

      if filename != "messages":
        continue

      if filename in visitedFiles_s:
        print("File has checked: {} ".format(filename))
        continue

      if TimeStamps_RemoteServer_Root_Polling_l and Hostnames_RemoteServer_Root_Polling_l and Messages_RemoteServer_Root_Polling_l:

        visitedFiles_s.add(filename)

        print("File - /var/log/messages: {} ".format(filename))

        rfilePath = "/var/log/" + filename

        with sftp.file(rfilePath, 'r', -1) as messages:

          for line in messages:

            if not line.startswith(self.LastMonth):
              continue

            if any(item in line for item in Excluded):
              continue

            if Included_Any and any(term in line for term in Included_Any):
              if Included_All and all(term in line for term in Included_All):

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            elif Included_All and all(term in line for term in Included_All):

              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            else:
              continue
      else:
        break

    sftp.close()
    return TimeStamps_RemoteServer_Root_Polling_l, Hostnames_RemoteServer_Root_Polling_l, Messages_RemoteServer_Root_Polling_l



  def scanHostAccess_RemoteServer_VarLogMessages_BZ2_Root_Polling(self, **kwFilters):
    """ /etc/messages-*  bz2  """

    pattern_messages = re.compile("(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*$)")
    compiled_messages = re.compile(pattern_messages)

    Included_All_A = kwFilters["Include_all_A"]
    Included_All_B = kwFilters["Include_all_B"]
    Included_Any = kwFilters["Include_any"]
    Excluded = kwFilters["Exclude"]

    sftp = self.ssh.open_sftp()

    TimeStamps_RemoteServer_Root_Polling_l = []
    Hostnames_RemoteServer_Root_Polling_l = []
    Messages_RemoteServer_Root_Polling_l = []

    visitedFiles_s = set()

    for filename in sftp.listdir("/var/log/"):

      if filename in visitedFiles_s:
        print("File has checked: {} ".format(filename))
        break

      if not filename.startswith("messages"):
        continue

      elif not filename.endswith(".bz2"):
        continue

      else:

        print("File - messageXXXXX.bz2: {} ".format(filename))

        visitedFiles_s.add(filename)

        rfilePath = "/var/log/" + filename

        with bz2.open(sftp.open(rfilePath, 'r', -1), 'rt', encoding="utf-8") as messages_bz2:

          for line in messages_bz2:

            if not line.startswith(self.LastMonth):
              continue

            if any(item in line for item in Excluded):
              continue

            if Included_Any and any(term in line for term in Included_Any):
              if all(termA in line for termA in Included_All_A) or all(termB in line for termB in Included_All_B):

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            elif all(termA in line for termA in Included_All_A) or all(termB in line for termB in Included_All_B):

              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))
            else:
              continue

    for filename in sftp.listdir("/var/log/"):

      if filename != "messages":
        continue

      if filename in visitedFiles_s:
        print("File has checked: {} ".format(filename))
        continue

      if TimeStamps_RemoteServer_Root_Polling_l and Hostnames_RemoteServer_Root_Polling_l and Messages_RemoteServer_Root_Polling_l:

        visitedFiles_s.add(filename)

        print("File - /var/log/messages: {} ".format(filename))

        rfilePath = "/var/log/" + filename

        with sftp.file(rfilePath, 'r', -1) as messages:

          for line in messages:

            if not line.startswith(self.LastMonth):
              continue

            if any(item in line for item in Excluded):
              continue

            if Included_Any and any(term in line for term in Included_Any):

              if all(termA in line for termA in Included_All_A) or all(termB in line for termB in Included_All_B):

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            elif all(termA in line for termA in Included_All_A) or all(termB in line for termB in Included_All_B):

              groups = compiled_messages.search(line)

              TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
              Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
              Messages_RemoteServer_Root_Polling_l.append(groups.group(3))
            else:
              continue
      else:
        break


    sftp.close()
    return TimeStamps_RemoteServer_Root_Polling_l, Hostnames_RemoteServer_Root_Polling_l, Messages_RemoteServer_Root_Polling_l


  def scanHostAccess_RemoteServer_VarLogMessages_BZ2_Polling_sav(self, **kwFilters):
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

      if filename == "messages":

        rfilePath = "/var/log/" + filename

        with sftp.file(rfilePath, 'r', -1) as messages:

          for line in messages:

            if not line.startswith(self.LastMonth):
              continue

            if any(item in line for item in Excluded):
              continue

            if any(term in line for term in Included):

              print("/var/log/messages: {}".format(line))

              if "Include_Nest1" in kwFilters and kwFilters["Include_Nest1"] and any( nestItem in line for nestItem in kwFilters["Include_Nest1"]):

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

              else:

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

            if any(item in line for item in Excluded):
              continue

            if any(term in line for term in Included):
              print("/var/log/messages*.bz2: {}".format(line))

              if "Include_Nest1" in kwFilters and kwFilters["Include_Nest1"] and any(
                  nestItem in line for nestItem in kwFilters["Include_Nest1"]):

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

              else:

                groups = compiled_messages.search(line)

                TimeStamps_RemoteServer_Root_Polling_l.append(groups.group(1).strip())
                Hostnames_RemoteServer_Root_Polling_l.append(groups.group(2).strip())
                Messages_RemoteServer_Root_Polling_l.append(groups.group(3))

            else:
              continue

    sftp.close()
    return TimeStamps_RemoteServer_Root_Polling_l, Hostnames_RemoteServer_Root_Polling_l, Messages_RemoteServer_Root_Polling_l





if __name__ == "__main__":

  # ###############################################################################################
  # ## Argparse Initiatives:
  # parser = argparse.ArgumentParser(prog='dev_oshr.py', prefix_chars='-+', description='util to execute Linux commands',
  #                                  add_help=True, allow_abbrev=True)
  # parser.add_argument("-C", "--command", required=True, help="Linux command to execute")
  # # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # # parser.add_argument("-C", "--command", action="store_true", help="Linux command to execute")
  # ## Positional:
  # # parser.add_argument('bar', help='positional bar')
  # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # # pp.pprint(parser)
  #
  # args = parser.parse_args()
  # # pp.pprint(args)
  #
  # ## Have to execute with "python" in front!!
  # ## C:\staging\python\pilot>python dev_oshr.py --command date
  # ## Namespace(command='date', reportPath='C:/staging/python/pilot')
  #
  # ## Doesn't work:
  # ## C:\staging\python\pilot> dev_oshr.py --command date  # unable to recognize "--command date"
  #
  #
  # # print(args.command)
  # # print("Command: {}".format(args.command))
  # print("Command: {},\tReport: {}".format(args.command, args.report))
  # # pp.pprint(args.command)
  # # result_l = auditSC_LocalAdminAccess.exeC(args.co)
  #
  # # pp.pprint(result_l)
  #
  #
  # ##############################################################################################
  # ## Worked!
  # ## Can run any Linux commands as root@admin01
  # ## Get /etc/sudoers as root
  #
  # # Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
  # # server = '10.1.19.21'  # wms-app91.orchard.osh
  # host = '10.1.2.210'  # wms-wmosapp01.orchard.osh
  # port = 22
  # userid = 'root'
  #
  # privateKey_root = "C:/admin/id_rsa_root"
  # # ssh.connect(server, port, user, passwd)  # Worked!!
  # # ssh.connect(server, port, username=user, password=passwd, key_filename="C:/admin/id_rsa_root") # Private Key!!
  #
  #
  # ################# Generic ##################################################################################
  # curNum = '00001'
  # nextNum = str( int(curNum) + 1 )  # To do: should detect the number from existing filename_sample and increment by 1
  # pathF = r"C:/staging/python/pilot/testWMS Account Review " + nextNum + r".xlsx"
  #
  # auditSC_LocalAdminAccess = auditSoxCompliance_ServerLocal(host=host, port=port, userid=userid, privateKey=privateKey_root, reportPath=pathF)
  #
  # # cmd_sudoers = 'cat /etc/sudoers'
  # # cmd_passwd = 'cat /etc/passwd'
  # ## If "sudo" is required the script need to promput user for password though:
  # # cmd = 'cat /var/log/secure | head -30'
  # cmd = "server; cat /etc/*release; date"
  #
  # # stdin, stdout, stderr = auditSC_LocalAdminAccess.exeC(cmd)
  #
  # # result_l = auditSC_LocalAdminAccess.exeC(cmd_passwd)
  # result_l = auditSC_LocalAdminAccess.exeC(cmd)
  #
  #
  #
  # df_pollingLinuxAccess = pd.DataFrame({'TimeStamp': result_l})
  # df_pollingLinuxAccess.to_excel(auditSC_LocalAdminAccess.wb2, sheet_name="Host Access", index=False)
  #
  # auditSC_LocalAdminAccess.wb2.save()
  #
  # # pp.pprint(result_l)
  # # ##############################################################################################

  # ldapServer = "dc01.orchard.osh"
  # userDN = "CN=Lookitup4,OU=Users,OU=Administrative,DC=Orchard,DC=osh"
  # passwd = "Ld@p$3cAuth!"
  #
  # reportPath = r"C:/staging/python/pilot/test_fromBZ2_all.xlsx"
  #
  # stg_auditOSHSecurityCompliance_ServerLocalAccess = auditSoxCompliance_Ldap(ldapServer, userDN, passwd, reportPath)
  # # stg_auditOSHSecurityCompliance_ServerLocalAccess = auditSoxCompliance_Ldap(reportPath)

  # ## /etc/passwd, shadow, sudoers:
  # filename1 = "passwd"
  # filename2 = "shadow"
  # filename3 = "sudoers"
  # result_l = stg_auditOSHSecurityCompliance_ServerLocalAccess.scanLocalAdminAccounts_Server_Solo(filename1)
  # filenames = [filename1, filename2, filename3]
  # auditResults_l = stg_auditOSHSecurityCompliance_ServerLocalAccess.scanLocalAdminAccounts_Local_Files(*filenames)
  # for entry in auditResults_l:
  #   print(entry)

  # stg_auditOSHSecurityCompliance_ServerLocalAccess.scanHostAccess_Local_VarLogSecure()

  # stg_auditOSHSecurityCompliance_ServerLocalAccess.scanHostAccess_Local_VarLogSecure()
  # stg_auditOSHSecurityCompliance_ServerLocalAccess.scanHostAccess_Local_VarLogSecure_Oracle()
  # stg_auditOSHSecurityCompliance_ServerLocalAccess.scanHostAccess_Local_VarLogMessages_BZ2_Informix_Polling()
  # stg_auditOSHSecurityCompliance_ServerLocalAccess.scanHostAccess_Local_VarLogMessages_BZ2_Root_Polling()

  # ##############################################################################################

  hostname = '10.1.2.210'  # wms-wmosapp01.orchard.osh
  port = 22
  userid = 'root'

  # privateKey_root = "C:/admin/id_rsa_root"
  privateKey_root = "/root/.ssh/id_rsa"
  # ssh.connect(server, port, user, passwd)  # Worked!!
  # ssh.connect(server, port, username=user, password=passwd, key_filename="C:/admin/id_rsa_root") # Private Key!!


  ################# Generic ##################################################################################

  pathF = r"C:/staging/python/pilot/testReadRemoteFileViaParamiko.xlsx"

  auditSC_LocalAdminAccess = auditSoxCompliance_ServerLocal(hostname=hostname, port=port, userid=userid, privateKey=privateKey_root, reportPath=pathF)

  # cmd = "server; cat /etc/*release; date"
  # stdin, stdout, stderr = auditSC_LocalAdminAccess.exeC(cmd)
  # result_l = auditSC_LocalAdminAccess.exeC(cmd)

  # filename = "/etc/passwd"
  # Excluded_passwd = ('nologin', 'false')
  # auditSC_LocalAdminAccess.scanLocalAdminAccounts_RemoteServer_SingleFile(filename=filename, excludedPhrases=Excluded_passwd)

  # filename = "/var/log/secure"
  # Excluded_secure = ('rfuser', 'disconnect', 'pam_unix', 'subsystem request for sftp')
  # auditSC_LocalAdminAccess.scanLocalAdminAccounts_RemoteServer_SingleFile(filename=filename, excludedPhrases=Excluded_secure)
  # result_l = auditSC_LocalAdminAccess.scanLocalAdminAccounts_RemoteServer_SingleFile(filename=filename, excludedPhrases=Excluded_secure)
  # pp.pprint(result_l)

  # host = '10.1.1.23'  # wms-wmosdb01.orchard.osh
  servers = ['10.1.2.210', '10.1.1.23']
  results_d = auditSC_LocalAdminAccess.scanLocalAdminAccounts_RemoteServers_Files(*servers)

  pp.pprint(results_d)

  # df_pollingLinuxAccess = pd.DataFrame({'TimeStamp': result_l})
  # df_pollingLinuxAccess.to_excel(auditSC_LocalAdminAccess.wb2, sheet_name="Host Access", index=False)
  #
  # auditSC_LocalAdminAccess.wb2.save()

