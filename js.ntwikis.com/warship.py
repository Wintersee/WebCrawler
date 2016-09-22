import requests
from bs4 import BeautifulSoup

URL = 'http://js.ntwikis.com/jsp/apps/cancollezh/charactors/listpage.jsp'


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = requests.get(url, headers=headers).content
    return data


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    warship_5_stars_list = soup.find_all('div', style ="color:#FF9900;")

    warship_6_stars = []
    warship_5_stars = []
    warship_4_stars = []
    warship_3_stars = []
    warship_2_stars = []
    warship_1_stars = []

    for warship in warship_5_stars_list:
        print(warship)
        warship_5_stars.append(warship.getText())
    return warship_5_stars


    # movie_list = soup.findAll('em')
    # movie_title_list = []
    #
    # for movie in movie_list:
    #     movie_title_list.append(movie.getText())
    #
    # next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    #
    # if next_page:
    #     return movie_title_list, next_page['href']
    # return movie_title_list, None
    #
    # movie_list = soup.find('ol', attrs={'class': 'grid_view'})
    # movie_title_list = []
    #
    # for movie in movie_list.find_all('li'):
    #     detail = movie.find('div', attrs={'class': 'hd'})
    #     movie_title = detail.find('span', attrs={'class': 'title'}).getText()
    #     movie_title_list.append(movie_title)
    #
    # next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    #
    # if next_page:
    #     return movie_title_list, URL + next_page['href']
    # return movie_title_list, None


def main():
    html = download_page(URL)
    warship_5_stars = parse_page(html)
    print(warship_5_stars)
    print('--------------------------------------------------------------------------------------')

if __name__ == '__main__':
    main()