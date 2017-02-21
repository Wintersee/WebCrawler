import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON



import re
from json import loads as JSON

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 05:41:01 2016

@author: Keith
"""

# coding: utf-8

'''''
以关键词收集新浪微博
'''

import time
import base64
import rsa
import binascii
import requests
import re
import urllib
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from lxml import etree

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


# 预登陆获得 servertime, nonce, pubkey, rsakv
def get_server_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    prelogin_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(prelogin_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data


# 这一段用户加密密码，需要参考加密文件
def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥,
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def login(username, password):
    # su 是加密后的用户名
    su = get_su(username)
    sever_data = get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    password_secret = get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    login_page = session.post(login_url, data=postdata, headers=headers)
    login_loop = (login_page.content.decode("GBK"))
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    loop_url = re.findall(pa, login_loop)[0]
    login_index = session.get(loop_url, headers=headers)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    weibo_pa = r'<title>(.*?)</title>'
    userName = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    print('登陆成功，你的用户名为：' + userName)


class CollectData():
    """数据收集类
       利用微博高级搜索功能，按关键字搜集一定时间范围内的微博。
    """

    def __init__(self, keyword, startTime, endTime, region, interval='50', flag=True,
                 begin_url_per="http://s.weibo.com/weibo/"):
        self.begin_url_per = begin_url_per  # 设置固定地址部分
        self.setKeyword(keyword)  # 设置关键字
        self.setTimescope(startTime, endTime)  # 设置搜索的开始时间
        self.setRegion(region)  # 设置搜索区域
        self.setInterval(interval)  # 设置邻近网页请求之间的基础时间间隔（注意：过于频繁会被认为是机器人）
        self.setFlag(flag)
        ##设置关键字

    ##关键字需解码后编码为utf-8
    def setKeyword(self, keyword):
        self.keyword = keyword
        print('twice encode:', self.getKeyWord())

        ##关键字需要进行两次urlencode

    def getKeyWord(self):
        return urllib.parse.quote(urllib.parse.quote(self.keyword))

        ##设置起始范围，间隔为1天

    ##格式为：yyyy-mm-dd
    def setTimescope(self, startTime, endTime):

        if not (startTime == '-'):
            self.timescope = startTime + ":" + endTime
        else:
            self.timescope = '-'

    def setRegion(self, region):
        self.region = region

        ##设置邻近网页请求之间的基础时间间隔

    def setInterval(self, interval):
        self.interval = int(interval)

        ##设置是否被认为机器人的标志。若为False，需要进入页面，手动输入验证码

    def setFlag(self, flag):
        self.flag = flag

        ##构建URL

    def getURL(self):
        return self.begin_url_per + self.getKeyWord() + "&region=custom:" + self.region + "&typeall=1&suball=1&timescope=custom:" + self.timescope + "&page="


login("15659805057", "Qq7758521")
keyword = "中国好声音"
startTime = "2016-12-01"
endTime = "2016-12-10"
region = "35:1"
interval = "50"

##实例化收集类，收集指定关键字和起始时间的微博
cd = CollectData(keyword, startTime, endTime, region, interval)
result_url = cd.getURL()
page = session.get(result_url, headers=headers).text.encode("utf-8").decode('unicode_escape').replace("\\", "")

page2 = urllib.request.urlopen(result_url).read()

print(page)
soup = BeautifulSoup(page, 'html.parser')
# print(soup)
ps = soup.find('p', attrs={'class': 'comment_txt'}).getText()
print(ps)
print('jjj')
# print(soup)



# a = ''
# print(type(a))
#
# a = """
#
#
#         var mapObj,imgurl="http://img1.soufun.com",MapRoot="/newsecond/Map",cityName="南宁",province="广西省",ShortInDB="nn",shortDomain="nn.fang.com",isSecond="Y",FileVision="2016.07.211";
#         var mapInfo={zoom:14,mapZoom:14,px:"108.33668518066406",py:"22.855602264404297",isKey:"1"};
#         var searchInfo={district:"",comarea:"",projcode:"2911130226",projName:"江宇世纪广场"};
#         var labelHtml="<table border='0' cellspacing='0' cellpadding='0'><tr><td class='maskleft'><div>江宇世纪广场</div></td><td class='maskright'>&nbsp;</td></tr></table>";
#
#
# """
# # 将正则表达式编译成Pattern对象
# # script = soup.findAll('script', attrs={'type': 'text/javascript', 'src': '', 'language': ''})[1]
# # def download_page(url, retries=10):
# #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
# #
# #     try:
# #         time.sleep(round(random.uniform(1, 5), 2))
# #
# #         # # headers = {'User-Agent': user_agent}
# #         # # data = urllib.parse.urlencode(values)
# #         # # req = urllib.request.Request(url, headers)
# #         # response = urllib.request.urlopen(url, headers)
# #         # the_page = response.read()
# #         # print(the_page.decode("utf8"))
# #
# #         response = requests.get(url, headers=headers)
# #         # print(response.encoding + '  response')
# #         if response.encoding == 'gb2312':
# #             data = response.content.decode("GB18030").encode('utf-8')
# #         # if response.encoding == 'ISO-8859-1':
# #         else:
# #             data = response.content.decode("GB18030").encode('utf-8')
# #
# #         soup = BeautifulSoup(data, "html.parser")
# #
# #         if 'aspx?newcode=' not in url:
# #             test = soup.find('a', attrs={'href': 'http://wap.fang.com/xc/mobile.html'}).getText()
# #
# #     except Exception as err:
# #         print("|||test failed ! didn't get the right content: "+str(err)+' ||| ' + url)
# #         if retries > 0:
# #             time.sleep(random.randint(10, 15))
# #             print("try again, %d times left" % int(retries-1))
# #             return download_page(url, retries - 1)
# #         else:
# #             print("|||failed in scaping : %s|||" % url)
# #             # with open(city_url_failed_file, 'a', 'utf-8') as f:
# #             #     f.write(url+'\n')
# #             # # return ''
# #     return soup
# #
# # soup = download_page('http://esf.nn.fang.com/housing/_7030_0_0_0_0_3_0_0/')
# # script = soup.findAll('script', attrs={'type': 'text/javascript', 'src': '', 'language': ''})[1]
# pattern = re.compile(r'px\:(.*)\"\,')
# match = pattern.search(a)
# res = match.group().split(',')
# px = res[0][4:-1]
# py = res[1][4:-1]
# print(res)
# if match:
#     # 使用Match获得分组信息
#     res = match.group().split(',')
#     print(match.group())
#     print(res)
#     px = res[0][4:-1]
#     py = res[1][4:-1]
#     print(px)
#     print(py)
    # json_data = JSON(match.group())
    # print(json_data['px'])
    # ids = json_data['vwx.showhouseid'].split(',')
    # print(ids)
    # for i in range(0, len(ids)):
    #     ids[i] = ids[i][1:-1]
    # print(ids)
