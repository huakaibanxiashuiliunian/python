# -*- coding = utf-8 -*-
# @Time :  11:31
# @Author : XX
# @File : aatest.py
# @Software : PyCharm
import re
import urllib.request
from urllib import request, error
from urllib import parse
import pymysql
from bs4 import BeautifulSoup
import datetime

from bs4 import BeautifulSoup

time = datetime.datetime.now()
print(time)


# 得到一个指定url的网页
def askURL(url):
    head = {
        "cookie": "QCCSESSID=f80be9492bdf4a20273fa33293; qcc_did=44385d06-39bd-4e65-8393-843cdf3d7ae5; UM_distinctid=1837f41389f53-05c49a2ec82e6a-78565470-144000-1837f4138a06f6; acw_tc=6548ca9716642903114815521e200c6f6606cffdcb272eff226456a3fd; CNZZDATA1254842228=2124133448-1664285801-%7C1664289401",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"
    }
    html = ""
    try:
        req = urllib.request.Request(url, headers=head)
        resp = urllib.request.urlopen(req)
        # html = json.load(resp)
        html = resp.read()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(html, null=None):
    bs = BeautifulSoup(html, "html.parser")
    # print(bs)
    # str = "app-copy-box copy-hover-item copy-part"
    data = bs.select(".maininfo > .app-copy-box.copy-hover-item.copy-part > .copy-title > a")  # 找出详情
    resource = {}
    for item in data:
        name = item.get_text()  # 公司名称
        href = item["href"]  # 公司详情网页
        resource[name] = href
    return resource



def getUrl():
    url = "https://www.qcc.com/web/search?key="
    key = '海康'
    finalUrl = parse.quote(key)
    url = url + finalUrl  # 对关键字进行加密处理使浏览器识别
    print(url)
    html = askURL(url)  # 获取网页信息
    urllist = getData(html)
    if key in urllist:
        print(key)
        print(urllist[key])
    elif key not in urllist:
        for i in urllist:
            print(i)
    print(urllist)
    return urllist



def main():
    getUrl()



if __name__ == '__main__':
    main()
