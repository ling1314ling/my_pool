from urllib.request import build_opener, ProxyHandler, Request

from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()
headers = {
    "User-Agent": ua.random
}

url = "https://ip.cn/"


# opener = build_opener(ProxyHandler(proxies={'https': '119.101.117.31:9999'}))
opener = build_opener(ProxyHandler(proxies={'https': '119.101.115.82:9999'}))



def start_spider():
    try:
        resp = opener.open(Request(url, headers=headers), timeout=15)
        html = resp.read().decode()
        parse(html)

    except Exception as e:
        print(e)


def parse(html):
    et = etree.HTML(html)
    ip_ = str(et.xpath("//div[@class='well']/p[1]/code/text()")[0])
    address = str(et.xpath("//div[@class='well']/p[2]/code/text()")[0])
    print("您的ip是:",str(ip_),type(ip_))
    print("地理位置:",address,type(address))



if __name__ == '__main__':
    start_spider()
