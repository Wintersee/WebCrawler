import requests
from bs4 import BeautifulSoup

URL = 'http://movie.douban.com/top250/'


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = requests.get(url, headers=headers).content
    return data


def parse_page(html):
    soup = BeautifulSoup(html)

    movie_list = soup.find('ol', attrs={'class': 'grid_view'})
    movie_title_list = []

    for movie in movie_list.find_all('li'):
        detail = movie.find('div', attrs={'class': 'hd'})
        movie_title = detail.find('span', attrs={'class': 'title'}).getText()
        movie_title_list.append(movie_title)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')

    if next_page:
        return movie_title_list, URL + next_page['href']
    return movie_title_list, None


def main():
    url = URL

    while url:
        html = download_page(url)
        movies, url = parse_page(html)
        print(movies)
        #print('--------------------------------------------------------------------------------------')

if __name__ == '__main__':
    main()