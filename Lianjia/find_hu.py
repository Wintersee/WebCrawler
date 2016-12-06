#coding=utf8

import requests
from bs4 import BeautifulSoup
import time, random


URL = 'http://sh.lianjia.com'
xiaoqu_url = 'http://sh.lianjia.com/xiaoqu/d'
detail_url = 'http://sh.lianjia.com/xiaoqu/5011102207057.html'
lines = [0]


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


def parse_page_for_noprice(link):
    detail_link = URL + link
    detail_soup = download_page(detail_link)

    price = detail_soup.find('div', attrs={'class': "item col1"}).find('span').getText().strip()
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


# url_more = []
# url_less = []
lines = []
with open('shanghai_noprice.txt', 'r') as f:
    lines = f.readlines()

# print(url_more[0:15])
# print(len(url_more))
# url_more = set(url_more)
print(len(lines))

with open('shanghai.txt', 'a') as f:
    for line in lines:
        f.write(line)
            # cols = line.strip().split('\t')
            #
            # url_less.append(cols[1][8:-5])

# print(url_less[0:10])
# print(len(url_less))
# url_less = set(url_less)
# print(len(url_less))

# print(url_more.difference(url_less))
#
# print(parse_page_for_noprice('/xiaoqu/5011000011288.html'))