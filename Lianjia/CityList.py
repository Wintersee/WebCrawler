
import requests
from bs4 import BeautifulSoup
import time





URL = 'http://sh.lianjia.com'
xiaoqu_url = 'http://sh.lianjia.com/xiaoqu/d'
detail_url = 'http://sh.lianjia.com/xiaoqu/5011102207057.html'

# def get_infos(url):
#     res = urllib2.urlopen(url)

#     content = res.read().decode('utf-8')

#     soup = BeautifulSoup(content,"html.parser")


def download_page(url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.content
        print(response.status_code)
        print(response.history)
    except Exception as err:
        print("fail to dowload the page, reason: ")
        print(err)
        if retries>1:
            print("try again")
            return download_page(url,retries-1)
        else:
            print("failed in scaping : %s" % url)
            return ''        
    
    return data


def get_city_list(html):
    soup = BeautifulSoup(html,"html.parser")
    city_dict = {}
    city_list = soup.find('div', attrs={'class': 'cityList clear'}).findAll('a')
    print(city_list, len(city_list))

    for city in city_list:
        # detail = movie.find('div', attrs={'class': 'hd'})
        link = city.get('href')
        name = city.getText()
        city_dict[name] = link
  
    print(city_dict)

    # # for link, name in zip(link_list, name_list):
        
    # #     parse_detail_page(name, link)
    
    # for link in link_list:
        
    #     parse_detail_page(link)


# def parse_detail_page(link):
#     result = ' '
#     detail_link = URL + link
#     detail_soup = BeautifulSoup(download_page(detail_link),"html.parser")
#     # get the price
#     price = detail_soup.find('span',attrs={'class':'p'}).getText().strip()

#     # get name, latitude and longitude
#     coord = detail_soup.find('a',attrs={'class':'actshowMap'}).get('xiaoqu')

#     coord = coord.split(',')

#     latitude = coord[1]
#     longitude = coord[0].strip('[')
#     # name = coord[2].strip(']').strip("'")
#     name = coord[2][2:-2]

#     # get address
#     adr = detail_soup.find('span',attrs={'class':'adr'}).getText().strip()

#     result = name + ' ' + link + ' ' + price + ' ' + latitude + ' ' + longitude + ' ' + adr

#     # get other info
#     others = []
#     other_info = detail_soup.findAll('span',attrs={'class':'other'})
#     # print(other_info)
#     for info in other_info:
#         # print(info.getText())
#         # print(info.getText().strip())
#         others.append(info.getText().strip())
    
    
#     i = 1
#     for other in others:
#         if i<3:
#             result += ' ' + other
#             i += 1
#         else:
#             break
  
#     result +=  '\n'
#     print(result)
#     with open('shanghai.txt', 'a') as f:
#         f.write(result)
    
#     # time.sleep(0.5)



def main():
    # detail_soup = BeautifulSoup(download_page(detail_url),"html.parser")
    # coord = detail_soup.find('a',attrs={'class':'actshowMap'}).get('xiaoqu')
    
    # parse_detail_page('hh', detail_url)
    # a = "'绿地威廉公寓']"
    # print(a)
    # print(a[1:-2])
    # print(a.strip("]").strip("'"))
    # a = a.strip("'")
    # print(a)

    url = URL
    html = download_page(url)
    # get_city_list(html)

 
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
