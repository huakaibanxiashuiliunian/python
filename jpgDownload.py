# -*- coding = utf-8 -*-
# @Time :  16:40
# @Author : XX
# @File : jpgDownload.py
# @Software : PyCharm
import json
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
findPagUrl = re.compile(r"<a class='.*' h='.*' style='.*'  href='.*' m='(.*?)' onclick=.* </a>", re.S)
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
        # html = json.load(resp)
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
    jpgList = []
    dataList = []
    for t_list in bs.find_all("a", class_="iusc"):
        item = str(t_list)
        # print(item)
        # PagUrl = re.findall(findPagUrl, item)
        pagUrl = re.findall("m=.*}",item,re.S)
        pagUrl = str(pagUrl)
        pagUrl = re.findall('{.*}',pagUrl)
        pagUrl = str(pagUrl)
        # pagUrl = re.findall(r'"murl":"(.*)"',pagUrl)
        # pagUrl = json.loads(pagUrl)
        # print(pagUrl[0:2])
        # print(pagUrl[len(pagUrl)-2:len(pagUrl)])
        # print(pagUrl[2:len(pagUrl)-2])
        pagUrl = pagUrl[2:len(pagUrl)-2]
        pagUrl = json.loads(pagUrl)
        # print(pagUrl['murl'])
        # print(pagUrl['t'])
        urlLink = pagUrl['murl']
        title  = pagUrl['mid']
        # print(title)
        # title = title.replace(r"","_")  # 字符串替换
        # title = title.replace(r"/","")
        print(title)
        #
        pageName = title+".jpg"
        print(pageName)
        # urllib.request.urlretrieve(urlLink,filename=pageName)   # 下载文件
        print("下载成功！！！")
        # print(pagUrl)
    return dataList


def main():
    url = "https://cn.bing.com/images/search?q=%e5%94%af%e7%be%8e%e5%9b%be%e7%89%87%e5%a5%b3%e7%94%9f&qs=MM&form=QBIR" \
          "&sp=4&pq=%e5%94%af%e7%be%8e%e5%9b%be%e7%89%87&sk=MM3&sc=10-4&cvid=E51555BD1DEF4065AAFE252989B84A58&first=1" \
          "&tsc=ImageHoverTitle "
    url2= "https://cn.bing.com/images/async?q=%e5%94%af%e7%be%8e%e5%9b%be%e7%89%87%e5%a5%b3%e7%94%9f&first=73&count=35&cw=1414&ch=969&relp=70&apc=0&tsc=ImageHoverTitle&datsrc=I&layout=ColumnBased&mmasync=1&dgState=c*7_y*2311s2221s2266s2424s2300s2306s2369_i*71_w*192&IG=B1B06403D90D4217A018556C7334BE0B&SFX=3&iid=images.5531"
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
