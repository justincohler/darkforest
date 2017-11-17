"""
These utilities represent a service layer for Coinbase interactions.

Author: Justin Cohler
Created: 11/17/2017
"""
from coinbase.wallet.client import Client
from config import Config

def setup_client():
    """Initialize Coinbase client."""
    client = Client(
                Config.get("coinbase_API_KEY"),
                Config.get("coinbase_SECRET"),
                api_version='2017-11-10'
            )
    return client

def buy(account, amount, currency, payment_method):
    """Buy an amount of BTC through a specific currency and payment type."""
    bought = account.buy(amount=amount,
                    currency=currency,
                    payment_method=payment_method.id)

    return bought

def sell(account, amount, currency, payment_method):
    """Sell an amount of BTC through a specific currency and payment type."""
    sold = account.sell(amount=amount,
                      currency=currency,
                      payment_method=payment_method.id)

    return sold
