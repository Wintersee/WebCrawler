
import requests
from bs4 import BeautifulSoup
import time
import math
from multiprocessing.dummy import Pool as ThreadPool


import datetime
from functools import wraps



URL = 'http://sh.lianjia.com'
xiaoqu_url = 'http://sh.lianjia.com/xiaoqu/d'
detail_url = 'http://sh.lianjia.com/xiaoqu/5011102207057.html'

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

def download_page(url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        data = requests.get(url, headers=headers).content
    except Exception as err:
        print("fail to dowload the page, reason: ")
        print(err)
        if retries>0:
            time.sleep(2)
            print("try again")
            return download_page(url,retries-1)
        else:
            print("failed in scaping : %s" % url)
            return ''        
    
    return data

def get_page_num(link):
    soup = BeautifulSoup(download_page(link),"html.parser")

    sum = soup.find('div', attrs={'class': 'list-head clear'}).find('span').getText()
    sum = int(sum)
    page_num = math.ceil(sum/20)
    print(sum)
    print(page_num)
    return page_num

def get_urls(num):
    print("----------getting page %d \n" % num)
    link = xiaoqu_url+str(num)

    results = []
    soup = BeautifulSoup(download_page(link),"html.parser")
    link_list = []
    xiaoqu_list = soup.findAll('div', attrs={'class': 'info-panel'})

    for xiaoqu in xiaoqu_list:
        link = xiaoqu.find('a').get('href')
        link_list.append(link)
    
    return link_list

    


def parse_page(link):
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
    spans = detail_soup.find('span',attrs={'class':'t'}).findAll('span')
    adr = spans[0].getText()[1:-1] + spans[1].getText().strip()

    result = name + '\t' + link + '\t' + price + '\t' + latitude + '\t' + longitude + '\t' + adr

    # get other info
    others = []
    other_info = detail_soup.findAll('span',attrs={'class':'other'})

    for info in other_info:
        others.append(info.getText().strip())
    
    for i in [0,1,5,6]:
        result += '\t' + others[i]
 
    result +=  '\n'
    # print(result)
    return result
    
    # time.sleep(0.5)


def go_thread(num):
    print('start thread !!! \n')
    results = []
    url_list = get_urls(num)
    
    for url in url_list:
        print('+1', end='')
        results.append(parse_page(url))
    
    with open('shanghai.txt', 'a') as f:
        for res in results:
            f.write(res)
        print("20 xiaoqu written successfully \n")
        
    # re = parse_page(url)
    # # print('go_thread end')
    # return re
    
    # print('-----------------------------start scraping page !!!')
    # # urls = get_urls(xiaoqu_url+str(i))
    # pool = ThreadPool(20)
    
    # results = pool.map(parse_page,urls)
    
    
    # pool.close()
    # # pool.setDaemon(True)
    # pool.join()
    
    # print('-----------------------------got page  !!!')
    # return results

    
@fn_timer   
def main():
    # detail_soup = BeautifulSoup(download_page(detail_url),"html.parser")
    # coord = detail_soup.find('a',attrs={'class':'actshowMap'}).get('xiaoqu')


    # html = download_page(url)
    # urls = parse_page(html)

    page_num = get_page_num(xiaoqu_url + '1')
    

    # xiaoqu_urls = []
    # for i in range(1,page_num+1):
        
    #     xiaoqu_urls[-1:-1] = get_urls(xiaoqu_url+str(i))
    #     print('got page %d !!! %d pages left!!! size of url list is %d !!!' % (i, page_num-i,len(xiaoqu_urls)))
     
    

    pool = ThreadPool(20)
    pool.map(go_thread,list(range(1,page_num+1)))
    pool.close()
    pool.join() 
    print("good good ")

    
 
    # for i in range(89,101):
        
    #     url = xiaoqu_url + str(i)
    #     print("start scraping " + url)
    # # url = xiaoqu_url
    #     html = download_page(url)
    #     parse_page(html)
    #     print("# ----------------- got page %d !!!" % i)

    # while url:
    #     html = download_page(url)
    #     movies, url = parse_page(html)
    #     print(movies)
        #print('--------------------------------------------------------------------------------------')

if __name__ == '__main__':
    main()
    print('good')
# -------------------------------------------------------------------------------------------------------








# def get_cities(url, page):
#     data = {'mddid': 21536, 'page': page}
#     json = requests.post(url, data).json()

#     page = json['list']

#     soup = BeautifulSoup(page, "html.parser")

#     divs = soup.findAll('div', attrs={'class': 'title'})

#     cities = []
#     for div in divs:
#         # 抓取时发现部分网页内的城市列表部分城市名缺失
#         try:
#             name = div.getText().split()[0]
#             cities.append(name)
#         except IndexError as e:
#             print('IndexError', e)

#     print(cities)

#     # detailIDs = []
#     #
#     # for link in link_list:
#     #     link = link.get('href')
#     #     detail_id = link.split('?')[-1].split('=')[-1]
#     #     detailIDs.append(detail_id)
#     #
#     # print(detailIDs)
#     # print(len(detailIDs))
#     # return detailIDs
#     #
#     # soup = BeautifulSoup(html, "html.parser")
#     #
#     # movie_list = soup.findAll('td', attrs={'class': 'titleColumn'})
#     # # print(movie_list)
#     # movie_title_list = []
#     #
#     # for movie in movie_list:
#     #     # detail = movie.find('div', attrs={'class': 'hd'})
#     #     movie_title = movie.find('a').getText()
#     #     # print(movie_title)
#     #     movie_title_list.append(movie_title)
#     #
#     # return movie_title_list
#     # list_con = json['content']['positionResult']['result']
#     # print(list_con)
#     # info_list = []
#     #
#     # for i in list_con:
#     #     #         print(i)
#     #     info = []
#     #     info.append(i['companyShortName'])
#     #     info.append(i['companyFullName'])
#     #     #         info.append(i['companyName'])
#     #     info.append(i['salary'])
#     #     info.append(i['city'])
#     #     info.append(i['education'])
#     #     info_list.append(info)
#     # return info_list


# def main():
#     #     lang_name = input('职位名：')
#     # lang_name = 'python'
#     page = 1
#     url = 'http://www.mafengwo.cn/mdd/base/list/pagedata_citylist'
#     get_cities(url, 288)

#     # while page < 298:
#     #     print(page)
#     #     get_cities(url, page)
#     #     page += 1


# if __name__ == '__main__':
#     main()
#     print('good')
# # -------------------------------------------------------------------------------------------------------
