import requests
import random
from functions import fn_timer
from json import loads as JSON
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import sys
print(sys.version)

def send_mail(sender, receivers, subject, content, attachment, attachment_path):
    # 邮箱相关
    smtpserver = 'smtp.sina.com'
    username = '****@sina.com'
    password = '****'

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(attachment_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="'+attachment+'"'
    message.attach(att1)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receivers.split(','), message.as_string())
        # receivers.split(',') 方法还是只能发送第一个收件人，故此处分两次发送
        # try:
        #     smtp.sendmail(sender, receivers.split(',')[0], message.as_string())
        #     print("收件人" + receivers.split(',')[0] + "的邮件发送成功")
        # except smtplib.SMTPException as e:
        #     print(e)
        #     print("Error: 无法发送邮件收件人为"+ receivers.split(',')[0] + "的邮件")
        # try:
        #     smtp.sendmail(sender, receivers.split(',')[1], message.as_string())
        #     print("收件人" + receivers.split(',')[1] + "的邮件发送成功")
        # except smtplib.SMTPException as e:
        #     print(e)
        #     print("Error: 无法发送邮件收件人为" + receivers.split(',')[1] + "的邮件")
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")


def get_data(arr, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    events = []
    try:
        start = str(arr[1])
        end = str(arr[2])
        url = "https://api-prod.wallstreetcn.com/apiv1/finfo/calendars?start=" + start + "&end=" + end
        print(url)
        response = requests.get(url, headers=headers)

        json_data = JSON(str(response.text), encoding='utf-8')

        data = json_data["data"]["items"]
        for info in data:
            country = info["country"]
            title = info["title"]
            importance = str(info["importance"])
            actual = info["actual"]
            forecast = info["forecast"]
            previous = info["previous"]
            if importance == '3':
                event = arr[0] + "\t" + country + "\t" + title + "\t" + importance + "\t" + actual + "\t" + forecast + "\t" + previous
                events.append(event)

    except Exception as err:
        print("|||test failed ! didn't get the right content: "+str(err)+' ||| ' + url)
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return get_data(arr, retries - 1)
        else:
            print("|||failed in scraping : %s|||" % url)

    return events


def get_data_v2(start_time, end_time, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    events = []
    try:
        start = str(start_time)
        end = str(end_time)
        url = "https://api-prod.wallstreetcn.com/apiv1/finfo/calendars?start=" + start + "&end=" + end
        print(url)
        response = requests.get(url, headers=headers)

        json_data = JSON(str(response.text), encoding='utf-8')

        data = json_data["data"]["items"]
        data.sort(key=lambda x: x["timestamp"])  # 按照日期排序

        for info in data:
            country = info["country"]
            title = info["title"]
            importance = str(info["importance"])
            actual = info["actual"]
            forecast = info["forecast"]
            previous = info["previous"]
            date = time.strftime("%Y-%m-%d", time.localtime(info["timestamp"]))
            if importance == '3':
                event = date + "\t" + country + "\t" + title + "\t" + importance + "\t" + actual + "\t" + forecast + "\t" + previous
                events.append(event)

    except Exception as err:
        print("|||test failed ! didn't get the right content: "+str(err)+' ||| ' + url)
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return get_data_v2(start_time, end_time, retries - 1)
        else:
            print("|||failed in scraping : %s|||" % url)

    return events


"""
本程序意在爬取每周周一周周六的数据，计划每周六下午六点后执行
"""


@fn_timer
def main():
    # 获得当前时间戳
    now = datetime.datetime.now()  # 时间数组格式
    # 转换当日零时的时间，即每周周六零点时间
    saturday = now.strftime("%Y-%m-%d") + " 00:00:00"
    # 转换成每周周日零点的时间戳
    sunday = int(time.mktime(time.strptime(saturday, "%Y-%m-%d %H:%M:%S"))) + 86400
    # 爬取选择的时间段为 周一00:00 至 周六23:59
    start = sunday - 6*86400
    end = sunday - 1
    print("本次爬取开始时间： ")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)))
    print("本次爬取截至时间： ")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end)))

    # 爬取结果
    events = get_data_v2(start, end)
    print(" 本次获取的新闻总条数为: " + str(len(events)) + " 条")
    print(events)

    path = 'C:/workspace/GitHub/data/WebCrawler/WallStreetCN/'
    file_date = datetime.datetime.today().strftime('%Y%m%d')
    file_name = 'wall_street_calendar_' + file_date + '.txt'
    file = path + file_name

    sender = 'hi_iamarobot@sina.com'
    receivers = '****@foxmail.com,****@qq.com'
    subject = '大家好，我开始表演了'
    content = '欢愉小胖注意听讲！ \n \n今天是北京时间 ' + file_date + ' ! \n' + \
              '本次爬取内容为北京时间本周一（' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)) + \
              '）至本周六（' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '）期间的数据，' + \
              '本次爬取数量为 ' + str(len(events)) + ' 条。 \n' + \
              '好好加班!  别偷懒！ \n  \nFrom Robot W.'
    # print(content)
    attachment_path = file
    attachment = file_name
    # 写入文件
    with open(file, 'w', encoding='utf-8') as f:
        for event in events:
            f.write(event + '\n')
    # 发送结果
    send_mail(sender, receivers, subject, content, attachment, attachment_path)


"""

    # # 算出一周内的时间
    # date_list = []
    #
    # for i in range(1, 8):
    #     print(i)
    #     start = sunday - i*86400
    #     end = start + 86399
    #
    #     date = time.strftime("%Y-%m-%d", time.localtime(start))
    #     date_list.append((date, start, end))
    #
    #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)))
    #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end)))
    # print(date_list)
    # events = []
    # for item in date_list:
    #     res = get_data(item)
    #     print(str(item[0])+" 获得数据: "+str(len(res))+" 条")
    #     events.extend(res)
    #     time.sleep(5)
    #
    # print("本次获取的新闻总条数为： " + str(len(events)) + "条，具体如下：")
    # print(events)
    #
    # with open(file, 'w', encoding='utf-8') as f:
    #     for event in events:
    #         f.write(event + '\n')
    #
    # send_mail(sender, receivers, subject, content, attachment, attachment_path)
"""

if __name__ == '__main__':

    main()

    print('good')
