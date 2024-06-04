
import requests
import feedparser

# RSS feed URL
url = "https://news.pts.org.tw/xml/newsfeed.xml"

# 發送 GET 請求
response = requests.get(url)

# 解析 RSS feed
feed = feedparser.parse(response.content)

# 提取並列印所有的標題
for entry in feed.entries:
    print(entry.title)
    #印出 summary
    print(entry.summary)

    #檢查檔案的標題是否包含 美國 如果有的畫儲存成  excel 可讀取的格式
    #放在 使用者的桌面上
    #檔案名稱為 news.csv
    if "YouBike" in entry.title:
        with open("C:/Users/USER/Desktop/news.csv", "a", encoding="utf-8") as file:
            file.write(entry.title + "\n")
            file.write(entry.summary + "\n")
            file.write("=======================================\n")
    print("=======================================")