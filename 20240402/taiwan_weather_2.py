# crawler from rss of central weather agency

import requests
import json
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import os

import feedparser

# url = https://www.cwa.gov.tw/rss/forecast/36_01.xml
# 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, to 22

county_list = []


for num in range(1, 23):
    #string format with prefix 0 if num < 10
    url = 'https://www.cwa.gov.tw/rss/forecast/36_' + str(num).zfill(2) + '.xml'
    print(url)
    #get xml from url
    response = requests.get(url)
    #parse rss feed
    feed = feedparser.parse(response.content)

    tempdict = {}

    for entry in feed.entries:
        # entry.title includes '溫度'
        if '溫度' in entry.title:
        # 資料的格式 如下:
        # 金門縣04/02 今晚明晨 晴時多雲 溫度: 22 ~ 24 降雨機率: 10% (04/02 17:00發布)
            print(entry.title)
        #取出縣市名稱(前三個字)
            tempdict['county'] = entry.title[:3]

        #取出溫度的部分 使用空格切割後 取出 -7 與 -5 的部分
            tempdict['min'] = entry.title.split(' ')[-7]
            tempdict['max'] = entry.title.split(' ')[-5]
            print(tempdict['county'], tempdict['min'], tempdict['max'])
    
            county_list.append(tempdict)
        print("=======================================")

df_weather = pd.DataFrame(county_list)
print(df_weather)

