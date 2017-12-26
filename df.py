"""
Dark Forest is an automated tracker and trader of electronic currencies.

Author: Justin Cohler
Created: 11/17/2017
"""
import signal, sys, os
from datetime import datetime, date, time, timedelta
import time
import requests, json
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import AutoDateFormatter, AutoDateLocator
import gdax
from darkforest_trade_utils import setup_clients, get_gdax_history
from point import *
from ochl import *
from config import Config

ETH = "ETH"
BTC = "BTC"
USD = "USD"
PERIOD_DAYS = 20

if __name__ == "__main__":
    gdax_pub, gdax_auth = setup_clients()

    df_historic = get_gdax_history(gdax_pub, USD, [BTC, ETH])
    print(df_historic)

    df_historic.set_index('time')
    df_historic['time'] = pd.to_datetime(df_historic['time'], unit='s')
    print(df_historic)

    btc_historic = df_historic.where(df_historic['coin'] == 'BTC')
    btc_historic.sort_values(by='time', ascending=True)

    roll = btc_historic['close'].rolling(window=PERIOD_DAYS, min_periods=1)
    btc_historic['rolling_mean'] = roll.mean()
    btc_historic['rolling_std'] = roll.std()
    btc_historic['band_upper'] = btc_historic['rolling_mean'] + btc_historic['rolling_std']
    btc_historic['band_lower'] = btc_historic['rolling_mean'] - btc_historic['rolling_std']

    fig, ax = plt.subplots()

    xtick_locator = AutoDateLocator()
    xtick_formatter = AutoDateFormatter(xtick_locator)
    ax.xaxis.set_major_locator(xtick_locator)
    ax.xaxis.set_major_formatter(xtick_formatter)

    #btc_historic.loc[:,['time','close', 'rolling_mean', 'band_upper', 'band_lower']].plot(ax=ax, x='time')

    ax.plot(btc_historic['time'], btc_historic['close'])
    plt.show()
