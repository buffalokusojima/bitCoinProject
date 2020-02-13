import time, calendar, os, sys, glob
import json
from datetime import datetime, timedelta
from argparse import ArgumentParser
import traceback

import MySQLdb as sql
import json

sys.path.append("../")
from util import util


class DbDataContoroller():
    
    def __init__(self,path,term):

        self.TERM = term
        if self.TERM is None:
            self.TERM = "1minute"

        self.PATH = path
        if self.PATH is None:
            self.PATH = "./dataOfBitstamp"

        dbInfo = None
        with open("./dbContorol/dbPath.json", 'r') as f:
            filePath = json.load(f)
            with open(filePath['filePath'], 'r') as f:
                dbInfo = json.load(f)
       
        self.CONN = sql.connect(
            host = dbInfo['host'],
            user = dbInfo['user'],
            password = dbInfo['password'],
            database = dbInfo['database']
        )


    def makeOHLC(self,directory,file_list,DATE_FORMAT,TERM):
       
        if directory is None:
            directory = self.PATH

        MINUTES = 60

        term = 0
        partisionMax = 0

        if TERM == "1minute":
            term = MINUTES
            
        elif TERM == "1hour":
            term = 60 * MINUTES
        
        else:
            print("TERM invalid")
            exit(0)
        
        startTime = 0
        partision = 0
        for file in file_list:
            
            if partision == 0:
                ohlc = []
            
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
                    ohlc.append(before)
                    startTime += term
                partision += 1
            if partision >= partisionMax or file == file_list[len(file_list)-1]:
                
                #print(ohlc[0])    
                self.writeToDB(ohlc, TERM)
                #util.write(path,ohlc)
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

    def writeToDB(self, ohlc_list, term):
        
        table_name = "price_"
        if term == "1minute":
            table_name += "1min"

        elif term == "1hour":
            table_name += term
        else:
            print("TERM invalid")
            exit(0)

        cursor = self.CONN.cursor()
        
        for ohlc in ohlc_list:
            try:
                #print(ohlc)
                #The latest data in DB should be replaced
                cursor.execute("INSERT INTO "+ table_name +" VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (ohlc[0], 1, 1, ohlc[1], ohlc[4], ohlc[2], ohlc[3], ohlc[5]))
                
            except:
                traceback.print_exc()
        self.CONN.commit()


    def selectData(self, term, date):

        
        table_name = "price_"
        if term == "1minute":
            table_name += "1min"

        elif term == "1hour":
            table_name += term
        else:
            print("TERM invalid")
            exit(0)

        cursor = self.CONN.cursor()

        try:
            #query = "SELECT * FROM "+ table_name + " WHERE date = %s"
            #print(query)
            date = "'" + date + "'"
            cursor.execute("SELECT * FROM "+ table_name + " WHERE date > " + date)
            rows = cursor.fetchall()
            
            return rows

            #exit(1)
            #cursor.execute("DELETE FROM " + table_name + " WHERE date = " + ohlc[0][0])
        except:
            traceback.print_exc()
            exit(1)

    def deleteData(self, date, term):

        table_name = "price_"
        if term == "1minute":
            table_name += "1min"

        elif term == "1hour":
            table_name += term
        else:
            print("TERM invalid")
            exit(0)

        cursor = self.CONN.cursor()

        try:
            date = "'" + date + "'"
            cursor.execute("DELETE FROM "+ table_name + " WHERE date > " + date)
            rows = cursor.fetchall()
            
            return rows

        except:
            traceback.print_exc()
            exit(1)



if __name__ == "__main__":

    URL = "https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
    #URL = "http://localhost:3000"

    #This should be latter than get_option to get args
    contoroller = DbDataContoroller(None,"1minute")
    #contoroller.downloadDataFromAPI(URL, "./bitStampUSD.csv.gzip")
    #contoroller.getBitHistory()

    #defaul items
    DATE_FORMAT = "NORMAL"
    FROM_DATE = datetime(2011, 9, 13)
    TERM = "1minute"

    #this should be called first
    args = contoroller.get_option(DATE_FORMAT, FROM_DATE, TERM)
    
    fromDate = args.from_date

    file_list = contoroller.getDirectoryFiles(None,fromDate)

    date = file_list[-1].split("_")[1].split(".")[0]

    #print(date)

    result = contoroller.selectData(args.term, date)
    #print(result)
    num = 0
    if args.term == "1min":
        num = 1441
    elif args.term == "1hour":
        num = 25

    if len(result) < num:
        contoroller.deleteData(date, args.term)

    #Now DATE_FORMAT is not used
    contoroller.makeOHLC(None, file_list, args.data_format, args.term)
    print("File Making End")