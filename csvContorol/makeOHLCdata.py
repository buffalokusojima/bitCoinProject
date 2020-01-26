import time, calendar, os, sys, glob
import json
from datetime import datetime, timedelta
from argparse import ArgumentParser

from util import util

def getOHLC(DIRECTORY,FILES,DATE_FORMAT,TERM):
   
    filenameSufix = ""
    PATH = ""
    term = 0
    partisionMax = 0

    if TERM == "1minute":
        filenameSufix = "OHLC_1minute.csv"
        term = MINUTES
        PATH = "./dataOfBitstampOHLC/1minute"

    elif TERM == "5minutes":
        filenameSufix = "OHLC_5minutes.csv"
        term = 5 * MINUTES
        PATH = "./dataOfBitstampOHLC/5minutes"
       
    elif TERM == "15minutes":
        filenameSufix = "OHLC_15minutes.csv"
        term = 15 * MINUTES
        PATH = "./dataOfBitstampOHLC/15minutes"

    elif TERM == "30minutes":
        filenameSufix = "OHLC_30minutes.csv"
        term = 30 * MINUTES
        PATH = "./dataOfBitstampOHLC/30minutes"

    elif TERM == "1hour":
        filenameSufix = "OHLC_1hour.csv"
        term = 60 * MINUTES
        PATH = "./dataOfBitstampOHLC/1hour"

    elif TERM == "4hours":
        filenameSufix = "OHLC_4hours.csv"
        term = 240 * MINUTES
        PATH = "./dataOfBitstampOHLC/4hours"
        

    elif TERM == "1day":
        filenameSufix = "OHLC_1day.csv"
        term = 3600 * MINUTES
        PATH = "./dataOfBitstampOHLC/1day"
        partisionMax = 7

    else:
        print("TERM invalid")
        exit(0)
    
    startTime = 0
    partision = 0
    for file in FILES:
        if partision == 0:
            filename = file.split(".")[0]+filenameSufix
            path = os.path.join(PATH, filename)
            print(filename)
            ohlc = ['time,open,high,low,close,volume\n']
        FILE_NAME = os.path.join(DIRECTORY, file)
        
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

                before = countOHLC(data, before, endTime)
                ohlc.append(",".join(before)+"\n")
                startTime += term
            partision += 1
        if partision >= partisionMax or file == FILES[len(FILES)-1]:
            
            #print(ohlc[0])    
            util.write(path,ohlc)
            #print(ohlc)
            ohlc=[]
            partision=0

def countOHLC(data, before, endTime):

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


def get_option(dateFormat, fromDate, term):
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

if __name__ == '__main__':

    global MINUTES
    MINUTES = 60
    DIRECTORY = "./dataOfBitstamp"

    DATE_FORMAT = "NORMAL"
    FROM_DATE = datetime(2011, 9, 13)
    TERM = "1minute"

    args = get_option(DATE_FORMAT, FROM_DATE, TERM)
    
    """
    if mode == "bitOHLC":
        FILE = os.listdir(DIRECTORY)
        #for file in FILE:
         #   print(file)
        getOHLC(DIRECTORY,FILE,DATE_FORMAT,TERM)
    #getOHLC(directory,"bitCoinHisOfBitStamp_2012-04-11.csv")
    """
    fromDate = args.from_date
    
    FILE = os.listdir(DIRECTORY)
    FILES = []
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
        FILES.append(fromDateFile)
        fromDate = fromDate + timedelta(days=1)
    getOHLC(DIRECTORY,FILES,args.data_format,args.term)
    print("File Making End")
            
