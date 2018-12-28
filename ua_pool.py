from fake_useragent import UserAgent

ua=UserAgent()

#ie浏览器的user agent
print("ie浏览器",ua.ie)
#opera浏览器
print("欧朋浏览器",ua.opera)
#chrome浏览器
print("谷歌浏览器",ua.chrome)
#firefox浏览器
print("火狐浏览器",ua.firefox)


#最常用的方式
#写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
print(ua.random)
print(ua.random)
print(ua.random)