""" DART financial statment fetcher. """

import requests
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd

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
        print("wget: ", url)
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
            self.wget(url_template % rdate, self.savedir + filename)
            fsize = os.path.getsize(self.savedir + filename)/(1024**2)
            print("%s (%.2f MB) downloaded" % (filename, fsize))
    



f = Fetcher("/tmp/")
f.get(0, 0, 0, 0)

fname = "/tmp/DART-20170405.html"

with open(fname, encoding="utf-8") as f:
    text = f.read()
    soup = BeautifulSoup(text, "lxml")

sel_list = soup.select('div p b')
count_str = sel_list[0].text
count_str = "".join(count_str.split())
print(count_str)
table = soup.find('table')
trs = table.findAll('tr')
print ("총 건수:", len(trs))
for tr in trs[1:6]:
    tds = tr.findAll('td')
    print(tds[0].text.strip(), end=" " )          # 시간
    print(tds[1].text.strip(), end=" " )          # 공시대상회사
    print(tds[1].img['alt'])                      # 이미지 태그 (유가증권, 코스닥, 코넥스 등)
    print(" ".join(tds[2].text.split()) )
    print('http://dart.fss.or.kr/' + tds[2].a['href'] )   # 링크
    print(tds[3].text.strip(), end=" ")                   # 제출인
    print(tds[4].text.strip().replace('.', '-') )         # 접수일자
    print()

table = soup.find('table')
trs = table.findAll('tr')     # <tr> </tr> : 1개의 공시.
counts = len(trs)
print(counts)

tr = trs[1]
print(tr)

# 각 컬럼별 데이터 추출
tds = tr.findAll('td')

link = 'http://dart.fss.or.kr' + tds[2].a['href']
doc_id = link.split('main.do?rcpNo=')[1]

time = tds[0].text.strip()
date = tds[4].text.strip().replace('.', '-') + ' ' + time

corp_name = tds[1].text.strip()
market = tds[1].img['alt']

title = " ".join(tds[2].text.split())

reporter = tds[3].text.strip()

dart_dict = {'doc_id':[doc_id],'date':[date],'corp_name':[corp_name],
'market':[market],'title':[title],'link':[link],'reporter':[reporter]}
df = pd.DataFrame(dart_dict)
print(df)

# 전체 데이터를 DataFrame으로 만들기
if counts > 0:
    link_list = []
    docid_list = []
    date_list = []
    corp_list = []
    market_list = []
    title_list = []
    reporter_list = []
    
    for tr in trs[1:]:
        tds = tr.findAll('td')
        link = 'http://dart.fss.or.kr' + tds[2].a['href']
        doc_id = link.split('main.do?rcpNo=')[1]
        time = tds[0].text.strip()
        date = tds[4].text.strip().replace('.', '-') + ' ' + time
        corp_name = tds[1].text.strip()
        market = tds[1].img['alt']
        title = " ".join(tds[2].text.split())
        reporter = tds[3].text.strip()
        
        link_list.append(link)
        docid_list.append(doc_id)
        date_list.append(date)
        corp_list.append(corp_name)
        market_list.append(market)
        title_list.append(title)
        reporter_list.append(reporter)
        
    dart_dict = {'doc_id':docid_list,'date':date_list,'corp_name':corp_list,'market':market_list,'title':title_list,
                 'link':link_list,'reporter':reporter_list}
    df_dart = pd.DataFrame(dart_dict)    

print(df_dart.head())


