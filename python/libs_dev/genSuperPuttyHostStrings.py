#!C:/staging/python/systems/Scripts/python.exe

import os

class OSHUtils:
  def __init__(self):
    pass

  def genSuperPuttySessionXML(self, domain, *sites):

    xmlSession_l = []

    if not domain:
      domain = "orchard.osh"

    xmlSession_l.append('<?xml version="1.0" encoding="utf-8"?>')
    xmlSession_l.append('<ArrayOfSessionData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">')

    # C:\staging\data
    if not sites:
      with open("C:/staging/data/hosts", 'r') as file:
        for host in file:
          xmlSession_l.append('  <SessionData SessionId="{}" SessionName="{}" ImageKey="computer" Host="{}" Port="22"'
                          ' Proto="SSH" PuttySession="Default Settings" Username="" ExtraArgs="" SPSLFileName=""'
                          ' />'.format(host, host, host))
    else:
      for site in sites:
        filename = "C:/staging/data/hosts_" + site

        try:
          with open(filename, 'r') as site_file:
            for host in site_file:
              host = host.strip() + '.' + domain
              xmlSession_l.append('  <SessionData SessionId="{}/{}" SessionName="{}" ImageKey="computer" Host="{}"'
                                  ' Port="22" Proto="SSH" PuttySession="Default Settings" Username=""'
                                  ' ExtraArgs="" SPSLFileName="" />'.format(site, host, host, host))
        except FileNotFoundError as e:
          print("{} does not exist.".format(filename))
          print(repr(e))

    xmlSession_l.append('</ArrayOfSessionData>')

    return '\n'.join(xmlSession_l)


if __name__ == '__main__':

  domain = 'orchard.osh'
  # site = 'ssc'  # stores, dr
  sites = ['ssc', 'stores', 'dr']

  oshUtils = OSHUtils()

  # xmlSession = oshUtils.genSuperPuttySessionXML(domain, site)
  xmlSession = oshUtils.genSuperPuttySessionXML(domain, *sites)
  print(xmlSession)

