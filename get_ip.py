import random
import pymysql

from settings import database


class Get_ip(object):
    def __init__(self):
        super().__init__()
        self.conn = self.__connect()
        self.cursor = self.conn.cursor()

    #  连接数据库
    def __connect(self):
        conn = pymysql.connections.Connection(**database)
        return conn


    # 关闭数据库连接
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # 获取ip
    def get_ip(self):
        sql = "SELECT type,ip FROM ip_pool"
        try:
            self.cursor.execute(sql)
            ip_list = self.cursor.fetchall()
            ip = random.choice(ip_list)
            proxy_ip = {ip[0]:ip[1]}
            return proxy_ip
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ip = Get_ip()
    print(ip.get_ip())