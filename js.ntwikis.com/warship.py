import requests
import re
from bs4 import BeautifulSoup
import requests
import json
import csv
# import unicodecsv as csv
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
url_ids = 'http://js.ntwikis.com/rest/cancollezh/charactorquery'
url_detail = 'http://js.ntwikis.com/rest/cancollezh/charactordetail'


def get_ids():
    data = {
        "ismobile": 0
    }

    r = requests.post(url_ids, data=data, headers=headers)
    page = r.text

    soup = BeautifulSoup(page, "html.parser")

    link_list = soup.findAll('a', attrs={'href': re.compile("^/jsp/apps/cancollezh/charactors/detail.jsp\?detailid")})

    detailIDs = []

    for link in link_list:
        link = link.get('href')
        detail_id = link.split('?')[-1].split('=')[-1]
        detailIDs.append(detail_id)

    print(detailIDs)
    print(len(detailIDs))
    return detailIDs


def get_detail(IDs):

    warships = []
    i = 0
    for id in IDs:
        data = {
            "detailid": id,
            "language": "zh"
        }
        data_json = requests.post(url_detail, data, headers=headers).json()

        subkey = ['ID', 'NAME', 'NI_CHENG', 'NO',
                  'SU_DU', 'SHE_CHENG',
                  'ATTACK', 'ROCKETS',
                  'DEFENCE', 'DUI_KONG',
                  'LIFE', 'SHAN_BI',
                  'DUI_QIAN', 'ZHEN_CHA',
                  'XING_YUN', 'ITEM_NUM',
                  'DAN', 'YOU',
                  'DA_ZAI', 'FEN_BU',
                  'EXP', 'SELL',
                  'BUILD_TIME',
                  'OIL_COST', 'GANG_COST',
                  'GAI_ZAO_INFO', 'GAI_ZAO_USE',
                  'DESC', 'GETTING_TALK', 'WEDDING_TALK',
                  'WEAPON',
                  'DROP_INFO',
                  'SKILL_NAME', 'SKILL_INFO',
                  'STARS']
        subdict = {key: data_json[key] for key in subkey}
        warships.append(subdict)
        i += 1
        print('yes  ' + str(i))
    print(len(warships))
    # with open('fuckencoding.txt', 'w') as f:
    #     f.write(warships)
    return warships


if __name__ == '__main__':
    # data = get_detail(['1', '2', '3', '4', '5', '187'])
    data = get_detail(get_ids())
    with open('warships.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', '名称', '昵称', 'NO',
                         '速度', '射程',
                         '火力', '鱼雷',
                         '装甲', '对空',
                         '耐久', '闪避',
                         '对潜', '索敌',
                         '幸运', '装备槽',
                         '弹药总量', '油箱总量',
                         '搭载量', '搭载分布',
                         '狗粮口感', '贩卖回收',
                         '建造时间',
                         '修理油耗', '修理钢耗',
                         '改造信息', '改造消耗',
                         # '舰船描述',
                         # '登场台词',
                         # '结婚对白',
                         '初始装备',
                         '掉落信息',
                         '技能名称', '技能信息',
                         '星级'])
        j = 0
        for ship in data:
            j += 1
            print(j)
            writer.writerow([ship["ID"], ship["NAME"], ship["NI_CHENG"], ship["NO"],
                             ship["SU_DU"], ship["SHE_CHENG"], ship["ATTACK"], ship["ROCKETS"],
                             ship["DEFENCE"], ship["DUI_KONG"], ship["LIFE"], ship["SHAN_BI"],
                             ship["DUI_QIAN"], ship["ZHEN_CHA"], ship["XING_YUN"],
                             ship["ITEM_NUM"], ship["DAN"], ship["YOU"], ship['DA_ZAI'],
                             ship["FEN_BU"], ship["EXP"], ship["SELL"], ship["BUILD_TIME"],
                             ship["OIL_COST"], ship["GANG_COST"], ship["GAI_ZAO_INFO"],
                             ship["GAI_ZAO_USE"],
                             # ship["DESC"],
                             # ship["GETTING_TALK"],
                             # ship["WEDDING_TALK"],
                             ship["WEAPON"], ship["DROP_INFO"],
                             ship["SKILL_NAME"], ship["SKILL_INFO"], ship["STARS"]])




    print("Thanks")

