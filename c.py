# coding: utf-8




import datetime
import time


# 获得当前时间戳
now = datetime.datetime.now()  # 时间数组格式
# 转换当日零时的时间，即每周周六零点时间
saturday = now.strftime("%Y-%m-%d") + " 00:00:00"
# 转换成每周周日零点的时间戳
sunday = int(time.mktime(time.strptime(saturday, "%Y-%m-%d %H:%M:%S"))) + 86400
# 爬取选择的时间段为 周一00:00 至 周六23:59
start = sunday - 6*86400

print(now)
print(start)
print(time.localtime(start))
print(datetime.datetime.now())
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print(time.localtime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


receivers = 'wintersee@outlook.com,wintersee@outlook.com'
print(receivers.split(',')[0])