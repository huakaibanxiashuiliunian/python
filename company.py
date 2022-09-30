# -*- coding = utf-8 -*-
# @Time :  16:40
# @Author : XX
# @File : jpgDownload.py
# @Software : PyCharm
import json
import re
import time
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
    '''"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"'''
    '''"cookie": "qcc_did=42c3b7a0-cacb-4762-bfdb-34ed485187e7; UM_distinctid=183782db56b276-024f85f7b83c-6b3e555b-1fa400-183782db56cc26; acw_tc=d3a2ab1816644212703026389e44387fc395b7ad0a5a921fb00b0cf2e2; CNZZDATA1254842228=1432742392-1664165618-https%253A%252F%252Fwww.baidu.com%252F%7C1664421240; QCCSESSID=eba4889f8ff6aec354e671ee1b",'''
    head = {
        "cookie": "qcc_did=25b01b41-4b08-4f7f-891c-4be0f9d193d0; UM_distinctid=183875d8346341-06f8c6eacbad9-78565473-1fa400-183875d8347c57; QCCSESSID=825d0b3e52e1411e3167ef5cc3; acw_tc=7c0e13a216645024796777559ecc2f77d6e4f3b19be04bd4bc285ca980; CNZZDATA1254842228=1617853709-1664421240-https%253A%252F%252Fwww.qcc.com%252F%7C1664500628",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"  }
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
    try:
        resource[dataList[dataList.index("统一社会信用代码")]] = dataList[dataList.index("统一社会信用代码") + 1]  # 获取指定的字符串及数据
    except TypeError as e:
        print("该关键字不存在-----------------------"+str(e))
    except ValueError as v:
        print("该关键字不存在-----------------------"+str(v))
    try:
        resource[dataList[dataList.index("电话")]] = dataList[dataList.index("电话") + 1]  # 获取指定的字符串及数据
    except TypeError as e:
        print("该关键字不存在-----------------------"+str(e))
    except ValueError as v:
        print("该关键字不存在-----------------------"+str(v))
    try:
        resource[dataList[dataList.index("官网")]] = dataList[dataList.index("官网") + 1]  # 获取指定的字符串及数据
    except TypeError as e:
        print("该关键字不存在-----------------------"+str(e))
    except ValueError as v:
        print("该关键字不存在-----------------------"+str(v))
    try:
        resource[dataList[dataList.index("邮箱")]] = dataList[dataList.index("邮箱") + 1]  # 获取指定的字符串及数据
    except TypeError as e:
        print("该关键字不存在-----------------------"+str(e))
    except ValueError as v:
        print("该关键字不存在-----------------------"+str(v))
    try:
        resource[dataList[dataList.index("地址")]] = dataList[dataList.index("地址") + 1]  # 获取指定的字符串及数据
    except TypeError as e:
        print("该关键字不存在-----------------------"+str(e))
    except ValueError as v:
        print("该关键字不存在-----------------------"+str(v))
    try:
        resource[dataList[dataList.index("法定代表人")]] = dataList[dataList.index("法定代表人") + 1]  # 获取指定的字符串及数据
    except TypeError as e:
        print("该关键字不存在-----------------------"+str(e))
    except ValueError as v:
        print("该关键字不存在-----------------------"+str(v))
    return resource


def getUrl(url, key, finalUrl):
    urlList = {}
    keyList = []
    try:
        for i in range(1,3):       #查询1-2页内容
            i = str(i)
            newurl = url + finalUrl + "&p=" + i  # 对关键字进行加密处理使浏览器识别
            html = askURL(newurl)  # 获取网页信息
            urllist = getData(html)
            for key in urllist:
                urlList[key] = urllist.get(key)
                keyList.append(key)
            # if key in urllist:
            #     print(key)
            #     print(urllist[key])
            if key not in urllist:
                for i in urllist:
                    keyList.append(i)
            # print(urlList)
            # print(keyList)
        return urlList,keyList
    except error as e:
        print(e)


# def getUrl(url, key):
#     html = askURL(url)  # 获取网页信息
#     urllist = getData(html)
#     return urllist


def main():
    url = "https://www.qcc.com/web/search?key="
    key = '华为'
    finalUrl = parse.quote(key)
    url = url + finalUrl  # 对关键字进行加密处理使浏览器识别
    html = askURL(url)  # 获取网页信息
    urllist,keyList = getUrl(url, key, finalUrl)  # 获取url  和 详情网址
    print(urllist)
    print(keyList)
    for company in keyList:
        if company in urllist:
            print('----------------------------------------------------------------------')
            key = company
            if key in urllist:  # 判断 如果关键字再查出的urllist字典中 重新指定url  如果不在字典中 查询列表第一个详情网址
                url = urllist.get(key)
                print("-------------------------查询%s-------------------------"%key)
                print("-------------------------地址%s-------------------------"%url)
            print(url)
            html = askURL(url)  # 获取网页信息
            time.sleep(10)
            # detailsList = details(html)  # 测试方法
            resource = extract(html)  # 获取详情，提取方法
            resource['单位名称'] = key
            print(resource)
            time.sleep(20)
            # save_mysql(resource)  # 保存到mysql中


def save_mysql(resource):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database)  # 连接mysql
        cur = conn.cursor()  # 获取游标
        print("------------------------------数据库连接成功------------------------------")
        time = datetime.datetime.now()
        count = cur.execute("select name from obj_company where name = '%s'"%resource.get("单位名称"))      # 查看数据库是否有该数据

        if count != 0:
            # 存在   更新数据库的sql
            updateSql = '''
            update obj_company set address='%s',website='%s',bankAccountName='%s',createDate='%s',no='%s',法人='%s',公司邮箱='%s',公司电话='%s'  where name='%s'
            ''' % (resource.get("地址"), resource.get("官网"), resource.get("单位名称"),
               datetime.datetime.now(), resource.get("统一社会信用代码"), resource.get("法定代表人"),
               resource.get("邮箱"), resource.get("电话"), resource.get("单位名称"))
            print(updateSql)
            print(time)
            cur.execute(updateSql)  # 执行sql
            print("-----------------------------数据更新成功------------------------------")
        else:
            # 不存在 插入数据库的sql
            instersql = '''
                    INSERT INTO obj_company set address='%s',name='%s',website='%s',bankAccountName='%s',createDate='%s',no='%s',法人='%s',公司邮箱='%s',公司电话='%s'
                ''' % (resource.get("地址"), resource.get("单位名称"), resource.get("官网"), resource.get("单位名称"),
                       datetime.datetime.now(), resource.get("统一社会信用代码"), resource.get("法定代表人"),
                       resource.get("邮箱"), resource.get("电话"))
            print(instersql)
            print(time)
            cur.execute(instersql)  # 执行sql
            conn.commit()  # 向数据库提交
            print("-----------------------------数据插入成功------------------------------")
    except pymysql.Error as e:
        print("数据更新失败,该公司已存在！！！: " + str(e))
        conn.rollback()
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    print("-----------------------------关闭数据库连接------------------------------")


if __name__ == "__main__":
    main()
