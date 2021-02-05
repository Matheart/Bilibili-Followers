import requests
from urllib import robotparser
import time
import math
import re
import chardet
import json
import pandas as pd
from bs4 import BeautifulSoup

def get_headers(): 
    # 请手动输入 headers，步骤：
    # 1. 在电脑打开https://member.bilibili.com/x/h5/data/fan/list?ps=500
    # 2. 然后按F12 + Network找到自己的cookie和user-agent
    # 3. 把它们分别填在下面的cookie和user-agent里面
    headers = {
        "cookie" : "_uuid=9E10EEFD-71CF-5F4D-8DE3-FE91123C923A88422infoc; buvid3=E5E4F3EA-72AD-4AAA-9CF2-0126D2160BE7138370infoc; sid=jn0iwgp8; DedeUserID=346660989; DedeUserID__ckMd5=b4abd21c62ac4606; SESSDATA=cef903b6,1615102782,8c79c*91; bili_jct=46ef7b1a287db5f70308e48aaee26afc; blackside_state=1; CURRENT_FNVAL=80; rpdid=|(kJuYlJ||l|0J'ulmmlYJRk|; LIVE_BUVID=AUTO7616001761848285; CURRENT_QUALITY=116; fingerprint3=a5901396dde2c6593f9c20b4b7cf2835; fingerprint=7773c6657dac82d5a2538e54fbb3eada; fingerprint_s=cc494a362078e5e36b6784129da7896a; buivd_fp=E5E4F3EA-72AD-4AAA-9CF2-0126D2160BE7138370infoc; buvid_fp_plain=E5E4F3EA-72AD-4AAA-9CF2-0126D2160BE7138370infoc; dy_spec_agreed=1; bp_t_offset_346660989=484877502504078720; PVID=2; bp_video_offset_346660989=486426452390985747",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    return headers

def get_data(link):
    try:
        raw_dt = requests.get(link , headers = get_headers())
        charset = chardet.detect(raw_dt.content)
        raw_dt.encoding = charset['encoding']
        dt = json.loads(raw_dt.text)
        something = dt['data']
        return dt
    except:
        time.sleep(30) # 如果搜索服务异常wait 30s
        print("Retrying ...")
        return get_data(link)
    
def save_data(mid, name, sex, mtime, follower):
    res = pd.DataFrame()
    res['mid'] = mid # 用户编号
    res['name'] = name # 名字
    res['sex'] = sex # 性別
    res['mtime'] = mtime # 关注时间
    res['follower'] = follower # 粉丝数

    res.to_csv('FollowerData.csv', index = None)

if __name__ == "__main__":
    origin_link = "https://member.bilibili.com/x/h5/data/fan/list?ps=500"
    NotFirstTime = False

    # 请在这里填入你目前的粉丝数
    NumOfFollowers = 16614

    mid = []
    name = []
    sex = []
    mtime = []
    follower = []

    try:
        for Nm in range(math.ceil(NumOfFollowers/500.0)): 
            #  每次获取能取得500粉丝的信息
            link = origin_link
            if NotFirstTime == True:
                link = link + "&last_id=" + LastMID
                
            dt = get_data(link)
            for i in dt['data']['result']:
                mid.append(i['card']['mid'])
                name.append(i['card']['name'])
                sex.append(i['card']['sex'])
                mtime.append(i['mtime'])
                follower.append(i['follower'])

            # 当前组最后一个粉丝的信息
            print(dt['data']['result'][-1]['card']['name'], dt['data']['result'][-1]['mtime'])
            NotFirstTime = True
            LastMID = dt['data']['result'][-1]['mtime_id']
            time.sleep(15) 
            # 可自由设置sleep时间，这里设置15s以防止被反爬虫系统拦截
        save_data(mid, name, sex, mtime, follower)
    except:
        # 如果遇到异常直接保存数据
        save_data(mid, name, sex, mtime, follower)