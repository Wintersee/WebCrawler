import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON
import re

URL = 'http://esf.fang.com'
RESIDENCE_URL = 'http://esf.fang.com/housing/'

JINAN_URL = 'http://esf.jn.fang.com/'
JINAN_RESIDENCE_URL = 'http://esf.jn.fang.com/housing/'


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    try:
        time.sleep(round(random.uniform(1, 5), 2))
        response = requests.get(url, headers=headers)
        # print(response.encoding + '  response')
        if response.encoding == 'gb2312':
            data = response.content.decode("gbk").encode('utf-8')
        if response.encoding == 'ISO-8859-1':
            data = response.content

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


def get_districts_urls(link):
    print("---getting districts  ---")

    soup = download_page(link)
    link_list = []
    alphabet_list = soup.findAll('div', attrs={'class': 'sq-info mt10'})
    for letter in alphabet_list:
        districts = letter.findAll('a')
        for district in districts:
            link_list.append(district.get('href'))
    return link_list


def get_page_num(soup):
    residence_sum = soup.find('b', attrs={'class': 'findplotNum'}).getText()
    residence_sum = int(residence_sum)
    page_num = math.ceil(residence_sum / 20)
    # print(residence_sum)

    return page_num


def get_id(link):
    print(link+'     lol')
    detail_soup = download_page(link)
    # print(detail_soup)
    residence_id = detail_soup.find('input', attrs={'id': "projCode"}).get('value')
    # print(str(residence_id))
    return residence_id


def get_record_2(link):

    # xhr_url = 'http://esf.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    # xhr_url += str(residence_id)
    # print(xhr_url)

    # map_url = 'http://esf.fang.com/newsecond/map/newhouse/ShequMap.aspx?newcode=' + str(residence_id)

    soup = download_page(link)
    result = ''
    try:
        info = soup.find('div', attrs={'class': 'lpblbox borderb01'})
        name = info.find('span', attrs={'class': 'biaoti'}).getText()
        price = info.find('strong', attrs={'class': 'org font14'}).getText()
        address = info.find('span', attrs={'class': 'gray6'}).find('span').getText()
        purpose = info.find('div', attrs={'class': 'xiangqing'}).find('dd').getText()[5:]

        map_url = soup.find('div', attrs={'id': 'map'}).find('iframe').get('src')
        print('------------------------------' + map_url)
        map_soup = download_page(map_url)
        script = map_soup.find('script', attrs={'type': 'text/javascript', 'language': 'javascript'})
        pattern = re.compile(r'px\:(.*)\"\,')
        match = pattern.search(str(script))
        res = match.group().split(',')
        px = res[0][4:-1]
        py = res[1][4:-1]

    except Exception as err:
        print("|||failed get_record_2  |||" + str(err))
        with open('jinan/fangtianxia_jinan_failed.txt', 'a') as f:
            f.write(link + '\n')
    else:
        result = name + '\t' + link + '\t' + price + '\t' + px + '\t' + py + '\t' + address + '\t' + purpose
        print(result)

    return result


def get_record(residence_id, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    # xhr_url = 'http://esf.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url = 'http://esf.jn.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url += str(residence_id)
    # print(xhr_url)

    result = ''

    try:
        time.sleep(round(random.uniform(0, 3), 2))
        response = requests.get(xhr_url, headers=headers)
        data = response.text

        json_data = JSON(str(data))

    except Exception as err:
        print("|||fail to get json, reason: " + str(err) + '|||')
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries - 1))
            return get_record(residence_id, retries - 1)
        else:
            print("|||failed in : %d |||" % residence_id)
            with open('jinan/fangtianxia_jinan_failed_to_download_json.txt', 'a') as f:
                f.write(residence_id + '\n')
    else:
        # print(json_data)
        info = json_data['project'][0]
        result = info['projname'] + '\t' + info['xiaoqudomain'] + '\t' + info['avgprice'][0:-4] + '\t' + info['coordx'] + '\t' \
                 + info['coordy'] + '\t' + info['addresslong'] + '\t' + info['purpose']
        print(result)
    return result


def go_thread(link):
    print('go go go!!!')
    try:
        # url = URL + link
        url = JINAN_URL + link
        soup = download_page(url)
        page_num = get_page_num(soup)
        for i in range(1, page_num+1):
            results = []
            page_url = url[0:-6] + str(i) + '_0_0/'
            soup = download_page(page_url)
            div_list = soup.findAll('dl', attrs={'class': 'plotListwrap clearfix'})
            for div in div_list:
                residence = div.find('a', attrs={'class': 'plotTit'}).get('href')
                # print('residence :' + residence)
                residence_type = div.find('span', attrs={'class': 'plotFangType'}).getText()
                # print(residence_type)
                if residence_type == '写字楼' or residence_type == '商铺':
                    res = get_record_2(residence)
                else:
                    residence_id = get_id(residence)
                    # print(residence_id)
                    res = get_record(residence_id)
                    # print(res)
                if re:
                    results.append(res)
            with open('jinan/fangtianxia_jinan.txt', 'a') as f:
                for res in results:
                    try:
                        f.write(res + '\n')
                    except Exception as err:
                        print('           so sad *_* :' + str(err))
                        pattern = re.compile(r'http\:(.*)\/')
                        match = pattern.search(str(res))
                        res = match.group()
                        with open('jinan/fangtianxia_jinan_luanma.txt', 'a') as sad:
                            sad.write(res + '\n')
                    print('+1', end=' ')
    except Exception as err:
        print('lol   go thread  :' + str(err))


#

@fn_timer
def main():
    # urls = get_districts_urls(RESIDENCE_URL)

    urls = get_districts_urls(JINAN_RESIDENCE_URL)

    print(urls)

    pool = ThreadPool(20)
    pool.map(go_thread, urls)
    pool.close()
    pool.join()

    # go_thread('/housing/1_5510_0_0_0_0_1_0_0/')

    print("good good ")

if __name__ == '__main__':
    main()
    print('good')
