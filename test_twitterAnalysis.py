"""
Test cases for the Twitter listener used for sentiment analysis.

Author: Justin Cohler
Created: 11/18/2017
"""
import unittest
from  darkforest_twitter_utils import create_twitter_api, get_currency_tweets
import time
import darkforest_trade_utils as trade_utils
from datetime import datetime, timedelta
import pandas as pd

class TestTwitterSentiments(unittest.TestCase):
    """Unit tests for CryptoCompare's API."""
api = create_twitter_api()
tweets = get_currency_tweets(api)

print(tweets[0])
