#!/usr/bin/python

"""
a reference
"""

import xmlrpclib
import sys
import getpass

MANAGER_URL = "https://suma01.chameleoncorp.com/rpc/api"
MANAGER_LOGIN = input("Please Enter the SUSE Manager Login Name: ")
MANAGER_PASSWORD = getpass.getpass("Please Enter the Password: ")
MERGE_SOURCE = input("Enter the SOURCE channel label to Merge FROM: ")
MERGE_TARGET = input("Enter the TARGET channel label to Merge INTO: ")
print("This tool is going to take all packages and errata from the SOURCE")
print("Channel : " + MERGE_SOURCE)
print("and merge it into the TARGET ")
print("Channel : " + MERGE_TARGET)


def query_yes_no(question, default="yes"):
  """Ask a yes/no question via raw_input() and return their answer.

  "question" is a string that is presented to the user.
  "default" is the presumed answer if the user just hits <Enter>.
  It must be "yes" (the default), "no" or None (meaning
  an answer is required of the user).

  The "answer" return value is True for "yes" or False for "no".
  """
  valid = {"yes": True, "y": True, "ye": True,
           "no": False, "n": False}
  if default is None:
    prompt = " [y/n] "
  elif default == "yes":
    prompt = " [Y/n] "
  elif default == "no":
    prompt = " [y/N] "
  else:
    raise ValueError("invalid default answer: '%s'" % default)

  while True:
    sys.stdout.write(question + prompt)
    choice = raw_input().lower()
    if default is not None and choice == '':
      return valid[default]
    elif choice in valid:
      return valid[choice]
    else:
      sys.stdout.write("Please respond with 'yes' or 'no' "
                         "(or 'y' or 'n').\n")


query_yes_no("Is this information correct?")
client = xmlrpclib.Server(MANAGER_URL, verbose=0)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
client.channel.software.mergePackages(key, MERGE_SOURCE, MERGE_TARGET)
client.channel.software.mergeErrata(key, MERGE_SOURCE, MERGE_TARGET)
client.auth.logout(key)
