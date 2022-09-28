# -*- coding = utf-8 -*-
# @Time :  14:54
# @Author : XX
# @File : testBeautifulsoup4.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import re

'''
    BeautifulSoup4将复杂的html文档转化为一个复杂的树形结构，每个节点都是python对象，所有对象可以归为四种
    
    -Tag
    -NavigableString
    -BeautifulSoup
    - comment
'''

file = open('./templates/index.html', "rb")
html = file.read()

bs = BeautifulSoup(html, "html.parser")

# print(bs.title)
# print(bs.a)
# print(bs.head)  # bs.标签名  拿到第一个标签及内容
# print(bs.a.string)
# print(bs.a)


# 文档的遍历
# for i in range(0,len(bs.mate)):
#     print(bs.meta[i])

# 文档的搜索
# t_list = bs.find_all("a")       # 字符串过滤   匹配到与字符串完全匹配的内容
# print(t_list)
# 正则表达式搜索

# t_a = bs.find_all(re.compile("a"))
# print(t_a)

# t_list = bs.find_all("li",class_="ui-slide-item")
# t_list = bs.select("li[class='title']")         # 通过属性来查找
t_list = bs.find_all("a",class_="")



for item in t_list:
    print(item.get_text())
    # findName = re.compile(r'<a class="" href=".*" onclick=".*">(.*)</a>')
    # item = str(item)
    # # print(item)
    # name = re.findall(findName,item)
    # print(name)