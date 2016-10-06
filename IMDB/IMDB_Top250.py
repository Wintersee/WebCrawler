import requests
from bs4 import BeautifulSoup

URL = 'http://www.imdb.com/chart/top?ref_=nv_wl_img_3'


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = requests.get(url, headers=headers).content
    return data


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")

    movie_list = soup.findAll('td', attrs={'class': 'titleColumn'})
    # print(movie_list)
    movie_title_list = []

    for movie in movie_list:
        # detail = movie.find('div', attrs={'class': 'hd'})
        movie_title = movie.find('a').getText()
        # print(movie_title)
        movie_title_list.append(movie_title)

    return movie_title_list
    # next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    #
    # if next_page:
    #     return movie_title_list, URL + next_page['href']
    # return movie_title_list, None


def main():
    url = URL

    html = download_page(url)
    movies = parse_page(html)
    print(movies)

if __name__ == '__main__':
    main()