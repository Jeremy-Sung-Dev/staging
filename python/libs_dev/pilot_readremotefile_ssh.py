#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" pilot_readremotefile_ssh.py


Description:
Attributes:
  __version__ = "0.0.0"
  __project__ = pilot
  __author__ = Jeremy Sung
  __date__ = 6/21/2018 3:25 PM
  __Email__ = jsung8@gmail.com
Todo:

Referrences:
 - https://stackoverflow.com/questions/1596963/read-a-file-from-server-with-ssh-using-python

"""


class pilot_readremotefile_ssh:

  def pilot_readremotefile_ssh(self, rfilename):
    sftp_client = ssh_client.open_sftp()
    remote_file = sftp_client.open(rfilename)
    try:
      for line in remote_file:
    # process line
    finally:
      remote_file.close()

if __name__ == "__main__":
  sol = pilot_readremotefile_ssh()

  rfilename = "/etc/secure"  # remote filenames
  
  