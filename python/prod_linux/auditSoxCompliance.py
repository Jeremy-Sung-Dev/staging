#!/usr/lib/anaconda3/bin/python
# -*- coding: utf-8 -*-
""" auditSoxCompliance.py

Challenges:
Solutions:
Description:
Attributes:
  __version__ = "2.0.2"
  __project__ = Prod
  __author__ = Jeremy Sung
  __date__ = 6/27/2018 11:29 AM
  __Email__ = Jeremy.Sung@osh.com

"""

from ldap3 import Server, Connection, SUBTREE, DEREF_ALWAYS
import pandas as pd
import argparse
import pprint as pp
import auditSoxCompliance_Ldap, auditSoxCompliance_ServerLocal
import Utils
import Enums



class auditSoxCompliance():


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

    walk_trees = Utils.walkTrees()
    files_l = walk_trees.listFiles(dirReports)

    nextNum = '####01'

    curNums_l = []  # in case if we have multiple reports in the same directory, take the latest report w/ max seq num;

    for file in files_l:

      if ".xlsx" in file or ".xls" in file:

        if projName and projName in file:

          curNum = self.getFileSeqNum(file)

          if not curNum:
            continue

          curNums_l.append(curNum)

    if len(curNums_l) > 0 and sorted(curNums_l)[0].isdigit():
      nextNum = str(int(max(curNums_l)) + 1)

    ## pathNewReport_stg = r"C:/staging/python/pilot/test" + projName + r" Account Review " + nextNum + r".xlsx"
    ## pathNewReport_prd = r"C:/staging/python/pilot/" + projName + r" Account Review " + nextNum + r".xlsx"
    pathNewReport_prd = r"/root/data/auditReports/" + projName + r" Account Review " + nextNum + r".xlsx"

    ## return pathNewReport_stg
    return pathNewReport_prd



