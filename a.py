import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON

# URL = 'http://esf.fang.com'
# RESIDENCE_URL = 'http://esf.fang.com/housing/'
#
#
# def download_page(url, retries=10):
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
#     try:
#         time.sleep(round(random.uniform(1, 5), 2))
#         response = requests.get(url, headers=headers)
#         print(response.encoding)
#         if response.encoding == 'gb2312':
#             data = response.content.decode("gbk").encode('utf-8')
#         if response.encoding == 'ISO-8859-1':
#             data = response.content.decode("gbk").encode('utf-8')
#         # data = response.content.decode("gbk").encode('utf-8')
#
#         soup = BeautifulSoup(data, "html.parser")
#         test = soup.find('div', attrs={'class': 's4Box'}).getText()
#         print(test)
#
#     except Exception as err:
#         print("|||fail to download the page, reason: "+str(err)+'|||')
#         if retries > 0:
#             time.sleep(random.randint(10, 15))
#             print("try again, %d times left" % int(retries-1))
#             return download_page(url, retries - 1)
#         else:
#             print("|||failed in scaping : %s|||" % url)
#             with open('fangtianxia_beijing_failed_to_download.txt', 'a') as f:
#                 f.write(url+'\n')
#             # return ''
#     return soup
#
# s = download_page('http://beiyingxiaoqu.fang.com/')
# print(s)


import re
from json import loads as JSON

a = """
        var mapObj,imgurl="http://img.soufun.com",MapRoot="/newsecond/Map",cityName="北京",province="北京市",ShortInDB="bj",shortDomain="fang.com",isSecond="Y",FileVision="2016.07.211";
        var mapInfo={zoom:14,mapZoom:14,px:"116.41487121582031",py:"39.979888916015625",isKey:"1"};
        var searchInfo={district:"",comarea:"",projcode:"1010181265",projName:"国典大厦商铺"};
        var labelHtml="<table border='0' cellspacing='0' cellpadding='0'><tr><td class='maskleft'><div>国典大厦商铺</div></td><td class='maskright'>&nbsp;</td></tr></table>";
"""
# 将正则表达式编译成Pattern对象
pattern = re.compile(r'px\:(.*)\"\,')

# 使用search()查找匹配的子串，不存在能匹配的子串时将返回None
# 这个例子中使用match()无法成功匹配
match = pattern.search(a)
if match:
    # 使用Match获得分组信息
    res = match.group().split(',')
    print(match.group())
    print(res)
    px = res[0][4:-1]
    py = res[1][4:-1]
    print(px)
    print(py)
    # json_data = JSON(match.group())
    # print(json_data['px'])
    # ids = json_data['vwx.showhouseid'].split(',')
    # print(ids)
    # for i in range(0, len(ids)):
    #     ids[i] = ids[i][1:-1]
    # print(ids)
else:
    print('no')


b = 'http://esf.fang.com/newsecond/map/newhouse/ShequMap.aspx?newcode=1010087100'
if 'newcode' not in b:
    print('aa')




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
