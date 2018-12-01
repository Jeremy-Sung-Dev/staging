#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" auditSecComp.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "1.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 6/27/2018 11:29 AM
  __Email__ = Jeremy.Sung@osh.com
Todo:
"""


import os, re
from ldap3 import Server, Connection, SUBTREE, DEREF_ALWAYS
import Enums
import pandas as pd
from openpyxl import Workbook, load_workbook
import bz2
import paramiko
import pprint as pp
import argparse

import auditSecComp_Ldap, auditSecComp_LocalAdminAccess, walkTrees



class auditSecComp():


  def getFileSeqNum(self, filename):

    if ".xlsx" in filename[-5:]:

      if '#' in filename[-11:-5]:
        pass
      else:
        return filename[-11:-5]

    elif ".xls" in filename[-4:]:
      if '#' in filename[-10:-4]:
        pass
      else:
        return filename[-10:-4]

    else:
      pass


  def getFilename(self, projName="Default", dirReports="."):
    """
    Find old reports in specified repository

    :param projName:
    :param dirReports:
    :return:
    """

    #
    walkTree = walkTrees.walkTrees()
    files_l = walkTree.listFiles(dirReports)

    nextNum = '####01'

    curNums_l = []  # in case if we have multiple reports in the same directory, take the latest report w/ max seq num;

    for file in files_l:

      if ".xlsx" in file or ".xls" in file:

        if projName and projName in file:

          curNum = self.getFileSeqNum(file)

          if not curNum:
            continue

          curNums_l.append(curNum)

    # pp.pprint(curNums_l)
    if len(curNums_l) > 0 and sorted(curNums_l)[0].isdigit():
      nextNum = str(int(max(curNums_l)) + 1)

    pathNewReport = r"C:/staging/python/pilot/test" + projName + r" Account Review " + nextNum + r".xlsx"

    # print(pathNewReport)
    return pathNewReport



if __name__ == "__main__":

  pathReports = "C:/staging/python/pilot"
  # pathReports = "C:/22-Linux-Architect/Audit-SOX-Compliance"
  projectName = "WMS"  # WMS, MARS, Polling

  auditSC_WMS = auditSecComp()
  # pathNewWMSReport = auditSC_WMS.getFilename(projName=projectName, dirReports=pathReports)
  pathNewWMSReport = auditSC_WMS.getFilename(dirReports=pathReports)
  print(pathNewWMSReport)

  ldapServer = "dc01.orchard.osh"
  userDN = "CN=Lookitup4,OU=Users,OU=Administrative,DC=Orchard,DC=osh"
  password = "Ld@p$3cAuth!"

  auditSC_ldap_WMS = auditSecComp_Ldap(ldapServer, userDN, password, pathNewWMSReport)



  ## WMS - Access Groups:
  baseDN_WMS_AccessGroup = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  searchScope_WMS_AccessGroup = SUBTREE
  searchFilter_WMS_AccessGroup = '(cn=Linux-WMS-Access*)'
  retrieveAttributes_WMS_AccessGroup = ['cn', 'member']
  derefAliases_WMS_AccessGroup = DEREF_ALWAYS

  wmsLinuxAccessGroupMembers_l = auditSC_ldap_WMS.getLDAPLinuxAccessGroupMembers(baseDN_WMS_AccessGroup, searchScope_WMS_AccessGroup,
                                                                                                  searchFilter_WMS_AccessGroup,
                                                                                                  retrieveAttributes_WMS_AccessGroup, derefAliases_WMS_AccessGroup)
  # pp.pprint(wmsLinuxAccessGroupMembers_l)

  df_secures = pd.DataFrame({'WMS': wmsLinuxAccessGroupMembers_l})
  df_secures.to_excel(auditSC_ldap_WMS.wb2, sheet_name="WMS LDAP Access", index=False)

  auditSC_ldap_WMS.wb2.save()

  ## WMS - Linux groups:
  baseDN_WMS_LinuxGroups = "dc=orchard,dc=osh"
  searchScope_WMS_LinuxGroups = SUBTREE
  gidNumbers_WMS_LinuxGroups = ['10000', '10001', '10004', '10005']
  retrieveAttributes_WMS_LinuxGroups = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  derefAliases_WMS_LinuxGroups = DEREF_ALWAYS

  gidMembers_WMS_d = auditSC_ldap_WMS.getLinuxGroupMembers(baseDN_WMS_LinuxGroups, searchScope_WMS_LinuxGroups,
                                                                        retrieveAttributes_WMS_LinuxGroups, gidNumbers_WMS_LinuxGroups)
  WMS_Members_l = []
  for grpID in gidMembers_WMS_d.keys():

    # print('{} - Linux Group ID [{}]:'.format(stg_auditOSHSecurityComplianceWMS.DateTime, grpID))
    WMS_Members_l.append('{} - Linux Group ID [{}]:'.format(auditSC_ldap_WMS.DateTime, grpID))

    countGroupMembers = 0
    for member in gidMembers_WMS_d[grpID]:
      # print(member)
      WMS_Members_l.append(member)
      countGroupMembers += 1

    # print('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))
    WMS_Members_l.append('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))

  df_secures = pd.DataFrame({'WMS': WMS_Members_l})
  df_secures.to_excel(auditSC_ldap_WMS.wb2, sheet_name="WMS LDAP Groups", index=False)

  auditSC_ldap_WMS.wb2.save()


  # # ===================================================================================== #
  # #
  # ## Can run any Linux commands as root@admin01
  # ## Get /etc/sudoers as root
  #
  # # Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
  # # hostname = '10.1.19.21'  # wms-app91.orchard.osh
  # hostname = '10.1.2.210'  # wms-wmosapp01.orchard.osh
  # port = 22
  # userid = 'root'
  #
  # privateKey_root = "C:/admin/id_rsa_root"
  # # ssh.connect(hostname, port, user, passwd)  # Worked!!
  # # ssh.connect(hostname, port, username=user, password=passwd, key_filename="C:/admin/id_rsa_root") # Private Key!!
  #
  # auditSC_localaccess_WMS = auditSecComp_LocalAdminAccess(hostname=hostname, port=port, userid=userid,
  #                                                         privateKey=privateKey_root, reportPath = pathNewWMSReport)
  #
  # # cmd_sudoers = 'cat /etc/sudoers'
  # # cmd_passwd = 'cat /etc/passwd'
  # ## If "sudo" is required the script need to promput user for password though:
  # # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")
  # # cmd = 'cat /var/log/secure | head -30'
  # cmd = "hostname; cat /etc/*release; date"
  #
  # # stdin, stdout, stderr = auditSC_LocalAdminAccess.exeC(cmd)
  #
  # # result_l = auditSC_LocalAdminAccess.exeC(cmd_passwd)
  # result_l = auditSC_localaccess_WMS.exeC(cmd)
  #
  # pp.pprint(result_l)
  #
  # auditSC_localaccess_WMS.auditAdminAccounts()
  # auditSC_localaccess_WMS.auditHostAccess_ServerLocalSecureMessages()
  #
  # #############################################################################################################
  #
  #
  # #############################################################################################################
  # ## MARS - Access Groups:
  # baseDN_MARS_AccessGroup = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  # searchScope_MARS_AccessGroup = SUBTREE
  # searchFilter_App_MARS_AccessGroup = '(cn=Linux-MARS-App-Access*)'
  # searchFilter_DB_MARS_AccessGroup = '(cn=Linux-MARS-DB-Access*)'
  # retrieveAttributes_MARS_AccessGroup = ['cn', 'member']
  # derefAliases_MARS_AccessGroup = DEREF_ALWAYS
  #
  #
  # curMARS = '00001'
  # nextMARS = str( int(curMARS) + 1 )  # To do: should detect the number from existing filename_sample and increment by 1
  # pathMARS = r"C:/staging/python/pilot/testMARS Account Review " + nextMARS + r".xlsx"
  #
  # auditSC_ldap_MARS = auditSecComp_Ldap(ldapServer, userDN, password, pathMARS)
  #
  #
  #
  #
  #
  #
  #
  # marsLinuxAccessGroupMembers_l = auditSC_ldap_MARS.getLDAPLinuxAccessGroupMembers(baseDN_MARS_AccessGroup, searchScope_MARS_AccessGroup,
  #                                                                                                   searchFilter_App_MARS_AccessGroup,
  #                                                                                                   retrieveAttributes_MARS_AccessGroup, derefAliases_MARS_AccessGroup)
  # marsLinuxAccessGroupMembers_l.append(auditSC_ldap_MARS.getLDAPLinuxAccessGroupMembers(baseDN_MARS_AccessGroup, searchScope_MARS_AccessGroup,
  #                                                                                                        searchFilter_DB_MARS_AccessGroup,
  #                                                                                                        retrieveAttributes_MARS_AccessGroup, derefAliases_MARS_AccessGroup))
  # # pp.pprint(marsLinuxAccessGroupMembers_l)
  # df_secures = pd.DataFrame({'MARS': marsLinuxAccessGroupMembers_l})
  # df_secures.to_excel(auditSC_ldap_MARS.wb2, sheet_name="MARS LDAP Access", index=False)
  #
  # auditSC_ldap_MARS.wb2.save()
  #
  # ## MARS - Linux groups:
  # baseDN_MARS_LinuxGroups = "dc=orchard,dc=osh"
  # searchScope_MARS_LinuxGroups = SUBTREE
  # gidNumbers_MARS_LinuxGroups = ['10000', '10001', '10004', '10005']
  # retrieveAttributes_MARS_LinuxGroups = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  # derefAliases_MARS_LinuxGroups = DEREF_ALWAYS
  #
  # gidMembers_MARS_d = auditSecComp_Ldap.getLinuxGroupMembers(baseDN_MARS_LinuxGroups, searchScope_MARS_LinuxGroups,
  #                                                                        retrieveAttributes_MARS_LinuxGroups, gidNumbers_MARS_LinuxGroups)
  #
  # for grpID in gidMembers_MARS_d.keys():
  #
  #   print('{} - Linux Group ID [{}]:'.format(auditSC_ldap_MARS.DateTime, grpID))
  #
  #   countGroupMembers = 0
  #   for member in gidMembers_MARS_d[grpID]:
  #
  #     print(member)
  #     countGroupMembers += 1
  #
  #   print('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))
  #
  # df_secures = pd.DataFrame({'MARS': marsLinuxAccessGroupMembers_l})
  # df_secures.to_excel(auditSC_ldap_MARS.wb2, sheet_name="MARS LDAP Groups", index=False)
  #
  # auditSC_ldap_MARS.wb2.save()
  #
  #
  # # ===================================================================================== #
  # #
  # ## Can run any Linux commands as root@admin01
  # ## Get /etc/sudoers as root
  #
  # # Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
  # # hostname = '10.1.19.21'  # wms-app91.orchard.osh
  # hostname = '10.1.2.210'  # wms-wmosapp01.orchard.osh
  # port = 22
  # userid = 'root'
  #
  # privateKey_root = "C:/admin/id_rsa_root"
  # # ssh.connect(hostname, port, user, passwd)  # Worked!!
  # # ssh.connect(hostname, port, username=user, password=passwd, key_filename="C:/admin/id_rsa_root") # Private Key!!
  #
  # auditSC_localaccess_MARS = auditSecComp_LocalAdminAccess(hostname=hostname, port=port, userid=userid,
  #                                                         privateKey=privateKey_root, reportPath=pathMARS)
  #
  # # cmd_sudoers = 'cat /etc/sudoers'
  # # cmd_passwd = 'cat /etc/passwd'
  # ## If "sudo" is required the script need to promput user for password though:
  # # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")
  # # cmd = 'cat /var/log/secure | head -30'
  # cmd = "hostname; cat /etc/*release; date"
  #
  # # stdin, stdout, stderr = auditSC_LocalAdminAccess.exeC(cmd)
  #
  # # result_l = auditSC_LocalAdminAccess.exeC(cmd_passwd)
  # result_l = auditSC_localaccess_MARS.exeC(cmd)
  #
  # pp.pprint(result_l)
  # auditSC_localaccess_MARS.auditAdminAccounts()
  # auditSC_localaccess_MARS.auditHostAccess_ServerLocalSecureMessages()
  # auditSC_localaccess_MARS.audit_OracleAccountAccess_DFIODB01_Secure()
  #
  # #############################################################################################################
  # #############################################################################################################
  # #
  # #
  # #############################################################################################################
  # ## Polling - Access Groups:
  # baseDN_Polling_AccessGroup = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  # searchScope_Polling_AccessGroup = SUBTREE
  # searchFilter_Polling_AccessGroup = '(cn=Linux-Polling-Access*)'
  # # searchFilter_DB_Polling_AccessGroup = '(cn=Linux-Polling-DB-Access*)'
  # retrieveAttributes_Polling_AccessGroup = ['cn', 'member']
  # derefAliases_Polling_AccessGroup = DEREF_ALWAYS
  #
  #
  # curPolling = '00001'
  # nextPolling = str( int(curPolling) + 1 )  # To do: should detect the number from existing filename_sample and increment by 1
  # pathPolling = r"C:/staging/python/pilot/testPolling Account Review " + nextPolling + r".xlsx"
  #
  # auditSC_ldap_Polling = auditSecComp_Ldap(ldapServer, userDN, password, pathPolling)
  #
  #
  # pollingLinuxAccessGroupMembers_l = auditSC_ldap_Polling.getLDAPLinuxAccessGroupMembers(baseDN_Polling_AccessGroup, searchScope_Polling_AccessGroup,
  #                                                                                                         searchFilter_Polling_AccessGroup,
  #                                                                                                         retrieveAttributes_Polling_AccessGroup, derefAliases_Polling_AccessGroup)
  #
  # # pp.pprint(marsLinuxAccessGroupMembers_l)
  # df_secures = pd.DataFrame({'Polling': pollingLinuxAccessGroupMembers_l})
  # df_secures.to_excel(auditSC_ldap_Polling.wb2, sheet_name="Polling LDAP Access", index=False)
  #
  # auditSC_ldap_Polling.wb2.save()
  #
  # ## MARS - Linux groups:
  # baseDN_Polling_LinuxGroups = "dc=orchard,dc=osh"
  # searchScope_Polling_LinuxGroups = SUBTREE
  # gidNumbers_Polling_LinuxGroups = ['10000', '10001', '10003']
  # retrieveAttributes_Polling_LinuxGroups = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  # derefAliases_Polling_LinuxGroups = DEREF_ALWAYS
  #
  # gidMembers_Polling_d = auditSC_ldap_Polling.getLinuxGroupMembers(baseDN_Polling_LinuxGroups, searchScope_Polling_LinuxGroups,
  #                                                                           retrieveAttributes_Polling_LinuxGroups, gidNumbers_Polling_LinuxGroups)
  #
  # PollingMembers_l = []
  # for grpID in gidMembers_Polling_d.keys():
  #
  #   print('{} - Linux Group ID [{}]:'.format(Enums.strDateTime, grpID))
  #
  #   countGroupMembers = 0
  #   for member in gidMembers_Polling_d[grpID]:
  #
  #     # print(member)
  #     PollingMembers_l.append(member)
  #     countGroupMembers += 1
  #
  #   print('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))
  #
  #
  # df_secures = pd.DataFrame({'Polling': PollingMembers_l})
  # df_secures.to_excel(auditSC_ldap_Polling.wb2, sheet_name="Polling LDAP Groups", index=False)
  #
  # auditSC_ldap_Polling.wb2.save()
  #
  #
  # ############################################################################################################
  #
  #
  # # ldapServer = "dc01.orchard.osh"
  # # userDN = "CN=Lookitup4,OU=Users,OU=Administrative,DC=Orchard,DC=osh"
  # # passwd = "Ld@p$3cAuth!"
  # #
  # # reportPath = r"C:/staging/python/pilot/test_fromBZ2_all.xlsx"
  # #
  # # stg_auditOSHSecurityCompliance_ServerLocalAccess = auditSecComp_ldap(ldapServer, userDN, passwd, reportPath)
  # # # stg_auditOSHSecurityCompliance_ServerLocalAccess = auditSecComp_ldap(reportPath)
  #
  #
  # # ## /etc/passwd, shadow, sudoers:
  # # filename1 = "passwd"
  # # filename2 = "shadow"
  # # filename3 = "sudoers"
  # # result_l = stg_auditOSHSecurityCompliance_ServerLocalAccess.auditAdminAccountsSolo(filename1)
  # # filenames = [filename1, filename2, filename3]
  # # auditResults_l = stg_auditOSHSecurityCompliance_ServerLocalAccess.auditAdminAccounts(*filenames)
  # # for entry in auditResults_l:
  # #   print(entry)
  #
  # # stg_auditOSHSecurityCompliance_ServerLocalAccess.auditHostAccess_ServerLocalSecureMessages()
  #
  #
  #
  # # ===================================================================================== #
  # #
  # ## Can run any Linux commands as root@admin01
  # ## Get /etc/sudoers as root
  #
  # # Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
  # # hostname = '10.1.19.21'  # wms-app91.orchard.osh
  # hostname = '10.1.2.210'  # wms-wmosapp01.orchard.osh
  # port = 22
  # userid = 'root'
  #
  # privateKey_root = "C:/admin/id_rsa_root"
  # # ssh.connect(hostname, port, user, passwd)  # Worked!!
  # # ssh.connect(hostname, port, username=user, password=passwd, key_filename="C:/admin/id_rsa_root") # Private Key!!
  #
  # auditSC_localaccess_Polling = auditSecComp_LocalAdminAccess(hostname=hostname, port=port, userid=userid,
  #                                                         privateKey=privateKey_root, reportPath=pathPolling)
  #
  # # cmd_sudoers = 'cat /etc/sudoers'
  # # cmd_passwd = 'cat /etc/passwd'
  # ## If "sudo" is required the script need to promput user for password though:
  # # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")
  # # cmd = 'cat /var/log/secure | head -30'
  # cmd = "hostname; cat /etc/*release; date"
  #
  # # stdin, stdout, stderr = auditSC_LocalAdminAccess.exeC(cmd)
  #
  # # result_l = auditSC_LocalAdminAccess.exeC(cmd_passwd)
  # result_l = auditSC_localaccess_Polling.exeC(cmd)
  #
  # pp.pprint(result_l)
  #
  # auditSC_localaccess_Polling.auditAdminAccounts()
  # auditSC_localaccess_Polling.auditHostRootAccess_Polling_ServerLocalMessages_BZ2()
  # auditSC_localaccess_Polling.auditInformixAccess_Polling_ServerLocalMessages_BZ2()
  #
  # auditSC_localaccess_Polling.auditHostAccess_ServerLocalSecureMessages()
  # auditSC_localaccess_Polling.audit_OracleAccountAccess_DFIODB01_Secure()
  # auditSC_localaccess_Polling.auditInformixAccess_Polling_ServerLocalMessages_BZ2()
  # auditSC_localaccess_Polling.auditHostRootAccess_Polling_ServerLocalMessages_BZ2()
  #
  #
  #
  # #############################################################################################################
  #
  #
  #
  # # ###############################################################################################
  # # ## Argparse Initiatives:
  # # ## Allow interaction with console:
  # #
  # # parser = argparse.ArgumentParser(prog='dev_oshr.py', prefix_chars='-+', description='util to execute Linux commands',
  # #                                  add_help=True, allow_abbrev=True)
  # # parser.add_argument("-C", "--command", required=True, help="Linux command to execute")
  # # # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # # # parser.add_argument("-C", "--command", action="store_true", help="Linux command to execute")
  # # ## Positional:
  # # # parser.add_argument('bar', help='positional bar')
  # # parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  # # # pp.pprint(parser)
  # #
  # # args = parser.parse_args()
  # # # pp.pprint(args)
  # #
  # # ## Have to execute with "python" in front!!
  # # ## C:\staging\python\pilot>python dev_oshr.py --command date
  # # ## Namespace(command='date', reportPath='C:/staging/python/pilot')
  # #
  # # ## Doesn't work:
  # # ## C:\staging\python\pilot> dev_oshr.py --command date  # unable to recognize "--command date"
  # #
  # #
  # # # print(args.command)
  # # # print("Command: {}".format(args.command))
  # # print("Command: {},\tReport: {}".format(args.command, args.report))
  # # # pp.pprint(args.command)
  # # # result_l = auditSC_LocalAdminAccess.exeC(args.co)
  # #
  # # # pp.pprint(result_l)


