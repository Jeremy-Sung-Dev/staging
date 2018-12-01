#!C:\staging\python\systems\Scripts\python.exd




if __name__ == "__main__":

  from Enums import DateTime, LastMonth

  ## Verify local Server Accounts and Sudo file:
  auditHosts = ['wms-wmosapp01', 'wms-wmosdb01', 'wms-sciapp01', 'wms-scidb01', 'wms-ifeeapp01']

  print(DateTime)

  # with open('passwd', 'r') as fpasswd:
  #   for passwd in fpasswd:
  #     if 'nologin' in passwd or 'false' in passwd:
  #       continue
  #     print(passwd)
  #
  # with open('shadow', 'r') as fshadow:
  #   for shadow in fshadow:
  #     if ':!' in shadow or ':*' in shadow:
  #       continue
  #     print(shadow)
  #
  # with open('sudoers', 'r') as fsudoers:
  #   for sudoer in fsudoers:
  #     if '^#' in sudoer or '^$' in sudoer:
  #       continue
  #     print(sudoer)

  import os, re
  pattern = re.compile("(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*$)")
  compiled = re.compile(pattern)

  Excluded = ('rfuser', 'disconnect', 'pam_unix', 'subsystem request for sftp')

  # print(LastMonth)  # May

  import pandas as pd

  # writer = pd.ExcelWriter("test.xlsx", engine='xlsxwriter')
  writer = pd.ExcelWriter("test.xlsx", engine='openpyxl')

  # workbook = writer.book
  # worksheet = writer.sheets['Host Access']

  timestamps_l = []
  hostnames_l = []
  messages_l = []

  for filename in os.listdir("."):

    if filename.startswith("secure"):

      with open(filename, 'r') as secure:

        for line in secure:

          if not line.startswith(LastMonth):
            continue

          # words =  line.split()
          # reduced_line = " ".join([w for w in words if w not in Excluded])

          # if not any(term in line for term in Excluded):
          if any(term in line for term in Excluded):
            continue

          groups = compiled.search(line)
          # print(groups.group(1).strip())  # May 15 10:16:19
          # print(groups.group(2).strip())  # hostnames
          # print(groups.group(3).strip())  # Messages

          # timestamp, host, message = groups.group(1).strip(), groups.group(2).strip(), groups.group(3)
          # print("{}, {}, {}".format(timestamp, host, message))
          # print("{} -- {} -- {}".format(timestamps, host, messages))

          timestamps_l.append(groups.group(1).strip())
          hostnames_l.append(groups.group(2).strip())
          messages_l.append(groups.group(3))

      ## Mark the filename_sample.
      # timestamps_l.append(0)
      # hostnames_l.append(0)
      # messages_l.append(filename_sample)

  df_secures = pd.DataFrame({'TimeStamp' : timestamps_l, 'Hosts' : hostnames_l, 'Messages' : messages_l})
  df_secures = df_secures[["TimeStamp", "Hosts", "Messages"]]
  df_secures.to_excel(writer, sheet_name = "Host Access", index = False)

  writer.save()