import csv
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

class Symbol:
    def __init__(self, name, company, market, sector):
        self.name = name
        self.company = company
        self.market = market
        self.sector = sector
        self.prices = dict()

    def add_price(self, price):
        if (not isinstance(price, StockPrice)):
            print("Failed to add price")
            return

    def get_name(self):
        return self.name

    def print(self):
        print("%s (%s) %s" % (self.name, self.company, self.sector))

class Market:
    def __init__(self, name, csvfile):
        self.name = name
        self.symbols = dict()
        reader = csv.reader(open(csvfile))
        for line in reader:
            if (line[0] == "Symbol"):
                continue
            symbol = Symbol(line[0], line[1], self.name, line[5])
            if (symbol.sector != "n/a"):
                self.symbols[symbol.get_name()] = symbol
                symbol.print()

