import requests
import json
import csv
from bs4 import BeautifulSoup

URL = 'http://js.ntwikis.com/rest/cancollezh/charactordetail'
url = 'http://js.ntwikis.com/jsp/apps/cancollezh/charactors/detail.jsp?detailid=100'
data ={
    "detailid": 1197,
    "language": "zh"
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}


json = requests.post(URL, data, headers=headers).json()

print(json)
print(type(json))
subkey = ['NAME', 'TYPE', 'ATTACK', 'NO', 'STARS']
subdict = {key: json[key] for key in subkey}
print(subdict)

f = csv.writer(open("testt.csv", "w", newline=''))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["NAME", "TYPE", "ATTACK", "NO", "STARS"])


f.writerow([subdict["NAME"],
            subdict["TYPE"],
            subdict["ATTACK"],
            subdict["NO"],
            subdict["STARS"]])


