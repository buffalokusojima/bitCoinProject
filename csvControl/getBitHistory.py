# coding: utf-8
import requests,time, datetime, calendar, os, sys
import urllib.request
import json
from coinapi_v1 import CoinAPIv1

#ご自分のAPIキーに差し替え
test_key = '1C0B080A-6ED8-4056-8AA4-5C20B9C7E849'

api = CoinAPIv1(test_key)
exchanges = api.metadata_list_exchanges()

def write(path, fileName, filemode, Msg):
   
   try:
       path = os.path.join(path, fileName)
       with open(path, mode=filemode, encoding="utf-8") as f:
           f.write(Msg)
       
   except Exception as e:
       print(str(TimeCurrent()), " Exception => Output Write: ", fileName, str(e))

def writeFile(res, path, file_Name):
   
   try:
       for i in range(len(res)):
           timeVal = res[i]['time_period_start']
           timestmp = timeRegex(timeVal)

           _O = res[i]['price_open']
           _H = res[i]['price_high']
           _L = res[i]['price_low']
           _C = res[i]['price_close']

           val = "{0};{1};{2};{3};{4}{5}".format(timestmp, str(_O), str(_H), str(_L), str(_C), "\n")

           write(path, file_Name, "a", val)
           
       print(str(TimeCurrent()), "作業中")
       
   except Exception as e:
       print("Exception => writeFile: " + str(e))

def TimeCurrent():
   now = datetime.datetime.now()
   return now

def timeRegex(timeVal):
   import re
   regex_1 = r'\d\d\d\d-\d\d-\d\d.\d\d:\d\d:\d\d'

   try:
       p1 = re.compile(regex_1)
       text = timeVal
       m1 = p1.match(text)
       src = m1.group()
       dst = src.replace('T', ' ')
       return dst

   except Exception as e:
       print("Exception => timeRegex: " + str(e))
       return "0000-00-00 00:00:00"

if __name__ == '__main__':

   #日付を指定する
   year = 2015
   month = '1'
   day = '1' 

   start_of = datetime.date(year, (int)(month), (int)(day)).isoformat()
   #例
   #ohlcv_historical = api.ohlcv_historical_data('BITFINEX_SPOT_BTC_USD', {'period_id': '1MIN', 'time_start': start_of, 'limit': 10000})
   
   ohlcv_historical = api.ohlcv_historical_data('BITSTAMP_SPOT_BTC_USD', {'period_id': '1MIN', 'time_start': start_of, 'limit': 10000})
   print("len: ", len(ohlcv_historical))
   
   #保存
   PATH = "./"
   FILE_NAME = "bitData_"+str(year)+month+day+".csv" #ファイル名

   writeFile(ohlcv_historical, PATH, FILE_NAME)

   print(str(TimeCurrent()), "作業完了")