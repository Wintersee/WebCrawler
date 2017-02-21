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


PATH = 'C:/workspace/GitHub/data/WebCrawler/stock/'

month_ago = datetime.datetime.today() - datetime.timedelta(days=30)
month_ago = month_ago.strftime("%Y%m%d")
today = datetime.datetime.today().strftime('%Y%m%d')

original_stock_code_file = PATH + 'original_stock_code_' + today + '.txt'
processed_stock_code_file = PATH + 'processed_stock_code_' + today + '.txt'
history_stock_file = PATH + 'history_stock_' + today + '.txt'


def download_page(url, retries=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    try:
        # time.sleep(round(random.uniform(1, 5), 2))
        response = requests.get(url, headers=headers)
        # # print(response.encoding + '  response')
        # if response.encoding == 'gb2312':
        #     data = response.content.decode("GB18030").encode('utf-8')
        # # if response.encoding == 'ISO-8859-1':
        # else:
        #     data = response.content.decode("GB18030").encode('utf-8')
        data = response.content.decode('GB18030', 'replace').encode('utf-8', 'replace')
        # print(data)

        # soup = BeautifulSoup(data, "html.parser")

        # print(soup)

    except Exception as err:
        print("|||test failed ! didn't get the right content: "+str(err)+' ||| ' + url)
        if retries > 0:
            time.sleep(random.randint(10, 15))
            print("try again, %d times left" % int(retries-1))
            return download_page(url, retries - 1)
        else:
            print("|||failed in scraping : %s|||" % url)

    return data


def get_name_and_code(link):
    print("---getting code  ---")

    # soup = download_page(link)
    soup = BeautifulSoup(download_page(link), "html.parser")
    res = []
    div = soup.find('div', attrs={'id': 'quotesearch'})
    lis = div.findAll('li')
    for li in lis:
        li = li.getText()
        res.append(li)

    with open(original_stock_code_file, 'w', encoding='utf-8') as f:
        for item in res:
            f.write(item+'\n')

    return res


def processing_code(url):
    name_code = get_name_and_code(url)
    print(name_code)
    foo = []

    for nc in name_code:
        n = nc[0:-8]
        c = nc[-7:-1]
        if nc[-7] == '6':
            fo = '上证\t' + n + '\t' + c + '\n'
            foo.append(fo)
        if nc[-7:-5] == '00':
            fo = '深证\t' + n + '\t' + c + '\n'
            foo.append(fo)

    with open(processed_stock_code_file, 'w', encoding='utf-8') as f:
        for fo in foo:
            print(fo)
            f.write(fo)


def get_history_data(stock_record):
    # print("---getting data  ---")
    stock_info = stock_record.split('\t')
    exchange = stock_info[0]
    name = stock_info[1]
    code = stock_info[2]
    print('begin scraping --------------------------------------------: ' + exchange + ' : ' + name + ' : ' + code)

    url = 'http://q.stock.sohu.com/hisHq?code=cn_'+code+'&start='+month_ago+'&end='+today
    result = str(download_page(url), encoding="utf-8")

    res = stock_record + '\t' + result

    return res


@fn_timer
def main():

    # url = 'http://quote.eastmoney.com/stocklist.html'
    # processing_code(url)

    # ------------------------
    stock_all = []
    with open(processed_stock_code_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stock_all.append(line.strip())

    pool = ThreadPool(10)
    # results = []
    results = pool.map(get_history_data, stock_all)
    pool.close()
    pool.join()

    with open(history_stock_file, 'w', encoding='utf-8') as f:
        for res in results:
            f.write(res)

    print("good good ")

if __name__ == '__main__':

    main()

    print('good')
