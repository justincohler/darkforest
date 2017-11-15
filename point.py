from datetime import datetime

class Point:

    def __init__(self, buy, sell):
        self.buy_price=float(buy["amount"])
        self.sell_price=float(sell["amount"])
        self.base=buy["base"]
        self.currency=buy["currency"]
        self.dt = datetime.now()

    def __repr__(self):
        return repr([self.buy_price, self.sell_price, self.base, self.currency, self.dt])

    def to_dict(self):
        return {
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'base': self.base,
            'currency': self.currency,
            'dt': self.dt,
        }
