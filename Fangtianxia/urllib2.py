import requests
from bs4 import BeautifulSoup
import time, random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON
import re
import urllib

# URL = 'http://esf.sy.fang.com'
# RESIDENCE_URL = 'http://esf.sy.fang.com/housing/'
# CITY = 'shenyang'

# URL = 'http://esf.gz.fang.com'
# RESIDENCE_URL = 'http://esf.gz.fang.com/housing/'
# CITY = 'guangzhou'

URL = 'http://esf.nn.fang.com'
RESIDENCE_URL = 'http://esf.nn.fang.com/housing/'
CITY = 'nanning'



city_file = 'results/fangtianxia_' + CITY + '.txt'
city_xiezilou_failed_file = 'results/fangtianxia_' + CITY + '_xiezilou_failed.txt'
city_zhuzhai_failed_file = 'results/fangtianxia_' + CITY + '_zhuzhai_failed.txt'
city_luanma_failed_file = 'results/fangtianxia_' + CITY + '_luanma_failed.txt'
city_url_failed_file = 'results/fangtianxia_' + CITY + '_url_failed.txt'

# JINAN_URL = 'http://esf.jn.fang.com/'
# JINAN_RESIDENCE_URL = 'http://esf.jn.fang.com/housing/'


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    try:
        time.sleep(round(random.uniform(1, 5), 2))

        # # headers = {'User-Agent': user_agent}
        # # data = urllib.parse.urlencode(values)
        # # req = urllib.request.Request(url, headers)
        # response = urllib.request.urlopen(url, headers)
        # the_page = response.read()
        # print(the_page.decode("utf8"))

        response = requests.get(url, headers=headers)
        # print(response.encoding + '  response')
        if response.encoding == 'gb2312':
            data = response.content.decode("GB18030").encode('utf-8')
        # if response.encoding == 'ISO-8859-1':
        else:
            data = response.content.decode("GB18030").encode('utf-8')

        soup = BeautifulSoup(data, "html.parser")

        if 'aspx?newcode=' not in url:
            test = soup.find('a', attrs={'href': 'http://wap.fang.com/xc/mobile.html'}).getText()

    except Exception as err:
        print("|||test failed ! didn't get the right content: "+str(err)+' ||| ' + url)
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return download_page(url, retries - 1)
        else:
            print("|||failed in scaping : %s|||" % url)
            with open(city_url_failed_file, 'a', 'utf-8') as f:
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

    residence_sum = soup.find('b', attrs={'class': 'findplotNum'}).getText()
    print(residence_sum)

    return link_list


def get_page_num(soup):
    residence_sum = soup.find('b', attrs={'class': 'findplotNum'}).getText()
    residence_sum = int(residence_sum)
    page_num = math.ceil(residence_sum / 20)
    return page_num


def get_id(link):
    # print(link+'     lol')
    detail_soup = download_page(link)
    # print(detail_soup)
    residence_id = detail_soup.find('input', attrs={'id': "projCode"}).get('value')
    # print(str(residence_id))
    return residence_id


def get_ids(soup):
    script = soup.findAll('script', attrs={'type': 'text/javascript', 'src': '', 'language': ''})[1]

    pattern = re.compile(r'showhouseid(.*)\}')
    match = pattern.search(str(script))
    ids = match.group()[14:-2].split(',')
    print(ids)
    return ids


