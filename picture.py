# -*- coding = utf-8 -*-
# @Time :  16:40
# @Author : XX
# @File : jpgDownload.py
# @Software : PyCharm
import json
import re
import urllib.request
from urllib import request, error
from urllib import parse
import pymysql
from bs4 import BeautifulSoup
import datetime

# 数据库配置
host = "192.168.1.252"
user = "root"
password = 'tekinfo119TOPower'
port = 3306
database = "ipower_carrier"
# 提取规则
findPagUrl = re.compile(r"<a class='.*' h='.*' style='.*'  href='.*' m='(.*?)' onclick=.* </a>", re.S)
findName = re.compile(r'<td class="tb" width="13%">(.*?)<i aria-label.* </i></td>', re.S)
findLink = re.compile(r'<a class="" href="(.*)" onclick=".*</a>', re.S)


# 得到一个指定url的网页
def askURL(url):
    head = {
        "cookie": "qcc_did=6239ac14-b935-4bb2-8828-c3f7ce40fdb9; UM_distinctid=183782db56b276-024f85f7b83c-6b3e555b-1fa400-183782db56cc26; QCCSESSID=54639d03a40bcda5f1bbd2e1ff; acw_tc=d3a2ab1816643473185105729ece31edf71afa72200bc464580add63c5; CNZZDATA1254842228=1778944365-1663920800-https%253A%252F%252Fcn.bing.com%252F%7C1664345625",
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


# def getData(html, null=None):
#     bs = BeautifulSoup(html, "html.parser")
#     # print(bs)
#     # str = "app-copy-box copy-hover-item copy-part"
#     data = bs.select(".maininfo > .app-copy-box.copy-hover-item.copy-part > .copy-title > a")  # 找出详情
#     resource = {}
#     dataList = []
#     for item in data:
#         name = item.get_text()  # 公司名称
#         href = item["href"]  # 公司详情网页
#         resource = {name: href}
#         dataList.append(resource)
#     print(dataList)
#     return dataList


def details(html):
    # file = open("templates/tyc.html",encoding='utf-8')        # 避免爬取过多被封 先提取页面到本地 之后注释
    bs = BeautifulSoup(html, "html.parser")
    data = bs.select(".cominfo-normal > .ntable > tr")
    dataList = []
    finalList = {}
    # print(data)
    for item in data:
        data = item.get_text().replace("\n", "").replace("复制", "").replace("：", ": ").replace(" 至 ", "至").split()
        for i in range(0, len(data)):
            # print(data[i])
            dataList.append(data[i])
    print(dataList)
    finalList[dataList[dataList.index("统一社会信用代码")]] = finalList[
        dataList[dataList.index("统一社会信用代码") + 1]]
    finalList[dataList[dataList.index("企业名称")]] = finalList[dataList[dataList.index("企业名称") + 1]]

    print(finalList)
    return finalList


def extract(html):
    bs = BeautifulSoup(html, "html.parser")

    data = bs.find_all("div", class_="rline")
    resource = {}
    dataList = []
    for item in data:
        data = item.get_text().replace("\n", "").replace("复制", "").replace("：", " ").replace(" 至 ", "至").split()
        for i in range(0, len(data)):
            # print(data[i])
            dataList.append(data[i])  # 获取所有查询出的字符串 并通过空格进行分割  添加到列表中
    print(dataList)
    resource[dataList[dataList.index("统一社会信用代码")]] = dataList[
        dataList.index("统一社会信用代码") + 1]  # 获取指定的字符串及数据
    resource[dataList[dataList.index("电话")]] = dataList[dataList.index("电话") + 1]  # 获取指定的字符串及数据
    resource[dataList[dataList.index("官网")]] = dataList[dataList.index("官网") + 1]  # 获取指定的字符串及数据
    resource[dataList[dataList.index("邮箱")]] = dataList[dataList.index("邮箱") + 1]  # 获取指定的字符串及数据
    resource[dataList[dataList.index("地址")]] = dataList[dataList.index("地址") + 1]  # 获取指定的字符串及数据
    resource[dataList[dataList.index("法定代表人")]] = dataList[dataList.index("法定代表人") + 1]  # 获取指定的字符串及数据
    # print(resource)
    return resource


def getUrl(url, key):
    html = askURL(url)  # 获取网页信息
    urllist = getData(html)
    return urllist


def main():
    url = "https://www.qcc.com/web/search?key="
    key = '小米'
    finalUrl = parse.quote(key)
    url = url + finalUrl  # 对关键字进行加密处理使浏览器识别
    html = askURL(url)  # 获取网页信息
    urllist = getUrl(url, key)  # 获取url  和 详情网址
    print(urllist)
    if key is urllist:  # 判断 如果关键字再查出的urllist字典中 重新指定url  如果不在字典中 查询列表第一个详情网址
        url = urllist.get(key)
    print(url)
    html = askURL(url)  # 获取网页信息
    # detailsList = details(html)  # 测试方法
    resource = extract(html)  # 获取详情，提取方法
    resource['单位名称'] = key
    print(resource)
    save_mysql(resource)  # 保存到mysql中


def save_mysql(resource):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database)  # 连接mysql
        cur = conn.cursor()  # 获取游标
        print("------------------------------数据库连接成功------------------------------")
        time = datetime.datetime.now()
        sql = '''
            INSERT INTO obj_company set address='%s',name='%s',website='%s',bankAccountName='%s',createDate='%s',no='%s',法人='%s',公司邮箱='%s',公司电话='%s'
        ''' % (resource.get("地址"), resource.get("单位名称"), resource.get("官网"), resource.get("单位名称"),
               datetime.datetime.now(), resource.get("统一社会信用代码"), resource.get("法定代表人"),
               resource.get("邮箱"), resource.get("电话"))
        print(sql)
        print(time)
        # value = (
        #     finalList.get("地址"), finalList.get("单位名称"), finalList.get("官网"), finalList.get("单位名称"), time,
        #     finalList.get("统一社会信用代码"), finalList.get("法定代表人"), finalList.get("邮箱"),
        #     finalList.get("电话"))
        cur.execute(sql)  # 执行sql
        conn.commit()  # 向数据库提交
        print("------------------------------数据插入成功------------------------------")
    except pymysql.Error as e:
        print("数据插入失败: " + str(e))
        conn.rollback()
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接


if __name__ == "__main__":
    main()
