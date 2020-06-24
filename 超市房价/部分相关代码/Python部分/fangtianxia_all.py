import requests
from bs4 import BeautifulSoup
import time
import random
import math
from multiprocessing.dummy import Pool as ThreadPool
from functions import fn_timer
from json import loads as JSON
import re

# URL = 'http://esf.sy.fang.com'
# RESIDENCE_URL = 'http://esf.sy.fang.com/housing/'
# CITY = 'shenyang'

# URL = 'http://esf.gz.fang.com'
# RESIDENCE_URL = 'http://esf.gz.fang.com/housing/'
# CITY = 'guangzhou'

# URL = 'http://esf.sjz.fang.com'
# RESIDENCE_URL = 'http://esf.sjz.fang.com/housing/'
# CITY = 'shijiazhuang'

# URL = 'http://esf.cq.fang.com'
# RESIDENCE_URL = 'http://esf.cq.fang.com/housing/'
# CITY = 'chongqing'

# URL = 'http://esf.wuhan.fang.com'
# RESIDENCE_URL = 'http://esf.wuhan.fang.com/housing/'
# CITY = 'wuhan'

# URL = 'http://esf.sz.fang.com'
# RESIDENCE_URL = 'http://esf.sz.fang.com/housing/'
# CITY = 'shenzhen'

# URL = 'http://esf.cd.fang.com'
# RESIDENCE_URL = 'http://esf.cd.fang.com/housing/'
# CITY = 'chengdu'

# URL = 'http://esf.tj.fang.com'
# RESIDENCE_URL = 'http://esf.tj.fang.com/housing/'
# CITY = 'tianjin'

# URL = 'http://esf.suzhou.fang.com'
# RESIDENCE_URL = 'http://esf.suzhou.fang.com/housing/'
# CITY = 'suzhou'

# URL = 'http://esf.xian.fang.com'
# RESIDENCE_URL = 'http://esf.xian.fang.com/housing/'
# CITY = 'xian'

# URL = 'http://esf.zz.fang.com'
# RESIDENCE_URL = 'http://esf.zz.fang.com/housing/'
# CITY = 'zhengzhou'

# URL = 'http://esf.cs.fang.com'
# RESIDENCE_URL = 'http://esf.cs.fang.com/housing/'
# CITY = 'changsha'

# URL = 'http://esf.nn.fang.com'
# RESIDENCE_URL = 'http://esf.nn.fang.com/housing/'
# CITY = 'nanning'

# URL = 'http://esf.qd.fang.com'
# RESIDENCE_URL = 'http://esf.qd.fang.com/housing/'
# CITY = 'qingdao'

# URL = 'http://esf.km.fang.com'
# RESIDENCE_URL = 'http://esf.km.fang.com/housing/'
# CITY = 'kunming'


# 江苏：changzhou cz huaian huaian kunshan ks jiangyin jy nantong tz taizhou taizhou xuzhou xz
CITY = 'yulin'     # nanchang wuxi fuzhou xiamen suzhou hangzhou dalian dongguan nanjing
CITY_SHORT = 'yl'  # nc wuxi fz xm suzhou hz dl dg nanjing
URL = 'http://esf.'+CITY_SHORT+'.fang.com'
RESIDENCE_URL = 'http://esf.'+CITY_SHORT+'.fang.com/housing/'

PROVINCE = '上海'
CITY_NAME = '上海'


PATH = 'C:/workspace/GitHub/data/WebCrawler/Fangtianxia/'
# 正确结果
city_file = PATH + 'fangtianxia_' + CITY + '.txt'
# 获取写字楼，商铺失败的链接
city_xiezilou_failed_file = PATH + 'fangtianxia_' + CITY + '_xiezilou_failed.txt'
# 获取住宅、别墅失败的链接
city_zhuzhai_failed_file = PATH + 'fangtianxia_' + CITY + '_zhuzhai_failed.txt'
# 未知原因的失败 和 获取ids时失败 的小区列表链接
city_failed_file = PATH + 'fangtianxia_' + CITY + '_failed.txt'
# 写入时因特殊字符乱码失败的链接
city_luanma_failed_file = PATH + 'fangtianxia_' + CITY + '_luanma_failed.txt'
# 请求url时失败的链接 ---- 一般不会失败
city_url_failed_file = PATH + 'fangtianxia_' + CITY + '_url_failed.txt'

