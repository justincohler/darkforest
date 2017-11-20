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

analyzer = SentimentIntensityAnalyzer()

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

def calculate_sentiment(self, text):
    """Take a list of words and return a sentimental score."""
    return self.analyzer.polarity_scores(text)

def make_sentiment(tweet):
    return {"dt": tweet.created_at, "tweet": tweet.text, "sentiment": analyzer.polarity_scores(tweet.text)}

def get_currency_tweets(api):
    """
    Return tweets since since_days regarding various cryptocurrencies.

    since_days defaults to 7 days if not otherwise specified.
    """
    query = "bitcoin OR ethereum OR cryptocurrency"

    tweets = pd.DataFrame()
    for block in tweepy.Cursor(api.search,q=query, count=100).pages():
        formatted = list(map(make_sentiment, block))
        tweets.append(formatted)
        print(formatted[-1])
    return tweets
