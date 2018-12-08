import pandas as pd
import csv
import sys
import decimal

qkdict_name = dict()
qkdict_code = dict()


def get_num(data):
    return float(data.replace(',',''))
                 
def get_delta(delta):
    print(delta)
    if (delta[1] == "▼"):
        return float(get_num(delta[2:])) * -1
    elif (delta[1] == "▲"):
        return float(get_num(delta[2:]))
    else:
        return get_num(delta)

class qkItem:
    def __init__(self, data):
        self.code = data[1]                             # 코드번호
        self.company = data[2]                          # 회사명
        self.sector0 = data[3]                          # 업종 (대)
        self.sector1 = data[4]                          # 업종 (소)
        self.market = data[5]                           # 코스피/코스닥
        self.price = get_num(data[6])                   # 주가 (원)
        if (self.price == 0):
            return

        self.marketcap = get_num(data[7]) * 10**8       # 시가총액 (원)
        self.nstocks = get_num(data[8]) * 10**5         # 상장주식수
        self.ntreasury = get_num(data[9]) * 10**5       # 자사주
        self.ptreasury = get_num(data[10])              # 자사주비중 (%)

        self.delta_1day = get_delta(data[12])           # 1일 등락률 (%)
        self.delta_5day = get_delta(data[13])           # 15일 등락률 (%)
        self.delta_1mo = get_delta(data[14])            # 1개월 등락률 (%)
        self.delta_3mo = get_delta(data[15])            # 3개월 등락률 (%)
        self.delta_6mo = get_delta(data[16])            # 6개월 등락률 (%)
        self.delta_9mo = get_delta(data[17])            # 9개월 등락률 (%)
        self.delta_1yr = get_delta(data[18])            # 1년 등락률 (%)
        self.delta_3yr = get_delta(data[19])            # 3년 등락률 (%)
        self.gpa = get_num(data[20])                    # 과거 GP/A
        self.gpm = get_num(data[21])                    # 과거 GPM
        self.opm = get_num(data[22])                    # 발표 OPM
        self.opm_this = get_num(data[23])               # 올해 OPM
        self.roe = get_num(data[24])                    # 과거 ROE
        self.roa = get_num(data[25])                    # 과거 ROA
        self.pcr = get_num(data[26])                    # 과거 PCR
        

    def print(self):
        print("%s (%s) %.0f(원) %.1f(억)" % (self.code, self.company,
                                          self.price, self.marketcap/10**8))
        print("  * 등락률: %.1f(5day), %.1f(1mo), %.1f(3mo), %.1f(6mo), %1.f(9mo), %1.f(1yr), %1.f(3yr)" % (self.delta_5day, self.delta_1mo, self.delta_3mo, self.delta_6mo, self.delta_9mo, self.delta_1yr, self.delta_3yr))

    def code(self):
        return self.code

    def name(self):
        return self.name

    def price(self):
        return self.price

    def nstocks(self):
        return self.stocks

    def ntreasury(self):
        return self.ntreasury

    def ptreasury(self):
        return self.ptreasury

    def isValid(self):
        if (self.price == 0):
            return False
        return True

reader = csv.reader(open("../data/QuantKing-2018-11-30.csv"))
for line in reader:
    if (line[2] == "" or line[2] == "회사명"):
        continue
    item = qkItem(line)
    if (not item.isValid()):
        continue
    qkdict_code[item.code] = item
    qkdict_name[item.name] = item
    item.print()


for name, item in qkdict_name.items():
    if (item.delta_1mo > 0.0 and item.delta_3mo > 0.0 and item.delta_6mo > 0.0 and
        item.delta_1yr > 0.0 and item.delta_3yr >0.0):
        item.print()
