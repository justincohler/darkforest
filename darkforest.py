"""
Dark Forest is an automated tracker and trader of electronic currencies.

Author: Justin Cohler
Copyright: 2017
"""
from datetime import datetime, date, time, timedelta
import time
import requests, json
import signal, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from coinbase.wallet.client import Client
from darkforest_trade_utils import setup_client
from matplotlib.finance import candlestick_ohlc
from point import *
from ochl import *
from config import Config

def exit_handler(signum, frame):
    """Close all threads running in background due to wait calls in the trader."""
    print("Interrupted by %d, shutting down" % signum)
    sys.exit()

signal.signal(signal.SIGINT, exit_handler)

xs = []
ybuys = []
ysells = []
ykelt_up = []
ykelt_dn = []

df = pd.DataFrame()
btc_api_base="https://www.quandl.com/api/v3/datasets/BITSTAMP/USD.json?api_key="+Config.get("quandl_API_KEY")

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


def update_candlestick_plot(ochls):
    """Plot given ochls on a candlestick plot on the global ax plot."""
    candlestick_ohlc(ax, ochls, colorup='g', colordown='r', width=0.6)

    ax.xaxis_date()
    ax.autoscale_view(True, True, True)

def update_multiline_plot(point):
    """Plot given points on a line plot on the global ax plot."""
    xs.append(point.dt)
    ybuys.append(point.buy_price)
    ysells.append(point.sell_price)

    ax.plot(xs, ybuys, 'c')
    ax.plot(xs, ysells, 'm')

    ax.xaxis_date()
    ax.autoscale_view(True, True, True)

def get_historic_btc_data(start_date, end_date):
    """
    Return a list of ochl.OCHL objects.

    Given a start and end date, query a Quandl API for BTC ochl data within
    the given timeframe.
    """
    response = requests.get(btc_api_base+"&start_date="+start_date.strftime("%Y-%m-%d")+"&end_date"+end_date.strftime("%Y-%m-%d"))
    data = json.loads(response.text)['dataset']['data']

    ochls = []
    for i in range(1, len(data)):
        datum = data[i]
        dt = datetime.strptime(datum[0], '%Y-%m-%d')
        ochl = OCHL(date=dt, o=data[i-1][3], c=datum[3], h=datum[1], l=datum[2], bid=datum[4], ask=datum[5], volume=datum[6], vwap=datum[7])
        ochls.append(ochl)

    return ochls

def populate(ochls):
    """Populate plot axes with given ochl data."""
    for ochl in ochls:
        xs.append(ochl.date)
        ybuys.append(ochl.high)
        ysells.append(ochl.low)



if __name__ == "__main__":
    today = datetime.now()
    td = timedelta(days=31)
    last_period = today - td
    ochls = get_historic_btc_data(last_period, today)
    ochls.sort(key=lambda ochl: ochl.date, reverse=False)
    populate(ochls)


    fig, ax = setup_plot()
    client = setup_client()
    account = client.get_primary_account()
    payment_methods = client.get_payment_methods()
    payment_method = payment_methods[0]

    for i in range(1000):
        buy = client.get_buy_price(currency='USD', base='BTC')
        sell = client.get_sell_price(currency='USD', base='BTC')

        p = Point(buy, sell)

        # Create time series index for all points
        datum = pd.DataFrame(p.to_dict(), index=['dt'])
        df = df.append(datum)

        update_multiline_plot(p)

        time.sleep(1)
        plt.pause(1)
