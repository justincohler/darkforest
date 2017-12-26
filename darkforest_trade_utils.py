"""
These utilities represent a service layer for Coinbase interactions.

Author: Justin Cohler
Created: 11/17/2017
"""
from config import Config
from crycompare import History, Price
from datetime import datetime
import gdax
import pandas as pd
import numpy as np

def setup_clients():
    """Initialize Coinbase client."""
    auth_client = gdax.AuthenticatedClient(Config.get("gdax_API_KEY")
                                            , Config.get("gdax_SECRET")
                                            , Config.get("gdax_PASSPHRASE"))


    public_client = gdax.PublicClient()
    return public_client, auth_client

def buy(client, bid_price, bid_size, currency_pair):
    """Buy an amount (size) of cryptocurrency for a given bid price."""
    bought = client.buy(price=bid_price,
               size=bid_size,
               product_id=currency_pair) #e.g. BTC-USD

    return bought

def sell(client, ask_price, ask_size, currency_pair):
    """Sell an amount (size) of cryptocurrency for a given ask price."""
    sold = client.buy(price=ask_price,
               size=ask_size,
               product_id=currency_pair) #e.g. BTC-USD

    return sold

def get_gdax_history(client, curr, coins):
    """Return historic data for the given coins and currency."""
    coin_history = []
    df_history = pd.DataFrame()
    for coin in coins:
        res = client.get_product_historic_rates(coin+"-"+curr)

        df = pd.DataFrame(res, columns=('time', 'low', 'high', 'open', 'close', 'volume'))
        df['coin'] = coin
        df_history = df_history.append(df)

    return df_history

def get_historic_coin_data(curr, coins):
    """Return n days of historic data for the given coins and currency."""
    h = History()
    historic_data = []
    for coin in coins:
        res =  h.histoDay(from_curr=curr, to_curr=coin, allData=True)

        if res['Response'].lower() != "success":
            raise(AssertionError)

        res = [dict(item, coin=coin) for item in res['Data']]

        historic_data.extend(res)

    return historic_data

def atr(df, window):

    i = 0

    while i < df.index[-1]:
        tr = max(df.get_value(i+1, ''))
    return df
