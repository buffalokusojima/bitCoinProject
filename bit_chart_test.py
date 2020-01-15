import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas_datareader import data as dr
import datetime as dt
from mpl_finance import candlestick2_ohlc
import datetime

from pylab import rcParams

rcParams['figure.figsize'] = 20,10

df = pd.read_csv('./dataOfBitstampOHLC/1hour/bitCoinHisOfBitStamp_2019-05-01OHLC_1hour.csv',index_col='time', parse_dates=['time'])

fig, ax = plt.subplots()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
ax.grid(True)

plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Price")
plt.title("BTC-USD")

candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup="b", colordown="r")

plt.show()
