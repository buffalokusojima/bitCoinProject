from csvContorol import csvDataContoroller
from dbContorol import dbDataContoroller

from datetime import timedelta, datetime

URL = "https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"

#This should be latter than get_option to get args
contoroller = csvDataContoroller.CsvDataContoroller(None,None)

contoroller.downloadDataFromAPI(URL, "./bitStampUSD.csv.gzip")
contoroller.getBitHistory()

#defaul items
DATE_FORMAT = "NORMAL"
FROM_DATE = datetime.now()
print(FROM_DATE)
FROM_DATE += timedelta(days=-1)


MINUTE = "1minute"
HOUR = "1hour"

file_list = contoroller.getDirectoryFiles(None,FROM_DATE)

date = file_list[-1].split("_")[1].split(".")[0]

contoroller.makeOHLC(None, file_list, DATE_FORMAT, MINUTE)
print(MINUTE, "File Making End")


contoroller.makeOHLC(None, file_list, DATE_FORMAT, MINUTE)
print(HOUR, "File Making End")


print(date)

contoroller = dbDataContoroller.DbDataContoroller(None,MINUTE)

result = contoroller.selectData(MINUTE, date)
#print(result)

num = 1441
    
if len(result) < num:
    contoroller.deleteData(date, MINUTE)
print(len(result))

#Now DATE_FORMAT is not used
contoroller.makeOHLC(None, file_list, DATE_FORMAT, MINUTE)
print("Data added End")



contoroller = dbDataContoroller.DbDataContoroller(None,HOUR)

result = contoroller.selectData(HOUR, date)
#print(result)

num = 25
    
if len(result) < num:
    contoroller.deleteData(date, HOUR)

#Now DATE_FORMAT is not used
contoroller.makeOHLC(None, file_list, DATE_FORMAT, HOUR)
print("Data added End")

