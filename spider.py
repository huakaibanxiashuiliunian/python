# -*- coding = utf-8 -*-
# @Time :  14:03
# @Author : XX
# @File : spider.py
# @Software : PyCharm
import re
import urllib.request
from urllib import request, error

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
    print(bs)
    jpgList = []
    dataList = []
    # for t_list in bs.find_all("a", class_=""):
    #     item = str(t_list)
    #     # print(item)
    #     PagUrl = re.findall(findPagUrl, item)
    # for t_list in bs.find_all("a", class_=""):

        # print(PagUrl)
        # if None != PagUrl:
        #     jpgList.append(PagUrl)
    # for t_list in bs.find_all("li", class_="title"):
    #     item = str(t_list)
    #     # print(item)
    #     name = re.findall(findName, item)
    #     link = re.findall(findLink, item)
    #     dataList.append(name)
    #     dataList.append(link)
    # print(jpgList)
    # print(dataList)
    return dataList


def main():
    url = "https://movie.douban.com/"
    html = askURL(url)
    getData(html)
    # bs =  BeautifulSoup(html, "html.parser")
    # print(html)


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
    cur.execute(sql)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
