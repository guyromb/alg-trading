from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_date = '2018-01-01'
    end_date = '2020-01-01'
    pd.set_option('display.width', 1000)
    goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)

    goog_data_signal = pd.DataFrame(index=goog_data.index)
    goog_data_signal['price'] = goog_data['Adj Close']
    goog_data_signal['daily_difference'] = goog_data_signal['price'].diff()
    # print(goog_data_signal.head())

    goog_data_signal['signal'] = 0.0
    goog_data_signal['signal'] = np.where(goog_data_signal['daily_difference'] > 0, 1.0, 0.0)
    goog_data_signal['positions'] = goog_data_signal['signal'].diff()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Google price in $')
    goog_data_signal['price'].plot(ax=ax1, color='r', lw=2.)
    ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,
             goog_data_signal.price[goog_data_signal.positions == 1.0], '^', markersize=5, color='m')
    ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
             goog_data_signal.price[goog_data_signal.positions == -1.0],
             'v', markersize=5, color='k')
    # plt.show()

    ## backtesting
    initial_capital = float(1000.0)
    positions = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
    portfolio = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
    positions['GOOG'] = goog_data_signal['signal']
    portfolio['positions'] = (positions.multiply(goog_data_signal['price'], axis=0))
    portfolio['cash'] = initial_capital - (positions.diff().multiply(goog_data_signal['price'], axis=0)).cumsum()
    portfolio['total'] = portfolio['positions'] + portfolio['cash']
    print(portfolio['total'])


