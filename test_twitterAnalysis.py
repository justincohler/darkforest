"""
Test cases for the CurrencyStreamListener used for sentiment analysis.

Author: Justin Cohler
Created: 11/18/2017
"""
from  darkforest_twitter_utils import create_twitter_api, get_currency_tweets
import time
from datetime import datetime

api = create_twitter_api()
tweets = get_currency_tweets(api)

print(tweets[0])
