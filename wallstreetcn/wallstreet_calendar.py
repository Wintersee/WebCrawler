import requests
from bs4 import BeautifulSoup
import time
import datetime
import random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON
import re
import time
import datetime


PATH = 'C:/workspace/GitHub/data/WebCrawler/WallStreetCN/'


today = datetime.datetime.today().strftime('%Y%m%d')

file = PATH + 'wall_street_calendar_' + today + '.txt'


def get_data(arr, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    events = []
    try:
        start = str(arr[1])
        end = str(arr[2])
        url = "https://api-prod.wallstreetcn.com/apiv1/finfo/calendars?start=" + start + "&end=" + end
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
            return get_data(url, retries - 1)
        else:
            print("|||failed in scraping : %s|||" % url)

    return events




@fn_timer
def main():

    # 获得当前时间戳
    now = datetime.datetime.now()  # 时间数组格式
    # 转换当日零时的时间，转转换成时间戳
    today = now.strftime("%Y-%m-%d") + " 00:00:00"
    sunday = int(time.mktime(time.strptime(today, "%Y-%m-%d %H:%M:%S")))
    print(today)
    print(sunday)

    # 算出一周内的时间
    date_list = []

    for i in range(1, 8):
        print(i)
        start = sunday - i*86400
        end = start + 86399

        date = time.strftime("%Y-%m-%d", time.localtime(start))
        date_list.append((date, start, end))

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end)))

    events = []
    for item in date_list:
        res = get_data(item)
        print(len(res))
        events.extend(res)
    print(events)

    with open(file, 'w', encoding='utf-8') as f:
        for event in events:
            f.write(event + '\n')


if __name__ == '__main__':

    main()

    print('good')
