import requests
from bs4 import BeautifulSoup

URL = 'https://movie.douban.com/people/39636766/collect'


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = requests.get(url, headers=headers).content
    return data


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")

    movie_list = soup.findAll('em')
    movie_title_list = []

    for movie in movie_list:
        movie_title_list.append(movie.getText())

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')

    if next_page:
        return movie_title_list, next_page['href']
    return movie_title_list, None


def main():
    url = URL

    while url:
        html = download_page(url)
        movies, url = parse_page(html)
        print(movies)
        print('--------------------------------------------------------------------------------------')

if __name__ == '__main__':
    main()