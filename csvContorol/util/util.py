import time, calendar, os, sys, glob
import json
from datetime import datetime, timedelta

def write(path, data):
   
   try:
       with open(path, 'w') as f:
           for d in data:
               f.write(d)
       
   except Exception as e:
       print(" Exception => Output Write: ", path, str(e))


#unixTime -> dateTime year-month-day 
def timeRegex(timeVal):
   import re
   regex_1 = r'\d\d\d\d-\d\d-\d\d'

   try:
       p1 = re.compile(regex_1)
       text = timeVal
       m1 = p1.match(text)
       src = m1.group()
       dst = src.replace('T', ' ')
       return dst

   except Exception as e:
       print("Exception => timeRegex: " + str(e))
       return "0000-00-00"


#unixTime -> dateTime year-month-day hour:minute
def timeRegexToMinute(timeVal):
   import re
   regex_1 = r'\d\d\d\d-\d\d-\d\d \d\d:\d\d'
   try:
       p1 = re.compile(regex_1)
       text = timeVal
       m1 = p1.match(text)
       src = m1.group()
       dst = src.replace('T', ' ')
       return dst

   except Exception as e:
       print("Exception => timeRegex: " + str(e))
       return "0000-00-00"


def timeRegexToSeconds(timeVal):
   import re
   regex_1 = r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d'
   try:
       p1 = re.compile(regex_1)
       text = timeVal
       m1 = p1.match(text)
       src = m1.group()
       dst = src.replace('T', ' ')
       return dst

   except Exception as e:
       print("Exception => timeRegex: " + str(e))
       return "0000-00-00"


#get first time of the day
def getDateFirstTime(date):

    date = datetime.fromtimestamp(int(date))
    date = timeRegex(str(date))
    date = date.split("-")
    date = datetime(int(date[0]), int(date[1]), int(date[2]))
    date = time.mktime(date.timetuple())
    
    return int(date)

#get first minute of the time
def getDateFirstMinute(date):

    date = datetime.fromtimestamp(int(date))
    date = timeRegexToMinute(str(date))
    date = date.split(" ")
    
    hour = date[1].split(":")
    minute = hour[1]
    hour = hour[0]

    date = date[0].split("-")

    date = datetime(int(date[0]), int(date[1]), int(date[2]), int(hour), int(minute))
    date = time.mktime(date.timetuple())

    return int(date)