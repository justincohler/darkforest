"""
A set of utilities for twitter sentiment analysis.

Author: Justin Cohler
Created: 11/17/2017

"""
import tweepy
import pandas as pd
from nltk import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import Config
from datetime import datetime, timedelta

class CurrencyStreamListener(tweepy.StreamListener):
    """Implement StreamListener to capture Currency-related tweets."""

    def __init__(self):
        """Overwrite init method to create btc and eth sentiment dataframes."""
        super(CurrencyStreamListener, self).__init__()
        self.df_btc=pd.DataFrame()
        self.df_eth=pd.DataFrame()

    def on_status(self, status):
        """Overwrite on_status method to analyze tweet sentiments."""
        words = status.text.split()
        sentiment = get_sentiment(words)
        dt = datetime.now()
        if "bitcoin" in status.lower():
            btc = {"sentiment": sentiment, "dt": dt}
            self.df_btc.append(pd.DataFrame(btc, index=["dt"]))

        if "ethereum" in status.lower():
            etc = {"sentiment": sentiment, "dt": dt}
            self.df_eth.append(pd.DataFrame(eth, index=["dt"]))

    def get_daily_sentiments(d):
        """Return the sentiment for a given date."""
        s_btc = self.df_btc[(self.df_btc['dt'] > d) & (self.df_btc['dt'] < d + timedelta(days=1)].groupby(df.index.date).mean()
        s_eth = self.df_eth[(self.df_btc['dt'] > d) & (self.df_btc['dt'] < d + timedelta(days=1)].groupby(df.index.date).mean()

        return s_btc, s_eth

def create_twitter_api():
    """Create a twitter api client wrapper."""
    ACCESS_TOKEN = Config.get("twitter_ACCESS_TOKEN")
    ACCESS_SECRET = Config.get("twitter_ACCESS_SECRET")
    CONSUMER_KEY = Config.get("twitter_CONSUMER_KEY")
    CONSUMER_SECRET = Config.get("twitter_CONSUMER_SECRET")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

def create_twitter_stream():
    """Return a Twitter stream to constantly analyze sentiments for various electronic currencies."""
    api = create_twitter_api()
    streamListener = CurrencyStreamListener()
    twitterStream = tweepy.Stream(auth = api.auth, listener=streamListener())

def create_currency_stream():
    """Stream tweets related to Bitcoin and Ethereum for analysis."""
    twitterStream = create_twitter_stream()
    twitterStream.filter(track=['bitcoin','ethereum'], async=True)

    return twitterStream

def calculate_sentiment(words):
    """Take a list of words and return a sentimental score."""
    analyzer = SentimentIntensityAnalyzer()
    total_compound = 0

    for w in words:
        score = analyzer.polarity_scores(w)
        total_compound += score['compound']

    return total_compound
