"""
Dark Forest is an automated tracker and trader of electronic currencies.

Author: Justin Cohler
Created: 11/17/2017
"""
import signal, sys
from datetime import datetime, date, time, timedelta
import time
import requests, json
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
import gdax
from darkforest_trade_utils import setup_clients, get_historic_coin_data
from point import *
from ochl import *
from config import Config

ETH = "ETH"
BTC = "BTC"
USD = "USD"
PERIOD = 20

def exit_handler(signum, frame):
    """Close all threads running in background due to wait calls in the trader."""
    print("Interrupted by %d, shutting down" % signum)
    sys.exit()

signal.signal(signal.SIGINT, exit_handler)

def setup_plot():
    """Return a figure and a plot, ax for BTC data over time."""
    style.use('fivethirtyeight')
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%b %d')

    plt.ion()
    fig  = plt.figure()
    plt.xlabel("Time")
    plt.ylabel("BTC Price ($)")
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)

    fig.canvas.draw()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.show(block=False)

    return fig, ax

def update_plot(historic_dfs, rt_dfs):
    """Plot given points on a line plot on the global ax plot."""
    '''TODO - make plot with updated parameters.'''
    for df in historic_dfs:
        df.set_index('time')
        print(df.tail)
        df.plot(x='time', y='close')

    for df in rt_dfs:
        df.set_index('time')
        df.plot(x='time', y='ask')

    plt.show()


if __name__ == "__main__":
    gdax_pub, gdax_auth = setup_clients()
    #fig, ax = setup_plot()
    historic = get_historic_coin_data(gdax_pub, USD, [BTC, ETH])
    #historic['time'] = pd.to_datetime(historic['time'])
    for doc in historic:
        for k, v in doc.items():
            if k not in ['coin', 'time']:
                doc[k] = float(v)
            else:
                doc[k] = v

    btc_rt = pd.DataFrame()
    df_historic = pd.DataFrame.from_dict(historic)

    btc_historic = df_historic[df_historic['coin'] == BTC]
    print(btc_historic.tail)
    btc_historic['rolling_mean'] = btc_historic.set_index('time').rolling(PERIOD).mean()
    btc_historic['rolling_std'] = btc_historic.set_index('time').rolling(PERIOD).std()
    btc_historic['upper'] = btc_historic['rolling_mean'] + btc_historic['rolling_std']
    btc_historic['lower'] = btc_historic['rolling_mean'] - btc_historic['rolling_std']

    print(btc_historic.tail)
    plt.plot(xs, ys)
    plt.show()

    while True:
        btc_tick = gdax_pub.get_product_ticker(product_id='BTC-USD')
        btc_tick['coin'] = BTC
        btc_tick['time'] = pd.to_datetime(btc_tick['time'])

        # Create time series index for all points
        df_btc = pd.DataFrame(btc_tick, index=['time'])

        btc_rt = btc_rt.append(df_btc)

        # FIXME
        btc_historic.set_index('time')
        print(btc_historic.dtypes)



        time.sleep(1)
        #plt.pause(1)
