#!/usr/lib/anaconda3/bin/python
#!C:\staging\python\systems\Scripts\python.exe

# -*- coding: utf-8 -*-
""" Enums.py
Description: Constants shared among Python modules
Attributes:
  __version__ = "3.0.1"
  __project__ = Prod
  __author__ = Jeremy Sung
  __date__ = 6/27/2018 11:31 AM
  __Email__ = Jeremy.Sung@osh.com

"""
import datetime
import time
import pytz

Now = datetime.datetime.now()
Today = datetime.date.today()

DayOfWeek = Now.strftime("%a")      # Thu
MonthOfYear = Now.strftime("%b")    # Jun
DayOfTheMonth = Now.strftime("%d")  # 06
Time = Now.strftime("%H:%M:%S")     # 15:29:55

## TimeZone = Now.strftime("%Z")       # None!?
## TimeZone = time.tzname       # ('Pacific Standard Time', 'Pacific Daylight Time')
TimeZone = time.localtime().tm_zone

## def localTimeNow():
##   return datetime.datetime.now(tz=pytz.timezone("US/Pacific"))

TimeZone_LocalTime_Verbose = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname() # Pacific Daylight Time
TimeZone = "".join( [ x[0] for x in TimeZone_LocalTime_Verbose.split()] ) # PDT

Year = Now.strftime("%Y")           # 2018

### User Defined Enums - Shared among all programs:
## DateTime = Now.strftime("%a %b %d %H:%M:%S %Z %Y")  ## %Z returns None because datetime unaware of Timezone
DateTime = Now.strftime("%a %b %d %H:%M:%S %Y") + " " + TimeZone  ## %Z returns None because datetime unaware of Timezone


## Ref. https://stackoverflow.com/questions/9724906/python-date-of-the-previous-month
FirstDayofMonth = Today.replace(day=1)
numLastMonth = FirstDayofMonth - datetime.timedelta(days=1)
LastMonth = numLastMonth.strftime("%b") # May

## Hosts list - Linux SOX Compliance Audit -
auditSC_Servers_WMS = ["wms-app01", "wms-app02", "wms-mifapp01", "wms-mifapp02", "wms-mmcapp01", "wms-seaapp01",
                       "sci-app01", "sci-app02", "sci-app03", "wms-db01", "sci-db01"]  ## WMS 2017
# WMS 2017 - Oracle DB servers
auditSC_Servers_WMS_DB_2017 = ["wms-db01", "sci-db01"]

auditSC_Servers_MARS = ['mars-app01', 'mars-sciapp01', 'oracledb01']
auditSC_Servers_MARS_DB = ['oracledb01']
auditSC_Servers_Polling = ['polling01', 'polling02', 'dr-polling01']

## Hosts List -
## WMS 2017 - All Hosts -
Servers_WMS_2017 = ["wmsci-db91",  "wms-app91", "wms-app92", "sci-app91", "sci-app92",
                    "wms-app01", "wms-app02",
                    "wms-mifapp01", "wms-mifapp02", "wms-mmcapp01", "wms-seaapp01", "wms-sciapp91",
                    "sci-app01", "sci-app02", "sci-app03",
                    "wms-db01", "sci-db01"]

## WMS 2017 - Oracle DB servers - Prod & Dev
Servers_WMS_DB_2017 = ["wmsci-db91", "wms-db01", "sci-db01"]
Servers_WMS_2017_Dev = ["wms-app91", "wms-app92", "wms-mifapp91", "wms-sciapp91", "sci-app91", "sci-app92", "wmsci-db91"]

## WMS 2012 - Audited Hosts -  Off-lined now; ready to be decommissioned:
## auditSC_Servers_WMS_2012 = ["wms-wmosapp01", "wms-wmosdb01", "wms-sciapp01", "wms-scidb01", "wms-ifeeapp01"]

## WMS 2012 - All Hosts -
Servers_WMS_2012 = ["wms-wmosapp01", "wms-ifeeapp01", "wms-sciapp01", "wms-wmosapp91", "wms-ifeeapp91", "wms-sciapp91", "wms-wmosdb01", "wms-scidb01", "wms-db91", "dr-wms-scidb01", "dr-wms-wmosdb01"]


## MARS - All Hosts -
Servers_MARS = ["mars-app01", "mars-sciapp01", "oracledb01", "mars-app91", "mars-sciapp91", "oracledb91"]
Servers_MARS_DB = ["oracledb01", "oracledb91"]

## Pollings & Support - All Hosts -
Servers_Polling_Support = ['polling01', 'polling02', 'dr-polling01', 'polling61', 'polling91', 'support01', 'dr-support01' ]  ## All Polling/Support Hosts
Servers_Polling = ['polling01', 'polling02', 'dr-polling01', 'polling61', 'polling91']

## Polling Dev Hosts -
Servers_Polling_Dev = ['polling61', 'polling91' ]
Servers_Support = ['support01', 'dr-support01' ]

## Bare Metal Hosts -
Servers_BareMetal = ['polling01', 'polling91', 'support01', 'oracledb01', 'oracledb91']


if __name__ == "__main__":

  ## print(TimeZone_LocalTime_Verbose)  # Pacific Daylight Time
  ## print(TimeZone)  # PDT
  print(DateTime)
