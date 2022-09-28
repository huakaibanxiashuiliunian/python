# -*- coding = utf-8 -*-
# @Time :  14:03
# @Author : XX
# @File : spider.py
# @Software : PyCharm
import re
import urllib.request
from urllib import request, error,parse

import pymysql
from bs4 import BeautifulSoup  #
# 数据库配置
host = "localhost"
user = "root"
password = '123456'
port = 3306
database = "test"
# 提取规则
findPagUrl = re.compile(r'<img alt="(.*?)" class="" rel="nofollow" src=".*"/>', re.S)
findName = re.compile(r'<a class="" href=".*">(.*)</a>', re.S)
findLink = re.compile(r'<a class="" href="(.*)" onclick=".*</a>', re.S)


# 得到一个指定url的网页
def askURL(url):
    head = {
        "cookie": "qcc_did = 6239 ac14 - b935 - 4bb2 - 8828 - c3f7ce40fdb9; UM_distinctid = 183699a18c0503 - 023e8f01203072 - 78565473 - 1fa400 - 183699a18c1d04; QCCSESSID = e449d1eb14d668804693a209a3; acw_tc = 7c0e139516641690362418572e3e9d7b7112cdd1d833c1bda1631a2663; CNZZDATA1254842228 = 1778944365 - 1663920800 - https % 253A % 252F % 252Fcn.bing.com % 252 F % 7C1664169218",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"
    }
    html = ""
    try:
        req = urllib.request.Request(url, headers=head)
        resp = urllib.request.urlopen(req)
        html = resp.read().decode("utf-8")
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
    name = re.compile(r'<a class=".*">(.*?)</span></a>')
    data = bs.select(".maininfo > .app-copy-box.copy-hover-item.copy-part > .copy-title > a")
    resource = {}
    dataList = []
    for item in data:
        # print(item.get_text())
        name = item.get_text()
        # print(item["href"])
        href = item["href"]
        resource = {name:href}
        dataList.append(resource)
    return dataList


def saveData(dataList):
    init_db()
    conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database)
    cur = conn.cursor()
    sql = '''
          
      '''



def main():

    url = "https://www.qcc.com"
    key = "深圳市腾讯计算机系统有限公司"  # 要搜索的关键字
    key = parse.quote(key)
    url = url+"/web/search?key="+key
    # url = "https://www.qcc.com/web/search?key=%E5%8C%97%E4%BA%AC%E6%99%BA%E6%B1%87%E5%8D%9A%E9%80%9A%E7%A7%91%E6%8A%80%E5%8F%91%E5%B1%95%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"
    print(url)        # 打印加密后的网址
    html = askURL(url)
    data = getData(html)
    print(data)
    # saveData(data)


def init_db():
    conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database)
    cur = conn.cursor()
    sql = '''
        CREATE TABLE `movie` (
            `link` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
            `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
            `jpglink` varchar(255) CHARACTER SET utf8 DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    '''
    sql2 = '''
        CREATE TABLE `company` (
            `name` varchar(255) CHARACTER SET utf8 NOT NULL,
            `link` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
            PRIMARY KEY (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    '''
    cur.execute(sql2)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
    # init_db()
