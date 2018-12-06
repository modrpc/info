import pandas as pd
import csv
import sys
import decimal

#xl =pd.ExcelFile("../data/QuantKing-2018-11-30.xlsx")
#df = xl.parse('퀀트데이타')


qkdict = dict()

class qkItem:
    def __init__(self, data):
        self.code = data[1]
        self.company = data[2]
        self.sector0 = data[3]
        self.sector1 = data[4]
        self.market = data[5]
        self.price = float(data[6].replace(',',''))
        self.marketcap = float(data[7].replace(',','')) * 10**8

    def print(self):
        print("%s (%s) %.0f %.1f" % (self.code, self.company, self.price, self.marketcap))

    def code(self):
        return self.code

    def name(self):
        return self.name

#data = pd.read_csv("../data/QuantKing-2018-11-30.csv")
reader = csv.reader(open("../data/QuantKing-2018-11-30.csv"))
for line in reader:
    if (line[2] == "" or line[2] == "회사명"):
        continue
    print(line)
    item = qkItem(line)
    qkdict[item.code] = item
    qkdict[item.name] = item
    item.print()
