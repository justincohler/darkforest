"""
point is a container for the Point class.

Author: Justin Cohler
Created: 11/17/2017
"""

from datetime import datetime

class Point:
    """Point contains point-in-time data for a given base and currency.

    e.g. base: BTC, currency: USD
    """

    def __init__(self, buy, sell):
        """Construct using a buy and sell object from coinbase API."""
        self.buy_price=float(buy["amount"])
        self.sell_price=float(sell["amount"])
        self.base=buy["base"]
        self.currency=buy["currency"]
        self.dt = datetime.now()

    def __repr__(self):
        """Represent as a list of object attributes."""
        return repr([self.buy_price, self.sell_price, self.base, self.currency, self.dt])

    def to_dict(self):
        """Transform object to simple dict."""
        return {
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'base': self.base,
            'currency': self.currency,
            'dt': self.dt,
        }
