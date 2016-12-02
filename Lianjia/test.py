import urllib.request
 
from multiprocessing.dummy import Pool as ThreadPool
 




import requests
from bs4 import BeautifulSoup
import time


import time
import datetime
from functools import wraps


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
def fn_timer_microsecond(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = datetime.datetime.now().microsecond
        print(datetime.datetime.now())
        result = function(*args, **kwargs)
        t1 = datetime.datetime.now().microsecond
        print(datetime.datetime.now())
        print("Total time running %s: %s seconds" %
              (function.__name__, str(t1 - t0))
              )
        return result

    return function_timer

URL = 'http://sh.lianjia.com'
xiaoqu_url = 'http://sh.lianjia.com/xiaoqu/d'
detail_url = 'http://sh.lianjia.com/xiaoqu/5011102207057.html'



def download_page(url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        data = requests.get(url, headers=headers).content
    except Exception as err:
        print("fail to dowload the page, reason: ")
        print(err)
        if retries>0:
            print("try again")
            return download_page(url,retries-1)
        else:
            print("failed in scaping : %s" % url)
            return ''        
    
    return data


def parse_page(html):
    soup = BeautifulSoup(html,"html.parser")
    link_list = []
    name_list = []
    xiaoqu_list = soup.findAll('div', attrs={'class': 'info-panel'})
    # print(xiaoqu_list)

    for xiaoqu in xiaoqu_list:
        link = xiaoqu.find('a').get('href')
        name = xiaoqu.find('a').get('title')
        link_list.append(link)
    
    for link in link_list:
        
        parse_detail_page(link)


def parse_detail_page(link):
    result = ' '
    detail_link = URL + link
    detail_soup = BeautifulSoup(download_page(detail_link),"html.parser")
    # get the price
    price = detail_soup.find('span',attrs={'class':'p'}).getText().strip()

    # get name, latitude and longitude
    coord = detail_soup.find('a',attrs={'class':'actshowMap'}).get('xiaoqu')

    coord = coord.split(',')

    latitude = coord[1]
    longitude = coord[0].strip('[')
    # name = coord[2].strip(']').strip("'")
    name = coord[2][2:-2]

    # get address
    adr = detail_soup.find('span',attrs={'class':'adr'}).getText().strip()

    result = name + ' ' + link + ' ' + price + ' ' + latitude + ' ' + longitude + ' ' + adr

    # get other info
    others = []
    other_info = detail_soup.findAll('span',attrs={'class':'other'})
    # print(other_info)
    for info in other_info:
        # print(info.getText())
        # print(info.getText().strip())
        others.append(info.getText().strip())
    
    
    i = 1
    for other in others:
        if i<3:
            result += ' ' + other
            i += 1
        else:
            break
  
    result +=  '\n'
    print(result)
    with open('shanghai_old.txt', 'a') as f:
        f.write(result)
    
    # time.sleep(0.5)

def parse_detail_page_test(html):

    detail_soup = BeautifulSoup(html,"html.parser")
    # get the price
    price = detail_soup.find('span',attrs={'class':'p'}).getText().strip()

    # get name, latitude and longitude
    coord = detail_soup.find('a',attrs={'class':'actshowMap'}).get('xiaoqu')

    coord = coord.split(',')

    latitude = coord[1]
    longitude = coord[0].strip('[')
    # name = coord[2].strip(']').strip("'")
    name = coord[2][2:-2]

    # get address
    adr = detail_soup.find('span',attrs={'class':'adr'}).getText().strip()

#     result = name + ' ' + link + ' ' + price + ' ' + latitude + ' ' + longitude + ' ' + adr
    result = name + ' ' + price + ' ' + latitude + ' ' + longitude + ' ' + adr


    # get other info
    others = []
    other_info = detail_soup.findAll('span',attrs={'class':'other'})
    # print(other_info)
    for info in other_info:
        # print(info.getText())
        # print(info.getText().strip())
        others.append(info.getText().strip())
    
    
    i = 1
    for other in others:
        if i<3:
            result += ' ' + other
            i += 1
        else:
            break
  
    result +=  '\n'
    print(result)
    with open('shanghai_new.txt', 'a') as f:
        f.write(result)
    
    # time.sleep(0.5)
    
    
def parse_page_test(html):
    soup = BeautifulSoup(html,"html.parser")
    link_list = []
    name_list = []
    xiaoqu_list = soup.findAll('div', attrs={'class': 'info-panel'})
    # print(xiaoqu_list)

    for xiaoqu in xiaoqu_list:
        link = xiaoqu.find('a').get('href')
        detail_link = URL + link
        link_list.append(detail_link)
    
    return link_list

@fn_timer
def m1():
    
    url = xiaoqu_url + '1'
    html = download_page(url)
    urls = parse_page_test(html)
     
    pool = ThreadPool()

#     results = pool.map(urllib.request.urlopen,urls)
    results = pool.map(download_page,urls)
#     print(results)
    for http_obj in results:
        parse_detail_page_test(http_obj)
    pool.close()
    pool.join()

    print('main1 ended')
    # detail_soup = BeautifulSoup(download_page(detail_url),"html.parser")
    # coord = detail_soup.find('a',attrs={'class':'actshowMap'}).get('xiaoqu')
    


#     url = xiaoqu_url + '1'
#     html = download_page(url)
#     parse_page(html)

 
#     for i in range(89,101):
        
#         url = xiaoqu_url + str(i)
#         print("start scraping " + url)
#     # url = xiaoqu_url
#         html = download_page(url)
#         parse_page(html)
#         print("# ----------------- got page %d !!!" % i)

    # while url:
    #     html = download_page(url)
    #     movies, url = parse_page(html)
    #     print(movies)
        #print('--------------------------------------------------------------------------------------')
@fn_timer
def m2():
    


    url = xiaoqu_url + '1'
    html = download_page(url)
    parse_page(html)
    print('main2 ended')

def main():
    # m1()
    # m2()

if __name__ == '__main__':
    main()
    print('good')
# -------------------------------------------------------------------------------------------------------



