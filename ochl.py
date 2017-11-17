from datetime import datetime

class OCHL:

    def __init__(self, o, c, h, l, bid, ask, volume, vwap, date=None):
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
        return [self.date.toordinal(), self.open, self.close, self.high, self.low]

    def to_dict(self):
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
