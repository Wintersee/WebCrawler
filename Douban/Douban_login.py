import requests
from bs4 import BeautifulSoup

URL = 'https://www.douban.com/login'
email = 'tianxia91@qq.com'
password = 'ng91911'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}
data = {
    'redir': 'http://www.douban.com',
    'form_email': email,
    'form_password': password,
    'remember': 'on'
}


def login():
    session = requests.Session()
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    # _xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin',headers=headers).content,'html.parser').find('input',attrs={'name':'_xsrf'}).get('value')
    # captcha_content = session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login'%(time.time()*1000),headers=headers).content


    #resp = session.post('https://www.zhihu.com/login/email',data,headers=headers).content
    resp = session.post(URL, data=data, headers=headers).content

    print(resp)
    print('+++++++++++++++++++++++++++++++++++++++')
    html = session.get("https://movie.douban.com/mine", headers=headers).content
    print(html)
    print('+++++++++++++++++++++++++++++++++++++++')

    return session

if __name__ == "__main__":
    session = login()
    print(session)
    # # error:
    # # b'<html><body><h1>500 Server Error</h1>\nAn internal server error occured.\n</body></html>\n'
    # html = session.get("https://www.zhihu.com").content
    # soup = BeautifulSoup(html)
    # print(html)
    # name = soup.find('span', attrs={'class': 'name'})
    # print('---------------------------')
    # print(name)

