import datetime as dt

class StockPrice:
    def __init__(self, time, price):
        if (not isinstance(time, dt.datetime)):
            print("bad date")
            return None
        if (not isinstance(price, float) and not isinstance(price, int)):
            print("bad price")
            return None
        self.time = time
        self.price = float(price)

class Stock:

    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.market = market
        self.prices = dict()

    def addPrice(price):
        if (not isinstance(price, StockPrice)):
            print("Failed to add price")
            return

class Market:
    def __init__(self, symbol
            
sp = StockPrice(dt.datetime.now(), 3)