def get_record_2(div):
    # 还在小区列表
    name = div.find('a', attrs={'class': 'plotTit'}).getText()
    link = div.find('a', attrs={'class': 'plotTit'}).get('href')
    price_div = div.find('p', attrs={'class': 'priceAverage'})
    if price_div:
        price = price_div.find('span').getText()
    else:
        price = '无'
    purpose = div.find('span', attrs={'class': 'plotFangType'}).getText()
    address = '无'

    # 进入小区详细信息网页
    if 'http' not in link:
        link = URL + link

    try:
        detail_soup = download_page(link)

        address_span = detail_soup.find('span', attrs={'class': 'gray6'})
        if address_span:
            address = address_span.find('span').getText()
        map_div = detail_soup.find('div', attrs={'id': 'map'})
        if map_div:
            map_url = map_div.find('iframe').get('src')
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
            v = 20
            while v:
                response = requests.get(map_url, headers=headers)
                data = response.content
                map_soup = BeautifulSoup(data, "html.parser")
                script = map_soup.find('script', attrs={'type': 'text/javascript', 'language': 'javascript'})
                if script:
                    v = 0
                else:
                    v -= 1
            pattern = re.compile(r'px\:(.*)\"\,')
            match = pattern.search(str(script))
            res = match.group().split(',')
            px = res[0][4:-1]
            py = res[1][4:-1]
        else:
            px = '无'
            py = '无'
        #     珠海
        # map_frame = detail_soup.find('iframe', attrs={'id': 'iframe_map'})
        # # 判断页面是否含有信息
        # if map_frame:
        #     map_url = map_frame.get('src')
        #     # 进入地图信息网页
        #     # map_soup = download_page(map_url)
        #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        #     response = requests.get(map_url, headers=headers)
        #     data = response.content
        #     map_soup = BeautifulSoup(data, "html.parser")
        #     script = map_soup.find('script')
        #     pattern = re.compile(r'mapx\"(.*)\_x')
        #     match = pattern.search(str(script))
        #     res = match.group().split(',')
        #     px = res[0][7:-1]
        #     py = res[1][8:-1]
        # else:
        #     px = '无'
        #     py = '无'
    except Exception as err:
        print("|||failed get_record_2  |||" + str(err))
        with open(city_xiezilou_failed_file, 'a') as f:
            f.write(link + '\n')
    else:
        result = name + '\t' + link + '\t' + price + '\t' + px + '\t' + py + '\t' + address + '\t' + purpose
        print(result)
        return result

# -------------- for other style
        # try:
        #     # info = soup.find('div', attrs={'class': 'lpblbox borderb01'})
        #     # name = info.find('span', attrs={'class': 'biaoti'}).getText()
        #     # price = info.find('strong', attrs={'class': 'org font14'}).getText()
        #     # address = info.find('span', attrs={'class': 'gray6'}).find('span').getText()
        #     # purpose = info.find('div', attrs={'class': 'xiangqing'}).find('dd').getText()[5:]
        #
        #     detail_soup = download_page(link)
        #     map_url = detail_soup.find('div', attrs={'id': 'map'}).find('iframe').get('src')
        #     map_soup = download_page(map_url)
        #     script = map_soup.find('script', attrs={'type': 'text/javascript', 'language': 'javascript'})
        #     pattern = re.compile(r'px\:(.*)\"\,')
        #     match = pattern.search(str(script))
        #     res = match.group().split(',')
        #     px = res[0][4:-1]
        #     py = res[1][4:-1]
        #
        # except Exception as err:
        #     print("|||failed get_record_2  |||" + str(err))
        #     with open(city_xiezilou_failed_file, 'a') as f:
        #         f.write(link + '\n')
        # else:
        #     result = name + '\t' + link + '\t' + price + '\t' + px + '\t' + py + '\t' + address + '\t' + purpose
        #     print(result)
        #     return result


def get_record(residence_id, retries=20):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    # xhr_url = 'http://esf.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url = URL + '/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url += str(residence_id)
    # print(xhr_url)

    result = ''

    try:
        time.sleep(round(random.uniform(0, 3), 2))
        response = requests.get(xhr_url, headers=headers)
        data = response.text

        json_data = JSON(str(data))

    except Exception as err:
        print("|||fail to get json, reason: " + str(err) + ' ||| ' + xhr_url)
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries - 1))
            return get_record(residence_id, retries - 1)
        else:
            print("|||failed in : %d |||" % residence_id)
            with open(city_zhuzhai_failed_file, 'a') as f:
                f.write(residence_id + '\n')
    else:
        # print(json_data)
        info = json_data['project'][0]
        # print(info['xiaoqudomain']+ '                      lol')
        result = info['projname'] + '\t' + info['xiaoqudomain'] + '\t' + info['avgprice'][0:-4] + '\t' + info['coordx'] + '\t' \
                 + info['coordy'] + '\t' + info['addresslong'] + '\t' + info['purpose']
        print(result)
    return result


