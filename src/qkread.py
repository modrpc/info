import pandas as pd
import csv
import sys

#xl =pd.ExcelFile("../data/QuantKing-2018-11-30.xlsx")
#df = xl.parse('퀀트데이타')


qkdict = dict()

class qkItem:
    def __init__(self, data):
        self.code = data[1]
        self.company = data[2]
        self.sector0 = data[3]
        self.sector1 = data[4]

    def print(self):
        print("%s (%s)" % (self.code, self.company))

    def code(self):
        return self.code

    def name(self):
        return self.name

data = pd.read_csv("../data/QuantKing-2018-11-30.csv")
print(data)

reader = csv.reader(open("../data/QuantKing-2018-11-30.csv"))
for line in reader:
    item = qkItem(line)
    qkdict[item.code] = item
    qkdict[item.name] = item
    item.print()