if __name__ == "__main__":


  ## Specify ldapServer and authorized credential to perform the audits:
  ldapServer = "dc01.orchard.osh"
  userDN = "CN=Lookitup4,OU=Users,OU=Administrative,DC=Orchard,DC=osh"
  password = "Ld@p$3cAuth!"

  ## Generate new report with updated sequence number in specified repository:
  ## repoReports = "C:/staging/python/pilot"  # Dev env
  ## repoReports = "C:/22-Linux-Architect/Audit-SOX-Compliance"  # Staging env
  repoReports = "/root/data/auditReports"  # Prod env  -  at admin01
  projectName_WMS = "WMS"  # WMS, MARS, Polling
  auditSC_WMS = auditSoxCompliance()
  pathNewWMSReport = auditSC_WMS.getFilename(projName=projectName_WMS, dirReports=repoReports)
  print(pathNewWMSReport)
  #
  ## Spawn an LDAP audit instance to carry out Ldap related audits:
  auditSC_Ldap_WMS = auditSoxCompliance_Ldap.auditSoxCompliance_Ldap(ldapServer, userDN, password, pathNewWMSReport)

  ##
  ## WMS - LDAP Access audit:
  ##
  baseDN_WMS_LdapAccessGroups = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  searchScope_WMS_LdapAccessGroups = SUBTREE
  searchFilter_WMS_LdapAccessGroups = '(cn=Linux-WMS-Access*)'
  retrieveAttributes_WMS_LdapAccessGroups = ['cn', 'member']
  derefAliases_WMS_LdapAccessGroups = DEREF_ALWAYS

  wmsLinuxAccess_l = auditSC_Ldap_WMS.auditLinuxAdminLdapAccess(baseDN_WMS_LdapAccessGroups,
                                                                searchScope_WMS_LdapAccessGroups,
                                                                searchFilter_WMS_LdapAccessGroups,
                                                                retrieveAttributes_WMS_LdapAccessGroups,
                                                                derefAliases_WMS_LdapAccessGroups)

  df_wmsLinuxAccess = pd.DataFrame({'LDAP Access (Who has Access to WMS Hosts):': wmsLinuxAccess_l})
  df_wmsLinuxAccess.to_excel(auditSC_Ldap_WMS.wb2, sheet_name="WMS LDAP Access", index=False)

  auditSC_Ldap_WMS.wb2.save()

  ##
  ## WMS - LDAP Admin Group Membership audit:
  ##
  baseDN_WMS_LinuxGroups = "dc=orchard,dc=osh"
  searchScope_WMS_LinuxGroups = SUBTREE
  gidNumbers_WMS_LinuxGroups = ['10000', '10001', '10004', '10005']
  retrieveAttributes_WMS_LinuxGroups = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  derefAliases_WMS_LinuxGroups = DEREF_ALWAYS

  gidMembers_Groups_WMS_d = auditSC_Ldap_WMS.listLdapAdminGroupMembership(baseDN_WMS_LinuxGroups, searchScope_WMS_LinuxGroups,
                                                                          retrieveAttributes_WMS_LinuxGroups, gidNumbers_WMS_LinuxGroups)

  wmsLdapAdminGroups_l = []
  for grpID in gidMembers_Groups_WMS_d.keys():
    # strRetrievedAttributes = " ".join(retrieveAttributes_WMS_LinuxGroups)
    wmsLdapAdminGroups_l.append("\n")
    wmsLdapAdminGroups_l.append('Linux Group ID [{}]:'.format(grpID))
    wmsLdapAdminGroups_l.append(r'date && ldapsearch -H ldaps://' + auditSC_Ldap_WMS.ldapServer + r':636 -x -D CN=<ldap_user>,OU=Users,OU=Administrative,DC=Orchard,DC=osh" -w "<ldap_passwd>" -b "' + baseDN_WMS_LinuxGroups +
                                r'" -s sub "(gidNumber=' + grpID + r')" ' + " ".join(retrieveAttributes_WMS_LinuxGroups) +
                                r' | grep "^dn\|^gid"')

    # wmsLdapAdminGroups_l.append(r'date && ldapsearch -H ldaps://' + auditSC_Ldap_WMS.ldapServer + r':636 -x -D "' +
    #                             auditSC_Ldap_WMS.UserDN + r'" -w "<passwd>" -b "' + baseDN_WMS_LinuxGroups +
    #                             r'" -s sub "(gidNumber=' + grpID + r')" ' + " ".join(retrieveAttributes_WMS_LinuxGroups) +
    #                             r' | grep "^dn\|^gid"')
    wmsLdapAdminGroups_l.append("\n")
    wmsLdapAdminGroups_l.append('{}'.format(auditSC_Ldap_WMS.DateTime))

    countGroupMembers = 0
    for member in gidMembers_Groups_WMS_d[grpID]:
      wmsLdapAdminGroups_l.append(member)
      countGroupMembers += 1

    wmsLdapAdminGroups_l.append('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))
    wmsLdapAdminGroups_l.append("\n")

  df_wmsLdapAdminGroups = pd.DataFrame({'LADP Groups Access (Who is assigned to what group):': wmsLdapAdminGroups_l})
  df_wmsLdapAdminGroups.to_excel(auditSC_Ldap_WMS.wb2, sheet_name="WMS LDAP Groups", index=False)

  auditSC_Ldap_WMS.wb2.save()

  ##
  ## Audit Linux Server Local - Accounts & Logs: /etc/passwd, shadow, sudoers; /var/logs/secure, messages, etc.
  ##
  ## /etc/sudoers
  ##

  wmsServers = Enums.auditSC_Servers_WMS

  port = 22
  userid = 'root'
  privateKey_root = "/root/.ssh/id_rsa"
  # privateKey_root = "C:/admin/id_rsa_root"

  ##
  ## Audit Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  resLocalAdminAccounts_Servers_WMS_d = {}
  resLocalAdminAccounts_Servers_WMS_l = []

  resLocalAdminAccess_Servers_WMS_d = {}

  df_AdminAccess_Servers_Frames_WMS_l = []

  dfLocalAdminAccess_Columns = ['TimeStamp', 'Hosts', 'Messages']

  for server in wmsServers:

    auditSC_LocalAccess_Server_WMS = auditSoxCompliance_ServerLocal.auditSoxCompliance_ServerLocal(hostname=server, port=port,
                                                                                                   userid=userid,
                                                                                                   privateKey=privateKey_root,
                                                                                                   reportPath = pathNewWMSReport)
    ##
    ## Audit Linux Admin Accounts on Server Local:
    ##
    ## Result of /etc/password & shadow audit:
    resPasswordShadow_RemoteServer_l = auditSC_LocalAccess_Server_WMS.scanPasswdShadow_RemoteServer()

    resLocalAdminAccounts_Servers_WMS_l.append(server + ":~ # " + auditSC_LocalAccess_Server_WMS.CMD_passwd_shadow)
    resLocalAdminAccounts_Servers_WMS_l.append(auditSC_LocalAccess_Server_WMS.DateTime)
    resLocalAdminAccounts_Servers_WMS_l.extend(resPasswordShadow_RemoteServer_l)
    resLocalAdminAccounts_Servers_WMS_l.append("\n")

    ## Result of /etc/sudoers audit:
    resSudoers_RemoteServer_l = auditSC_LocalAccess_Server_WMS.scanSudoers_RemoteServer()

    resLocalAdminAccounts_Servers_WMS_l.append(server + ":~ # " + auditSC_LocalAccess_Server_WMS.CMD_sudoers)
    resLocalAdminAccounts_Servers_WMS_l.append(auditSC_LocalAccess_Server_WMS.DateTime)
    resLocalAdminAccounts_Servers_WMS_l.extend(resSudoers_RemoteServer_l)
    resLocalAdminAccounts_Servers_WMS_l.append("\n\n")

    ## Result per Server:
    resLocalAdminAccounts_Servers_WMS_d[server] = [resPasswordShadow_RemoteServer_l, resSudoers_RemoteServer_l]

    ##
    ## Audit Admin Access to Server Local - Host Access:
    ##

    filterHostAccess_WMS = { "Include_All":[], "Include_Any":[], "Exclude": ["rfuser", "disconnect", "pam_unix", "subsystem request for sftp"] }
    timestamps_wms_server_l, hostnames_wms_server_l, messages_wms_server_l = auditSC_LocalAccess_Server_WMS.scanHostAccess_RemoteServer_VarLogSecure_Generic(**filterHostAccess_WMS)

    resLocalAdminAccess_Server_WMS_d = {}  ## Key Move!!

    resLocalAdminAccess_Server_WMS_d["TimeStamp"] = timestamps_wms_server_l
    resLocalAdminAccess_Server_WMS_d["Hosts"] = hostnames_wms_server_l
    resLocalAdminAccess_Server_WMS_d["Messages"] = messages_wms_server_l

    resLocalAdminAccess_Servers_WMS_d[server] = resLocalAdminAccess_Server_WMS_d

    df_AdminAccess_Servers_Frames_WMS_l.append(pd.DataFrame.from_records(resLocalAdminAccess_Server_WMS_d,
                                                                         columns=dfLocalAdminAccess_Columns))

  ##
  ### For Audit: Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  ## pp.pprint(resLocalAdminAccounts_Servers_WMS_l)
  ## pp.pprint(resLocalAdminAccounts_Servers_WMS_d)
  ##
  ### For Audit: Admin Access to Server Local:
  ##
  ## pp.pprint(resLocalAdminAccess_Servers_WMS_d)

  ##
  ## For Audit: Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  df_LocalAdminAccounts_Servers_WMS = pd.DataFrame( {"Local Access and SUDO File" : resLocalAdminAccounts_Servers_WMS_l} )
  df_LocalAdminAccounts_Servers_WMS.to_excel(auditSC_LocalAccess_Server_WMS.wb2, sheet_name="Local Access - SUDO", index=False)
  ##
  ## For Audit: Admin Access to Server Local:
  ##
  df_wmsLinuxAccess = pd.concat(df_AdminAccess_Servers_Frames_WMS_l)
  df_wmsLinuxAccess.to_excel(auditSC_LocalAccess_Server_WMS.wb2, sheet_name="Host Access", index=False)

  ########################################################################################################
  ##
  ## Save updates on Excel Workbook:
  ##
  auditSC_LocalAccess_Server_WMS.wb2.save()

  ##
  ## Remove the redundant default worksheet, titled "Sheet"
  ##
  default_sheet = auditSC_LocalAccess_Server_WMS.wb2.book["Sheet"]
  auditSC_LocalAccess_Server_WMS.wb2.book.remove(default_sheet)
  auditSC_LocalAccess_Server_WMS.wb2.save()

  #############################################################################################################
  ##
  ###  MARS
  ##
  ##############################################################################################################

  ## Generate new report with updated sequence number in specified repository:
  ## repoReports = "C:/staging/python/pilot"  # Dev env
  ## repoReports = "C:/22-Linux-Architect/Audit-SOX-Compliance"  # Staging env
  repoReports = "/root/data/auditReports"  # Prod env  -  at admin01
  projectName_MARS = "MARS"  # WMS, MARS, Polling
  auditSC_MARS = auditSoxCompliance()
  pathNewMARSReport = auditSC_MARS.getFilename(projName=projectName_MARS, dirReports=repoReports)
  print(pathNewMARSReport)

  ## Spawn an LDAP audit instance to carry out Ldap related audits:
  auditSC_Ldap_MARS = auditSoxCompliance_Ldap.auditSoxCompliance_Ldap(ldapServer, userDN, password, pathNewMARSReport)

  ##
  ## MARS - Access Groups:
  ##
  baseDN_MARS_LdapAccessGroups = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  searchScope_MARS_LdapAccessGroup = SUBTREE
  searchFilter_App_MARS_LdapAccessGroup = '(cn=Linux-MARS-App-Access*)'
  searchFilter_DB_MARS_AccessGroup = '(cn=Linux-MARS-DB-Access*)'
  retrieveAttributes_MARS_LdapAccessGroup = ['cn', 'member']
  derefAliases_MARS_LdapAccessGroup = DEREF_ALWAYS

  marsLinuxAccess_l = auditSC_Ldap_MARS.auditLinuxAdminLdapAccess(baseDN_MARS_LdapAccessGroups, searchScope_MARS_LdapAccessGroup,
                                                                  searchFilter_App_MARS_LdapAccessGroup,
                                                                  retrieveAttributes_MARS_LdapAccessGroup, derefAliases_MARS_LdapAccessGroup)

  marsLinuxAccess_l.append("\n")
  marsLinuxAccess_l.extend(auditSC_Ldap_MARS.auditLinuxAdminLdapAccess(baseDN_MARS_LdapAccessGroups, searchScope_MARS_LdapAccessGroup,
                                                                       searchFilter_DB_MARS_AccessGroup,
                                                                       retrieveAttributes_MARS_LdapAccessGroup, derefAliases_MARS_LdapAccessGroup))

  df_marsAdminAccess = pd.DataFrame({'LDAP Access (Who has Access to MARS App & DB Hosts):': marsLinuxAccess_l})
  df_marsAdminAccess.to_excel(auditSC_Ldap_MARS.wb2, sheet_name="MARS LDAP Access", index=False)

  auditSC_Ldap_MARS.wb2.save()

  ##
  ## MARS - LDAP Admin Group Membership audit:
  ##
  baseDN_MARS_LinuxGroups = "dc=orchard,dc=osh"
  searchScope_MARS_LinuxGroups = SUBTREE
  gidNumbers_MARS_LinuxGroups = ['10000', '10001', '10004', '10005']
  retrieveAttributes_MARS_LinuxGroups = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  derefAliases_MARS_LinuxGroups = DEREF_ALWAYS

  gidMembers_Groups_MARS_d = auditSC_Ldap_MARS.listLdapAdminGroupMembership(baseDN_MARS_LinuxGroups, searchScope_MARS_LinuxGroups,
                                                                            retrieveAttributes_MARS_LinuxGroups, gidNumbers_MARS_LinuxGroups)

  marsLdapAdminGroups_l = []
  for grpID in gidMembers_Groups_MARS_d.keys():

    marsLdapAdminGroups_l.append("\n")
    marsLdapAdminGroups_l.append('Linux Group ID [{}]:'.format(grpID))
    marsLdapAdminGroups_l.append(r'date && ldapsearch -H ldaps://' + auditSC_Ldap_MARS.ldapServer + r':636 -x -D CN=<ldap_user>,OU=Users,OU=Administrative,DC=Orchard,DC=osh" -w "<ldap_passwd>" -b "' + baseDN_MARS_LinuxGroups +
                                r'" -s sub "(gidNumber=' + grpID + r')" ' + " ".join(retrieveAttributes_MARS_LinuxGroups) +
                                r' | grep "^dn\|^gid"')
    # marsLdapAdminGroups_l.append(r'date && ldapsearch -H ldaps://' + auditSC_Ldap_MARS.ldapServer + r':636 -x -D "' +
    #                             auditSC_Ldap_MARS.UserDN + r'" -w "<passwd>" -b "' + baseDN_MARS_LinuxGroups +
    #                             r'" -s sub "(gidNumber=' + grpID + r')" ' + " ".join(retrieveAttributes_MARS_LinuxGroups) +
    #                             r' | grep "^dn\|^gid"')

    marsLdapAdminGroups_l.append("\n")
    marsLdapAdminGroups_l.append('{}'.format(auditSC_Ldap_MARS.DateTime))

    countGroupMembers = 0
    for member in gidMembers_Groups_MARS_d[grpID]:
      marsLdapAdminGroups_l.append(member)
      countGroupMembers += 1

    marsLdapAdminGroups_l.append('>>  Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))
    marsLdapAdminGroups_l.append("\n")

  df_marsLdapAdminGroups = pd.DataFrame({'LADP Groups Access (Who is assigned to what group):': marsLdapAdminGroups_l})
  df_marsLdapAdminGroups.to_excel(auditSC_Ldap_MARS.wb2, sheet_name="MARS LDAP Groups", index=False)

  auditSC_Ldap_MARS.wb2.save()

  ##
  ## Audit Linux Server Local - Accounts & Logs: /etc/passwd, shadow, sudoers; /var/logs/secure, messages, etc.
  ##
  ## /etc/sudoers
  ##
  marsServers = Enums.auditSC_Servers_MARS

  port = 22
  userid = 'root'
  privateKey_root = "/root/.ssh/id_rsa"

  ##
  ## Audit Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  resLocalAdminAccounts_Servers_MARS_d = {}
  resLocalAdminAccounts_Servers_MARS_l = []
  resLocalAdminAccess_Servers_MARS_d = {}
  resOracleAccess_Servers_MARS_d = {}
  df_AdminAccess_Servers_Frames_MARS_l = []
  df_OracleAccess_Servers_Frames_MARS_l = []

  dfLocalAdminAccess_Columns_MARS = ['Dates', 'Hosts', 'Messages']

  for server in marsServers:

    auditSC_LocalAccess_Server_MARS = auditSoxCompliance_ServerLocal.auditSoxCompliance_ServerLocal(hostname=server, port=port,
                                                                                                   userid=userid,
                                                                                                   privateKey=privateKey_root,
                                                                                                   reportPath = pathNewMARSReport)
    ##
    ## Audit Linux Admin Accounts on Server Local - "Local Access and SUDO":
    ##
    ## Result of /etc/password & shadow audit:
    resPasswordShadow_RemoteServer_l = auditSC_LocalAccess_Server_MARS.scanPasswdShadow_RemoteServer()

    resLocalAdminAccounts_Servers_MARS_l.append(server + ":~ # " + auditSC_LocalAccess_Server_MARS.CMD_passwd_shadow)
    resLocalAdminAccounts_Servers_MARS_l.append(auditSC_LocalAccess_Server_MARS.DateTime)
    resLocalAdminAccounts_Servers_MARS_l.extend(resPasswordShadow_RemoteServer_l)
    resLocalAdminAccounts_Servers_MARS_l.append("\n")

    ## Result of /etc/sudoers audit:
    resSudoers_RemoteServer_l = auditSC_LocalAccess_Server_MARS.scanSudoers_RemoteServer()

    resLocalAdminAccounts_Servers_MARS_l.append(server + ":~ # " + auditSC_LocalAccess_Server_MARS.CMD_sudoers)
    resLocalAdminAccounts_Servers_MARS_l.append(auditSC_LocalAccess_Server_MARS.DateTime)
    resLocalAdminAccounts_Servers_MARS_l.extend(resSudoers_RemoteServer_l)
    resLocalAdminAccounts_Servers_MARS_l.append("\n")

    ## Result per Server:
    resLocalAdminAccounts_Servers_MARS_d[server] = [resPasswordShadow_RemoteServer_l, resSudoers_RemoteServer_l]


    ##
    ## Audit "Oracle Account Access" to Server Local:
    ##

    resOracleAccess_Server_MARS_d = {}

    filterOracleAccess = { "Include_All":["sudo", "USER=oracle"], "Include_Any":[], "Exclude": [] }

    timestamps_mars_server_oracle_l, hostnames_mars_server_oracle_l, messages_mars_server_oracle_l = auditSC_LocalAccess_Server_MARS.scanHostAccess_RemoteServer_VarLogSecures(**filterOracleAccess)

    resOracleAccess_Server_MARS_d = {}  ## Key move!!! Must initialize (reset) this Dict here, instead of outside the loop!

    resOracleAccess_Server_MARS_d["Dates"] = timestamps_mars_server_oracle_l
    resOracleAccess_Server_MARS_d["Hosts"] = hostnames_mars_server_oracle_l
    resOracleAccess_Server_MARS_d["Messages"] = messages_mars_server_oracle_l

    resOracleAccess_Servers_MARS_d[server] = resOracleAccess_Server_MARS_d


    df_OracleAccess_Servers_Frames_MARS_l.append(pd.DataFrame.from_records(resOracleAccess_Server_MARS_d,
                                                                                columns=dfLocalAdminAccess_Columns_MARS))

    ##
    ## Audit Admin "Host Access" to Server Local - Host Access:
    ##

    filterHostAccess_MARS = { "Include_All":[], "Include_Any":[], "Exclude": ['rfuser', 'disconnect', 'pam_unix', 'subsystem request for sftp', 'marssftp from 10.1.1.63',] }
    timestamps_mars_server_l, hostnames_mars_server_l, messages_mars_server_l = auditSC_LocalAccess_Server_MARS.scanHostAccess_RemoteServer_VarLogSecure_Generic(**filterHostAccess_MARS)

    ## Key move!!! Must initialize (reset) this Dict here, instead of outside the loop!
    resLocalAdminAccess_Server_MARS_d = {}  ## Key Move!!

    resLocalAdminAccess_Server_MARS_d["Dates"] = timestamps_mars_server_l
    resLocalAdminAccess_Server_MARS_d["Hosts"] = hostnames_mars_server_l
    resLocalAdminAccess_Server_MARS_d["Messages"] = messages_mars_server_l

    resLocalAdminAccess_Servers_MARS_d[server] = resLocalAdminAccess_Server_MARS_d

    df_AdminAccess_Servers_Frames_MARS_l.append(pd.DataFrame.from_records(resLocalAdminAccess_Server_MARS_d,
                                                                         columns=dfLocalAdminAccess_Columns_MARS))

  ##
  ## For Audit: Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  df_LocalAdminAccounts_Servers_MARS = pd.DataFrame( {"Local Access and SUDO File" : resLocalAdminAccounts_Servers_MARS_l} )
  df_LocalAdminAccounts_Servers_MARS.to_excel(auditSC_LocalAccess_Server_MARS.wb2, sheet_name="Local Access and SUDO", index=False)

  df_OracleAccess_Servers_MARS = pd.concat( df_OracleAccess_Servers_Frames_MARS_l )
  df_OracleAccess_Servers_MARS.to_excel(auditSC_LocalAccess_Server_MARS.wb2, sheet_name="Oracle Account Access", index=False)

  ##
  ## For Audit: Admin Access to Server Local:
  ##
  df_AdminAccess_Servers_MARS = pd.concat(df_AdminAccess_Servers_Frames_MARS_l)
  df_AdminAccess_Servers_MARS.to_excel(auditSC_LocalAccess_Server_MARS.wb2, sheet_name="Host Access", index=False)

  ##
  ## Save updates on Excel Workbook:
  ##
  auditSC_LocalAccess_Server_MARS.wb2.save()
  ##
  ## Remove the redundant default worksheet, titled "Sheet"
  ##
  default_sheet = auditSC_LocalAccess_Server_MARS.wb2.book["Sheet"]
  auditSC_LocalAccess_Server_MARS.wb2.book.remove(default_sheet)
  auditSC_LocalAccess_Server_MARS.wb2.save()


  ############################################################################################################
  #
  ##  Polling
  #
  ############################################################################################################

  ## Generate new report with updated sequence number in specified repository:
  ## repoReports = "C:/staging/python/pilot"  # Dev env
  ## repoReports = "C:/22-Linux-Architect/Audit-SOX-Compliance"  # Staging env
  repoReports = "/root/data/auditReports"  # Prod env  -  at admin01
  projectName_Polling = "Polling"  # WMS, MARS, Polling
  auditSC_Polling = auditSoxCompliance()
  pathNewPollingReport = auditSC_Polling.getFilename(projName=projectName_Polling, dirReports=repoReports)
  print(pathNewPollingReport)

  ## Spawn an LDAP audit instance to carry out Ldap related audits:
  auditSC_Ldap_Polling = auditSoxCompliance_Ldap.auditSoxCompliance_Ldap(ldapServer, userDN, password, pathNewPollingReport)

  ##
  ## Polling - LDAP Access audit:
  ##
  ## Polling - Access Groups:
  baseDN_Polling_AccessGroups = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  searchScope_Polling_AccessGroups = SUBTREE
  searchFilter_Polling_AccessGroups = '(cn=Linux-Polling-Access*)'
  retrieveAttributes_Polling_AccessGroups = ['cn', 'member']
  derefAliases_Polling_AccessGroups = DEREF_ALWAYS

  pollingLinuxAccess_l = auditSC_Ldap_Polling.auditLinuxAdminLdapAccess(baseDN_Polling_AccessGroups,
                                                                        searchScope_Polling_AccessGroups,
                                                                        searchFilter_Polling_AccessGroups,
                                                                        retrieveAttributes_Polling_AccessGroups,
                                                                        derefAliases_Polling_AccessGroups)

  df_pollingLinuxAccess = pd.DataFrame({'LDAP Access (Who has Access to Polling Hosts):': pollingLinuxAccess_l})
  df_pollingLinuxAccess.to_excel(auditSC_Ldap_Polling.wb2, sheet_name="Polling LDAP Access", index=False)

  auditSC_Ldap_Polling.wb2.save()

  ##
  ## Polling - LDAP Admin Group Membership audit:
  ##
  baseDN_Polling_LinuxGroups = "dc=orchard,dc=osh"
  searchScope_Polling_LinuxGroups = SUBTREE
  gidNumbers_Polling_LinuxGroups = ['10000', '10001', '10003']
  retrieveAttributes_Polling_LinuxGroups = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  derefAliases_Polling_LinuxGroups = DEREF_ALWAYS

  gidMembers_Groups_Polling_d = auditSC_Ldap_Polling.listLdapAdminGroupMembership(baseDN_Polling_LinuxGroups,
                                                                                  searchScope_Polling_LinuxGroups,
                                                                                  retrieveAttributes_Polling_LinuxGroups,
                                                                                  gidNumbers_Polling_LinuxGroups)

  pollingLdapAdminGroups_l = []
  for grpID in gidMembers_Groups_Polling_d.keys():

    pollingLdapAdminGroups_l.append("\n")
    pollingLdapAdminGroups_l.append('Linux Group ID [{}]:'.format(grpID))
    pollingLdapAdminGroups_l.append(r'date && ldapsearch -H ldaps://' + auditSC_Ldap_Polling.ldapServer + r':636 -x -D CN=<ldap_user>,OU=Users,OU=Administrative,DC=Orchard,DC=osh" -w "<ldap_passwd>" -b "' + baseDN_Polling_LinuxGroups +
                                r'" -s sub "(gidNumber=' + grpID + r')" ' + " ".join(retrieveAttributes_Polling_LinuxGroups) +
                                r' | grep "^dn\|^gid"')
    # pollingLdapAdminGroups_l.append(r'date && ldapsearch -H ldaps://' + auditSC_Ldap_Polling.ldapServer + r':636 -x -D "' +
    #                             auditSC_Ldap_Polling.UserDN + r'" -w "<passwd>" -b "' + baseDN_Polling_LinuxGroups +
    #                             r'" -s sub "(gidNumber=' + grpID + r')" ' + " ".join(retrieveAttributes_Polling_LinuxGroups) +
    #                             r' | grep "^dn\|^gid"')

    pollingLdapAdminGroups_l.append("\n")
    pollingLdapAdminGroups_l.append('{}'.format(auditSC_Ldap_Polling.DateTime))

    countGroupMembers = 0
    for member in gidMembers_Groups_Polling_d[grpID]:
      pollingLdapAdminGroups_l.append(member)
      countGroupMembers += 1

    pollingLdapAdminGroups_l.append('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))
    pollingLdapAdminGroups_l.append("\n")

  df_pollingLdapAdminGroups = pd.DataFrame({'LADP Groups Access (Who is assigned to what group):': pollingLdapAdminGroups_l})
  df_pollingLdapAdminGroups.to_excel(auditSC_Ldap_Polling.wb2, sheet_name="Polling LDAP Groups", index=False)

  auditSC_Ldap_Polling.wb2.save()

  ##
  ## Audit Linux Server Local - Accounts & Logs: /etc/passwd, shadow, sudoers; /var/logs/secure, messages, etc.
  ##
  ## /etc/sudoers as root
  ##

  pollingServers = Enums.auditSC_Servers_Polling

  port = 22
  userid = 'root'
  privateKey_root = "/root/.ssh/id_rsa"
  ## privateKey_root = "C:/admin/id_rsa_root"

  ##
  ## Audit Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  resLocalAdminAccounts_Servers_Polling_d = {}
  resLocalPasswdShadow_Servers_Polling_l = []
  resSudoers_Servers_Polling_l = []
  resInformixAccess_Servers_Polling_d = {}
  resRootAccess_Servers_Polling_d = {}

  df_InformixAccess_Servers_Frames_Polling_l = []
  df_RootAccess_Servers_Frames_Polling_l = []

  dfLocalAdminAccess_Columns_Polling = ['Dates', 'Hosts', 'Messages']

  for server in pollingServers:

    auditSC_LocalAccess_Server_Polling = auditSoxCompliance_ServerLocal.auditSoxCompliance_ServerLocal(hostname=server,
                                                                                                       port=port,
                                                                                                       userid=userid,
                                                                                                       privateKey=privateKey_root,
                                                                                                       reportPath = pathNewPollingReport)
    ##
    ## Audit Linux Admin Accounts on Server Local:
    ##
    ## Result of /etc/password & shadow audit:
    resPasswordShadow_RemoteServer_l = auditSC_LocalAccess_Server_Polling.scanPasswdShadow_RemoteServer()

    resLocalPasswdShadow_Servers_Polling_l.append(server + ":~ # " + auditSC_LocalAccess_Server_Polling.CMD_passwd_shadow)
    resLocalPasswdShadow_Servers_Polling_l.append(auditSC_LocalAccess_Server_Polling.DateTime)
    resLocalPasswdShadow_Servers_Polling_l.extend(resPasswordShadow_RemoteServer_l)
    resLocalPasswdShadow_Servers_Polling_l.append("\n")

    ## Result of /etc/sudoers audit:
    resSudoers_RemoteServer_l = auditSC_LocalAccess_Server_Polling.scanSudoers_RemoteServer()

    resSudoers_Servers_Polling_l.append(server + ":~ # " + auditSC_LocalAccess_Server_Polling.CMD_sudoers)
    resSudoers_Servers_Polling_l.append(auditSC_LocalAccess_Server_Polling.DateTime)
    resSudoers_Servers_Polling_l.extend(resSudoers_RemoteServer_l)
    resSudoers_Servers_Polling_l.append("\n")

    ## Result per Server:
    resLocalAdminAccounts_Servers_Polling_d[server] = [resPasswordShadow_RemoteServer_l, resSudoers_RemoteServer_l]

    ##
    ## Audit Informix & Root Access to Polling Server Local:
    ##

    filterInformixAccess = { "Include_all":["sudo","informix",], "Include_any":[], "Exclude":[]}
    timestamps_polling_server_informix_l, hostnames_polling_server_informix_l, messages_polling_server_informix_l = auditSC_LocalAccess_Server_Polling.scanHostAccess_RemoteServer_VarLogMessages_BZ2_Polling(**filterInformixAccess)

    resInformixAccess_Server_Polling_d = {}  ## Key move!!! Must initialize (reset) this Dict here, instead of outside the loop!

    resInformixAccess_Server_Polling_d["Dates"] = timestamps_polling_server_informix_l
    resInformixAccess_Server_Polling_d["Hosts"] = hostnames_polling_server_informix_l
    resInformixAccess_Server_Polling_d["Messages"] = messages_polling_server_informix_l

    resInformixAccess_Servers_Polling_d[server] = resInformixAccess_Server_Polling_d


    df_InformixAccess_Servers_Frames_Polling_l.append(pd.DataFrame.from_records(resInformixAccess_Server_Polling_d,
                                                                                columns=dfLocalAdminAccess_Columns_Polling))
    resRootAccess_Server_Polling_d = {}  ## Key Move!!

    filterRootAccess = { "Include_all_A":["sudo", "root",], "Include_all_B":["sshd", "root",], "Include_any":["sudo", "sshd",], "Exclude":["nagios",] }
    timestamps_polling_server_rootaccess_l, hostnames_polling_server_rootaccess_l, messages_polling_server_rootaccess_l = auditSC_LocalAccess_Server_Polling.scanHostAccess_RemoteServer_VarLogMessages_BZ2_Root_Polling(**filterRootAccess)

    resRootAccess_Server_Polling_d["Dates"] = timestamps_polling_server_rootaccess_l
    resRootAccess_Server_Polling_d["Hosts"] = hostnames_polling_server_rootaccess_l
    resRootAccess_Server_Polling_d["Messages"] = messages_polling_server_rootaccess_l

    resRootAccess_Servers_Polling_d[server] = resRootAccess_Server_Polling_d
    df_RootAccess_Servers_Frames_Polling_l.append(pd.DataFrame.from_records(resRootAccess_Server_Polling_d,
                                                                            columns=dfLocalAdminAccess_Columns_Polling))

  ##
  ## For Audit: Local Admin Accounts: /etc/passwd, shadow, and sudoers:
  ##
  df_LocalAdminAccounts_Servers_Polling = pd.DataFrame({"Local Access" : resLocalPasswdShadow_Servers_Polling_l})
  df_LocalAdminAccounts_Servers_Polling.to_excel(auditSC_LocalAccess_Server_Polling.wb2, sheet_name="Polling - Local Access", index=False)

  df_LocalAdminAccounts_Servers_Polling = pd.DataFrame( {"SUDO File" : resSudoers_Servers_Polling_l} )
  df_LocalAdminAccounts_Servers_Polling.to_excel(auditSC_LocalAccess_Server_Polling.wb2, sheet_name="Polling - SUDO File", index=False)


  ##
  ## For Audit: Form DataFrame - Informix & Root Access to Polling Server Local:
  ##
  # pp.pprint(df_InformixAccess_Servers_Frames_Polling_l)
  df_InformixAccess_Servers_Polling = pd.concat( df_InformixAccess_Servers_Frames_Polling_l )
  df_InformixAccess_Servers_Polling.to_excel(auditSC_LocalAccess_Server_Polling.wb2, sheet_name="Informix Access", index=False)

  df_RootAccess_Servers_Polling = pd.concat(df_RootAccess_Servers_Frames_Polling_l)
  df_RootAccess_Servers_Polling.to_excel(auditSC_LocalAccess_Server_Polling.wb2, sheet_name="Root Access", index=False)

  ##
  ## Wrap Up and Save updates to Excel Workbook:
  ##
  auditSC_LocalAccess_Server_Polling.wb2.save()

  ##
  ## Remove the redundant default worksheet, titled "Sheet"
  ##
  default_sheet = auditSC_LocalAccess_Server_Polling.wb2.book["Sheet"]
  auditSC_LocalAccess_Server_Polling.wb2.book.remove(default_sheet)
  auditSC_LocalAccess_Server_Polling.wb2.save()


  # ###############################################################################################
  #
  # ## Argparse Initiatives:
  # ## Allow interaction with console:
  #
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


