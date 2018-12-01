#!C:\staging\python\systems\Scripts\python.exd

import pprint as pp

from Enums import DateTime



if __name__ == "__main__":

  # print(DateTime)

  from ldap3 import Server, Connection, SUBTREE, DEREF_ALWAYS

  ## first open a connection to the server

  # ldapServer = "dc01.orchard.osh"
  # server = Server(ldapServer)
  # # Port = 636
  # # server = Server(ldapServer, Port)  # Error:
  # # ldap3.core.exceptions.LDAPSocketReceiveError: error receiving data: [WinError 10054] An existing connection was forcibly closed by the remote host
  #
  # UserDN = "CN=Lookitup4,OU=Users,OU=Administrative,DC=Orchard,DC=osh"
  # Password = "Ld@p$3cAuth!"
  #
  # conn = Connection(server, user=UserDN, passwd=Password)
  # # conn = Connection(s, authentication=AUTH_SIMPLE, user=UserDN, passwd=Password, check_names=True, lazy=False, client_strategy=STRATEGY_SYNC, raise_exceptions=False)
  # conn.open()
  # conn.bind()


  ## your search requirements and directory:
  # baseDN = "dc=orchard,dc=osh"
  #
  # searchFilter = '(gidNumber=10000)'
  #
  # searchScope = SUBTREE
  # retrieveAttributes = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  #
  # derefAliases =  DEREF_ALWAYS


  ## Linux Audit - WMS:

  Domain = '.orchard.osh'
  # auditHosts = ['wms-wmosapp01', 'wms-wmosdb01', 'wms-sciapp01', 'wms-scidb01', 'wms-ifeeapp01']

  ldapServer = "dc01" + Domain

  server = Server(ldapServer)

  UserDN = "CN=Lookitup4,OU=Users,OU=Administrative,DC=Orchard,DC=osh"
  Password = "Ld@p$3cAuth!"

  conn = Connection(server, user=UserDN, password=Password)
  # conn = Connection(s, authentication=AUTH_SIMPLE, user=UserDN, passwd=Password, check_names=True, lazy=False, client_strategy=STRATEGY_SYNC, raise_exceptions=False)
  conn.open()
  conn.bind()


  # ## Review WMS Access Groups - Print group members for server access.
  # baseDN = "ou=Groups,ou=Administrative,dc=orchard,dc=osh"
  # searchFilter = '(cn=Linux-WMS-Access*)'
  # searchScope = SUBTREE
  # retrieveAttributes = ['cn', 'member']
  # derefAliases = DEREF_ALWAYS
  #
  # ## retrieve all attributes - again adjust to your needs - see documentation for more options
  # conn.search(search_base=baseDN, search_filter=searchFilter, search_scope=searchScope, attributes=retrieveAttributes)
  #
  # pp.pprint(conn.response)  # a list with 1 entry - a set obj.
  ## conn.response['attributes']['member'] is what we're looking for. print each member.
  #
  # responses_d = conn.response[0]
  # attributes_d = responses_d['attributes']
  #
  # for member in attributes_d['member']:
  #   print(member)



  ## Print group members for Linux groups:
  baseDN = "dc=orchard,dc=osh"
  gidNumbers = ['10000', '10001', '10004', '10005']
  # gid = 10000 # gid is one of numbers in gidNumbers;
  # searchFilter = '(gidNumber=gid)'
  searchScope = SUBTREE
  retrieveAttributes = ['cn', 'gidNumber', 'uidNumber', 'loginShell', 'unixHomeDirectory']
  derefAliases = DEREF_ALWAYS

  gidMembers_d = {}  # { gidNumber : { members_of_gid_List } }

  for gid in gidNumbers:
    searchFilter = '(gidNumber=' + gid + ')'
    conn.search(search_base=baseDN, search_filter=searchFilter, search_scope=searchScope, attributes=retrieveAttributes)

    gidMembers_l = []

    for member_d in conn.response:

      for key, value in member_d.items():
        if key == 'dn':
          gidMembers_l.append(member_d[key])
        else:
          continue

      gidMembers_d[gid] = gidMembers_l

  # pp.pprint(gidMembers_d)

  # for grpID in gidMembers_d:
  #   print(entry)

  for grpID in gidMembers_d.keys():
    # print(DateTime)
    # print('Linux Group ID: {}'.format(grpID))
    print('{} - Linux Group ID [{}]:'.format(DateTime, grpID))
    countGroupMembers = 0
    for member in gidMembers_d[grpID]:
      print(member)
      countGroupMembers += 1

    print('Total number of members in Linux Group [{}]: {}\n'.format(grpID, countGroupMembers))


  ## Verify local Server Accounts and Sudo file:
  auditHosts = ['wms-wmosapp01', 'wms-wmosdb01', 'wms-sciapp01', 'wms-scidb01', 'wms-ifeeapp01']

  # with open('passwd', 'r') as fpasswd:
  #
  #   # users = fpasswd.read()
  #   for user in fpasswd:
  #     print(user)







  conn.unbind()

