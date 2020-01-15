import pandas as pd
import numpy as np 
import datetime
 
# Matplotlibのインポート
import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib import ticker
import matplotlib.dates as mdates

# Talibのインポート
import talib as ta
ta.get_function_groups

def candlechart(data, width=0.8):
    fig, ax = plt.subplots()    
 
    # ローソク足
    mpf.candlestick2_ohlc(ax, opens=data.open.values, closes=data.close.values,
                          lows=data.low.values, highs=data.high.values,
                          width=width, colorup='r', colordown='b')
 
    xdate = data.index
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
 
    def mydate(x, pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''
 

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    ax.format_xdata = mdates.DateFormatter('%H-%m')
 
    fig.autofmt_xdate()
    fig.tight_layout()
 
    return fig, ax

masta = pd.read_csv('./dataOfBitstampOHLC/1hour/bitCoinHisOfBitStamp_2019-05-01OHLC_1hour.csv')
df = masta.copy()

df.index = pd.to_datetime(df.time)
del df['time']

o = np.array(df['open'])
c = np.array(df['close'])
l = np.array(df['low'])
h = np.array(df['high'])

# 4種類のローソク足パターンを抽出
df['Marubozu'] = ta.CDLMARUBOZU(o, h, l, c)
df['Engulfing_Pattern'] = ta.CDLENGULFING(o, h, l, c)
df['Hammer'] = ta.CDLHAMMER(o, h, l, c)
df['Dragonfly_Doji'] = ta.CDLDRAGONFLYDOJI(o, h, l, c)

#print(df[(df['Marubozu'] < 0) | (df['Marubozu'] > 0)].head())


set_time = datetime.datetime.strptime('2019-05-01 00:00', '%Y-%m-%d %H:%M')
before = set_time - datetime.timedelta(hours=0)
after = set_time + datetime.timedelta(days=1)
candlechart(df.loc[(df.index > before )&(df.index < after)])
plt.show()
