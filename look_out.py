"""
注意事项:
1. 使用代理时,如果即将访问的网页,协议为 https ,则代理服务器也要选择 https,反之亦然
2. 代理ip 格式一定要正确,协议区分大小写
3. xpath解析得到的数据并不是字符串

"""


from urllib.request import build_opener, ProxyHandler, Request

from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()
headers = {
    "User-Agent": ua.random
}


url = "http://ip.tool.chinaz.com/"


# opener = build_opener(ProxyHandler(proxies={'https': '119.101.117.31:9999'}))
opener = build_opener(ProxyHandler(proxies={'https': '124.235.135.87:80'}))


def start_spider():
    try:
        resp = opener.open(Request(url, headers=headers), timeout=15)
        html = resp.read().decode()
        parse(html)

    except Exception as e:
        print(e)


def parse(html):
    et = etree.HTML(html)
    div_ = et.xpath("//dl[@class='IpMRig-tit']")[0]
    ip_ = div_.xpath("./dd[@class='fz24']/text()")[0]
    address = str(div_.xpath("./dd[2]/text()")[0])
    system_ = str(div_.xpath("./dd[3]/text()")[0])
    browser = str(div_.xpath("./dd[6]/text()")[0])
    print(ip_,type(ip_))
    print(address,type(address))
    data = {
        "ip":ip_,
        "address":address,
        "system":system_,
        "browser":browser
    }
    print(data)


if __name__ == '__main__':
    start_spider()
