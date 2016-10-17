
import requests
from bs4 import BeautifulSoup


def get_cities(url, page):
    data = {'mddid': 21536, 'page': page}
    json = requests.post(url, data).json()

    page = json['list']

    soup = BeautifulSoup(page, "html.parser")

    divs = soup.findAll('div', attrs={'class': 'title'})

    cities = []
    for div in divs:
        # 抓取时发现部分网页内的城市列表部分城市名缺失
        try:
            name = div.getText().split()[0]
            cities.append(name)
        except IndexError as e:
            print('IndexError', e)

    print(cities)

    # detailIDs = []
    #
    # for link in link_list:
    #     link = link.get('href')
    #     detail_id = link.split('?')[-1].split('=')[-1]
    #     detailIDs.append(detail_id)
    #
    # print(detailIDs)
    # print(len(detailIDs))
    # return detailIDs
    #
    # soup = BeautifulSoup(html, "html.parser")
    #
    # movie_list = soup.findAll('td', attrs={'class': 'titleColumn'})
    # # print(movie_list)
    # movie_title_list = []
    #
    # for movie in movie_list:
    #     # detail = movie.find('div', attrs={'class': 'hd'})
    #     movie_title = movie.find('a').getText()
    #     # print(movie_title)
    #     movie_title_list.append(movie_title)
    #
    # return movie_title_list
    # list_con = json['content']['positionResult']['result']
    # print(list_con)
    # info_list = []
    #
    # for i in list_con:
    #     #         print(i)
    #     info = []
    #     info.append(i['companyShortName'])
    #     info.append(i['companyFullName'])
    #     #         info.append(i['companyName'])
    #     info.append(i['salary'])
    #     info.append(i['city'])
    #     info.append(i['education'])
    #     info_list.append(info)
    # return info_list


def main():
    #     lang_name = input('职位名：')
    # lang_name = 'python'
    page = 1
    url = 'http://www.mafengwo.cn/mdd/base/list/pagedata_citylist'
    get_cities(url, 288)

    # while page < 298:
    #     print(page)
    #     get_cities(url, page)
    #     page += 1


if __name__ == '__main__':
    main()
    print('good')
# -------------------------------------------------------------------------------------------------------
