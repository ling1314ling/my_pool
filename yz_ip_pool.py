"""
如果,要直接使用该代码,需:
   在setting中填写数据库配置信息

   对于数据库有时会连接不上的问题,大家一起看看代码是否有问题.
"""


import pymysql
import time
from queue import Queue
from threading import Thread, current_thread, Lock
import csv
from urllib.request import build_opener, ProxyHandler, Request

from fake_useragent import UserAgent
from lxml import etree

from settings import database

ua = UserAgent()
headers = {
    "User-Agent": ua.random
}


class YZ_Ip(Thread):
    def __init__(self):
        super().__init__()
        self.conn = self.__connect()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    #  连接数据库
    def __connect(self):
        conn = pymysql.connections.Connection(**database)
        return conn


    # 关闭数据库连接
    def __del__(self):
        self.cursor.close()
        self.conn.close()


    # 从本地文件中拿取ip
    def get_ip(self,q1):
        with open("pool/ip_pool.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=['type', 'ip'])
            reader_list = list(reader)
            i = 1
            for info in reader_list:
                print("读取本地第%d条信息"%(i))
                i += 1
                q1.put((info['type'].lower(),info['ip']))


    def start_yz(self,q1):
        i = 1
        while True:
            try:
                type_, ip = q1.get(timeout=50)
                print(current_thread().name,"开始验证第%d条信息"%(i))
                i += 1
                try:
                    opener = build_opener(ProxyHandler(proxies={type_: ip}))

                    if type_ == 'http':
                        url = "http://ip.tool.chinaz.com/"
                        resp = opener.open(Request(url, headers=headers), timeout=20)
                        html = resp.read().decode()
                        self.__parse_http(html,ip)
                    elif type_ == 'https':
                        url = "https://ip.cn/"
                        resp = opener.open(Request(url, headers=headers), timeout=20)
                        html = resp.read().decode()
                        self.__parse_https(html,ip)
                except:
                    pass

            except Exception as e:
                print(e)
                break


    def __parse_http(self,html,ip):
        et = etree.HTML(html)
        div_ = et.xpath("//dl[@class='IpMRig-tit']")[0]
        ip_ = str(div_.xpath("./dd[@class='fz24']/text()")[0])
        address = str(div_.xpath("./dd[2]/text()")[0])
        print(ip_, ip)
        try:
            ip1, port1 = ip.split(":")[0],ip.split(":")[1]
            if ip_ == ip1:
                # 将验证OK的ip数据存入本地文件
                with open("pool/new_http.csv", "a", encoding="utf-8", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["http", ip, address])
                # 将验证OK的ip数据存入数据库
                try:
                    sql = "insert into ip_pool(type,ip) values('http','%s')"%(ip)
                    self.cursor.execute(sql)
                    self.conn.commit()
                    print("*"*10,ip,"保存成功")
                except Exception as e:
                    self.conn.rollback()
                    print("*"*10,ip, "保存失败")
                    print(e)

            else:
                with open("pool/fail_http.csv", "a", encoding="utf-8", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["http", ip, ip_ +":"+ port1])
        except Exception as e:
            print(e)


    def __parse_https(self,html,ip):
        et = etree.HTML(html)
        ip_ = str(et.xpath("//div[@class='well']/p[1]/code/text()")[0])
        address = str(et.xpath("//div[@class='well']/p[2]/code/text()")[0])
        print(ip_, ip)
        try:
            ip1, port1 = ip.split(":")[0], ip.split(":")[1]
            with lock:
                if ip_ == ip1:
                    # 将验证OK的ip数据存入本地文件
                    with open("pool/new_https.csv", "a", encoding="utf-8", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["https", ip, address])
                    # 将验证OK的ip数据存入数据库
                    try:
                        sql = "insert into ip_pool(type,ip) values('https','%s')" % (ip)
                        self.cursor.execute(sql)
                        self.conn.commit()
                        print("*"*10,ip, "保存成功")
                    except Exception as e:
                        self.conn.rollback()
                        print(e)
                        print("*"*10,ip, "保存失败")


                else:
                    with open("pool/fail_https.csv", "a", encoding="utf-8", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["https", ip, ip_ +":"+ port1])

        except Exception as e:
            print(e)


if __name__ == '__main__':
    lock = Lock()
    q1 = Queue()
    q2 = Queue()
    yz = YZ_Ip()

    t100 = time.time()
    get_ip_thread = Thread(target=yz.get_ip,args=(q1,))
    get_ip_thread.start()
    get_ip_thread.join()

    ts = [Thread(target=yz.start_yz, args=(q1,)) for _ in range(10)]
    for t in ts:
        t.start()

    for t in ts:
        t.join()

    t200 = time.time()

    print(t200 - t100)