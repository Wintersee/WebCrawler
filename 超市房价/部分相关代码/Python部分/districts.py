#coding=utf8

import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON

URL = 'http://esf.fang.com'
RESIDENCE_URL = 'http://esf.fang.com/housing/'


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        time.sleep(round(random.uniform(1, 5), 2))
        response = requests.get(url, headers=headers)
        print(response.encoding)
        if response.encoding == 'gb2312':
            data = response.content.decode("gbk").encode('utf-8')
        if response.encoding == 'ISO-8859-1':
            data = response.content.decode("GB18030").encode('utf-8')
        # data = response.content.decode("gbk").encode('utf-8')

        soup = BeautifulSoup(data, "html.parser")

        test = soup.find('div', attrs={'class': 's4Box'}).getText()

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


def get_districts_urls(link):
    print("---getting districts  ---")

    soup = download_page(link)
    link_list = []
    alphabet_list = soup.findAll('div', attrs={'class': 'sq-info mt10'})
    for letter in alphabet_list:
        districts = letter.findAll('a')
        for district in districts:
            link_list.append(district.get('href'))
    print(len(link_list))
    return link_list


def go_thread(link):
    print('go go go!!!')
    url = URL + link
    soup = download_page(url)

    page_num = get_page_num(soup)
    print('in ' + url + 'there are ' + str(page_num) + ' pages  ')

    for i in range(1, page_num+1):
        results = []

        page_url = url[0:-5] + str(i) + '_0_0/'
        print(page_url)

        soup = download_page(page_url)
        # print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        # print(soup)
        # print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        residence_list = soup.findAll('a', attrs={'class': 'plotTit'})
        print(str(len(residence_list)) + ' residence ')

        for residence in residence_list:
            residence_id = get_id(residence.get('href'))
            print(residence_id)
            re = get_record(residence_id)
            results.append(re)

        with open('fangtianxia_beijing.txt', 'a') as f:
            for re in results:
                f.write(re + '\n')
                print('+1', end=' ')


def get_page_num(soup):
    residence_sum = soup.find('b', attrs={'class': 'findplotNum'}).getText()
    residence_sum = int(residence_sum)
    page_num = math.ceil(residence_sum / 20)
    # print(residence_sum)

    return page_num


def get_id(link):
    print(link)
    detail_soup = download_page(link)
    # print(detail_soup)
    residence_id = detail_soup.find('input', attrs={'id': "projCode"}).value
    return residence_id


def get_record(residence_id, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    xhr_url = 'http://esf.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url += str(residence_id)

    json_data = ''

    try:
        time.sleep(round(random.uniform(0, 3), 2))
        response = requests.get(xhr_url, headers=headers)
        data = response.text
        print(data)
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
    print(json_data)
    info = json_data['project'][0]
    result = info['projname'] + '\t' + info['coverimg'] + '\t' + info['avgprice'][0:-4] + '\t' + info['coordx'] + '\t' \
             + info['coordy'] + '\t' + info['addresslong'] + '\t' + info['purpose']

    return result


# def go_thread(num):
#     print('!!!new thread mission!!!')
#     results = []
#     url_list = get_urls(num)
#
#     for url in url_list:
#
#         try:
#             re = parse_page(url)
#             results.append(re)
#             print('+1', end='')
#         except Exception as err:
#             print("*** no result, reason: " + str(err) + "***")
#             # print(err)
#             with open('shanghai_failed_to_parse.txt', 'a') as f:
#                 f.write(url+'\n')
#
#     lines[0] += len(results)
#     with open('shanghai.txt', 'a') as f:
#         for res in results:
#             f.write(res)
#         # print("20 xiaoqu written successfully \n")
#         print("+++%d xiaoqu in file +++" % lines[0])


@fn_timer
def main():
    # urls = get_districts_urls(RESIDENCE_URL)
    #
    # pool = ThreadPool(5)
    # pool.map(go_thread, urls)
    # pool.close()
    # pool.join()

    go_thread('/housing/1_1121_0_0_0_0_1_0_0/')

    print("good good ")

if __name__ == '__main__':
    # global lines
    # lines = 1
    main()
    print('good')
