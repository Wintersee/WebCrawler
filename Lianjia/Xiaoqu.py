
import requests
from bs4 import BeautifulSoup





URL = 'http://sh.lianjia.com'
xiaoqu_url = 'http://sh.lianjia.com/xiaoqu/d1rs'
detail_url = 'http://sh.lianjia.com/xiaoqu/5011102207057.html'

# def get_infos(url):
#     res = urllib2.urlopen(url)

#     content = res.read().decode('utf-8')

#     soup = BeautifulSoup(content,"html.parser")


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    data = requests.get(url, headers=headers).content
    return data


def parse_page(html):
    soup = BeautifulSoup(html,"html.parser")
    link_list = []
    name_list = []
    xiaoqu_list = soup.findAll('div', attrs={'class': 'info-panel'})
    # print(xiaoqu_list)

    for xiaoqu in xiaoqu_list:
        # detail = movie.find('div', attrs={'class': 'hd'})
        link = xiaoqu.find('a').get('href')
        name = xiaoqu.find('a').get('title')
        link_list.append(link)
        name_list.append(name)

        


    # print(link_list, name_list)

    for link, name in zip(link_list, name_list):
        
        parse_detail_page(name, link)


def parse_detail_page(name, link):
    result = ' '
    detail_link = URL + link
    detail_soup = BeautifulSoup(download_page(detail_link),"html.parser")
    price = detail_soup.find('span',attrs={'class':'p'}).getText().strip()
    # print(price)
    others = []
    other_info = detail_soup.findAll('span',attrs={'class':'other'})
    # print(other_info)
    for info in other_info:
        # print(info.getText().strip())
        others.append(info.getText().strip())
    
    result = name + ' ' + link + ' ' + price
    for other in others:
        result += ' ' + other
    print(result)


    # next_page = soup.find('span', attrs={'class': 'next'}).find('a')

    # if next_page:
    #     return movie_title_list, URL + next_page['href']
    # return movie_title_list, None


def main():
    # parse_detail_page('hh', detail_url)
    url = xiaoqu_url
    html = download_page(url)
    parse_page(html)

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
