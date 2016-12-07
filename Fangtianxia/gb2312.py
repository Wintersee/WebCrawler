#coding=utf8

import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON
import re
from io import StringIO

URL = 'http://esf.fang.com'
RESIDENCE_URL = 'http://esf.fang.com/housing/'


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        time.sleep(round(random.uniform(1, 5), 2))
        response = requests.get(url, headers=headers)
        # print(response.text)
        print(response.encoding)
        if response.encoding == 'gb2312':
            data = response.content.decode("gbk").encode('utf-8')
        if response.encoding == 'ISO-8859-1':
            data = response.content

            # data = response.content.decode("ISO-8859-1").encode('utf-8')
        #data = response.text

        soup = BeautifulSoup(data, "html.parser", from_encoding="GB18030")

        if 'aspx?newcode=' not in url:
            test = soup.find('a', attrs={'href': 'http://wap.fang.com/xc/mobile.html'}).getText()

    except Exception as err:
        print("|||test failed ! didn't get the right content: "+str(err)+'|||')
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return download_page(url, retries - 1)
        else:
            print("|||failed in scaping : %s|||" % url)
            with open('fangtianxia_beijing_failed_to_download.txt', 'a') as f:
                f.write(url+'\n')
            # return ''
    return soup


def get_record_2(link):

    soup = download_page(link)
    result = ''
    try:
        info = soup.find('div', attrs={'class': 'lpblbox borderb01'})
        name = info.find('span', attrs={'class': 'biaoti'}).getText()
        price = info.find('strong', attrs={'class': 'org font14'}).getText()
        address = info.find('span', attrs={'class': 'gray6'}).find('span').getText()
        purpose = info.find('div', attrs={'class': 'xiangqing'}).find('dd').getText()[5:]

        map_url = soup.find('div', attrs={'id': 'map'}).find('iframe').get('src')
        map_soup = download_page(map_url)
        script = map_soup.find('script', attrs={'type': 'text/javascript', 'language': 'javascript'})
        pattern = re.compile(r'px\:(.*)\"\,')
        match = pattern.search(str(script))
        res = match.group().split(',')
        px = res[0][4:-1]
        py = res[1][4:-1]

    except Exception as err:
        print("|||failed get_record_2  |||" + str(err))
        with open('fangtianxia_beijing_failed.txt', 'a') as f:
            f.write(link + '\n')
    else:
        result = name + '\t' + link + '\t' + price + '\t' + px + '\t' + py + '\t' + address + '\t' + purpose
        print(result)

    return result


def get_record(residence_id, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    xhr_url = 'http://esf.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url += str(residence_id)
    print(xhr_url)

    result = ''

    try:
        time.sleep(round(random.uniform(0, 3), 2))
        response = requests.get(xhr_url, headers=headers)
        print(response.status_code)
        data = response.text
        print('=====')
        # print(data)
        json_data = JSON(str(data))

    except Exception as err:
        print("|||fail to get json, reason: " + str(err) + '|||')
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries - 1))
            return get_record(residence_id, retries - 1)
        else:
            print("|||failed in : %d |||" % residence_id)
            with open('fangtianxia_beijing_failed_to_download_json.txt', 'a') as f:
                f.write(residence_id + '\n')
    else:
        # print(json_data)
        info = json_data['project'][0]
        result = info['projname'] + '\t' + info['xiaoqudomain'] + '\t' + info['avgprice'][0:-4] + '\t' + info['coordx'] + '\t' \
                 + info['coordy'] + '\t' + info['addresslong'] + '\t' + info['purpose']
        print(result)
    return result


def get_id(link):
    print(link+'     lol')
    detail_soup = download_page(link)
    # print(detail_soup)
    residence_id = detail_soup.find('input', attrs={'id': "projCode"}).get('value')
    print(str(residence_id))
    return residence_id

@fn_timer
def main():
    # urls = get_districts_urls(RESIDENCE_URL)
    #
    # pool = ThreadPool(5)
    # pool.map(go_thread, urls)
    # pool.close()
    # pool.join()

    res = get_record_2('http://jianwaisoho010.fang.com/office/')

    print(res)

    html = get_record(get_id('http://daduhuiwk.fang.com/'))
    print(html)

if __name__ == '__main__':
    # global lines
    # lines = 1
    main()
    print('good')
