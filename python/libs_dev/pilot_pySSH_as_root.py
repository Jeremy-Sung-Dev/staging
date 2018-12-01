#!/usr/lib/anaconda3/bin/python
# #!/usr/local/bin/python3.6
#!C:/staging/python/systems/Scripts/python.exe
# -*- coding: utf-8 -*-
""" auditSoxCompliance_ServerLocal.py

Description:
Attributes:
  __version__ = "0.0.0"
  __project__ = python
  __author__ = Jeremy Sung
  __date__ = 5/16/2018 1:17 PM
  __Email__ = Jeremy.Sung@osh.com

"""

import sys
import paramiko
import pprint as pp

class pilot_pySSH:

  def __init__(self, hostname="", port=22, userid="", passwd="", privateKey=""):
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




  def pyScp(self, param1):
    """
    @param :
    @return:
    """

    # rpi = {"user":"_jsung", "server":"admin01.orchard.osh"}
    # command = " ".join(sys.argv[1:])


if __name__ == "__main__":
  # utils = auditSoxCompliance_ServerLocal()

  # rpi = {"user": "_jsung", "server": "admin01.orchard.osh"}
  # command = " ".join(sys.argv[1:])
  #
  # ssh = paramiko.SSHClient()
  # ssh.load_host_keys()
  # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  # ssh.connect(**rpi)
  # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

  # # sFTP get demo:
  # # https://gist.githubusercontent.com/mlafeldt/841944/raw/f8dae8972e7c76d24c1bc8f44090354ea87e846e/scp_demo.py
  # if len(sys.argv) < 5:
  #   print("args missing")
  #   sys.exit(1)
  # server = sys.argv[1]
  # passwd = sys.argv[2]
  # source = sys.argv[3]
  # dest = sys.argv[4]
  # user = "_jsung"
  # port = 22
  # try:
  #   t = paramiko.Transport((server, port))
  #   t.connect(user=user, passwd=passwd)
  #   sftp = paramiko.SFTPClient.from_transport(t)
  #   sftp.get(source, dest)
  # finally:
  #   t.close()

  ## demo - working on it:
  # import base64
  # import paramiko

  # key = paramiko.RSAKey(data=base64.b64decode(b'AAA...'))

  # Not working:
  # key_wms_seaapp01 = paramiko.RSAKey(data=base64.b64decode(b'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBK64SjCrw5q//xMrTPdMdLQ2/ga8t+ARjqdeKJqaY07LA/4mEjRFqTp5WJfWinPoR81hHg2m0txJa6/lwABX2J0='))
  ## ?? key_wms_seaapp01 = paramiko.RSAKey(data=decodebytes(b'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBK64SjCrw5q//xMrTPdMdLQ2/ga8t+ARjqdeKJqaY07LA/4mEjRFqTp5WJfWinPoR81hHg2m0txJa6/lwABX2J0='))

  # client = paramiko.SSHClient()
  # # client.get_host_keys().add('10.1.19.13', 'ecdsa-sha2-nistp256', key_wms_seaapp01) # raise SSHException(err
  # client.get_host_keys().add('10.1.19.13', 'ssh-rsa', key_wms_seaapp01)
  # client.connect('10.1.19.13', user='_jsung', passwd=',.SOLpx.01')
  # command = 'uptime'
  # stdin, stdout, stderr = client.exec_command(command)
  # # client.get_host_keys().add('wms-seaapp01.orchard.osh', 'ssh-rsa', key_wms_seaapp01)
  # # client.connect('ssh.example.com', user='strongbad', passwd='thecheat')
  # # stdin, stdout, stderr = client.exec_command('ls')
  # for line in stdout:
  #   print('... ' + line.strip('\n'))
  # client.close()

  # ##############################################################################################
  # ## Worked!
  #
  # # Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
  # # server = '10.1.19.13'  # wms_seaapp01
  # # server = '10.1.1.26'  # mars-dfioapp01.orchard.osh # Offlined???
  # server = '10.1.19.21' #  wms-app91.orchard.osh
  # port = 22
  # user = '_jsung'
  # passwd = ',.SOLpx.01'
  #
  # ssh = paramiko.SSHClient()
  # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #
  # ssh.connect(server, port, username=user, key_filename="C:/admin/id_rsa")  # Require my OpenSSH private key!
  # # ssh.connect(server, port, user, passwd)  # Worked!!
  # # ssh.connect(server, port, username=user, password=passwd, key_filename="C:/admin/id_rsa") # Worked!!
  # ## ssh.connect(server, port, username=user, password=passwd, pkey=None, key_filename="") # Not working
  # ## ssh.connect(server, port, username=user, key_filename="C:/admin/id_rsa.pub") # paramiko.ssh_exception.SSHException: not a valid OPENSSH private key file
  #
  #
  # # cmd = 'server; uptime; cat /etc/*release'
  # # cmd = 'cat /var/log/secure'
  # # cmd = 'cat /etc/sudoers'
  # # cmd = 'cat /etc/passwd'
  # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")
  #
  #
  # stdin, stdout, stderr = ssh.exec_command(cmd)
  #
  # # resp = ''.join(outlines)
  #
  # result_l = []
  #
  # for line in stdout.readlines():
  #
  #   # if '^#' in line or '^$' in line:
  #   #   continue
  #
  #   result_l.append(line)
  #
  # pp.pprint(result_l)
  # ssh.close()
  # # return result_l

  ##############################################################################################
  ## Worked!  Similar to Oshr.pl;

  # Ref.  https://stackoverflow.com/questions/10745138/python-paramiko-ssh
  # hostname = 'wms-wmosapp91'  # wms-app91.orchard.osh

  hosts = ['wms-wmosapp01','wms-wmosapp91', 'wms-ifeeapp91','wms-wmosdb01','wms-ifeeapp01', 'wms-db91', 'wms-sciapp01', 'wms-sciapp91']

  ### hosts = ['wms-scidb01', 'dr-wms-scidb01', 'dr-wms-wmosdb01']
  port = 22
  userid = 'root'

  privateKey_root = "C:/admin/id_rsa_root"
  # ssh.connect(server, port, user, passwd)  # Worked!!
  # ssh.connect(server, port, username=user, password=passwd, key_filename="C:/admin/id_rsa_root") # Private Key!!

  cmd_shutdown = "shutdown -P 2"
  # cmd_unsubscribed_all = 'subscription-manager unsubscribe --all'
  # cmd_unregistered = 'subscription-manager unregister'
  ## cmd = 'cat /etc/sudoers'
  ## If "sudo" is required the script need to promput user for password though:
  # cmd = "echo {} | sudo -S {}".format(",.SOLpx.01", "cat /etc/sudoers")

  result_l = []

  for host in hosts:
    result_l.append(host + ' :\n')

    pilotSSH = pilot_pySSH(hostname=host, port=port, userid=userid, privateKey=privateKey_root)

    stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_shutdown)
    # stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_unsubscribed_all)
    ## stdin, stdout, stderr = pilotSSH.ssh.exec_command(cmd_unregistered)


  for line in stdout.readlines():
    # if '^#' in line or '^$' in line:
    #   continue
    result_l.append("{}".format(line))

  pp.pprint(result_l)

  pilotSSH.ssh.close()
  # return result_l

