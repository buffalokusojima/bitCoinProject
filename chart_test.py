import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpf
from mpl_finance import candlestick_ohlc, volume_overlay
from matplotlib.dates import date2num

import datetime

import pandas as pd

from util import util


df = pd.read_csv('./dataOfBitstampOHLC/5minutes/bitCoinHisOfBitStamp_2019-09-29OHLC_5minutes.csv',index_col='time', parse_dates=['time'])

fromTime = datetime.datetime(2019, 9, 29, 0)
endTime = datetime.datetime(2019, 9, 30, 0)

df = df[df.index > fromTime]
df = df[df.index < endTime]

df.index = mdates.date2num(df.index)
data = df.reset_index().values

fig = plt.figure(figsize=(12,4))

ax = fig.add_subplot(1,1,1)

candlestick_ohlc(ax, data, width = 0.0005, colorup='r', colordown='b')

#candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup="b", colordown="r")

#ax.set_xticklabels([(df.index[int(x)] if x < df.shape[0] else x) for x in ax.get_xticks()], rotation=30)

ax.grid()

ax.plot(df.index, df['close'].rolling(5).mean())
ax.plot(df.index, df['close'].rolling(20).mean())
#ax.plot(df.index, df['close'].rolling(26).mean())

locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

plt.show()
#plt.savefig("test.png")

plt.close()