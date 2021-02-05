import pandas as pd
import numpy as np
import seaborn as sns
import codecs
import matplotlib.pyplot as plt

def read_data():
    dt = pd.read_csv('FollowerData.csv')
    mid, name, sex, mtime, follower = dt['mid'], dt['name'], dt['sex'], dt['mtime'], dt['follower']
    return mid, name, sex, mtime, follower

def take_follower(obj):
    return obj[4]

if __name__ == "__main__":
    #粉丝数据按粉丝数降序排序
    mid, name, sex, mtime, follower = read_data()
    lst = [[mid[i], name[i], sex[i], mtime[i], follower[i]] for i in range(len(mid))]
    lst.sort(key = take_follower, reverse = True)
    
    f = codecs.open(r'sorted.txt', 'w', encoding='utf-8')
    for i in range(len(mid)):
        tmp_str = str(i+1) +  ": " + lst[i][1] + ' ' + lst[i][3] + ' ' + str(lst[i][4]) + '\n'
        f.write(tmp_str)
    f.close()