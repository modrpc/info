""" DART financial statment fetcher. """

import requests
import os
from datetime import datetime, timedelta

url_template = 'http://dart.fss.or.kr/dsac001/search.ax?selectDate=%s'
headers = {'Cookie':'DSAC001_MAXRESULTS=5000;'}

class Fetcher:
    def __init__(self, savedir):
        self.savedir = savedir
        self.url_base = "http://dart.fss.or.kr/dsab002/search.ax?"
        self.field_dividend = "reportName"   # 검색보고서명
        self.field_startdate = "startDate"   # 시작기간 20180101
        self.field_enddate = "endDate"       # 종료기간 20180630
        self.field_company = "textCrpNm"     # 회사명
        self.field_maxresult = "maxResult"   # 최대 검색 결과

    def url_build(self, key, startdate, enddate, maxresult):
        url = self.url_base + "reportName=" + key + "&&"
        url = url + field_startdate + "=" + startdate + "&&"
        url = url + field_enddate + "=" + enddate + "&&"
        url = url + field_maxresult + "=" + maxresult

    def wget(self, url, local_filename):
        r = requests.get(url, headers=headers, stream=True)
        f = open(local_filename, "wb")
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    def get(self, key, startdate, enddate, maxresult):
        #url = self.url_build(key, startdate, enddate, maxresult)

        start = datetime(2017, 4, 1)
        end = datetime(2017, 4, 5)
        delta = end - start
        for i in range(delta.days+1):
            d = start + timedelta(days=i)
            rdate = d.strftime("%Y%m%d")
            filename = "DART-" + rdate + ".html"
            self.wge(turl_template % rdate, self.savedir + filename)
            fsize = os.path.getsize(self.savedir + filename)/(1024**2)
            print("%s (%.2f MB) downloaded" % (filename, fsize))
    



f = Fetcher("/tmp/")
f.get(0, 0, 0, 0)