# JINAN_URL = 'http://esf.jn.fang.com/'
# JINAN_RESIDENCE_URL = 'http://esf.jn.fang.com/housing/'


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    try:
        time.sleep(round(random.uniform(1, 5), 2))
        response = requests.get(url, headers=headers)
        # # print(response.encoding + '  response')
        # if response.encoding == 'gb2312':
        #     data = response.content.decode("GB18030").encode('utf-8')
        # # if response.encoding == 'ISO-8859-1':
        # else:
        #     data = response.content.decode("GB18030").encode('utf-8')
        data = response.content.decode('GB18030', 'replace').encode('utf-8', 'replace')
        # print(data)

        soup = BeautifulSoup(data, "html.parser")

        # print(soup)

        if 'aspx?newcode=' not in url:
            test = soup.find('a', attrs={'href': 'http://wap.fang.com/xc/mobile.html'}).getText()

    except Exception as err:
        print("|||test failed ! didn't get the right content: "+str(err)+' ||| ' + url)
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return download_page(url, retries - 1)
        else:
            print("|||failed in scraping : %s|||" % url)
            with open(city_url_failed_file, 'a', encoding='utf-8') as f:
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
            url = district.get('href')
            url = url[0:-10] + '1_0_1_0_0/'
            link_list.append(url)
    return link_list


def get_page_num(soup):
    residence_sum = soup.find('b', attrs={'class': 'findplotNum'}).getText()
    residence_sum = int(residence_sum)
    page_num = math.ceil(residence_sum / 20)
    return page_num


# def get_id(link):
#     # print(link+'     lol')
#     detail_soup = download_page(link)
#     # print(detail_soup)
#     residence_id = detail_soup.find('input', attrs={'id': "projCode"}).get('value')
#     # print(str(residence_id))
#     return residence_id


def get_ids(soup, link):
    script = soup.findAll('script', attrs={'type': 'text/javascript', 'src': '', 'language': ''})[1]

    pattern = re.compile(r'showhouseid(.*)\}')
    match = pattern.search(str(script))
    if match:
        ids = match.group()[14:-2].split(',')
        print(ids)
        print(link)
    else:
        ids = ''
        # print('------------------------------------------------- get ids failed: ' + link)
        # with open(city_failed_file, 'a') as sad:
        #     sad.write(link + '\n')
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
            v = 10
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
            if match:
                res = match.group().split(',')
                px = res[0][4:-1]
                py = res[1][4:-1]
            else:
                px = '无'
                py = '无'
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
        result = name + '\t' + link + '\t' + price + '\t' + px + '\t' + py + '\t' + address + '\t' + purpose + '\t' \
                 + PROVINCE + '\t' + CITY_NAME
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


def get_record(residence_id, div, retries=5):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    # xhr_url = 'http://esf.fang.com/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url = URL + '/newsecond/Map/Interfaces/baidu/GetTPointByKeyword.aspx?projcode='
    xhr_url += str(residence_id)

    result = ''

    xiaoqu_domain = div.find('a', attrs={'class': 'plotTit'}).get('href')
    if 'http' not in xiaoqu_domain:
        xiaoqu_domain = URL + xiaoqu_domain

    price_div = div.find('p', attrs={'class': 'priceAverage'})
    if price_div:
        price = price_div.find('span').getText()
    else:
        price = '无'

    try:
        time.sleep(round(random.uniform(0, 3), 2))
        response = requests.get(xhr_url, headers=headers)
        # ddata = response.text
        # print('|||||||||||||||||||||||||')
        # print(ddata)
        # print('|||||||||||||||||||||||||')
        data = response.content.decode('gbk', 'replace')
        # print(data)
        # print('|||||||||||||||||||||||||')
        # soup = BeautifulSoup(data, "html.parser")
        #
        # print(response.headers['content-type'])
        # print(response.encoding)
        # print(response.apparent_encoding)
        # print(requests.utils.get_encodings_from_content(response.text))

        json_data = JSON(str(data), encoding='utf-8')
        info = json_data['project'][0]

    except Exception as err:
        print("|||fail to get json, reason: " + str(err) + ' ||| ' + xhr_url)
        if retries > 0:
            time.sleep(random.randint(5, 15))
            print("try again, %d times left" % int(retries - 1))
            return get_record(residence_id, div, retries - 1)
        else:
            print("|||failed in : %s |||" % xhr_url)
            with open(city_zhuzhai_failed_file, 'a') as f:
                f.write(xhr_url + '\n')
    else:
        # print(json_data)

        # print(info['xiaoqudomain']+ '                      lol')
        # 有的小区url已废弃

        if not (xiaoqu_domain or info['xiaoqudomain']):
            xiaoqu_domain = residence_id
        # if info['avgprice'][0:-4]:
        #     avgprice = info['avgprice'][0:-4]
        result = info['projname'] + '\t' + xiaoqu_domain + '\t' + price + '\t' + info['coordx'] + '\t' \
                 + info['coordy'] + '\t' + info['addresslong'] + '\t' + info['purpose'] \
                 + '\t' + PROVINCE + '\t' + CITY_NAME
        print(result)
    return result