def go_thread(link):
    print('go go go!!!')
    try:
        url = URL + link
        soup = download_page(url)
        page_num = get_page_num(soup)
        for i in range(1, page_num+1):
            results = []
            page_url = url[0:-6] + str(i) + '_0_0/'
            soup = download_page(page_url)
            ids = get_ids(soup)
            div_list = soup.findAll('div', attrs={'class': 'list rel'})

            for div, residence_id in zip(div_list, ids):
                residence_type = div.find('span', attrs={'class': 'plotFangType'}).getText()
                # print(residence_type)
                if residence_type == '写字楼' or residence_type == '商铺':
                    res = get_record_2(div)
                else:
                    res = get_record(residence_id)
                if re:
                    results.append(res)
            with open(city_file, 'a') as f:
                for res in results:
                    try:
                        f.write(res + '\n')
                        print('+1', end=' ')
                    except Exception as err:
                        print('           so sad *_* :' + str(err))
                        pattern = re.compile(r'http\:(.*)\/')
                        match = pattern.search(str(res))
                        res = match.group()
                        if res:
                            with open(city_luanma_failed_file, 'a') as sad:
                                sad.write(res + '\n')
    except Exception as err:
        print('lol   go thread  :' + str(err))


def get_amount(link):
    print('go go go!!!')
    num = 0
    try:
        url = URL + link
        soup = download_page(url)
        page_num = get_page_num(soup)
        for i in range(1, page_num+1):
            results = []
            page_url = url[0:-6] + str(i) + '_0_0/'
            print(page_url)
            soup = download_page(page_url)
            ids = get_ids(soup)
            div_list = soup.findAll('div', attrs={'class': 'list rel'})

            for div, residence_id in zip(div_list, ids):
                residence_type = div.find('span', attrs={'class': 'plotFangType'}).getText()
                # print(residence_type)
                # if residence_type == '写字楼' or residence_type == '商铺':
                #     res = get_record_2(div)
                # else:
                #     res = get_record(residence_id)
                # if re:
                #     results.append(res)
                num += 1
            # with open(city_file, 'a') as f:
            #     for res in results:
            #         try:
            #             f.write(res + '\n')
            #             print('+1', end=' ')
            #         except Exception as err:
            #             print('           so sad *_* :' + str(err))
            #             pattern = re.compile(r'http\:(.*)\/')
            #             match = pattern.search(str(res))
            #             res = match.group()
            #             if res:
            #                 with open(city_luanma_failed_file, 'a') as sad:
            #                     sad.write(res + '\n')
    except Exception as err:
        print('lol   go thread  :' + str(err))
    else:
        return num


@fn_timer
def main():
    urls = get_districts_urls(RESIDENCE_URL)

    # urls = get_districts_urls(JINAN_RESIDENCE_URL)

    print(urls)
    # print(get_amount('/housing/_7030_0_0_0_0_3_0_0/'))

    num = 0

    # for url in urls:
    #     num += get_amount(url)
    #
    pool = ThreadPool(5)
    results = pool.map(get_amount, urls)
    pool.close()
    pool.join()

    for res in results:
        num += res
    print(num)

    # pool = ThreadPool(5)
    # pool.map(go_thread, urls)
    # pool.close()
    # pool.join()

    go_thread('/housing/_7028_0_0_0_0_3_0_0/')

    # get_ids(download_page('http://esf.zh.fang.com/housing/__0_0_0_0_1_0_0/'))

    print("good good ")

if __name__ == '__main__':
    main()
    print('good')
