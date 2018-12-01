#!/usr/local/bin/python3.6

import sys
# import argparse


if __name__ == "__main__":

  ## Display Python Libraries Version:
  # print(sys.version) # 3.6.4 |Anaconda, Inc.| (default, Jan 16 2018, 10:22:32) [MSC v.1900 64 bit (AMD64)]
  # print(sys.version_info) # sys.version_info(major=3, minor=6, micro=4, releaselevel='final', serial=0)
  # print(sys.hexversion) # 50726128

  ## Experience Argparse:
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("-v","--version", help="Show version")
  # parser.add_argument("-v","--version", choices=[3.6, 2.6], default=3.6, help="Show version")
  parser.add_argument("--path", default="C:/staging/python/pilot", help="Show content in path")
  parser.add_argument("-V", "--verbose", action="store_true")
  parser.add_argument("-q", "--quiet", action="store_true")
  ## Positional:
  # parser.add_argument('bar', help='positional bar')

  args = parser.parse_args()

  # parser.print_help()
  # print(args)
  # print("Path: {},\tVersion: {}".format(args.path, args.version))

  if args.quiet:
    print(args)
  elif args.verbose:
    print("Verbose - Path: {},\tVersion: {}".format(args.path, args.version))
  else:
    print("Path: {},\tVersion: {}".format(args.path, args.version))