def go_thread(link):
    print('go go go!!!')
    url = URL + link
    try:
        soup = download_page(url)
        page_num = get_page_num(soup)
        print(page_num)
        for i in range(1, page_num+1):
            results = []
            page_url = url[0:-6] + str(i) + '_0_0/'
            soup = download_page(page_url)
            ids = get_ids(soup, page_url)

            if ids == '':
                retries = 10
                while retries:
                    print('------------------------------- try to get ids again: ' + page_url)
                    soup = download_page(page_url)
                    ids = get_ids(soup, page_url)
                    if ids:
                        retries = 0
                    else:
                        if retries == 1:
                            print('------------------------------- get ids failed: ' + page_url)
                            with open(city_failed_file, 'a') as sad:
                                sad.write(link + '\n')
                        retries -= 1

            if ids:
                div_list = soup.findAll('div', attrs={'class': 'list rel'})
                for div, residence_id in zip(div_list, ids):
                    residence_type = div.find('span', attrs={'class': 'plotFangType'}).getText()
                    # print(residence_type)
                    if residence_type == '写字楼' or residence_type == '商铺':
                        res = get_record_2(div)
                    else:
                        # 部分城市的json数据里不含链接及价格
                        res = get_record(residence_id, div)
                    if res:
                        results.append(res)
                with open(city_file, 'a', encoding='utf-8') as f:
                    for result in results:
                        try:
                            f.write(result + '\n')
                            print('+1', end=' ')
                        except Exception as err:
                            print('   mess!!!        so sad *_* :' + str(err))
                            pattern = re.compile(r'http\:(.*)\/')
                            match = pattern.search(str(result))
                            if match:
                                luanma_url = match.group()
                                with open(city_luanma_failed_file, 'a') as sad:
                                    sad.write(luanma_url + '\n')
    except Exception as err:
        print('lol   do not know exact reason: ' + str(err))
        with open(city_failed_file, 'a') as sad:
            sad.write(url + '\n')


# def go_thread_for_cities(link, ):
#     print('go go go!!!')
#     url = URL + link
#     try:
#         soup = download_page(url)
#         page_num = get_page_num(soup)
#         for i in range(1, page_num+1):
#             results = []
#             page_url = url[0:-6] + str(i) + '_0_0/'
#             soup = download_page(page_url)
#             ids = get_ids(soup, page_url)
#
#             if ids == '':
#                 retries = 10
#                 while retries:
#                     print('------------------------------- try to get ids again: ' + page_url)
#                     soup = download_page(page_url)
#                     ids = get_ids(soup, page_url)
#                     if ids:
#                         retries = 0
#                     else:
#                         if retries == 1:
#                             print('------------------------------- get ids failed: ' + page_url)
#                             with open(city_failed_file, 'a') as sad:
#                                 sad.write(link + '\n')
#                         retries -= 1
#
#             if ids:
#                 div_list = soup.findAll('div', attrs={'class': 'list rel'})
#                 for div, residence_id in zip(div_list, ids):
#                     residence_type = div.find('span', attrs={'class': 'plotFangType'}).getText()
#                     # print(residence_type)
#                     if residence_type == '写字楼' or residence_type == '商铺':
#                         res = get_record_2(div)
#                     else:
#                         # 部分城市的json数据里不含链接及价格
#                         res = get_record(residence_id, div)
#                     if res:
#                         results.append(res)
#                 with open(city_file, 'a', encoding='utf-8') as f:
#                     for result in results:
#                         try:
#                             f.write(result + '\n')
#                             print('+1', end=' ')
#                         except Exception as err:
#                             print('   mess!!!        so sad *_* :' + str(err))
#                             pattern = re.compile(r'http\:(.*)\/')
#                             match = pattern.search(str(result))
#                             if match:
#                                 luanma_url = match.group()
#                                 with open(city_luanma_failed_file, 'a') as sad:
#                                     sad.write(luanma_url + '\n')
#     except Exception as err:
#         print('lol   do not know exact reason: ' + str(err))
#         with open(city_failed_file, 'a') as sad:
#             sad.write(url + '\n')


