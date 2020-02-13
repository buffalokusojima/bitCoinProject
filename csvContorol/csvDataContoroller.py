import time, calendar, os, sys, glob
import json
from datetime import datetime, timedelta
from argparse import ArgumentParser

import urllib.request
from io import StringIO

import gzip

sys.path.append("../")
from util import util

class CsvDataContoroller():
    
    def __init__(self,path,fileName):

        self.PATH = path
        if self.PATH is None:
            self.PATH = "./dataOfBitstamp"
        self.FILE_NAME = fileName
        if self.FILE_NAME is None:
            self.FILE_NAME = "bitstampUSD.csv"

    def downloadDataFromAPI(self, url, filePath):

        
        try:
            
            with urllib.request.urlopen(url) as web_file:
                data = web_file.read()
                with open(filePath, mode='wb') as local_file:
                    local_file.write(data)

            with gzip.open(filePath, mode='rt') as fp:
                 with open(self.FILE_NAME, 'w') as f:
                     f.write(fp.read())
            
            
        except urllib.error.URLError as e:
            print(e)


    def getBitHistory(self):
    
        DAY = 86400

        term = DAY

        with open(self.FILE_NAME,'r') as f: 
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
                path = os.path.join(self.PATH, filename)

                while True:
                    line = f.readline()
                    if line is None or line == '' or int(line.split(",")[0]) > endDate: break
                    data.append(line)

                util.write(path,data)
                print("file made:", filename)

    def makeOHLC(self,directory,file_list,DATE_FORMAT,TERM):
        
        if directory is None:
            directory = self.PATH

        MINUTES = 60
        filenameSufix = ""
        PATH = ""
        term = 0
        partisionMax = 0

        if TERM == "1minute":
            filenameSufix = "OHLC_1minute.csv"
            term = MINUTES
            PATH = "./dataOfBitstampOHLC/1minute"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return

        elif TERM == "5minutes":
            filenameSufix = "OHLC_5minutes.csv"
            term = 5 * MINUTES
            PATH = "./dataOfBitstampOHLC/5minutes"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return
        
        elif TERM == "15minutes":
            filenameSufix = "OHLC_15minutes.csv"
            term = 15 * MINUTES
            PATH = "./dataOfBitstampOHLC/15minutes"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return

        elif TERM == "30minutes":
            filenameSufix = "OHLC_30minutes.csv"
            term = 30 * MINUTES
            PATH = "./dataOfBitstampOHLC/30minutes"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return

        elif TERM == "1hour":
            filenameSufix = "OHLC_1hour.csv"
            term = 60 * MINUTES
            PATH = "./dataOfBitstampOHLC/1hour"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return

        elif TERM == "4hours":
            filenameSufix = "OHLC_4hours.csv"
            term = 240 * MINUTES
            PATH = "./dataOfBitstampOHLC/4hours"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return
            

        elif TERM == "1day":
            filenameSufix = "OHLC_1day.csv"
            term = 3600 * MINUTES
            PATH = "./dataOfBitstampOHLC/1day"
            if not os.path.isdir(PATH):
                print("PATH:",PATH,"does not exist")
                return
            partisionMax = 7

        else:
            print("TERM invalid")
            exit(0)
        
        startTime = 0
        partision = 0
        for file in file_list:
            if partision == 0:
                filename = file.split(".")[0]+filenameSufix
                path = os.path.join(PATH, filename)
                print(filename)
                ohlc = ['time,open,high,low,close,volume\n']
            FILE_NAME = os.path.join(directory, file)
            
            with open(FILE_NAME,'r') as f: 
                line = None
                while True:
                    if(line is None): 
                        try:
                            line = f.readline()
                            startTime = util.getDateFirstMinute(line.split(",")[0])
                        except Exception as e:
                            print(str(e))

                    if(line is None or line == ''): break
                    data = []
                    data.append(line)
                    endTime = startTime + term
                    #startTime = datetime.fromtimestamp(int(startTime))
                    #filename = "bitCoinHisOfBitStampOHLC_" + timeRegex(str(startTime)) + ".csv"
                    #path = os.path.join(PATH, filename)
            
                    before = []
                    while True:
                        line = f.readline()
                        if line is None or line == '' or int(line.split(",")[0]) > endTime: break
                        data.append(line)

                    before = self.countOHLC(data, before, endTime)
                    ohlc.append(",".join(before)+"\n")
                    startTime += term
                partision += 1
            if partision >= partisionMax or file == file_list[len(file_list)-1]:
                
                #print(ohlc[0])    
                util.write(path,ohlc)
                #print(ohlc)
                ohlc=[]
                partision=0

    def countOHLC(self, data, before, endTime):

        if data is None or data == []:
            before[0] = endTime
            #before[2] = before[3] = before[4] = str(0)
            return before

        min = 999999999999
        max = 0
        open = data[0].split(",")[1]
        close = data[len(data)-1].split(",")[1]
        amount = 0

        for d in data:
            price = float(d.split(",")[1])
            if(price < min):
                min = price
            if(price > max):
                max = price
            amount += float(d.split(",")[2])
        
        endTime = datetime.fromtimestamp(int(endTime))
        endTime = util.timeRegexToMinute(str(endTime))
        return [str(endTime),str(open), str(max), str(min), str(close), str(amount)]


    def get_option(self, dateFormat, fromDate, term):
        argparser = ArgumentParser()
        argparser.add_argument('-d', '--data-format', type=str,
                            default=dateFormat,
                            help='Specify format of date')
        argparser.add_argument('-f', '--from-date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                            default=fromDate,
                            help='Specify first date to make')

        argparser.add_argument('-t', '--term', type=str,
                                default=term,
                                help='Specify term to make data')
        
        return argparser.parse_args()

    def getDirectoryFiles(self,directory,fromDate):

        if directory is None:
            directory = self.PATH
        FILE = os.listdir(directory)
        file_list = []
        fromDateFile = "bitCoinHisOfBitStamp_" + util.timeRegex(str(fromDate)) + ".csv"
        while True:
            #fromDateFile = "bitCoinHisOfBitStamp_"+timeRegex(str(fromDate))+"OHLC.csv"
            fromDateFile = "bitCoinHisOfBitStamp_" + util.timeRegex(str(fromDate)) + ".csv"
            if fromDateFile not in FILE:
                if fromDate > datetime.now():
                    break
                fromDate = fromDate + timedelta(days=1)
                continue
            
            print(fromDateFile)
            file_list.append(fromDateFile)
            fromDate = fromDate + timedelta(days=1)

        return file_list

if __name__ == "__main__":

    URL = "https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
    #URL = "http://localhost:3000"

    #This should be latter than get_option to get args
    contoroller = CsvDataContoroller(None,None)
    contoroller.downloadDataFromAPI(URL, "./bitStampUSD.csv.gzip")
    contoroller.getBitHistory()

    #defaul items
    DATE_FORMAT = "NORMAL"
    FROM_DATE = datetime(2011, 9, 13)
    TERM = "1minute"

    #this should be called first
    args = contoroller.get_option(DATE_FORMAT, FROM_DATE, TERM)
    
    fromDate = args.from_date
    
    file_list = contoroller.getDirectoryFiles(None,fromDate)

    #Now DATE_FORMAT is not used
    contoroller.makeOHLC(None, file_list, args.data_format, args.term)
    print("File Making End")