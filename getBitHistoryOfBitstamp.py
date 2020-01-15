import time, calendar, os, sys, glob
import json
from datetime import datetime, timedelta

from util import util

def getBitHistory():
   
   #保存
   PATH = "./dataOfBitstamp"
   DAY = 86400
   FILE_NAME = "bitstampUSD.csv" #ファイル名
   
   term = DAY

   with open(FILE_NAME,'r') as f: 
       line = None
       while True:
           if(line is None): line = f.readline()
           if(line is None or line == ''): break
           data = []
           data.append(line)
           startDate = data[0].split(",")[0]
           endDate = util.getDateFirstTime(startDate) + term
           startDate = datetime.fromtimestamp(int(startDate))
           filename = "bitCoinHisOfBitStamp_" + util.timeRegex(str(startDate)) + ".csv"
           path = os.path.join(PATH, filename)
           
           while True:
               line = f.readline()
               if line is None or line == '' or int(line.split(",")[0]) > endDate: break
               data.append(line)
           
           util.write(path,data)
           print("file made:", filename)
    
if __name__ == '__main__':

    global MINUTES
    MINUTES = 60
    DIRECTORY = "./dataOfBitstamp"
    
    getBitHistory()
            
