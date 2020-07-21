from csvControl import csvDataController
from dbControl import dbDataController

from datetime import timedelta, datetime

URL = "https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"

#This should be latter than get_option to get args
contoroller = csvDataController.CsvDataController(None,None)

#contoroller.downloadDataFromAPI(URL, "./bitStampUSD.csv.gzip")
#contoroller.getBitHistory()

#defaul items
DATE_FORMAT = "NORMAL"
#FROM_DATE = datetime.now()
FROM_DATE = datetime(2020,4,1)
print(FROM_DATE)
FROM_DATE += timedelta(days=-1)


MINUTE = "1minute"
HOUR = "1hour"

TABLE_NAME = "price_bitstamp_btcusd_"

file_list = contoroller.getDirectoryFiles(None,FROM_DATE)

date = file_list[-1].split("_")[1].split(".")[0]

contoroller.makeOHLC(None, file_list, DATE_FORMAT, MINUTE)
print(MINUTE, "File Making End")


contoroller.makeOHLC(None, file_list, DATE_FORMAT, HOUR)
print(HOUR, "File Making End")


print(date)

table_name = TABLE_NAME + "1min"
contoroller = dbDataController.DbDataController(None,MINUTE,table_name=table_name)

result = contoroller.selectData(date)
#print(result)

num = 1441
    
if len(result) < num:
    contoroller.deleteData(date, table_name=table_name)
print(len(result))

#Now DATE_FORMAT is not used
contoroller.makeOHLC(None, file_list)
print("Data added End")


table_name = TABLE_NAME + "1hour"
contoroller = dbDataController.DbDataController(None,HOUR,table_name=table_name)

result = contoroller.selectData(date)
#print(result)

num = 25
    
if len(result) < num:
    contoroller.deleteData(date)

#Now DATE_FORMAT is not used
contoroller.makeOHLC(None, file_list)
print("Data added End")

