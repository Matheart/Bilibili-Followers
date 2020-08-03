import requests
from urllib import robotparser
import time
import math
import re
import chardet
import json
import pandas as pd
from bs4 import BeautifulSoup

def get_headers(): # 可以在瀏覽器按F12 + Network找到自己的cookie和user-agent
    headers = {
        "cookie" : "YourCookie",
        "user-agent": "YourUserAgent"
    }
    return headers

def get_data(link):
    raw_dt = requests.get(link , headers = get_headers())
    charset = chardet.detect(raw_dt.content)
    raw_dt.encoding = charset['encoding']
    dt = json.loads(raw_dt.text)

    try:
        something = dt['data']
        return dt
    except:
        print(dt) 
        time.sleep(30) # 如果搜索服務異常wait 30s
        print("Retrying ...")
        return get_data(link)
    
def save_data(mid, name, sex, mtime):
    res = pd.DataFrame()
    res['mid'] = mid # 用戶編號
    res['name'] = name # 名字
    res['sex'] = sex # 性別
    res['mtime'] = mtime # 關注時間

    res.to_csv('FollowerData.csv', index = None)

if __name__ == "__main__":
    origin_link = "https://member.bilibili.com/x/h5/data/fan/list?ps=500"
    NotFirstTime = False
    NumOfFollowers = 15150

    mid = []
    name = []
    sex = []
    mtime = []

    try:
        for Nm in range(math.ceil(NumOfFollowers/500.0)): # 粉絲數/500向上取整
            link = origin_link
            if NotFirstTime == True:
                link = link + "&last_id=" + LastMID
            dt = get_data(link)
            for i in dt['data']['result']:
                mid.append(i['card']['mid'])
                name.append(i['card']['name'])
                sex.append(i['card']['sex'])
                mtime.append(i['mtime'])

            print(dt['data']['result'][-1]['card']['name'], dt['data']['result'][-1]['mtime'])
            NotFirstTime = True
            LastMID = dt['data']['result'][-1]['mtime_id']
            time.sleep(5) # 可自由設置sleep時間
        save_data(mid, name, sex, mtime)
    except:
        save_data(mid, name, sex, mtime)