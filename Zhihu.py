import requests, time
from bs4 import BeautifulSoup


def get_captcha(data):
    with open('captcha.gif','wb') as fp:
        fp.write(data)
    return input('输入验证码：')


def login(username, password, oncaptcha):
    session = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    _xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin',headers=headers).content,'html.parser').find('input',attrs={'name':'_xsrf'}).get('value')
    captcha_content = session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login'%(time.time()*1000),headers=headers).content
    data = {
        "_xsrf":_xsrf,
        "email":username,
        "password":password,
        "remember_me":True,
        "captcha":oncaptcha(captcha_content)
    }
    #resp = session.post('https://www.zhihu.com/login/email',data,headers=headers).content
    session.post('https://www.zhihu.com/login/email', data, headers=headers)

    # print('\u767b\u9646\u6210\u529f')
    # print(resp)
    # print('\u767b\u5f55\u6210\u529f')
    # assert '\u767b\u9646\u6210\u529f' in resp

    print('+++++++++++++++++++++++++++++++++++++++')
    html = session.get("https://www.zhihu.com", headers=headers).content
    soup = BeautifulSoup(html)
    print(html)
    name = soup.find('span', attrs={'class': 'name'})
    print('---------------------------')
    print(name)
    print('+++++++++++++++++++++++++++++++++++++++')

    return session

if __name__ == "__main__":
    session = login('mrwangng@gmail.com', 'ng9191', get_captcha)
    print(session)
    # # error:
    # # b'<html><body><h1>500 Server Error</h1>\nAn internal server error occured.\n</body></html>\n'
    # html = session.get("https://www.zhihu.com", headers=headers).content
    # soup = BeautifulSoup(html)
    # print(html)
    # name = soup.find('span', attrs={'class': 'name'})
    # print('---------------------------')
    # print(name)

