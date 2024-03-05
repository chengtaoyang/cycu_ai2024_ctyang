import requests
from bs4 import BeautifulSoup
import pandas as pd

# 獲取網頁內容
response = requests.get('https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx')

# 解析網頁內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的表格元素
tables = soup.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]

# 印出 DataFrame
print(df1)
print(df2)

# 將 DataFrame 寫入 CSV 檔案
df2.to_csv("C:/Users/USER/Desktop/oil.csv", index=False)

# df2 只保留前2個欄位的資料
df2 = df2.iloc[:, :2]

# 去除第二欄值是NaN的資料
df2 = df2.dropna(subset=[df2.columns[1]])

# 把第一欄的資料型態 轉成 datetime
df2[df2.columns[0]] = pd.to_datetime(df2[df2.columns[0]])

print (df2)

# 使用 matplotlib 繪製折線圖 , x 軸是日期 , y 軸是油價
import matplotlib.pyplot as plt
plt.plot(df2[df2.columns[0]], df2[df2.columns[1]])
plt.show()