# else:
#     print('no')
#
#
# b = 'http://esf.fang.com/newsecond/map/newhouse/ShequMap.aspx?newcode=1010087100'
# if 'newcode' not in b:
#     print('aa')




# from json import loads as JSON
# json_data = JSON(str(a))
# info = json_data['project'][0]
# result = info['projname'] + '\t' + info['coverimg'] + '\t' + info['avgprice'][0:-4] + '\t' + info['coordx'] + '\t' + info['coordy'] + '\t' + info['addresslong'] + '\t' + info['purpose']
#
# print(result)






# import random
# for i in range(1,11):
#     print(round(random.uniform(2,5),2))

# import urllib.request
 
# from multiprocessing.dummy import Pool as ThreadPool
 
# urls = ['http://www.baidu.com','http://www.sina.com','http://www.qq.com']
 
# pool = ThreadPool()
 
# results = pool.map(urllib.request.urlopen,urls)
# print(results)
# pool.close()
# pool.join()
 
# print('main ended')


# import time
# import datetime
# from functools import wraps


# def fn_timer(function):
#     @wraps(function)
#     def function_timer(*args, **kwargs):
#         t0 = datetime.datetime.now().microsecond
#         print(datetime.datetime.now())
#         result = function(*args, **kwargs)
#         t1 = datetime.datetime.now().microsecond
#         print("Total time running %s: %s seconds" %
#               (function.__name__, str(t1 - t0))
#               )
#         return result

#     return function_timer

# @fn_timer
# def twoSum(nums, target):
#     """
#     :type nums: List[int]
#     :type target: int
#     :rtype: List[int]
#     """
#     dict = {}

#     for i in range(len(nums)):
#         dict[nums[i]] = i


#     a = 0
#     for i in range(len(nums)):
#         a += 1
#         print(a)
#         diff = target-nums[i]

#         if diff in dict.keys() and dict[diff] != i:
#             return [i, dict[target-nums[i]]]

# @fn_timer
# def twoSum2(nums, target):
#     """
#     :type nums: List[int]
#     :type target: int
#     :rtype: List[int]
#     """
#     dict = {}

#     # for i in range(len(nums)):
#     #     dict[nums[i]] = i

#     a = 0
#     for i in range(len(nums)):
#         a += 1
#         print(i)
#         diff = target-nums[i]

#         if diff in dict.keys():
#             return [dict[target-nums[i]], i]
#         dict[nums[i]] = i


# def findTheDifference(s, t):
#     """
#     :type s: str
#     :type t: str
#     :rtype: str
#     """

#     dict = {}
#     for item in s:
#         if item in dict:
#             dict[item] += 1
#         else:
#             dict[item] = 1

#     dict2 = {}
#     for item in t:
#         if item in dict2:
#             dict2[item] += 1
#         else:
#             dict2[item] = 1

#     for item in t:
#         if (not item in dict) or dict[item]!=dict2[item]:
#             return item


# if __name__ == "__main__":
#     # print(twoSum([0,4,10,13,3,0], 0))
#     # print(twoSum2([0,4,10,13,3,0], 0))
#     print(findTheDifference("ae", "aea"))
