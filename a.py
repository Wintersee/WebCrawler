import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON



import re
from json import loads as JSON


a = ''
print(type(a))

a = """
       var mainBuilding={"@attributes":{"score":"1.0"},"category":"1","newCode":"2813205046","create_time":"20150529","view_type":"","domain":"zh.fang.com","houseurl":"http:\/\/guojiguangchangbl0756.fang.com\/","extendnum":"0","last7daysordercount":"0","new_keyword_ad":"","buildcategory":"","maxarea":"0000000160.00","minarea":"0000000160.00","video":"","isshow":"390","title":"\u4fdd\u5229\u56fd\u9645\u5e7f\u573a","esftitle":"\u4fdd\u5229\u56fd\u9645\u5e7f\u573a\u5199\u5b57\u697c","roundstation":"","address":"\u4e2d\u56fd\u00b7\u73e0\u6d77\u00b7\u6a2a\u7434\u65b0\u533a\u00b7\u6e2f\u6fb3\u5927\u9053","tel":"4001-600048","developer":"\u73e0\u6d77\u6a2a\u7434\u4fdd\u5229\u5229\u548c\u6295\u8d44\u6709\u9650\u516c\u53f8","istopten":"0","detail":"\u6a2a\u7434\u4fdd\u5229\u56fd\u9645\u5e7f\u573a\u4f4d\u4e8e\u6a2a\u7434\u65b0\u533a\u7efc\u5408\u670d\u52a1\u533a\uff0c\u5750\u843d\u5728\u5c0f\u6a2a\u7434\u5c71\u4f53\u5ef6\u4f38\u7684\u7eff\u8272\u5927\u5730\u4e4b\u4e0a\u3002\u9879\u76ee\u7531\u4e24\u4e2a\u5730\u5757\u7ec4\u6210\uff0c\u5730\u5757\u4e00\u5317\u4e3a\u6e2f\u6fb3\u5927\u9053\uff0c\u5357\u4e3a\u7434\u653f\u8def\uff0c\u4e1c\u4e3a\u7434\u6717\u9053\uff0c\u897f\u4e3a\u7434\u8fbe\u9053\uff0c\u7531\u4e00\u680b99.9\u7c7319\u5c42\u5199\u5b57\u697c\u548c\u4e00\u4e2a\u4e2d\u8f74\u666f\u89c2\u7eff\u5730\u5e7f\u573a\u7ec4\u6210\u3002\u5730\u5757\u4e8c\u4f4d\u4e8e\u5730\u5757\u4e00\u4e1c\u4fa7\uff0c\u5317\u4e3a\u7434\u98de\u9053\uff0c\u897f\u4e3a\u7434\u6717\u9053\uff0c\u5efa\u8bbe\u4e00\u680b\u9ad8\u5ea693.5\u7c7327\u5c42\u5357\u5854\u697c\u548c\u4e00\u680b\u9ad8\u5ea69..","comarea":"\u6a2a\u7434","purpose":"\u5199\u5b57\u697c","officetype":"\u6807\u51c6\u5199\u5b57\u697c","bayareamin":"00000035.00","bayareamax":"00000425.00","shangzhupurpose":"","startTime":"20160110","saledateforsearch":"000003","opendateproj":"1608","orderandpv":"000000516","picAddress":"http:\/\/imgs.soufun.com\/house\/2015_11\/30\/zhuhai\/1448852164658_000.jpg","price":"35000\u5143\/\u5e73\u65b9\u7c73","price_num":"35000","price_unit":"\u5143\/\u5e73\u65b9\u7c73","price_type":"\u5747\u4ef7","bbs":"http:\/\/bbs.zh.fang.com\/board\/2813205046\/","bbs_id":"2813205046","photo":"guojiguangchangbl0756.fang.com\/photo\/2813205046.htm","areaurl":"","news":"http:\/\/search.fang.com\/news\/search.jsp?q=\u4fdd\u5229\u56fd\u9645\u5e7f\u573a","saling":"1","status":"","district":"\u6a2a\u7434","video_id":"0","videoid":"","dev_id":"20150610145104","city":"\u73e0\u6d77","blog":"","soufun_card":"","soufun_card_url":"","soufun_card_client":"","sale_client_info":"null","signupcity":"","signupname":"","signuplineid":"","signuptype":"","signuplinename":"","signupactivitiedate":"","signuplink":"","huxinginfos":"","tuangouinfo":"","qudaotag":"","guanggaotag":"","iskanfangtag":"0","activitiedate":"","isactivitytag":"0","tuanendtime":"","goumailiang":"0","show_yidi":"","isdsguanggao":"0","show_city":",","show_district":",","yidi_status":"local","newcodescore":"0.00","img_count":"3","news_count":"","price_date":"2016-11-09 00:00:00","character":"\u54c1\u724c\u5730\u4ea7,\u590d\u5408\u5730\u4ea7","sale_card":"","tuangou_count":"2","bbs_count":"0","projPubTimeString":"2015-05-29","projMoveinDate_s":"","mapx":"113.54103851318359375000","mapy":"22.14558792114257812500","baidu_coord_x":"113.54103851318359375000","baidu_coord_y":"22.14558792114257812500","startTime_s":"\u5df2\u4e8e2016\u5e741\u670810\u65e5\u5f00\u76d8","purposeArea":"230000.00","map_logo":"","area_buy":"","tel400":"400-890-0000 \u8f6c 829483","xfb400info":"","zygwuserid":"","zygwusername":"","isAD":"0","shoptype":"","pricerate":"0.0","score":"0.00","microblognum":"0","isopen":"n","iscomplex":"0","complexpurpose":"","projtype":"","propertyType":"","layout":"","parttotaldoor":"0","projfitment":"\u7cbe\u88c5\u4fee","appoint":"n","totalimg":"27","videocount":"0","dongid":"","taonum":"","miaosha":"0","miaoshatime":"","hits":"2292","hits7day":"516","yhtype":"4","householdpic":"[\u6682\u65e0\u8d44\u6599,]","roompiccount":"null","stationdistance":"","images":"[\u6548\u679c\u56fe,http:\/\/imgs.soufun.com\/house\/2015_11\/30\/zhuhai\/1448852164658_000.jpg];[\u6548\u679c\u56fe,http:\/\/imgs.soufun.com\/house\/2015_11\/30\/zhuhai\/1448852162397_000.jpg];[\u5b9e\u666f\u56fe,http:\/\/imgs.soufun.com\/house\/2015_11\/27\/zhuhai\/1448593565505_000.jpg];[\u5916\u666f\u56fe,http:\/\/imgs.soufun.com\/house\/2015_11\/27\/zhuhai\/1448593422086_000.jpg];","builddesc":"\u5730\u5757\u4e00\u9996\u5c42\u5546\u4e1a\u5c42\u9ad8\u4e3a7\u7c73\uff0c\u4e8c\u5c42\u5199\u5b57\u697c\u5927\u5802\u5c42\u9ad8\u4e3a13\u7c73\uff0c3~19\u5c42\u4e3a\u529e\u516c\u5c42\uff0c\u6807\u51c6\u5c42\u9ad84.2\u7c73\u5c42\u9ad8\u3002\u5730\u5757\u4e8c\u5546\u94fa1~2\u5c42\u9ad8\u4e3a6\u7c73\u3002","finishdate":"2015-05-01","propertyfee":"25","propfeetype":"\u5143\/\u33a1\u00b7\u6708","propertymanage":"\u4fdd\u5229\u7269\u4e1a\u7ba1\u7406\u6709\u9650\u516c\u53f8\u73e0\u6d77\u4f1a\u516c\u53f8,","parkdesc":"","carrentprice":"","carrentpricetype":"","carsaleprice":"","carsalepricetype":"","dimension":"2.00","virescencerate":"30.00","mobilepayment":"","onsale_detail":"new","enrollcount":"0","signroomcount":"0","zhiding":"0","iskuang":"0","miaoshaprice":"","qipaiprice":"","yhquan":"","isqudao":"0","sail_schedule":"0","butieinfo":"","brand":"\u4fdd\u5229\u5730\u4ea7","schoolname":"","school":"","isxuequ":"0","redmone":"","isPCRedBag":"0","houselevel":"b","housetag":";","kuanginfo":"","paiinfo":"","tuaninfo":"","isestimate":"1","iscommonproj":"","finaceinfo":"","guesslike":"0","interest":"0","dianpingcount":"7","dpHalfYearCount":"1","zongfen":"4.14","housesalenum":"","lowestprice":"","isyouhui":"0","tag":";;;","louPanYHInfoTag":";","finaceInfoTag":";","brandurl":"http:\/\/img.soufun.com\/map\/2016_01\/04\/house\/1451900881890.jpg","androidad":"","iosad":"","wapad":"","pcadnew":"","squares":"","main_info":"","act_info":"","ishongbao":"0","isdirectselling":["0","0"],"redbagreceivedcount":"null","certitype":"0","salenum":"0","iskeywordad":"null","adurl":"null","adshowurl":"null","hxarearange":"","@":{"score":"1.0"}};
"""
# 将正则表达式编译成Pattern对象
pattern = re.compile(r'mapx\"(.*)\_x')
match = pattern.search(str(a))
res = match.group().split(',')
print(res)
px = res[0][7:-1]
py = res[1][8:-1]
print(px)
print(py)
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
