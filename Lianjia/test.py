#coding=utf8

import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool

import datetime
from functools import wraps

URL = 'http://sh.lianjia.com'
xiaoqu_url = 'http://sh.lianjia.com/xiaoqu/d'
detail_url = 'http://sh.lianjia.com/xiaoqu/5011102207057.html'
lines = [0]


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = datetime.datetime.now()
        print(t0)
        result = function(*args, **kwargs)
        t1 = datetime.datetime.now()
        print(t1)
        print("Total time running %s: %s seconds" %
              (function.__name__, str(t1 - t0))
              )
        return result

    return function_timer


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    # time.sleep(0.5)
    try:
        time.sleep(round(random.uniform(1, 5), 2))
        response = requests.get(url, headers=headers)
        data = response.content

        soup = BeautifulSoup(data, "html.parser")
        test = soup.find('div', attrs={'class': 'label fl'}).getText()

    except Exception as err:
        print("|||fail to download the page, reason: "+str(err)+'|||')
        # print(str(err)+'|||', end='')
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return download_page(url, retries - 1)
        else:
            print("|||failed in scaping : %s|||" % url)
            with open('shanghai_failed_to_download.txt', 'a') as f:
                f.write(url+'\n')
            # return ''
    return soup


def get_page_num(link):
    # http = download_page(link)
    # soup = BeautifulSoup(http, "html.parser")
    soup = download_page(link)
    xiaoqu_sum = soup.find('div', attrs={'class': 'list-head clear'}).find('span').getText()
    xiaoqu_sum = int(xiaoqu_sum)
    page_num = math.ceil(xiaoqu_sum / 20)
    print(xiaoqu_sum)
    print(page_num)
    return page_num


def get_urls(num):
    print("---getting page %d ---" % num)
    link = xiaoqu_url + str(num)

    # results = []
    # soup = BeautifulSoup(download_page(link), "html.parser")
    soup = download_page(link)
    link_list = []
    xiaoqu_list = soup.findAll('div', attrs={'class': 'info-panel'})

    for xiaoqu in xiaoqu_list:
        link = xiaoqu.find('a').get('href')
        link_list.append(link)

    return link_list


def parse_page(link):
    detail_link = URL + link
    detail_soup = download_page(detail_link)

    price = detail_soup.find('span', attrs={'class': "p"}).getText().strip()
    coord = detail_soup.find('a', attrs={'class': 'actshowMap'}).get('xiaoqu')

    coord = coord.split(',')

    latitude = coord[1]
    longitude = coord[0].strip('[')
    # name = coord[2].strip(']').strip("'")
    name = coord[2][2:-2]

    # get address
    spans = detail_soup.find('span', attrs={'class': 't'}).findAll('span')
    adr = spans[0].getText()[1:-1] + spans[1].getText().strip()

    result = name + '\t' + link + '\t' + price + '\t' + latitude + '\t' + longitude + '\t' + adr

    # get other info
    others = []
    other_info = detail_soup.findAll('span', attrs={'class': 'other'})

    for info in other_info:
        others.append(info.getText().strip())

    for i in [0, 1, 5, 6]:
        result += '\t' + others[i]

    result += '\n'
    return result

    # time.sleep(0.5)


def go_thread(num):
    print('!!!new thread mission!!!')
    results = []
    url_list = get_urls(num)

    for url in url_list:

        try:
            re = parse_page(url)
            results.append(re)
            print('+1', end='')
        except Exception as err:
            print("*** no result, reason: " + str(err) + "***")
            # print(err)
            with open('shanghai_failed_to_parse.txt', 'a') as f:
                f.write(url+'\n')

    lines[0] += len(results)
    with open('shanghai.txt', 'a') as f:
        for res in results:
            f.write(res)
        # print("20 xiaoqu written successfully \n")
        print("+++%d xiaoqu in file +++" % lines[0])


@fn_timer
def main():

    page_num = get_page_num(xiaoqu_url + '1')

    pool = ThreadPool(20)
    pool.map(go_thread, list(range(1, page_num + 1)))
    pool.close()
    pool.join()
    print("good good ")

if __name__ == '__main__':
    # global lines
    # lines = 1
    main()
    print('good')
