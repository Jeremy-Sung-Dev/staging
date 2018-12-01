#!/usr/local/bin/python3.6

import argparse


if __name__ == "__main__":

  ## Argparse Initiatives:
  parser = argparse.ArgumentParser(prog='getArgparses.py', prefix_chars='-+', description='Demonstrate how argparse can be used.',
                                   add_help=True, allow_abbrev=True)
  parser.add_argument("-v","--version", required=True, help="Show version")
  # parser.add_argument("-v","--version", choices=[3.6, 2.6], default=3.6, help="Show version")
  parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  parser.add_argument("-V", "--verbose", action="store_true")
  parser.add_argument("-q", "--quiet", action="store_true")
  ## Positional:
  # parser.add_argument('bar', help='positional bar')

  args = parser.parse_args()

  # parser.print_help()
  # print(args)
  # print("Path: {},\tVersion: {}".format(args.reportPath, args.version))

  if args.quiet:
    print(args)
  elif args.verbose:
    print("Verbose - Path: {},\tVersion: {}".format(args.report, args.version))
  else:
    print("Path: {},\tVersion: {}".format(args.report, args.version))

  ## Have to execute with "python" in front!!
  ## C:\staging\python\pilot>python dev_oshr.py --command date
  ## Namespace(command='date', reportPath='C:/staging/python/pilot')

  ## Doesn't work:
  ## C:\staging\python\pilot> dev_oshr.py --command date  # unable to recognize "--command date"

  ##
  ## Example:
  ##
  ## Argparse Initiatives:
  parser = argparse.ArgumentParser(prog='extract_subtitles_from_srt.py', prefix_chars='-+', description='Extract Captions from SRT file',
                                   add_help=True, allow_abbrev=True)

  parser.add_argument("-p","--path", default="c:/lab", help="Path to source SRT file(s)")
  parser.add_argument("-s","--source_file", help="Source SRT Filename")
  parser.add_argument("-d","--destination_file", help="Name of Retrieved Text File")
  ## parser.add_argument("-p","--path", required=True, help="Path to source SRT file(s)")
  ## parser.add_argument("-s","--source_file", choices=[3.6, 2.6], default=3.6, help="Show version")
  ## parser.add_argument("--reportPath", default="C:/staging/python/pilot", help="Show content in reportPath")
  ## parser.add_argument("-V", "--verbose", action="store_true")
  parser.add_argument("-q", "--quiet", action="store_true")   ## ????

  ## Usage:  C:\staging\python\coding>python extract_subtitles_from_srt.py -p c:/lab  ## Worked!! 11/29/2018 1:25AM

  args = parser.parse_args()

  # parser.print_help()
  # print(args)

  ## path = r"c:/lab"    ## Should be replaced by:  args.path

  ## dstPath = path + '/' + subdirRetrieved
  dstPath = args.path + '/' + subdirRetrieved