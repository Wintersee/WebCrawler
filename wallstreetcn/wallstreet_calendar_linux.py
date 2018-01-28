# coding: utf-8

# 计划北京时间每周六17：05，对应时间为服务器时间 周六04：05
import requests
import random
from json import loads as JSON
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import timedelta, timezone, datetime
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = datetime.now()
        print("Listen! Go! The time is "+ str(t0))
        result = function(*args, **kwargs)
        t1 = datetime.now()
        print("Listen! Over! The time is "+ str(t1))
        print("Total time running %s: %s seconds" %
              (function.__name__, str(t1 - t0))
              )
        return result

    return function_timer


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
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")


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


@fn_timer
def main():
    # 获得当前时间戳
    now = datetime.now()  # 04：00
    # 转换北京时间周日零时，即服务器时间周六11：00
    ny_bj_sunday = now.strftime("%Y-%m-%d") + " 11:00:00"
    # 转换成北京时间周日零点的时间戳
    bj_sunday_timestamp = int(time.mktime(time.strptime(ny_bj_sunday, "%Y-%m-%d %H:%M:%S")))
    # 爬取选择的时间段为 周一00:00 至 周六23:59
    start = bj_sunday_timestamp - 6*86400
    end = bj_sunday_timestamp - 1
    # 46800 是13个小时的时差, 86400 是24h
    print("本次爬取开始时间(北京时间)： ")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start+46800)))
    print("本次爬取截至时间（北京时间）： ")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end+46800)))

    # 爬取结果
    events = get_data_v2(start, end)
    print(" 本次获取的新闻总条数为: " + str(len(events)) + " 条")
    print(events)

    path = '/home/job_results_and_logs/WallStreetCN/'
    # 当前北京时间
    file_date = datetime.today().astimezone(timezone(timedelta(hours=8))).strftime('%Y%m%d')
    file_name = 'wall_street_calendar_' + file_date + '.txt'
    file = path + file_name

    sender = 'hi_iamarobot@sina.com'
    receivers = '****@foxmail.com,****@qq.com'
    subject = '大家好，我要开始表演了' 
    content = '\n欢愉小胖注意听讲！ \n \n今天是北京时间 ' + file_date + ' ! \n' + \
              '本次爬取内容为北京时间本周一（' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start+46800)) + \
              '）至本周六（' + datetime.today().astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S") + '）期间的数据，' + \
              '本次爬取数量为 ' + str(len(events)) + ' 条。 \n' + \
              '好好加班!  别偷懒！ Good day! \n  \nFrom Robot W. at Linux Server'
    print(content)
    attachment_path = file
    attachment = file_name
    # 写入文件
    with open(file, 'w', encoding='utf-8') as f:
        for event in events:
            f.write(event + '\n')
    # 发送结果
    send_mail(sender, receivers, subject, content, attachment, attachment_path)

if __name__ == '__main__':

    main()

    print('good')
