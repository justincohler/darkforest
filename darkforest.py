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

def exit_handler(signum, frame):
    """Close all threads running in background due to wait calls in the trader."""
    print("Interrupted by %d, shutting down" % signum)
    sys.exit()

signal.signal(signal.SIGINT, exit_handler)

xs = []
df = pd.DataFrame()

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

def update_multiline_plot(df_historic, df_rt):
    """Plot given points on a line plot on the global ax plot."""
    '''TODO - make plot with updated parameters.'''
    xs.append(point.dt)
    ybuys.append(point.buy_price)
    ysells.append(point.sell_price)

    ax.plot(xs, ybuys, 'c')
    ax.plot(xs, ysells, 'm')

    ax.xaxis_date()
    ax.autoscale_view(True, True, True)

if __name__ == "__main__":
    df_historic = get_historic_coin_data("USD", ["BTC", "ETH"])
    today = datetime.now()
    td = timedelta(days=31)
    last_period = today - td

    btc_ticker = pd.DataFrame()
    eth_ticker = pd.DataFrame()

    gdax_pub, gdax_auth = setup_clients()

    fig, ax = setup_plot()

    while True:
        btc_tick = gdax_pub.get_product_ticker(product_id='BTC-USD')
        btc_tick['coin'] = 'BTC'
        btc_tick['time'] = pd.to_datetime(btc_tick['time'])

        eth_tick = gdax_pub.get_product_ticker(product_id='ETH-USD')
        eth_tick['coin'] = 'ETH'
        eth_tick['time'] = pd.to_datetime(eth_tick['time'])

        # Create time series index for all points
        df_btc = pd.DataFrame(btc_tick, index=['time'])
        df_eth = pd.DataFrame(eth_tick, index=['time'])

        btc_ticker = btc_ticker.append(df_btc)
        eth_ticker = eth_ticker.append(df_eth)

        print(eth_ticker)
        print(btc_ticker)
        #update_multiline_plot(df_historic, df_rt)

        time.sleep(1)
        plt.pause(1)
