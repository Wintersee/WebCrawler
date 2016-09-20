import requests
import re
import urllib.request
from bs4 import BeautifulSoup

URL = 'https://www.douban.com/accounts/login'
REDIR = 'http://movie.douban.com/mine?status=collect'
username = '@qq.com'
password = ''
data ={
    "redir": REDIR,
    "form_email": username,
    "form_password": password,
    "login": u'登录'
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

r = requests.get(URL, headers=headers)
page = r.text


def get_captcha(page):
    print(data)
    print('aaaaaaaaaaaaaaaaa')
    '''''获取验证码图片'''
    # 利用bs4获取captcha地址
    soup = BeautifulSoup(page, "html.parser")
    captchaAddr = soup.find('img', id='captcha_image')['src']
    # 利用正则表达式获取captcha的ID
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captchaID = re.findall(reCaptchaID, page)
    # print captchaID
    # 保存到本地
    urllib.request.urlretrieve(captchaAddr, "captcha.jpg")
    captcha = input('please input the captcha:')
    print(captcha)

    data['captcha-id'] = captchaID
    data['captcha-solution'] = captcha


def login():
    get_captcha(page)
    #
    # r = requests.post(REDIR, data=data, headers=headers)
    # print(r.url)
    # if r.url == 'https://movie.douban.com/mine?status=collect':
    #     print('Login successfully!!!')
    #
    #     print('我看过的电影', '-' * 60)
    #     # 获取看过的电影
    #     soup = BeautifulSoup(r.text, "html.parser")
    #     print(r.text)
    #     result = soup.findAll('em')
    #     print(result)
    #     for item in result:
    #         print(item.get_text())
    # else:
    #     print("failed!")


if __name__ == "__main__":
    login()