def go_after_scraping(link):
    print('after go go go!!!')
    try:
        results = []
        soup = download_page(link)
        ids = get_ids(soup, link)

        if ids:
            div_list = soup.findAll('div', attrs={'class': 'list rel'})
            for div, residence_id in zip(div_list, ids):
                residence_type = div.find('span', attrs={'class': 'plotFangType'}).getText()
                # print(residence_type)
                if residence_type == '写字楼' or residence_type == '商铺':
                    res = get_record_2(div)
                else:
                    res = get_record(residence_id, div)
                if res:
                    results.append(res)
            with open(city_file, 'a', encoding='utf-8') as f:
                for result in results:
                    try:
                        f.write(result + '\n')
                        print('+1', end=' ')
                    except Exception as err:
                        print('     mess!!!       so sad *_* :' + str(err))
                        pattern = re.compile(r'http\:(.*)\/')
                        match = pattern.search(str(result))
                        if match:
                            luanma_url = match.group()
                            with open(city_luanma_failed_file, 'a') as sad:
                                sad.write(luanma_url + '\n')
    except Exception as err:
        print('lol    do not know exact reason: ' + str(err))
        with open(city_failed_file, 'a') as sad:
            sad.write(link + '\n')


@fn_timer
def main():
    # print(download_page('http://esf.sh.fang.com/housing/'))

    # ------------------------文本城市列表抓取代码
    city_list = []
    with open('cityList.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            city_list.append(line.strip())

    pool = ThreadPool(3)

    for city in city_list:
        city_info = city.split('\t')
        city_url = city_info[0]
        province_name = city_info[1]
        name = city_info[2]
        print('begin scraping --------------------------------------------: ' + name + ' ' + city_url)

        global CITY_SHORT, URL, RESIDENCE_URL, PROVINCE, CITY_NAME, city_file, city_failed_file
        global city_xiezilou_failed_file, city_zhuzhai_failed_file, city_luanma_failed_file, city_url_failed_file

        URL = city_url
        RESIDENCE_URL = city_url + '/housing/'
        CITY_SHORT = city_url[11:-9]

        PROVINCE = province_name
        CITY_NAME = name

        # 正确结果
        city_file = PATH + 'fangtianxia_' + CITY_SHORT + '.txt'
        # 获取写字楼，商铺失败的链接
        city_xiezilou_failed_file = PATH + 'fangtianxia_' + CITY_SHORT + '_xiezilou_failed.txt'
        # 获取住宅、别墅失败的链接
        city_zhuzhai_failed_file = PATH + 'fangtianxia_' + CITY_SHORT + '_zhuzhai_failed.txt'
        # 未知原因的失败 和 获取ids时失败 的小区列表链接
        city_failed_file = PATH + 'fangtianxia_' + CITY_SHORT + '_failed.txt'
        # 写入时因特殊字符乱码失败的链接
        city_luanma_failed_file = PATH + 'fangtianxia_' + CITY_SHORT + '_luanma_failed.txt'
        # 请求url时失败的链接 ---- 一般不会失败
        city_url_failed_file = PATH + 'fangtianxia_' + CITY_SHORT + '_url_failed.txt'

        urls = get_districts_urls(RESIDENCE_URL)

        print(urls)

        pool.map(go_thread, urls)
    pool.close()
    pool.join()


    # # ------------------------ 单个城市抓取代码
    # urls = get_districts_urls(RESIDENCE_URL)
    #
    # print(urls)
    #
    # pool = ThreadPool(10)
    # pool.map(go_thread, urls)
    # pool.close()
    # pool.join()

    # # ------------------------- 重跑获取失败的小区列表网页
    # urls = []
    # with open(city_failed_file, 'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         urls.append(line.strip())
    # print(urls)
    # pool = ThreadPool(5)
    # pool.map(go_after_scraping, urls)
    # pool.close()
    # pool.join()

    # # ------------------------- 重跑获取失败的写字楼商铺网页
    # urls = []
    # with open('results/fangtianxia_guangzhou_xiezilou_failed.txt', 'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         urls.append(line.strip())
    # print(urls)
    # pool = ThreadPool(2)
    # results = pool.map(, urls)
    # pool.close()
    # pool.join()


    # go_thread('/housing/492_4979_0_0_0_0_1_0_0/')

    # get_record(2610419222)

    # download_page('http://yunhexiaoqu027.fang.com/')

    # urls = ['http://esf.nn.fang.com/housing/_15174_0_0_0_0_2_0_0/']
    # for url in urls:
    #     go_after_scraping(url)

    # get_ids(download_page('http://esf.zh.fang.com/housing/__0_0_0_0_1_0_0/'))

    print("good good ")

if __name__ == '__main__':
    main()
    print('good')
