"""
ochl is a container for the OCHL class.

Author: Justin Cohler
Created: 11/17/2017
"""
from datetime import datetime

class OCHL:
    """OCHL contains point-in-time data for an OCHL (open, high, low, close)."""

    def __init__(self, o, c, h, l, bid, ask, volume, vwap, date=None):
        """Construct using several data from Quandl API."""
        self.date = date if date else datetime.now().date
        self.open = o
        self.close = c
        self.high = h
        self.low = l
        self.bid = bid
        self.ask = ask
        self.volume = volume
        self.vwap = vwap

    def formatted(self):
        """Return a formatted version, compliant with Matplotlib."""
        return [self.date.toordinal(), self.open, self.close, self.high, self.low]

    def to_dict(self):
        """Transform object to simple dict."""
        return {
            'date': self.date,
            'open': self.open,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'bid': self.bid,
            'ask': self.ask,
            'volume': self.volume,
            'vwap': self.vwap,
        }
