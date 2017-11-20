"""
Unit tests for CryptoCompare's API.

Author: Justin Cohler
Created: 11/19/2017
"""
import unittest
from crycompare import History, Price
import darkforest_trade_utils as trade_utils
from datetime import datetime, timedelta
import pandas as pd

class TestCryptoCompare(unittest.TestCase):
    """Unit tests for CryptoCompare's API."""

    def test_histoDay(self):
        """Retrieve BTC and ETH prices from CryptoCompare's API."""
        h = History()

        res_btc = h.histoDay(from_curr="USD", to_curr="BTC", allData=True)
        res_eth = h.histoDay(from_curr="USD", to_curr="ETH", allData=True)

        self.assertIsNotNone(res_btc, res_eth)

    def test_get_historic_coin_data(self):
        """
        Retrieve BTC and ETH prices from CryptoCompare API.

        Return a DataFrame with all columns.
        """
        df = trade_utils.get_historic_coin_data("USD", ["BTC", "ETH"])

        self.assertIsNotNone(df)
        print(df.head(5))

if __name__ == '__main__':
    unittest.main()
