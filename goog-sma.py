import statistics as stats
import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt

if __name__ == '__main__':
   start_date = '2014-01-01'
   end_date = '2018-01-01'
   SRC_DATA_FILENAME = 'goog_data.pkl'
   try:
      goog_data = pd.read_pickle(SRC_DATA_FILENAME)
      print('File data found...reading GOOG data')
   except FileNotFoundError:
      print('File not found...downloading the GOOG data')
      goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)
      goog_data.to_pickle(SRC_DATA_FILENAME)
   time_period = 20  # number of days over which to average
   history = []  # to track a history of prices
   sma_values = []  # to track simple moving average values
   close = goog_data['Adj Close']
   for close_price in close:
      history.append(close_price)
      if len(history) > time_period:  # we remove oldest price because we only average over last 'time_period' prices
         del (history[0])
      sma_values.append(stats.mean(history))
   goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
   goog_data = goog_data.assign(Simple20DayMovingAverage=pd.Series(sma_values, index=goog_data.index))
   close_price = goog_data['ClosePrice']
   sma = goog_data['Simple20DayMovingAverage']
   import matplotlib.pyplot as plt

   fig = plt.figure()
   ax1 = fig.add_subplot(111, ylabel='Google price in $')
   close_price.plot(ax=ax1, color='g', lw=2., legend=True)
   sma.plot(ax=ax1, color='r', lw=2., legend=True)
   plt.show()