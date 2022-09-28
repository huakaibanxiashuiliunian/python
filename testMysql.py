# -*- coding = utf-8 -*-
# @Time :  14:04
# @Author : XX
# @File : testMysql.py
# @Software : PyCharm

import pymysql

host = "localhost"
user = "root"
password = '123456'
port = 3306
database = "test"


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


def main():
    init_db()
    conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database)
    cur = conn.cursor()
    data = []
    data = cur.execute("select * from movie")
    # cur.execute("drop table movie")
    sql1 = '''
            
        '''
    resource = cur.fetchall()  # 接收数据
    for item in resource:
        print(item)


if __name__ == "__main__":
    main()
